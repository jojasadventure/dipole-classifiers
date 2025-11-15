# run_pipeline.py
import argparse
import sys
import yaml
import logging
from pathlib import Path

from core.log_setup import setup_logging
setup_logging()
from core.context import ExperimentContext
from core.llm_router import LLMRouter
from core.embedding import EmbeddingGenerator

from pipeline.pair_generation import pair_generation_logic
from pipeline.embedding_generation import embedding_generation_logic
from pipeline.extract_vector import extract_vector_logic
from pipeline.validation_sample_generation import validation_sample_generation_logic
from pipeline.vector_validation import vector_validation_logic


def load_config(config_path: str = 'config.yaml') -> dict:
    """Loads configuration from a flat YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logging.info(f"Configuration defaults loaded from {config_path}")
        return config or {}
    except FileNotFoundError:
        logging.warning(f"Config file not found at {config_path}. Using CLI args and hard-coded defaults only.")
        return {}
    except yaml.YAMLError as e:
        logging.error(f"Error parsing configuration file {config_path}: {e}")
        sys.exit(1)

def define_and_parse_args(config_defaults: dict) -> argparse.Namespace:
    """Defines all arguments with user-friendly hyphens."""
    parser = argparse.ArgumentParser(description="Automated Semantic Dimension Discovery Pipeline.")
    parser.set_defaults(**config_defaults)
    parser.add_argument('--dimension', required=True, type=str, help='The semantic dimension, e.g., "Formality: Formal vs Informal"')
    parser.add_argument('--config', help='Path to the configuration file.')
    parser.add_argument('--validate-sample', action='store_true', help='Run validation on the pairs used to generate the vector.')
    parser.add_argument('--validate-new', action='store_true', help='Generate new single samples and run validation on them.')
    parser.add_argument('--llm-provider', type=str, choices=['google', 'openai', 'ollama'], help='The LLM provider.')
    parser.add_argument('--llm-api-key', type=str, help='API key for the LLM provider.')
    parser.add_argument('--llm-api-url', type=str, help='API URL override for LLM provider.')
    parser.add_argument('--llm-model-name', type=str, help='The specific model to use for generation.')
    parser.add_argument('--llm-temperature', type=float, help='Generation temperature.')
    parser.add_argument('--llm-num-pairs', '--num-pairs', type=int, help='Number of pairs to generate.')
    parser.add_argument('--llm-batch-size', type=int, help='Max number of pairs/samples to request in a single API call.')
    parser.add_argument('--embedding-api-url', type=str, help='URL for the embedding inference server.')
    parser.add_argument('--embedding-model-id', type=str, help='Model ID for the embedding model.')
    parser.add_argument('--pipeline-run-validation-by-default', action='store_true', help='Run in-sample validation by default.')
    parser.add_argument('--pipeline-num-validation-samples', type=int, help='Number of new samples to generate per pole for validation.')
    parser.add_argument('--pipeline-validation-pairs-override-path', type=str, help='Path to an alternative pairs file for validation.')
    parser.add_argument('--prompt-file', type=Path, help='Path to a custom prompt template to replace the default one.')
    parser.add_argument('--prompt-extra-text', type=str, default="", help='Optional text to add in the prompt.')
    return parser.parse_args()



def main():
    ARTIFACT_SCHEMA_VERSION = "1.0"
    temp_parser = argparse.ArgumentParser(add_help=False)
    temp_parser.add_argument('--config', default='config.yaml')
    temp_args, _ = temp_parser.parse_known_args()
    config_defaults = load_config(temp_args.config)
    args = define_and_parse_args(config_defaults)
    context = ExperimentContext(args, schema_version=ARTIFACT_SCHEMA_VERSION)


    llm_router = LLMRouter(
        provider=args.llm_provider, model_name=args.llm_model_name, api_key=args.llm_api_key,
        api_url=args.llm_api_url, temperature=args.llm_temperature
    )
    embed_generator = EmbeddingGenerator(base_url=args.embedding_api_url, model_name=args.embedding_model_id)

    logging.info("--- Starting Step 1: Generate Pairs ---")
    pairs_data, prompt_content = pair_generation_logic(context, llm_router)
    if not pairs_data: 
        logging.error("Pipeline aborted: Pair Generation failed."); sys.exit(1)      
    context.update_metadata({
        "num_pairs_generated": len(pairs_data),
        "prompt_template_content": prompt_content
    })    
    context.save_artifact("pairs", pairs_data)

    logging.info("--- Starting Step 2: Generate Embeddings ---")
    embeddings_data = embedding_generation_logic(context, embed_generator)
    if not embeddings_data: logging.error("Pipeline aborted: Embedding Generation failed."); sys.exit(1)
    context.save_artifact("embeddings", embeddings_data)
    
    logging.info("--- Starting Step 3: Extract Vector ---")
    vector_list, metadata_updates = extract_vector_logic(context)
    if vector_list is None: logging.error("Pipeline aborted: Vector Extraction failed."); sys.exit(1)
    context.update_metadata(metadata_updates)
    context.save_artifact("vector", {"vector": vector_list})

    # This logic is now robust and provides clear error messages.
    validation_input_path = None
    should_run_validation = False
    
    override_path_str = args.pipeline_validation_pairs_override_path

    # First, check if an override path was provided. This is the highest priority.
    if override_path_str:
        should_run_validation = True
        override_path = Path(override_path_str)
        if override_path.exists():
            logging.info(f"--- Preparing for Validation using Override File ---")
            validation_input_path = override_path
        else:
            # If the provided path is invalid, FAIL LOUDLY and exit.
            logging.error(f"Validation override file NOT FOUND at the specified path: {override_path_str}")
            logging.error("Please check the path and try again. Aborting.")
            sys.exit(1)
    
    # If no override was given, check the other flags.
    elif args.validate_new:
        should_run_validation = True
        logging.info("--- Starting Step 4a: Generate Validation Samples (Out-of-Sample) ---")
        samples = validation_sample_generation_logic(context, llm_router)
        if not samples: raise RuntimeError("Validation Sample Generation failed.")
        context.save_artifact("validation_samples", samples)
        validation_input_path = context.get_path_for("validation_samples")

    elif args.validate_sample or args.pipeline_run_validation_by_default:
        should_run_validation = True
        logging.info("--- Starting Step 4a: Preparing for In-Sample Validation ---")
        validation_input_path = context.get_path_for("pairs")
    
    # Now, run validation ONLY if one of the conditions was met and the path is valid.
    if should_run_validation:
        logging.info(f"--- Starting Step 4b: Running Validation on {validation_input_path.name} ---")
        report_text = vector_validation_logic(context, embed_generator, validation_input_path)
        if not report_text: raise RuntimeError("Validation step failed.")
        context.save_artifact("validation_report", report_text, is_json=False)

    logging.info(f"--- Pipeline completed successfully for run '{context.run_id}' ---")
    logging.info(f"Results are in: {context.run_dir}")

if __name__ == "__main__":
    main()
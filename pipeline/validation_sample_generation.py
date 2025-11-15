# pipeline/validation_sample_generation.py
import sys
import json
import logging
import random
from pathlib import Path
from typing import TYPE_CHECKING, List, Set, Optional

# Allow the module to import from the 'core' directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from core.llm_router import LLMRouter

if TYPE_CHECKING:
    from core.context import ExperimentContext


def _clean_llm_json_output(raw_text: str) -> List[str]:
    """Cleans LLM output and robustly parses it into a list of strings."""
    if not raw_text: return []
    try:
        start_brace = raw_text.find('[')
        end_brace = raw_text.rfind(']')
        if start_brace != -1 and end_brace != -1:
            json_str = raw_text[start_brace:end_brace+1]
            data = json.loads(json_str)
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                return data
    except json.JSONDecodeError as e:
        logging.warning(f"Could not decode JSON from LLM output: {e}")
    return []


def validation_sample_generation_logic(context: 'ExperimentContext', router: LLMRouter) -> Optional[List[dict]]:
    """
    Generates labeled single-sentence samples for out-of-sample validation.
    """
    num_samples_per_pole = context.args.pipeline_num_validation_samples
    batch_size = getattr(context.args, 'llm_batch_size', 20) # A safe default for samples
    
    project_root = Path(__file__).resolve().parent.parent
    prompt_file_path = project_root / "prompts" / "sample_generation_prompt.txt"
    try:
        with open(prompt_file_path, 'r') as f:
            prompt_template = f.read()
    except Exception as e:
        logging.error(f"Error reading prompt template file at {prompt_file_path}: {e}")
        return None

    # A single set to track all unique samples across both poles
    master_seen_samples = set()
    samples_a, samples_b = [], []

    
    for pole_name, sample_list in [(context.pole_a, samples_a), (context.pole_b, samples_b)]:
        logging.info(f"--- Generating {num_samples_per_pole} unique samples for pole: '{pole_name}' ---")
        
        # Consistent while loop, just like pair_generation.py
        total_api_calls = 0
        max_total_calls = (num_samples_per_pole // (batch_size // 2)) + 5 # Generous attempt limit

        while len(sample_list) < num_samples_per_pole and total_api_calls < max_total_calls:
            total_api_calls += 1
            samples_needed = num_samples_per_pole - len(sample_list)
            samples_to_request = min(batch_size, samples_needed + 2) # Request a bit more to account for duplicates
            
            logging.info(f"API Call {total_api_calls}/{max_total_calls}: Requesting {samples_to_request} for '{pole_name}'. Have {len(sample_list)}/{num_samples_per_pole}.")
            prompt = prompt_template.format(
                dimension_name=context.dimension_name, pole_name=pole_name, num_samples=samples_to_request
            )

            try:
                raw_response = router.generate(prompt)
                newly_received_samples = _clean_llm_json_output(raw_response)
            except Exception as e:
                logging.error(f"API call failed for pole '{pole_name}': {e}")
                continue
            
            newly_added_count = 0
            for sample in newly_received_samples:
                if sample and sample not in master_seen_samples:
                    master_seen_samples.add(sample)
                    sample_list.append(sample)
                    newly_added_count += 1
            
            logging.info(f"Parsed {len(newly_received_samples)}, added {newly_added_count} new unique samples.")
            
        if len(sample_list) < num_samples_per_pole:
            logging.warning(f"Could not generate target of {num_samples_per_pole} samples for '{pole_name}'. Got {len(sample_list)}.")
    

    if not samples_a or not samples_b:
        logging.error("Failed to generate sufficient samples for one or both poles. Aborting.")
        return None

    # Structure the data with labels
    labeled_data = []
    for text in samples_a:
        labeled_data.append({"text": text, "label": context.pole_a})
    for text in samples_b:
        labeled_data.append({"text": text, "label": context.pole_b})
    
    random.shuffle(labeled_data)
    
    logging.info(f"Successfully generated {len(labeled_data)} total unique labeled samples.")
    return labeled_data
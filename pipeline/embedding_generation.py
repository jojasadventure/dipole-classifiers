# pipeline/embedding_generation.py
import sys
import logging
from pathlib import Path
from typing import TYPE_CHECKING, List, Dict, Any, Optional

from tqdm import tqdm

# Allow the module to import from the 'core' directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from core.embedding import EmbeddingGenerator

if TYPE_CHECKING:
    from core.context import ExperimentContext

# --- Core Logic Function (The public API of this module) ---
def embedding_generation_logic(context: 'ExperimentContext', embed_generator: EmbeddingGenerator) -> Optional[list]:
    """
    Generates embeddings for all sentences in the pairs artifact.

    This function is intended to be called by an orchestrator. It loads
    the pairs artifact, generates embeddings for all texts, structures
    the results, and returns the final data.
    """
    try:
        input_artifact = context.load_artifact('pairs')
        pairs_data = input_artifact['data']
        logging.info(f"Loaded {len(pairs_data)} pairs for embedding.")
    except (FileNotFoundError, KeyError) as e:
        logging.error(f"Failed to load or parse pairs artifact: {e}")
        return None

    if not pairs_data:
        logging.warning("Pairs data is empty. No embeddings to generate.")
        return []

    pole_a_key = context.pole_a.lower()
    pole_b_key = context.pole_b.lower()
    logging.info(f"Using pole keys: '{pole_a_key}' and '{pole_b_key}'")

    all_texts_to_embed = []
    text_mapping = []  # To map flat list index back to pair and pole

    for i, pair in enumerate(pairs_data):
        if pole_a_key not in pair or pole_b_key not in pair:
            logging.warning(f"Skipping pair {i}: Missing expected keys.")
            continue
        all_texts_to_embed.append(pair[pole_a_key])
        text_mapping.append({'pair_index': i, 'pole': pole_a_key, 'original_text': pair[pole_a_key]})
        
        all_texts_to_embed.append(pair[pole_b_key])
        text_mapping.append({'pair_index': i, 'pole': pole_b_key, 'original_text': pair[pole_b_key]})

    if not all_texts_to_embed:
        logging.warning("No valid texts found to embed.")
        return []

    try:
        embeddings_list = embed_generator.generate_embeddings(all_texts_to_embed)
        if embeddings_list is None:
            logging.error("Embedding generator returned None. Aborting.")
            return None
        if len(embeddings_list) != len(all_texts_to_embed):
            logging.error(f"Mismatch between number of texts ({len(all_texts_to_embed)}) and embeddings ({len(embeddings_list)}).")
            return None
    except Exception as e:
        logging.error(f"An exception occurred during embedding generation: {e}", exc_info=True)
        return None
    
    # --- Structure Results ---
    structured_results = [{} for _ in range(len(pairs_data))]
    for i, embedding in enumerate(tqdm(embeddings_list, desc="Structuring results")):
        map_info = text_mapping[i]
        pair_idx, pole = map_info['pair_index'], map_info['pole']

        # Initialize the dictionary for the pair if it's the first time we see it
        if 'original_pair' not in structured_results[pair_idx]:
            structured_results[pair_idx]['original_pair'] = pairs_data[pair_idx]
            structured_results[pair_idx]['embeddings'] = {}

        structured_results[pair_idx]['embeddings'][pole] = {
            "text": map_info['original_text'], "vector": embedding
        }

    # Filter out any pairs that might have been skipped or failed
    final_results = [res for res in structured_results if 'original_pair' in res]
    logging.info(f"Successfully generated and structured embeddings for {len(final_results)} pairs.")
    
    return final_results
# pipeline/extract_vector.py
import sys
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Tuple, Optional, Dict, Any

import numpy as np
from tqdm import tqdm

# Allow the module to import from the 'core' directory
sys.path.append(str(Path(__file__).resolve().parent.parent))

if TYPE_CHECKING:
    from core.context import ExperimentContext


def _normalize_vector(vector: np.ndarray) -> np.ndarray:
    """Normalizes a numpy vector."""
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def extract_vector_logic(context: 'ExperimentContext') -> Tuple[Optional[list], Dict[str, Any]]:
    """
    Extracts a semantic vector from paired embeddings.

    This function is intended to be called by an orchestrator. It loads
    the embeddings artifact, calculates the dimension vector, and returns
    the vector along with any new metadata to be added to the context.
    """
    try:
        input_artifact = context.load_artifact('embeddings')
        metadata = input_artifact['metadata']
        embedding_data = input_artifact['data']
        logging.info(f"Loaded {len(embedding_data)} embedding entries.")
    except (FileNotFoundError, KeyError) as e:
        logging.error(f"Failed to load or parse embeddings artifact: {e}")
        return None, {}

    if not embedding_data:
        logging.warning("Embedding data is empty. Cannot extract vector.")
        return None, {}

    difference_vectors = []
    pole_a_key = context.pole_a.lower()
    pole_b_key = context.pole_b.lower()
    logging.info(f"Using pole keys from metadata: '{pole_a_key}' and '{pole_b_key}'")

    valid_pairs_count = 0
    for i, item in enumerate(tqdm(embedding_data, desc="Calculating difference vectors")):
        try:
            if 'embeddings' not in item or pole_a_key not in item['embeddings'] or pole_b_key not in item['embeddings']:
                logging.warning(f"Skipping item {i}: Missing required embedding structure.")
                continue
            
            vec_a = np.array(item['embeddings'][pole_a_key]['vector'])
            vec_b = np.array(item['embeddings'][pole_b_key]['vector'])

            if vec_a.shape != vec_b.shape:
                logging.warning(f"Skipping item {i}: Vector shape mismatch.")
                continue

            diff_vec = vec_b - vec_a
            norm_diff_vec = _normalize_vector(diff_vec)
            difference_vectors.append(norm_diff_vec)
            valid_pairs_count += 1

        except (KeyError, TypeError, Exception) as e:
            logging.warning(f"Skipping item {i} due to error: {e}")
            continue

    if not difference_vectors:
        logging.error("No valid difference vectors could be calculated.")
        return None, {}

    logging.info(f"Averaging {len(difference_vectors)} normalized difference vectors from {valid_pairs_count} valid pairs.")
    average_vector = np.mean(difference_vectors, axis=0)
    final_vector = _normalize_vector(average_vector)

    logging.info(f"Final dimension vector calculated with shape: {final_vector.shape}")
    
    
    metadata_updates = {
        "num_pairs_used_for_vector": valid_pairs_count,
        "vector_dimensionality": final_vector.shape[0]
    }
    
    return final_vector.tolist(), metadata_updates
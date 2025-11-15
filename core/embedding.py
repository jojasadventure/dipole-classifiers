# core/embedding.py

import logging
import requests
from typing import List, Optional

class EmbeddingGenerator:
    """
    Handles communication with the Embedding Inference Server to generate embeddings.
    This version is robust and sends data in managed chunks to avoid payload size errors.
    """
    
    # We'll send texts in chunks of this size. This is a safe number that balances
    # performance with the need to stay under server payload limits.
    BATCH_SIZE = 32

    def __init__(self, base_url: str, model_name: str, api_key: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.base_url = base_url
        self.model_name = model_name
        self.api_key = api_key

    def generate_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Generates embedding vectors for a list of texts by processing them in safe-sized chunks.

        Args:
            texts: A list of text strings to embed. Can be of any length.

        Returns:
            A list of embedding vectors, or None if any chunk fails.
        """
        if not texts:
            return []

        all_embeddings = []
        
        # This loop breaks the large 'texts' list into smaller 'batch' lists
        # of size self.BATCH_SIZE to send to the API.
        for i in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[i:i + self.BATCH_SIZE]
            
            try:
                url = f"{self.base_url}/embed"
                headers = {"Content-Type": "application/json"}
                data = {"inputs": batch}
                
                # self.logger.info(f"Requesting embeddings for a chunk of {len(batch)} texts (total processed: {i})...")
                response = requests.post(url, headers=headers, json=data, timeout=60)
                response.raise_for_status()
                
                response_json = response.json()

                if isinstance(response_json, list) and all(isinstance(item, list) for item in response_json):
                    all_embeddings.extend(response_json) # Add the results from this chunk
                else:
                    self.logger.error(f"API response for a chunk is not in the expected format. Response: {response_json}")
                    return None # Abort on malformed response

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request error to embedding server on a chunk: {e}")
                # You could add retry logic here in a real production system,
                # but for now, failing fast is safest.
                return None
            except Exception as e:
                self.logger.error(f"General error getting embeddings for a chunk: {e}", exc_info=False)
                return None

        # self.logger.info(f"Successfully received all {len(all_embeddings)} embeddings in { (len(texts) + self.BATCH_SIZE - 1) // self.BATCH_SIZE } chunks.")
        return all_embeddings
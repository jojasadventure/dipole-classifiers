# core/classifier.py
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

import numpy as np

from .embedding import EmbeddingGenerator

logger = logging.getLogger(__name__)

class DimensionClassifier:
    """
    Loads a dimension vector and classifies texts against it.
    This class is the central engine for using the generated classifiers.
    """
    def __init__(self, vector_path: Path, embed_generator: EmbeddingGenerator):
        """
        Initializes the classifier by loading the vector and its metadata.

        Args:
            vector_path: Path to the dimension_vector.json file.
            embed_generator: An initialized EmbeddingGenerator instance.
        """
        if not vector_path.exists():
            raise FileNotFoundError(f"Vector file not found at: {vector_path}")

        self.vector_path = vector_path
        self.embed_generator = embed_generator
        
        self.poles: Dict[str, str] = {}
        self.vector: np.ndarray = np.array([])
        
        self._load_vector_file()
        logger.info(f"Classifier initialized for dimension: '{self.poles.get('a', 'N/A')}' vs. '{self.poles.get('b', 'N/A')}'")

    def _load_vector_file(self):
        """Robustly loads a dimension_vector.json file, handling multiple formats."""
        with open(self.vector_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Try to find poles
        if 'metadata' in data and 'pole_a' in data['metadata']:
            self.poles = {'a': data['metadata']['pole_a'], 'b': data['metadata']['pole_b']}
        elif 'pole_a' in data:
            self.poles = {'a': data['pole_a'], 'b': data['pole_b']}
        
        if not self.poles:
            raise ValueError(f"Could not find 'pole_a' and 'pole_b' keys in vector file: {self.vector_path}")

        # Try to find vector
        vector_data = None
        if 'data' in data and 'vector' in data['data']:
            vector_data = data['data']['vector']
        elif 'data' in data and isinstance(data['data'], list):
            vector_data = data['data']
        elif 'vector' in data:
            vector_data = data['vector']

        if vector_data is None:
            raise ValueError(f"Found pole names but could not find 'vector' data in file: {self.vector_path}")
        
        self.vector = np.array(vector_data)

    def classify(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Classifies a list of texts against the dimension vector, using batching.

        Args:
            texts: A list of text strings to classify.

        Returns:
            A list of result dictionaries, one for each text.
        """
        if not texts:
            return []
        
        # logger.info(f"Generating embeddings for {len(texts)} texts...")
        embeddings = self.embed_generator.generate_embeddings(texts)
        if embeddings is None:
            raise RuntimeError("Failed to generate embeddings for the input text(s).")
        
        results = []
        for i, text in enumerate(texts):
            score = np.dot(np.array(embeddings[i]), self.vector)
            prediction = self.poles['b'] if score > 0 else self.poles['a']
            results.append({
                "text": text,
                "score": score,
                "prediction": prediction,
                "pole_a": self.poles['a'],
                "pole_b": self.poles['b']
            })
        return results
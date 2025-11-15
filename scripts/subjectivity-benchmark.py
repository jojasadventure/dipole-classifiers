#!/usr/bin/env python
import argparse
import sys
import logging
import json
from pathlib import Path
import time

# Add project root to path for imports from the 'core' directory
sys.path.append(str(Path(__file__).resolve().parent.parent))

# --- Project Imports ---
from core.log_setup import setup_logging
from core.embedding import EmbeddingGenerator
from core.classifier import DimensionClassifier

# --- Dependencies ---
try:
    from datasets import load_dataset
    from sklearn.metrics import accuracy_score
    from tqdm import tqdm
except ImportError:
    print("Error: 'datasets', 'scikit-learn', and 'tqdm' are required for this script.")
    print("Please install them with: pip install -r requirements.txt")
    sys.exit(1)

# --- Helper for colored output ---
class _Colors:
    GREEN, RED, ENDC = '\033[92m', '\033[91m', '\033[0m'

def define_and_parse_args():
    parser = argparse.ArgumentParser(description="Benchmark a dimension vector against the Subjectivity dataset.")
    parser.add_argument('-v', '--vector', type=Path, required=True, help='Path to the dimension_vector.json file.')
    parser.add_argument('--embedding-api-url', type=str, help='URL of the embedding inference server. Can be set in config.yaml.')
    parser.add_argument('--embedding-model-id', type=str, help='Model ID for embeddings. Can be set in config.yaml.')
    parser.add_argument('--config', default='config.yaml', help='Path to config file for default embedding settings.')
    return parser.parse_args()

def main():
    """Main execution function."""
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("datasets").setLevel(logging.ERROR)
    logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
    setup_logging()
    
    args = define_and_parse_args()

    config = {}
    if Path(args.config).exists():
        import yaml
        with open(args.config, 'r') as f: config = yaml.safe_load(f)
    
    embedding_api_url = args.embedding_api_url or config.get('embedding_api_url')
    embedding_model_id = args.embedding_model_id or config.get('embedding_model_id')

    if not (embedding_api_url and embedding_model_id):
        sys.exit("Error: Embedding API URL and Model ID must be provided via arguments or a valid config.yaml.")
    
    try:
        embed_generator = EmbeddingGenerator(base_url=embedding_api_url, model_name=embedding_model_id)
        classifier = DimensionClassifier(args.vector, embed_generator)
    except Exception as e:
        sys.exit(f"An error occurred during initialization: {e}")

    print(f"Loading Subjectivity dataset (test split)...")
    ds = load_dataset('tasksource/subjectivity', split='test')
    

    texts = [ex['Sentence'] for ex in ds]
    true_labels = [ex['Label'] for ex in ds] # This is now a list of 'SUBJ' and 'OBJ' strings.
    

    print(f"Benchmarking vector: {args.vector}")
    print(f"Dataset: tasksource/subjectivity")
    print(f"Number of samples: {len(texts)}")
    print("----------------------------------------")
    
    try:
        BATCH_SIZE = 32
        all_results = []
        
        start_time = time.perf_counter()
        
        with tqdm(total=len(texts), desc="Benchmarking", unit="samp") as pbar:
            for i in range(0, len(texts), BATCH_SIZE):
                batch_texts = texts[i:i + BATCH_SIZE]
                batch_results = classifier.classify(batch_texts)
                all_results.extend(batch_results)
                pbar.update(len(batch_texts))
                
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        total_words = sum(len(text.split()) for text in texts)
        words_per_second = total_words / duration

        scores = [r['score'] for r in all_results]
        
        # Vector: "Objective vs. Subjective" -> positive score means Subjective.
        # Predict the ground truth strings directly.
        predicted_labels = ['SUBJ' if score > 0 else 'OBJ' for score in scores]
        
        accuracy = accuracy_score(true_labels, predicted_labels)
        
    except Exception as e:
        logging.error(f"An error occurred during classification or evaluation: {e}", exc_info=True)
        sys.exit(1)
        
    detailed_results = []
    for i in range(len(texts)):
        detailed_results.append({
            "text": texts[i], "true_label": true_labels[i], "predicted_label": predicted_labels[i],
            "score": float(scores[i]), "correct": bool(true_labels[i] == predicted_labels[i])
        })
    
    report_path = args.vector.parent / "subjectivity_benchmark_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({"accuracy": accuracy, "results": detailed_results}, f, indent=2)
    print(f"Full report saved to: {report_path}")
    print("----------------------------------------")
    
    correct_samples = [r for r in detailed_results if r['correct']][:5]
    incorrect_samples = [r for r in detailed_results if not r['correct']][:5]
    
    print("\n--- Correct Classification Samples ---")
    if not correct_samples: print("None found.")
    for r in correct_samples: print(f"{_Colors.GREEN}[CORRECT]{_Colors.ENDC} True: {r['true_label']:<10} | Pred: {r['predicted_label']:<10} | Score: {r['score']:+.4f} | Text: \"{r['text'][:100]}...\"")

    print("\n--- Incorrect Classification Samples ---")
    if not incorrect_samples: print("None found.")
    for r in incorrect_samples: print(f"{_Colors.RED}[INCORRECT]{_Colors.ENDC} True: {r['true_label']:<10} | Pred: {r['predicted_label']:<10} | Score: {r['score']:+.4f} | Text: \"{r['text'][:100]}...\"")
    
    print("\n----------------------------------------")
    print(f"Final Accuracy @ zero threshold: {accuracy * 100:.2f}%")
    print(f"Performance ({embedding_model_id}): {words_per_second:,.0f} words/sec")

if __name__ == "__main__":
    main()
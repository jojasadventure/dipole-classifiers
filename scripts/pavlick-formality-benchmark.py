#!/usr/bin/env python
import argparse
import sys
import logging
import json
from pathlib import Path
import time
import numpy as np

# Add project root to path for imports from the 'core' directory
sys.path.append(str(Path(__file__).resolve().parent.parent))


from core.log_setup import setup_logging
from core.embedding import EmbeddingGenerator
from core.classifier import DimensionClassifier


try:
    from datasets import load_dataset
    from tqdm import tqdm
except ImportError:
    print("Error: 'datasets' and 'tqdm' are required for this script.")
    print("Please install them with: pip install -r requirements.txt")
    sys.exit(1)


class _Colors:
    GREEN, YELLOW, RED, BLUE, ENDC = '\033[92m', '\033[93m', '\033[91m', '\033[94m', '\033[0m'

def define_and_parse_args():
    parser = argparse.ArgumentParser(description="Benchmark a vector's correlation against all domains of the Pavlick-Formality-Scores dataset.")
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

    print(f"Loading Pavlick-Formality-Scores dataset...")
    ds = load_dataset('osyvokon/pavlick-formality-scores', split='train')
    
    all_samples = [{'sentence': ex['sentence'], 'ground_truth_score': ex['avg_score'], 'domain': ex['domain']} for ex in ds]
    texts = [s['sentence'] for s in all_samples]

    print(f"Benchmarking vector: {args.vector}")
    print(f"Dataset: Pavlick-Formality-Scores")
    print(f"Number of samples: {len(texts)}")
    print("----------------------------------------")
    
    try:
        BATCH_SIZE = 32
        all_results_from_classifier = []
        
        start_time = time.perf_counter()
        
        with tqdm(total=len(texts), desc="Benchmarking", unit="samp") as pbar:
            for i in range(0, len(texts), BATCH_SIZE):
                batch_texts = texts[i:i + BATCH_SIZE]
                batch_results = classifier.classify(batch_texts)
                all_results_from_classifier.extend(batch_results)
                pbar.update(len(batch_texts))
                
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        total_words = sum(len(text.split()) for text in texts)
        words_per_second = total_words / duration

        predicted_scores = [r['score'] for r in all_results_from_classifier]
        
        for i, sample in enumerate(all_samples):
            sample['predicted_score'] = predicted_scores[i]
        
    except Exception as e:
        logging.error(f"An error occurred during classification: {e}", exc_info=True)
        sys.exit(1)
        
    print("\n--- Pearson Correlation (r) Results ---")
    domains_to_test = ['all', 'answers', 'blog', 'email', 'news']
    final_report = {}

    for domain in domains_to_test:
        if domain == 'all':
            subset = all_samples
        else:
            subset = [s for s in all_samples if s['domain'] == domain]
            
        if not subset: continue
            
        pred_scores_subset = [s['predicted_score'] for s in subset]
        true_scores_subset = [s['ground_truth_score'] for s in subset]
        
        correlation_matrix = np.corrcoef(pred_scores_subset, true_scores_subset)
        pearson_r = correlation_matrix[0, 1]
        final_report[domain] = pearson_r
        
        # Use absolute value for color coding quality, but print the real number
        abs_r = abs(pearson_r)
        corr_color = _Colors.GREEN if abs_r > 0.6 else _Colors.YELLOW if abs_r > 0.4 else _Colors.RED
        print(f"Domain: {domain:<10} | Samples: {len(subset):<5} | Correlation: {corr_color}{pearson_r:+.4f}{_Colors.ENDC}")

    report_path = args.vector.parent / "pavlick_formality_full_correlation_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({"correlations": final_report, "all_results": all_samples}, f, indent=2)
    print(f"\nFull report saved to: {report_path}")
    
    
    all_samples.sort(key=lambda x: x['predicted_score'])
    # Positive predicted score means MORE INFORMAL
    most_informal = all_samples[-5:]
    most_formal = all_samples[:5]
    
    print(f"\n--- Samples Classified as Most Informal (by your vector) ---")
    for r in most_formal:
        
        color = _Colors.GREEN if r['ground_truth_score'] > 0 else _Colors.RED
        print(f"{_Colors.BLUE}Pred Score: {r['predicted_score']:+.4f}{_Colors.ENDC} | {color}Actual Score: {r['ground_truth_score']:+.4f}{_Colors.ENDC} | Text: \"{r['sentence'][:100]}...\"")

    print(f"\n--- Samples Classified as Most Formal (by your vector) ---")
    for r in reversed(most_informal):
        
        color = _Colors.GREEN if r['ground_truth_score'] < 0 else _Colors.RED
        print(f"{_Colors.YELLOW}Pred Score: {r['predicted_score']:+.4f}{_Colors.ENDC} | {color}Actual Score: {r['ground_truth_score']:+.4f}{_Colors.ENDC} | Text: \"{r['sentence'][:100]}...\"")
    

    print("\n----------------------------------------")
    print(f"Performance ({embedding_model_id}): {words_per_second:,.0f} words/sec")

if __name__ == "__main__":
    main()
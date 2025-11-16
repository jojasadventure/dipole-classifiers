#!/usr/bin/env python
import argparse
import sys
import json
import logging
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional

sys.path.append(str(Path(__file__).resolve().parent.parent))
from core.log_setup import setup_logging
from core.embedding import EmbeddingGenerator
from core.classifier import DimensionClassifier

class _Colors:
    BLUE, CYAN, ENDC = '\033[94m', '\033[96m', '\033[0m'

def discover_vectors() -> List[Dict]:
    results_dir = Path(__file__).resolve().parent.parent / "results"
    if not results_dir.exists():
        return []
    
    found_vectors = []
    for vector_path in results_dir.glob("**/dimension_vector.json"):
        try:
            dimension_name = vector_path.parent.parent.name
            run_id = vector_path.parent.name
            found_vectors.append({
                "path": vector_path, "dimension": dimension_name, "run_id": run_id
            })
        except Exception:
            continue
    return found_vectors

def prompt_for_vector_choice(vectors: List[Dict]) -> Optional[Dict]:
    print("No vector specified. Choose a vector to use:\n")
    for i, v in enumerate(vectors):
        print(f"  [{i+1}] {v['dimension']} / {v['run_id']}")
    
    while True:
        try:
            choice = input(f"\nEnter a number (1-{len(vectors)}) or 'q' to quit: ")
            if choice.lower() == 'q': return None
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(vectors): return vectors[choice_idx]
            print("Invalid number. Please try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting."); return None

def _get_score_qualifier(score: float) -> str:
    """Translates a raw score into a human-readable qualifier."""
    abs_score = abs(score)
    if abs_score > 0.15: return "Strongly"
    if abs_score > 0.05: return "Moderately"
    return "Slightly"

def handle_interactive_mode(classifier: DimensionClassifier):
    poles = classifier.poles
    print(f"\nLoaded Vector: {poles['a']} vs. {poles['b']}")
    print(f"Dimension: {_Colors.BLUE}{poles['a']}{_Colors.ENDC} (Pole A) vs. {_Colors.CYAN}{poles['b']}{_Colors.ENDC} (Pole B)")
    print("-" * 80)
    print("Entering interactive mode. Press Ctrl+C to exit.")
    
    while True:
        try:
            text = input("> ")
            if text.strip():
                result = classifier.classify([text])[0]
                score = result['score']
                color = _Colors.CYAN if score > 0 else _Colors.BLUE
                qualifier = _get_score_qualifier(score)
                # Simple, direct printing for interactive mode. No fuss.
                print(f"{color}{score:+.4f} ({qualifier} {result['prediction']}){_Colors.ENDC}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting."); break

def format_as_table(results: List[Dict]) -> str:
    """Formats a list of results into a full table string for batch processing."""
    if not results: return ""
    
    res = results[0]
    poles = {'a': res['pole_a'], 'b': res['pole_b']}
    header = f"Dimension: {_Colors.BLUE}{poles['a']}{_Colors.ENDC} (Pole A) vs. {_Colors.CYAN}{poles['b']}{_Colors.ENDC} (Pole B)\n" + "-" * 80
    
    lines = [header]
    for res in results:
        score = res['score']
        color = _Colors.CYAN if score > 0 else _Colors.BLUE
        qualifier = _get_score_qualifier(score)
        
        row = (
            f"Text:      \"{res['text']}\"\n"
            f"Score:     {color}{score:+.4f} ({qualifier} {res['prediction']}){_Colors.ENDC}"
        )
        lines.append(row)
        
    return f"\n{'-' * 40}\n".join(lines)

def format_as_json(results: List[Dict]) -> str:
    return json.dumps(results, indent=2)

def format_as_csv(results: List[Dict]):
    if not results: return
    writer = csv.DictWriter(sys.stdout, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

def define_and_parse_args():
    parser = argparse.ArgumentParser(description="Classify text using a pre-computed semantic dimension vector.")
    parser.add_argument('-v', '--vector', type=Path, help='Path to the dimension_vector.json file.')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--text', type=str, help='A single string of text to classify.')
    group.add_argument('-f', '--file', type=Path, help='Path to a text file or a CSV file to classify.')
    
    parser.add_argument('-c', '--column', type=str, help='If providing a CSV file, specify the column name containing the text.')
    parser.add_argument('--output-format', choices=['table', 'json', 'csv'], default='table', help='The format for the output.')
    
    parser.add_argument('--embedding-api-url', type=str, help='URL of the embedding inference server. Can be set in config.yaml.')
    parser.add_argument('--embedding-model-id', type=str, help='Model ID for embeddings. Can be set in config.yaml.')
    parser.add_argument('--config', default='config.yaml', help='Path to config file for default embedding settings.')

    return parser.parse_args()

def main():
    logging.getLogger("urllib3").setLevel(logging.WARNING)
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
    
    embed_generator = EmbeddingGenerator(base_url=embedding_api_url, model_name=embedding_model_id)
    
    vector_path = args.vector
    if not vector_path:
        discovered = discover_vectors()
        if not discovered: sys.exit("No dimension vectors found in 'results/'. Run the main pipeline first.")
        chosen = prompt_for_vector_choice(discovered)
        if not chosen: sys.exit()
        vector_path = chosen['path']

    try:
        classifier = DimensionClassifier(vector_path, embed_generator)
    except Exception as e:
        sys.exit(f"Error: {e}")

    texts_to_process, is_interactive = [], False
    if args.file:
        if not args.file.exists(): sys.exit(f"Error: Input file not found: {args.file}")
        if args.file.suffix.lower() == '.csv':
            if not args.column: sys.exit("Error: Must specify --column for CSV files.")
            with open(args.file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if args.column not in reader.fieldnames: sys.exit(f"Error: Column '{args.column}' not found. Available: {reader.fieldnames}")
                texts_to_process = [row[args.column] for row in reader]
        else:
            with open(args.file, 'r', encoding='utf-8') as f:
                texts_to_process = [line.strip() for line in f if line.strip()]
    elif args.text:
        texts_to_process = [args.text]
    elif not sys.stdin.isatty():
        texts_to_process = [line.strip() for line in sys.stdin if line.strip()]
    else:
        is_interactive = True
    
    if is_interactive:
        handle_interactive_mode(classifier)
    else:
        if not texts_to_process: sys.exit("No text to classify found in the input.")
        results = classifier.classify(texts_to_process)
        
        if args.output_format == 'json':
            print(format_as_json(results))
        elif args.output_format == 'csv':
            format_as_csv(results)
        else:
            print(format_as_table(results))

if __name__ == "__main__":
    main()
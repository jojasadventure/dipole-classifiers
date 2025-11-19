#!/usr/bin/env python
import argparse
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.log_setup import setup_logging
from core.embedding import EmbeddingGenerator

try:
    from datasets import load_from_disk, load_dataset
except ImportError:
    sys.exit("Error: 'datasets' library missing. Install with: pip install datasets")

def main():
    parser = argparse.ArgumentParser(description="Generate and cache embeddings for a dataset to JSONL.")
    
    # Inputs
    parser.add_argument('--dataset', type=str, required=True, help='Path to local dataset or Hugging Face ID')
    parser.add_argument('--column', type=str, default='text', help='The column name containing the text to embed')
    parser.add_argument('--limit', type=int, default=0, help='Only process the first N rows')
    
    # Outputs
    parser.add_argument('--output', type=str, required=True, help='Output JSONL file path')
    
    # Configuration
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    parser.add_argument('--embedding-api-url', type=str)
    parser.add_argument('--embedding-model-id', type=str)

    args = parser.parse_args()
    setup_logging()

    # 1. Configuration
    config = {}
    if Path(args.config).exists():
        import yaml
        with open(args.config, 'r') as f: config = yaml.safe_load(f)
    
    api_url = args.embedding_api_url or config.get('embedding_api_url')
    model_id = args.embedding_model_id or config.get('embedding_model_id')

    if not api_url or not model_id:
        sys.exit("Error: Embedding API URL and Model ID must be configured.")

    embedder = EmbeddingGenerator(base_url=api_url, model_name=model_id)

    # 2. Load Data
    print(f"Loading dataset: {args.dataset}")
    if Path(args.dataset).exists():
        ds = load_from_disk(args.dataset)
    else:
        ds = load_dataset(args.dataset, split='train')

    if args.limit > 0:
        print(f"Limiting to first {args.limit} rows.")
        ds = ds.select(range(args.limit))

    total_rows = len(ds)
    BATCH_SIZE = 32
    
    print(f"Starting embedding process for {total_rows} documents.")
    print(f"Model: {model_id}")
    print(f"Output: {args.output}")

    # 3. Process and Write
    with open(args.output, 'w', encoding='utf-8') as f_out:
        
        # Write Header/Metadata Line
        header = {
            "meta": True,
            "embedding_model": model_id,
            "source_dataset": str(args.dataset),
            "created_at": datetime.now().isoformat(),
            "count": total_rows
        }
        f_out.write(json.dumps(header) + "\n")

        # Loop in batches
        for i in range(0, total_rows, BATCH_SIZE):
            batch = ds[i:i+BATCH_SIZE]
            texts = batch[args.column]
            
            # Generate Vectors (using the robust generator)
            vectors = embedder.generate_embeddings(texts)
            
            # Write records
            for j, text in enumerate(texts):
                row_idx = i + j
                
                # Construct record with vector
                record = {
                    'row_index': row_idx,
                    'text': text,
                    'vector': vectors[j]
                }
                
                # Preserve other columns from the dataset
                for col in batch.keys():
                    if col != args.column:
                        # Convert any non-serializable types if necessary, 
                        # though standard HF datasets are usually JSON safe.
                        record[col] = batch[col][j]

                f_out.write(json.dumps(record) + "\n")
            
            # Progress update
            sys.stdout.write(f"\rProcessed {min(i + BATCH_SIZE, total_rows)}/{total_rows} documents...")
            sys.stdout.flush()

    print(f"\n\nComplete. Cache saved to: {args.output}")

if __name__ == "__main__":
    main()
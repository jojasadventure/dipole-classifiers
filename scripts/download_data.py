import argparse
import os
import sys
from datasets import load_dataset

def main():
    parser = argparse.ArgumentParser(description="Download HF datasets to a specific local path.")
    parser.add_argument('dataset', type=str, help="Hugging Face dataset ID (e.g., 'user/dataset' or 'sst2')")
    parser.add_argument('-o', '--output', type=str, required=True, help="The EXACT local folder to save to.")
    parser.add_argument('--split', type=str, default='train', help="Split to download (default: train)")
    parser.add_argument('--config', type=str, default=None, help="Dataset config name (if required, e.g. for GLUE)")

    args = parser.parse_args()

    # Safety check: Don't overwrite existing files effectively
    if os.path.exists(args.output) and os.listdir(args.output):
        print(f"WARNING: Target directory '{args.output}' is not empty.")
        confirm = input("Continue? [y/N]: ")
        if confirm.lower() != 'y':
            sys.exit("Aborted.")

    print(f"Downloading '{args.dataset}' [{args.split}]...")
    try:
        ds = load_dataset(args.dataset, args.config, split=args.split)
        print(f"Saving to: {args.output}")
        ds.save_to_disk(args.output)
        print("Done.")
    except Exception as e:
        sys.exit(f"Error: {e}")

if __name__ == "__main__":
    main()
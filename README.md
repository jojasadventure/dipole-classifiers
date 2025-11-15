# Dipole classifiers
Fast, lightweight semantic classifiers from contrastive sentence pairs. Train a ~1KB vector on 20 synthetic examples, achieve 82% accuracy on IMDB (Sentiment) at 30k words/second. 

This repo demonstrates a technique of creating semantic directions in embedding space from contrastive sentence pairs.
It identifies vectors (e.g., sentiment, formality, urgency) which can be used for lightweight classification or analysis with other embeddings in the same space. 

The benchmark results (see below) should be possible to recreate with this code.


![Training and classification workflow demonstration](docs/train-and-classify-demo.gif)


## Benchmarks

Tested against standard datasets with these results:

- **SST-2 (Sentiment)**: 84.3% accuracy
- **IMDB (Sentiment)**: 82.3% accuracy  
- **Pavlick Formality**: 0.61 correlation (r)

All using ~1KB semantic vectors derived from 20-100 synthetic training pairs.
Note: Increasing number of training pairs to 500 did not improve accuracy in one experiment.

**Speed**: ~30k words/second on RTX 3090 (embedding inference). Single dot product per classification runs on CPU.



### What This Is (And Isn't)

This is **not** a replacement for fine-tuned transformers when you need maximum accuracy. 

This could be useful for:
- Extremely fast inference
- Zero-shot classification without labeled training data
- Custom dimensions w/o training datasets ("insightful vs confused", "ephemeral vs important")
- Rapid prototyping and experimentation
- Edge deployment

**Trade-off**: ~10-15% accuracy penalty vs fine-tuned models, but 30x faster and trained in minutes on synthetic data, instead of hours on thousands of labeled examples.



## How to setup and run

This requires access to an embedding server and an LLM API as well as Python3.10. 

### **Step 1: Clone & Setup Python Environment**
```bash
git clone https://github.com/your-name/your-repo.git
cd your-repo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Step 2: Setup the Embedding Service**

You can use an external API or deploy your own Hugging Face `text-embeddings-inference` Docker container. Faster on GPU.
Both the docker steps will download the embedding model (~1GB) and start the required inference server. 
You need to stop it later. You can monitor it with eg. `docker stats`.

Choose one of the following paths:

- OPTION A: External API: Use your own embedding API like Jina: 
  - Copy config.yaml.template to config.yaml and set your api settings in there.

- OPTION B: CPU embedding: 
  - Copy config.yaml.cpu to config.yaml
  - Run TEI docker for CPU command below. Note: Stop later with `docker stop tei-cpu`.

```bash
docker run -d -p 8080:80 --name tei-cpu \
  ghcr.io/huggingface/text-embeddings-inference:cpu-1.6 \
  --model-id nomic-ai/nomic-embed-text-v1.5
```

- OPTION C: GPU embedding:
    - Edit the provided docker-compose.tei.yaml to set your GPU IMAGE_TAG
    - Optionally rename to docker-compose.yml and run



### **Step 3: Configure Your LLM API Key**
Keep editing the config.yaml and setup your LLM API details:
- e.g. set provider to "google", "openai" , "ollama" 
- edit their settings such as URL and API key



### **Step 4: Train Your First Dimension Vector**
```bash
python run_pipeline.py --dimension "Formality: Formal vs Informal" --num-pairs 50 --validate-new
```

**Step 5: Use Your New Classifier!**
The interactive tool will automatically discover the vector you just created.
```bash
python scripts/classify.py
```



## Command-line arguments for run_pipeline.py and settings in `config.yaml`

Important: Write CLI params with hyphens. 
```bash
$ python run_pipeline.py
usage: run_pipeline.py [-h] --dimension DIMENSION [--config CONFIG] [--validate-sample] [--validate-new] [--llm-provider {google,openai,ollama}] [--llm-api-key LLM_API_KEY] [--llm-api-url LLM_API_URL]
                       [--llm-model-name LLM_MODEL_NAME] [--llm-temperature LLM_TEMPERATURE] [--llm-num-pairs LLM_NUM_PAIRS] [--embedding-api-url EMBEDDING_API_URL] [--embedding-model-id EMBEDDING_MODEL_ID]
                       [--pipeline-run-validation-by-default] [--num-validation-samples NUM_VALIDATION_SAMPLES] [--pipeline-validation-pairs-override-path PIPELINE_VALIDATION_PAIRS_OVERRIDE_PATH]

$ python run_pipeline.py --dimension "Anthromomorphic: Cat-Person vs Dog-Person" --num-pairs 20 --validate-sample
```
Command-line arguments will always override the values in the file.

Write the config.yaml parameters with underscores: 

*   `llm_provider`: **Required.** `google`, `openai`, or `ollama`.
*   `llm_api_key`: **Required** for `google` and `openai`.
*   `llm_api_url`: Optional override for `openai` (e.g., OpenRouter), **Required** for `ollama` (e.g., `http://localhost:11434/v1`).
*   `llm_model_name`: The specific model identifier (e.g., `gemini-1.5-pro-latest`).
*   `llm_temperature`, `llm_num_pairs`: Control the generation process.
*   `embedding_api_url`: **Required.** The base URL of your embedding service (e.g., `http://localhost:8080`). The pipeline appends `/embed`.
*   `embedding_model_id`: **Required.** The model ID used by the embedding service (e.g., `nomic-ai/nomic-embed-text-v1.5`).
*   `pipeline_run_validation_by_default`: Set to `true` or `false` to run in-sample validation by default.
*   `pipeline_num_validation_samples`: The number of samples to generate per pole for out-of-sample validation.
*   `--prompt-file` Path to a custom prompt template to replace the default prompt.
*   `--prompt-extra-text "..."` Add text into the `{extra_instructions}` placeholder in the prompt (works also for default)

Examples:


```bash
python run_pipeline.py \
  --dimension "Insight: Confusion vs Insight" \
  --num-pairs 30 \
  --prompt-extra-text "The pairs should be in the context of learning, studying, or problem-solving. One sentence should reflect a moment of breakthrough or understanding, while the other reflects being stuck or confused about the same topic." \
  --validate-new
```

```bash
python run_pipeline.py \
  --dimension "Confidence: Tentative vs Confident" \
  --num-pairs 30 \
  --prompt-file ./prompts/confidence_prompt.txt \
  --validate-new
```

Below command will, instead of generating new validation samples, run its test against the benchmark set from another run.

```bash
python run_pipeline.py \
  --dimension "Confidence: Tentative vs Confident" \
  --num-pairs 30 \
  --prompt-file ./prompts/confidence_prompt.txt \
  --pipeline-validation-pairs-override-path results/Confidence_Tentative_vs_Confident/openaigpt-oss-120b_confidence_prompt_30p_20251115-200511/validation_samples.json
```

## Using a Classifier (`scripts/classify.py`)

#### Interactive Discovery (No arguments)
```bash
python scripts/classify.py
```

#### Classifying String or Files
```bash
# Classify a single string
python scripts/classify.py --vector <path_to_vector> --text "This is a sentence."

# Classify a column from a CSV and output as JSON
python scripts/classify.py \
  --vector <path_to_vector> \
  --file data/reviews.csv --column "review_text" \
  --output-format json > classified_reviews.json
```


## Usage

All commands should be run from the project root directory.

#### Running the Pipeline
```bash
# Generate a 'Formality' vector with 50 pairs
python run_pipeline.py --dimension "Formality: Formal vs Casual" --num-pairs 50

# Generate and run out-of-sample validation on a 'Sentiment' vector
python run_pipeline.py --dimension "Sentiment: Positive vs Negative" --validate-new

# Generate and run in-sample validation
python run_pipeline.py --dimension "Urgency: Urgent vs Non-Urgent" --validate-in-sample
```








## Output Directory Structure
The pipeline produces the following structure and artifacts:
```
results/
└── [DimensionName]_[PoleA]_vs_[PoleB]/
    └── [LLM-Name]_[NumPairs]_[Timestamp]/
        ├── _run_summary.json        # The complete "lab notebook" for the run, including all parameters.
        ├── pairs.json               # The raw LLM-generated text pairs.
        ├── embeddings.json          # Pairs with their corresponding embeddings.
        ├── dimension_vector.json    # The final, usable classifier artifact.
        ├── validation_samples.json  # (Optional) New samples for out-of-sample validation.
        └── validation_report.txt    # (Optional) The detailed accuracy report.
```





## Detailed Pipeline Workflow



run_pipeline.py automates the process of:
1.  Defining a semantic dimension (e.g., "Formality: Formal vs Casual", "Emotional Valence: Negative vs Positive").
2.  Generating contrastive sentence pairs representing the poles using an LLM.
3.  Embedding the synthetic sentence pairs.
4.  Extracting the semantic direction vector using the averaged normalized difference vector.
5.  Optionally validating the vector's effectiveness by asking the LLM to generate new single sentences.


The main orchestrator is `run_pipeline.py` and imports from modules in the `pipeline/` directory.

1.  **Parse & Configure:** The script loads settings from `config.yaml` 
2.  **Initialize Context:** It creates a unique run directory and a "Context" object that manages state and file paths
3.  **Generate Pairs (`pipeline/pair_generation.py`):** The orchestrator calls `pair_generation_logic()`, which uses the configured LLM to generate contrastive sentence pairs.
4.  **Generate Embeddings (`pipeline/embedding_generation.py`):** The orchestrator calls `embedding_generation_logic()`, which computes embeddings for each sentence.
5.  **Extract Vector (`pipeline/extract_vector.py`):** The orchestrator calls `extract_vector_logic()` for the core vector math:
    *   **Calculate Difference Vectors:** `v_diffᵢ = E(pole_bᵢ) - E(pole_aᵢ)` for each pair.
    *   **Normalize Difference Vectors:** Each vector is normalized to unit length to isolate its direction.
    *   **Average Normalized Vectors:** All unit vectors are averaged to find the consistent directional signal, canceling out noise from individual examples.
    *   **Normalize Final Vector:** The final average is normalized to produce the clean semantic unit vector.
6.  **Save Artifacts:** After each step, the orchestrator saves the resulting artifact (e.g., `pairs.json`, `dimension_vector.json`) to the unique run directory.
7.  **Validate Vector (Optional) (`pipeline/vector_validation.py`):** If a validation flag is used, the orchestrator calls `vector_validation_logic()` to test the new vector and save a detailed report.






## Future Directions

- Training data sources (synthetic vs real vs hybrid)
- Prompt engineering strategies for different dimensions
- Multi-model comparisons (LLM and embedding choices)
- Dimension combinations and multi-axis classification
- Domain-specific optimizations

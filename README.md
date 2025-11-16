# Dipole classifiers

Train a ~1KB vector in 2 minutes on 20 synthetic examples, run prediction at ~30k words/second on RTX 3090 (embedding inference). Single dot product per classification on CPU. Achieves 82% accuracy on IMDB (Sentiment). 

This repo demonstrates a technique for creating semantic directions in embedding space from contrastive sentence pairs. It identifies vectors (e.g., sentiment, formality, urgency) which can be used for lightweight classification or analysis with other embeddings in the same space. Read more about the [method](docs/method.md).

![Training and classification workflow demonstration](docs/train-and-classify-demo.gif)
(Screenshot of training and using classifier)

### Benchmarks

Tested against these standard datasets:

- **SST-2 (Sentiment)**: 84.3% accuracy
- **IMDB (Sentiment)**: 82.3% accuracy  
- **Pavlick Formality**: 0.61 correlation (r)



### What This Is (And Isn't)

This is **not** a replacement for fine-tuned transformers when you need maximum accuracy. 

This could be useful for:
- Extremely fast inference
- Zero-shot classification without labeled training data
- Custom dimensions without training datasets ("insightful vs confused", "ephemeral vs important")
- Rapid prototyping and experimentation
- Edge deployment

**Trade-off**: Accuracy penalty vs fine-tuned models, but 30x faster and trained in minutes on synthetic data vs hours on huge labeled datasets.

### Sample outputs

Example output from training runs here:
![Sample outputs](docs/sample-output.txt)


## How to setup and run

This requires access to an embedding server and an LLM API as well as Python3.10. 

### **Step 1: Clone & Setup Python Environment**
```bash
git clone https://github.com/jojasadventure/dipole-classifiers
cd dipole-classifiers
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Step 2: Setup the Embedding Service**

You can use an external API or deploy your own Hugging Face `text-embeddings-inference` docker container. Faster on GPU.
Docker option will download the embedding model (~1GB) and start the required API server.

**Choose one of the following paths:**

- OPTION A: External API: Use your own embedding API like Jina: 
  - Copy config.yaml.template to config.yaml and set your api settings in there.

- OPTION B: CPU embedding: 
  - Copy config.yaml.cpu to config.yaml
  - Run the TEI docker for CPU command below:

```bash
docker run -d -p 8080:80 --name tei-cpu \
  ghcr.io/huggingface/text-embeddings-inference:cpu-1.6 \
  --model-id nomic-ai/nomic-embed-text-v1.5
```

- OPTION C: GPU embedding:
    - Edit the provided docker-compose.tei.yaml to set your GPU IMAGE_TAG
    - Optionally rename to docker-compose.yml and run with `docker compose up`



### **Step 3: Configure Your LLM API Key**
Continue editing the config.yaml and set up your LLM API details:
- e.g. set provider to "google", "openai" , "ollama" 
- edit the settings such as URL and API key



### **Step 4: Train Dimension Vector**
```bash
python run_pipeline.py --dimension "Emotional Valence: Negative vs Positive" --num-pairs 50 --validate-new
```

**Step 5: Use New Classifier**
The interactive tool will automatically discover the vector you just created.
```bash
python scripts/classify.py
```

**Step 5: Benchmark a Classifier**

Once you have a vector, you can run the corresponding benchmark script. The required `-v`/`--vector` argument is the path to your `dimension_vector.json` file in the results dir. 


#### **Example: SST-2 Sentiment Benchmark**
```bash
python sst2-benchmark.py \
  --vector results/Sentiment_Positive_vs_Negative/qwen3:4b_20p_20250520-103000/dimension_vector.json
```

#### **Example: Pavlick Formality Benchmark**
```bash
python pavlick-formality-benchmark.py \
  --vector results/Formality_Formal_vs_Informal/qwen3:4b_20p_20250520-103500/dimension_vector.json
```


## Settings in `config.yaml`

Write the config.yaml parameters with underscores: 

*   `llm_provider`: **Required.** `google`, `openai`, or `ollama`.
*   `llm_api_key`: **Required** for `google` and `openai`.
*   `llm_api_url`: Optional override for `openai` (e.g., OpenRouter), **Required** for `ollama` (e.g., `http://localhost:11434/v1`).
*   `llm_batch_size`: How many sentence pairs or samples to request in a single API call.
*   `llm_model_name`: The specific model identifier (e.g., `qwen3:4b`).
*   `llm_temperature`, `llm_num_pairs`: Control the generation process.

*   `embedding_api_url`: **Required.** The base URL of your embedding service (e.g., `http://localhost:8080`). The pipeline appends `/embed`.
*   `embedding_model_id`: **Required.** The model ID used by the embedding service (e.g., `nomic-ai/nomic-embed-text-v1.5`).

*   `pipeline_run_validation_by_default`: Run in-sample validation by default.
*   `pipeline_num_validation_samples`:  Number of samples to generate per pole for out-of-sample validation.

If you want to run the above from terminal as arguments, please write with hyphens.
Command-line arguments will always override the values in the file. The below arguments make most sense for direct use in CLI: 
*   `dimension` Always state classifier in `Dimension: Pole A vs Pole B` format. 
*   `prompt-file` Path to a custom prompt template to replace the default prompt.
*   `prompt-extra-text "..."` Add text extra text to the built-in prompt
*   `validate-sample`  Run in-sample validation on the pairs used to generate the vector.
*   `validate-new` Generate new synthetic single samples and run validation on these.
*   `pipeline-num-validation-samples` How many in-model synthetic samples to validate on.
*   `pipeline-validation-pairs-override-path` Validate against samples from a previous run.


### CLI Examples:


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


## Benchmarking guide

These benchmarks are available: SST2, IMDB (Sentiment), Pavlick Formality, tasksource/subjectivity
Please consider the direction of Pole A **to** Pole B is hardcoded in the benchmarking scripts, so using a classifier with the poles swapped, may show reverse results in benchmarking. E.g. if you get negative correlation on the Pavlick benchmark, reverse Pole A and Pole B in the Formality classifier you trained.

### **Step 1: Train**

```bash
python run_pipeline.py --dimension "Emotional Valence: Negative vs Positive" --num-pairs 20 --validate-new
```

#### **Step 2: Run Benchmark**
```bash
python sst2-benchmark.py \
  --vector results/Sentiment_Positive_vs_Negative/mistral-small3.2:24b_20p_20250520-103000/dimension_vector.json
```



### **Step 1: Train a classifier for one of the scripts**


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





## Experimental Results & Findings

The following table showcases some of the most representative results. "Synthetic Accuracy" refers to the model's performance on new, synthetically generated samples from the same LLM that created the training pairs.

| Dimension                | LLM Generator                | # Pairs | Synthetic Accuracy | Benchmark Score (Dataset)            |
| ------------------------ | ---------------------------- | ------- | ------------------ | ------------------------------------ |
| **Sentiment / Valence**  | `openaigpt-oss-120b`         | 20      | 100%               | **84.3%** (SST-2), **82.3%** (IMDB)      |
| **Sentiment / Valence**  | `openaigpt-oss-120b`         | 500     | -                  | 84.5% (SST-2), 84.5% (IMDB)      |
| **Sentiment**            | `mistral-small-3.2`          | 20      | 97.5%              | 81.7% (IMDB)                         |
| **Confidence**           | `openaigpt-oss-120b`         | 10      | 97.5%              | -                                    |
| **Agency (Proactive)**   | `openaigpt-oss-120b`         | 30      | 87.5%              | -                                    |
| **Objectivity**          | `openaigpt-oss-120b`         | 50      | -                  | 66.7% (Subjectivity Dataset)         |
| **Insight (Confused)**   | `openaigpt-oss-120b`         | 30      | 60-85%             | -                                    |
| **Immediacy (Abstract)** | `z-aiglm-4.5-airfree`        | 30      | 56.5%              | -                                    |

### High Performance on Small Data

A sentiment vector trained on just **20 synthetic pairs** from a capable LLM (`openaigpt-oss-120b`) achieved **84.3% on SST-2** and **82.3% on IMDB**. 

### Diminishing Returns

When comparing a sentiment vector from 20 pairs against one from **500 pairs**:

*   **20 pairs:** 84.3% (SST-2) / 82.3% (IMDB)
*   **500 pairs:** 84.5% (SST-2) / 84.5% (IMDB)

Increasing the training data by **25x** yielded only a marginal **~0.2%** improvement on SST-2 and **~2.2%** on IMDB.



## Case Study: Prompt Engineering a "Confidence" Classifier

To understand the impact of prompting a targeted experiment was run with a "Confidence: Tentative vs. Confident" dimension.

**The Prompts:**
1.  **"Short & Consistent" (V1):** Used four highly parallel examples focusing on direct linguistic markers (e.g., "suggests" vs. "shows").
2.  **"Long & Detailed" (V4):** Used five more varied examples, including one specifically designed to teach the model about "implied confidence" (e.g., describing a confident action).

**The Process:**
1.  Realised a fixed synthetic validation was needed instead of new random samples each run.
2.  Refined prompt and ran a high-scoring validation set to use as a fixed synthetic benchmark.
3.  Created both short and long prompts. Tested resulting classifiers against fixed benchmark for a fair comparison.

**Results:**

| Prompt Version | Description | Accuracy on Fixed Benchmark |
| :--- | :--- | :---: |
| **V1** | **Short & Consistent** | **97.5%** |
| V4 | Long & Detailed | 92.5% |

**Takeaways:**

*   The "Short & Consistent" prompt, despite its simplicity, produced a significantly better and more robust classifier. The clean, focused signal was more effective than the more complex prompt that tried to account for every nuance. The simpler prompt's vector generalized better, even to the edge cases it wasn't explicitly shown.
*   Testing against a randomly generated validation set can create an illusion of performance. A prompt might just get lucky with the set of examples it's tested against. Using a fixed benchmark is better. (Obviously does not substitute real datasets.)
*   A few high-quality, highly parallel examples are more effective than a large, varied set. Focus on providing the LLM with a strong, unambiguous core concept.
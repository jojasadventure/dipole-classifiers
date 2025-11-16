# Semantic Direction Vectors in Embedding Spaces

## What This Is About

This describes a lightweight approach to sentiment analysis and semantic classification using the geometric properties of neural embedding spaces. By finding directional vectors that correspond to semantic concepts, you can do computationally cheap sentiment classification with minimal resources (~360MB VRAM). The approach uses contrastive pairs to extract semantic directions, which can then classify or modify content through simple vector arithmetic. It also shows how naturally occurring clusters in personal data can reveal domain-specific semantic dimensions without labeled training data.

## How It Works

### Extracting Semantic Direction Vectors

Given a semantic concept (e.g., sentiment polarity):

1. Generate or identify *n* pairs of statements {(p₁, n₁), (p₂, n₂), ..., (pₙ, nₙ)} where each pair expresses similar content with opposing semantic qualities
2. Compute embeddings for each statement: {E(p₁), E(n₁), E(p₂), E(n₂), ..., E(pₙ), E(nₙ)}
3. For each pair, calculate the normalized difference vector: v̂ᵢ = (E(pᵢ) - E(nᵢ)) / ||E(pᵢ) - E(nᵢ)||
4. Average these normalized vectors: v̂ₛₑₘₐₙₜᵢc = (1/n) ∑ᵢ₌₁ⁿ v̂ᵢ
5. Normalize the result: v̂ₛₑₘₐₙₜᵢc = v̂ₛₑₘₐₙₜᵢc / ||v̂ₛₑₘₐₙₜᵢc||

### Classification Using Semantic Direction Vectors

To classify a new statement x:

1. Compute its embedding E(x)
2. Calculate the projection onto the semantic direction vector: projection = E(x) · v̂ₛₑₘₐₙₜᵢc
3. The sign and magnitude indicate the statement's position along the semantic dimension

### Finding Natural Semantic Dimensions

To identify naturally occurring semantic dimensions in unlabeled data:

1. Compute embeddings for all data points
2. Apply clustering algorithms to identify distinct clusters
3. For opposing clusters, calculate the normalized vector between cluster centroids
4. Validate this vector as a semantic direction through classification of known examples

## Results

### Sentiment Analysis Performance

Using 20 synthetic contrastive pairs, a sentiment direction vector was constructed in a 756-dimensional embedding space. This vector achieved 84.3% accuracy on SST-2 and 82.3% on IMDB while requiring only 360MB VRAM. Traditional fine-tuned classifiers require significantly more computational resources and training time.

Processing speed was approximately 30,000 words/second on an RTX 3090 (for embedding inference), with classification itself being a single dot product on CPU.

### Diminishing Returns from More Data

Increasing training pairs from 20 to 500 yielded minimal improvement:
- 20 pairs: 84.3% (SST-2) / 82.3% (IMDB)
- 500 pairs: 84.5% (SST-2) / 84.5% (IMDB)

A 25x increase in training data produced only ~0.2% improvement on SST-2 and ~2.2% on IMDB.

### Natural Dimension Discovery

Applying clustering to personal journaling data revealed a natural semantic dimension distinguishing between personal/organic topics and technological/digital concepts. This dimension was validated through classification tests and worked without any labeled training data.

### Other Dimensions Tested

Various semantic dimensions were tested with different LLMs and training set sizes:

- Confidence (tentative vs. confident): 97.5% on synthetic validation with 10 pairs
- Agency (passive vs. proactive): 87.5% with 30 pairs
- Objectivity: 66.7% on subjectivity dataset with 50 pairs
- Insight (confused vs. clear): 60-85% accuracy depending on configuration
- Formality: 0.61 correlation (r) on Pavlick Formality benchmark

## Interpretation

Embedding spaces contain directional information that can be exploited for efficient semantic analysis. Classification through simple vector operations enables lightweight NLP applications that can run on edge devices or with minimal computational resources.

The discovery of natural semantic dimensions from unlabeled data suggests applications in personalized content analysis, trend detection, and semantic navigation of document collections.

## Prompt Engineering

Testing with a "Confidence" classifier showed that prompt design significantly impacts results:

- **Short & Consistent prompt** (4 parallel examples): 97.5% accuracy
- **Long & Detailed prompt** (5 varied examples): 92.5% accuracy

The simpler, more focused prompt produced a better classifier. Clean, parallel examples were more effective than complex prompts trying to cover edge cases.

Testing against randomly generated validation sets can be misleading. A fixed benchmark is more reliable for comparing different approaches.

## Limitations and Future Work

This is not a replacement for fine-tuned transformers when maximum accuracy is needed. The trade-off is an accuracy penalty versus fine-tuned models, but with  fster inference and training on minimal synthetic data.

Future work could explore:
- Orthogonalization of multiple semantic dimensions
- Stability of these dimensions across different embedding models
- Applications in content modification through vector arithmetic
- More complex semantic dimensions beyond binary poles
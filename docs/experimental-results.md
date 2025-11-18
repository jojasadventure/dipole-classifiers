# Experimental Classifiers (Tiered by Synthetic Accuracy)

This tiered view shows which concepts were clearly defined by the LLMs and which were more ambiguous or difficult to represent as a simple vector. The experiment reflects both the bias of the generating LLM as well as that of the embedding model.

A vector's strength appears to be determined by:

- Primal Nature: Is it core to physical, biological, or social experience?
- Symmetry & Extremity: Are the poles equal, opposite, and far apart? 
- Absoluteness: Does it describe an inherent state, not a relative comparison?
- Simplicity: Is it a simple core concept, or a high-level abstraction?
- Purity: Is it unambiguous, or does it suffer from metaphorical/homonymous contamination?
- Alignment: Does it require an uncensored model to represent fully?
- Exemplars: If an abstract concept, can it be represented by concrete, token-level examples? 


## Note on Synthetic Data

In this early version, each run generates synthetic data from the same model which generated the training pairs for the vector. Whilst this is limited as a validation method, it became apparent that the strongest and most stable vectors "show themselves" by being 100% across multiple runs of regenerating and using different sample data. 

## Variables

Prompting, few-shot examples, the LLM used, and the embedding generator used all influence the final result. A vector may work within it's model's examples but fail on IMDB's more nuanced expressions - use the provided benchmarks to compare against real data.


## Table

(Note: Trained with nomic-embed-text-v1_5)
| Tier | Dimension | Poles (A vs. B) | Synthetic Acc. | # Pairs | LLM Generator | Notes |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **---** | **Tier 1: (100%)** | **---** | **---** | **---** | **---** | **---** |
| 1 | Joy | Sadness vs. Joy | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Disgust | Attraction vs. Disgust | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Emotion | Fear vs. Safety | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Reason for visit | Business vs. Pleasure | 100.00% | 20 | `gemma3:4b` | |
| 1 | Energy | Kinetic vs. Static | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Speed | Fast vs. Slow | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Light | Dark vs. Light | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Logic | True vs. False | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Object | Broken vs. Whole | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Outcome | Success vs. Failure | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Phase | Solid vs. Gas | 100.00% | 20 | `gemma-3-12b-it` | |
| 1 | Sacred-Profane | Bible vs. Porn | 100.00% | 25 | `Phi-lthy4_GGUF` | Uncensored model |
| 1 | Sex | Consensual vs. Nonconsensual | 100.00% | 25 | `Phi-lthy4_GGUF` | Uncensored model |
| **---** | **Tier 2: Good (90%)** | **---** | **---** | **---** | **---** | **---** |
| 2 | Relationship | Love vs. Hate | 97.67% | 25 | `Phi-lthy4_GGUF` | |
| 2 | Condition | Sick vs. Healthy | 97.62% | 20 | `gemma3:4b` | |
| 2 | Accord | Dissonance vs. Harmony | 97.50% | 20 | `gemma-3-12b-it` | |
| 2 | Action | Create vs. Destroy | 97.50% | 20 | `gemma-3-12b-it` | |
| 2 | Emotion | Confident vs. Anxious | 97.50% | 20 | `gemma-3-12b-it` | |
| 2 | Interest | Boring vs. Exciting | 97.50% | 20 | `gemma-3-12b-it` | |
| 2 | Meaning | Meaningless vs. Meaningful | 97.50% | 20 | `gemma-3-12b-it` | |
| 2 | Morals | Good vs. Evil | 97.50% | 20 | `gemma-3-12b-it` |  |
| 2 | Property | Sharp vs. Dull | 97.50% | 20 | `gemma-3-12b-it` | |
| 2 | State | In control vs. Out of control | 97.50% | 20 | `gemma3:4b` | |
| 2 | Task | To-Do vs. Done | 97.50% | 20 | `gemma-3-12b-it` | |
| 2 | Existence | Present vs. Absent | 95.00% | 20 | `gemma-3-12b-it` | |
| 2 | Sensation | Pain vs. Relief | 95.00% | 20 | `gemma-3-12b-it` | |
| 2 | Sensation | Wet vs. Dry | 95.00% | 20 | `gemma-3-12b-it` | |
| 2 | Size | Small vs. Large | 95.00% | 20 | `gemma-3-12b-it` | |
| 2 | Sound | Loud vs. Quiet | 95.00% | 20 | `gemma-3-12b-it` | |
| 2 | State | Full vs. Empty | 95.00% | 20 | `gemma-3-12b-it` | |
| 2 | Straight | Form vs. Crooked | 95.00% | 20 | `gemma-3-12b-it` | |
| 2 | Struggle | Suffering vs. Salvation | 95.00% | 20 | `gemma-3-12b-it` | |
| 2 | Condition | Clean vs. Dirty | 92.50% | 20 | `gemma-3-12b-it` | |
| 2 | Existence | Life vs. Death | 92.50% | 20 | `gemma-3-12b-it` | |
| 2 | State | Resolved vs. Unresolved | 92.50% | 20 | `gemma-3-12b-it` | |
| 2 | State | War vs. Peace | 90.91% | 25 | `Phi-lthy4_GGUF` | |
| 2 | Content | Depravity vs. Family-Friendly | 90.48% | 24 | `Phi-lthy4_GGUF` | |
| 2 | Conflict | Attack vs. Defend | 90.00% | 20 | `gemma-3-12b-it` | |
| 2 | Handling | Brutality vs. Tenderness | 90.00% | 20 | `gemma3:4b` | |
| 2 | Mass | Heavy vs. Light | 90.00% | 20 | `gemma-3-12b-it` | |
| 2 | Reaction | Surprise vs. Expectation | 90.00% | 20 | `gemma-3-12b-it` | |
| 2 | Social | Lonely vs. Together | 90.00% | 25 | `gemma-3-12b-it` | |
| 2 | Taste | Sweet vs. Sour | 90.00% | 20 | `gemma-3-12b-it` | |
| 2 | Temperature | Hot vs. Cold | 90.00% | 20 | `gemma-3-12b-it` | |
| **---** | **Tier 3: Unstable (80%)** | **---** | **---** | **---** | **---** | **---** |
| 3 | Emotional State | Heightened emotion vs. Neutral state | 88.10% | 20 | `gemma3:4b` | |
| 3 | Santa's List | Naughty vs. Nice | 87.80% | 25 | `Phi-lthy4_GGUF` | |
| 3 | Emotion | Calm vs. Upset | 87.50% | 20 | `gemma-3-12b-it` | |
| 3 | Hierarchy | Wealthy vs. Poor | 87.50% | 20 | `gemma-3-12b-it` | |
| 3 | Morals | Bad vs. Good | 87.50% | 20 | `gemma-3-12b-it` | |
| 3 | Desire | Male vs. Female | 86.36% | 25 | `Phi-lthy4_GGUF` | |
| 3 | Sex | Dominance vs. Submission | 85.71% | 25 | `Phi-lthy4_GGUF` | |
| 3 | Gender | Male vs. Female | 85.00% | 25 | `gemma-3-12b-it` | Note: Bias apparent |
| 3 | Narrative | Vivid description vs. Factual exposition | 85.00% | 20 | `gemma3:4b` | |
| 3 | Condition | Possible vs. Impossible | 82.50% | 20 | `gemma-3-12b-it` | |
| 3 | Direction | Up vs. Down | 82.50% | 20 | `gemma-3-12b-it` | |
| 3 | Emotion | Anger vs. Acceptance | 82.50% | 20 | `gemma-3-12b-it` | |
| 3 | Knowledge Source | Scientific Evidence vs. Spiritual Wisdom | 82.50% | 20 | `gemma3:4b` | |
| 3 | News | Fact vs. Opinion | 82.50% | 21 | `gemma3:4b` | |
| 3 | Physics | Unstoppable force vs. Immovable object | 82.50% | 20 | `gemma3:4b` | |
| 3 | State | Open vs. Closed | 82.50% | 20 | `gemma-3-12b-it` | |
| 3 | Age | Young vs. Old | 80.00% | 20 | `gemma-3-12b-it` | |
| 3 | Movement | Arrive vs. Depart | 80.00% | 20 | `gemma-3-12b-it` | |
| **---** | **Tier 4: Weak (70%)** | **---** | **---** | **---** | **---** | **---** |
| 4 | Creative Process | Chaotic exploration vs. Systematic execution | 77.50% | 20 | `gemma3:4b` | |
| 4 | Culture | Natural vs. Man-made | 77.50% | 20 | `gemma-3-12b-it` | |
| 4 | Human Experience | Loneliness vs. Solitude | 77.50% | 20 | `gemma3:4b` | |
| 4 | Origin | Organic vs. Artificial | 77.50% | 20 | `gemma-3-12b-it` | |
| 4 | Power | Dominant vs. Submissive | 77.50% | 20 | `gemma-3-12b-it` | |
| 4 | Culture | Wild vs. Tame | 75.00% | 20 | `gemma-3-12b-it` | |
| 4 | Identity | Same vs. Different | 75.00% | 20 | `gemma-3-12b-it` | |
| 4 | Motivation | Have To vs. Want To | 75.00% | 20 | `gemma3:4b` | |
| 4 | Object | Relic vs. Junk | 75.00% | 20 | `gemma-3-12b-it` | |
| 4 | Perception | Distant vs. Nearby | 75.00% | 20 | `gemma-3-12b-it` | |
| 4 | Information | Signal vs. Noise | 70.00% | 20 | `gemma-3-12b-it` | |
| 4 | Language | Aggressive vs. Passive | 70.00% | 20 | `gemma-3-12b-it` | |
| 4 | Power | Strong vs. Weak | 70.00% | 20 | `gemma-3-12b-it` | |
| **---** | **Tier 5: Poor (60%)** | **---** | **---** | **---** | **---** | **---** |
| 5 | Articles | News vs. Commentary | 67.50% | 20 | `gemma3:4b` | |
| 5 | Distance | Far vs. Near | 67.50% | 20 | `gemma-3-12b-it` | |
| 5 | Society | Insider vs. Outsider | 67.50% | 20 | `gemma-3-12b-it` | |
| 5 | Condition | Raw vs. Cooked | 65.00% | 20 | `gemma-3-12b-it` | |
| 5 | Ethics | Right vs. Wrong | 65.00% | 20 | `gemma-3-12b-it` | |
| 5 | Information | Signal vs. Noise | 65.00% | 21 | `gemma3:4b` | |
| 5 | Thinking | Known Fact vs. Pure Speculation | 65.00% | 21 | `gemma3:4b` | |
| 5 | Visibility | Visible vs. Invisible | 65.00% | 20 | `gemma-3-12b-it` | |
| 5 | Analysis | Subjective vs. Objective | 62.50% | 20 | `gemma-3-12b-it` | |
| 5 | Thinking | Known Fact vs. Assumption | 62.50% | 20 | `gemma3:4b` | |
| 5 | Interaction | Give vs. Take | 60.00% | 20 | `gemma-3-12b-it` | |
| 5 | Structure | Whole vs. Part | 60.00% | 20 | `gemma-3-12b-it` | |
| **---** | **Tier 6: Non-working (< 60%)** | **---** | **---** | **---** | **---** | **---** |
| 6 | Knowledge | Absolute certainty vs. Pure speculation | 55.00% | 20 | `gemma3:4b` | |
| 6 | Flow of Text | Staying on subject vs. Changing topic | 52.50% | 21 | `gemma3:4b` | Near chance level |
| 6 | Meaning | Sacred vs. Profane | 52.50% | 20 | `gemma-3-12b-it` | |
| 6 | Political | Left-leaning vs. Right-wing | 52.50% | 20 | `gemma3:4b` | Near chance level |
| 6 | Logic/Math | Relative vs. Absolute | 50.00% | 20 | `gemma3:4b` | Chance level |
| 6 | State | Asleep vs. Awake | 45.00% | 20 | `gemma-3-12b-it` | Worse than chance |





# RAW OUTPUT - unordered





---------
VALIDATION REPORT for Dimension: Desire (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Male
Pole B (Positive Score): Female
---------
Overall Accuracy: 86.36% (38/44)
---------
---------
VALIDATION REPORT for Dimension: Action (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Violence
Pole B (Positive Score): Peaceful resolution
---------
Overall Accuracy: 97.73% (43/44)
---------



---------
VALIDATION REPORT for Dimension: Condition (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Raw
Pole B (Positive Score): Cooked
---------
Overall Accuracy: 65.00% (26/40)
---------
---------
VALIDATION REPORT for Dimension: Age (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Young
Pole B (Positive Score): Old
---------
Overall Accuracy: 80.00% (32/40)
---------


---------
VALIDATION REPORT for Dimension: Culture (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Wild
Pole B (Positive Score): Tame
---------
Overall Accuracy: 75.00% (30/40)
---------

---------
VALIDATION REPORT for Dimension: Culture (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Natural
Pole B (Positive Score): Man-made
---------
Overall Accuracy: 77.50% (31/40)
---------

---------
VALIDATION REPORT for Dimension: Meaning (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Sacred
Pole B (Positive Score): Profane
---------
Overall Accuracy: 52.50% (21/40)
---------
---------
VALIDATION REPORT for Dimension: Meaning (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Meaningless
Pole B (Positive Score): Meaningful
---------
Overall Accuracy: 97.50% (39/40)
---------




---------
VALIDATION REPORT for Dimension: Object (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Relic
Pole B (Positive Score): Junk
---------
Overall Accuracy: 75.00% (30/40)
---------
--- Training Pairs Used to Generate Vector ---

---------
VALIDATION REPORT for Dimension: Object (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Broken
Pole B (Positive Score): Whole
---------
Overall Accuracy: 100.00% (40/40)
-------------------------------------------------------------------------------

---------
VALIDATION REPORT for Dimension: Perception (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Distant
Pole B (Positive Score): Nearby
---------
Overall Accuracy: 75.00% (30/40)
---------

---------
VALIDATION REPORT for Dimension: Society (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Insider
Pole B (Positive Score): Outsider
---------
Overall Accuracy: 67.50% (27/40)
---------

---------
VALIDATION REPORT for Dimension: Emotion (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Confident
Pole B (Positive Score): Anxious
---------
Overall Accuracy: 97.50% (39/40)
---------

---------
VALIDATION REPORT for Dimension: Language (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Aggressive
Pole B (Positive Score): Passive
---------
Overall Accuracy: 70.00% (28/40)
---------


---------
VALIDATION REPORT for Dimension: XXX (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 24 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Depravity
Pole B (Positive Score): Family-Friendly
---------
Overall Accuracy: 90.48% (38/42)
---------

---------
VALIDATION REPORT for Dimension: Sex (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Consensual
Pole B (Positive Score): Nonconsensual
---------
Overall Accuracy: 100.00% (40/40)
---------

---------
VALIDATION REPORT for Dimension: Sex (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Dominance
Pole B (Positive Score): Submission
---------
Overall Accuracy: 85.71% (36/42)
---------


---------
VALIDATION REPORT for Dimension: Relationship (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Love
Pole B (Positive Score): Hate
---------
Overall Accuracy: 97.67% (42/43)
---------


---------
VALIDATION REPORT for Dimension: Santa's List (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Naughty
Pole B (Positive Score): Nice
---------
Overall Accuracy: 87.80% (36/41)
---------


---------
VALIDATION REPORT for Dimension: State (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): War
Pole B (Positive Score): Peace
---------
Overall Accuracy: 90.91% (40/44)
---------


---------
VALIDATION REPORT for Dimension: Sacred-Profane (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Bible
Pole B (Positive Score): Porn
---------
Overall Accuracy: 100.00% (42/42)
---------


---------
VALIDATION REPORT for Dimension: Sacred-Profane (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'hf.co/SicariusSicariiStuff/Phi-lthy4_GGUF:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Relgious imagery
Pole B (Positive Score): Hardcore Porn Scene
---------
Overall Accuracy: 100.00% (43/43)
---------
note: not that useful























---------
VALIDATION REPORT for Dimension: Conflict (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Attack
Pole B (Positive Score): Defend
---------
Overall Accuracy: 90.00% (36/40)
---------



---------
VALIDATION REPORT for Dimension: Hierarchy (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Wealthy
Pole B (Positive Score): Poor
---------
Overall Accuracy: 87.50% (35/40)
---------


---------
VALIDATION REPORT for Dimension: Power (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Dominant
Pole B (Positive Score): Submissive
---------
Overall Accuracy: 77.50% (31/40)
---------
---------
VALIDATION REPORT for Dimension: Power (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Strong
Pole B (Positive Score): Weak
---------
Overall Accuracy: 70.00% (28/40)
---------

---------
VALIDATION REPORT for Dimension: Action (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Create
Pole B (Positive Score): Destroy
---------
Overall Accuracy: 97.50% (39/40)
---------

---------
VALIDATION REPORT for Dimension: Ethics (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Right
Pole B (Positive Score): Wrong
---------
Overall Accuracy: 65.00% (26/40)
---------
---------
VALIDATION REPORT for Dimension: Morals (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Bad
Pole B (Positive Score): Good
---------
Overall Accuracy: 87.50% (35/40)
---------

---------
VALIDATION REPORT for Dimension: Sensation (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Pain
Pole B (Positive Score): Relief
---------
Overall Accuracy: 95.00% (38/40)
---------

---------
VALIDATION REPORT for Dimension: Struggle (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Suffering
Pole B (Positive Score): Salvation
---------
Overall Accuracy: 95.00% (38/40)
---------



oooh so dicey
---------
VALIDATION REPORT for Dimension: Morals (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Good
Pole B (Positive Score): Evil
---------
Overall Accuracy: 97.50% (39/40)
------------




---------
VALIDATION REPORT for Dimension: Speed (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Fast
Pole B (Positive Score): Slow
---------
Overall Accuracy: 100.00% (40/40)
---------



Bias apparent:
---------
VALIDATION REPORT for Dimension: Gender (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Male
Pole B (Positive Score): Female
---------
Overall Accuracy: 85.00% (34/40)
---------
--- Validation Sample Results ---
Overall Accuracy: 85.00% (34/40)
---------
--- Results for Pole B: Female ---
RESULT       | SCORE        | PREDICTION      | TEXT
........................................
[INCORRECT]   | -0.0945      | Male            | The CEO navigated the boardroom with quiet confidence and sharp intellect.
[INCORRECT]   | -0.0521      | Male            | The engineer designed a sustainable housing project for low-income families.
[INCORRECT]   | -0.0284      | Male            | The detective meticulously examined the crime scene, searching for clues.
[INCORRECT]   | -0.0107      | Male            | The biologist studied the reproductive patterns of marine mammals, uncovering fascinating insights.
[INCORRECT]   | -0.0020      | Male            | The musician composed a haunting melody, expressing deep emotional vulnerability.




---------
VALIDATION REPORT for Dimension: Interest (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Boring
Pole B (Positive Score): Exciting
---------
Overall Accuracy: 97.50% (39/40)
---------




---------
VALIDATION REPORT for Dimension: Accord (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Dissonance
Pole B (Positive Score): Harmony
---------
Overall Accuracy: 97.50% (39/40)
---------





---------
VALIDATION REPORT for Dimension: Interaction (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Give
Pole B (Positive Score): Take
---------
Overall Accuracy: 60.00% (24/40)
---------
---------
VALIDATION REPORT for Dimension: Movement (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Arrive
Pole B (Positive Score): Depart
---------
Overall Accuracy: 80.00% (32/40)
---------













---------
VALIDATION REPORT for Dimension: Outcome (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Success
Pole B (Positive Score): Failure
---------
Overall Accuracy: 100.00% (40/40)
---------


---------
VALIDATION REPORT for Dimension: Existence (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Present
Pole B (Positive Score): Absent
---------
Overall Accuracy: 95.00% (38/40)
---------


---------
VALIDATION REPORT for Dimension: Condition (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Clean
Pole B (Positive Score): Dirty
---------
Overall Accuracy: 92.50% (37/40)
---------

---------
VALIDATION REPORT for Dimension: Property (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Sharp
Pole B (Positive Score): Dull
---------
Overall Accuracy: 97.50% (39/40)
---------



---------
VALIDATION REPORT for Dimension: Phase (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Solid
Pole B (Positive Score): Gas
---------
Overall Accuracy: 100.00% (40/40)
---------















---------
VALIDATION REPORT for Dimension: Sensation (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Wet
Pole B (Positive Score): Dry
---------
Overall Accuracy: 95.00% (38/40)
---------



---------
VALIDATION REPORT for Dimension: Taste (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Sweet
Pole B (Positive Score): Sour
---------
Overall Accuracy: 90.00% (36/40)
---------



---------
VALIDATION REPORT for Dimension: Sound (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Loud
Pole B (Positive Score): Quiet
---------
Overall Accuracy: 95.00% (38/40)
---------





---------
VALIDATION REPORT for Dimension: State (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Asleep
Pole B (Positive Score): Awake
---------
Overall Accuracy: 45.00% (18/40)
---------




---------
VALIDATION REPORT for Dimension: State (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Full
Pole B (Positive Score): Empty
---------
Overall Accuracy: 95.00% (38/40)
---------


---------
VALIDATION REPORT for Dimension: Visibility (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Visible
Pole B (Positive Score): Invisible
---------
Overall Accuracy: 65.00% (26/40)
---------

---------
VALIDATION REPORT for Dimension: Form (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Straight
Pole B (Positive Score): Crooked
---------
Overall Accuracy: 95.00% (38/40)
---------




---------
VALIDATION REPORT for Dimension: Logic (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): True
Pole B (Positive Score): False
---------
Overall Accuracy: 100.00% (40/40)
---------
--- Training Pairs Used to Generate Vector ---
Pair 1:
  - True: The project was completed ahead of schedule and under budget.
  - False: The project fell behind schedule and exceeded the allocated budget.
Pair 2:
  - True: The restaurant's new menu features locally sourced, organic ingredients.
  - False: The restaurant's new menu uses primarily processed and imported ingredients.
Pair 3:
  - True: The software update successfully resolved all reported security vulnerabilities.
  - False: The software update introduced several new security vulnerabilities.
Pair 4:
  - True: The team effectively collaborated to achieve the shared goal.
  - False: The team experienced significant conflict and failed to reach a consensus.
Pair 5:
  - True: The customer service representative promptly and efficiently addressed the issue.
  - False: The customer service representative was unhelpful and prolonged the problem.
... and 15 more pairs.


--- Validation Sample Results ---
Overall Accuracy: 100.00% (40/40)
---------
--- Results for Pole B: False ---
RESULT       | SCORE        | PREDICTION      | TEXT
........................................
[CORRECT]     | +0.0171      | False           | The detective realized the alibi was a carefully constructed illusion.
[CORRECT]     | +0.0336      | False           | The weather forecast predicted sunshine, but it rained all day.
[CORRECT]     | +0.0440      | False           | The scientific theory, once widely accepted, was later disproven by new evidence.
[CORRECT]     | +0.0683      | False           | The experiment yielded null results, indicating no correlation.
[CORRECT]     | +0.0908      | False           | The rumor spread quickly, but it turned out to be entirely fabricated.
[CORRECT]     | +0.0914      | False           | The painting was a forgery, skillfully mimicking the artist's style.
[CORRECT]     | +0.1146      | False           | The antique clock chimed thirteen times, a clear malfunction.
[CORRECT]     | +0.1243      | False           | Despite his confident assertion, the data simply didn't support his claim.
[CORRECT]     | +0.1263      | False           | The legend of the monster was just a story to scare children.
[CORRECT]     | +0.1265      | False           | The security system failed to detect the intruder, a critical oversight.
[CORRECT]     | +0.1367      | False           | The politician's promise of lower taxes was a deceptive tactic.
[CORRECT]     | +0.1376      | False           | The treasure hunt ended abruptly when they discovered the clues were meaningless.
[CORRECT]     | +0.1448      | False           | Her memory of the event was distorted, a hazy recollection of what actually happened.
[CORRECT]     | +0.1704      | False           | The news report was retracted after it was discovered to be inaccurate.
[CORRECT]     | +0.1725      | False           | The map was hopelessly outdated, leading us in circles for hours.
[CORRECT]     | +0.1778      | False           | The company's financial report contained several significant errors.
[CORRECT]     | +0.1968      | False           | The automated system delivered the wrong package, a frustrating mistake.
[CORRECT]     | +0.2100      | False           | The translation was nonsensical, a complete misunderstanding of the original text.
[CORRECT]     | +0.2404      | False           | The witness's testimony proved unreliable, riddled with inconsistencies.
[CORRECT]     | +0.2653      | False           | The script contained plot holes so glaring, the play was unwatchable.
--- Results for Pole A: True ---
RESULT       | SCORE        | PREDICTION      | TEXT
........................................
[CORRECT]     | -0.2519      | True            | The experiment yielded results that aligned perfectly with the theory.
[CORRECT]     | -0.2510      | True            | Her understanding of the subject was complete and thorough.
[CORRECT]     | -0.2223      | True            | The solution to the puzzle was elegantly simple and undeniable.
[CORRECT]     | -0.2078      | True            | The map accurately depicted the terrain, leading them safely through the wilderness.
[CORRECT]     | -0.2075      | True            | His intuition proved correct, guiding him to the right decision.
[CORRECT]     | -0.2064      | True            | Her calculations confirmed the initial hypothesis with remarkable precision.
[CORRECT]     | -0.1825      | True            | The historical record consistently validated her family's legacy.
[CORRECT]     | -0.1591      | True            | The evidence overwhelmingly supported his account of the events.
[CORRECT]     | -0.1574      | True            | The detective's deductions were flawless, revealing the culprit's identity.
[CORRECT]     | -0.1424      | True            | The architect's design flawlessly integrated form and function.
[CORRECT]     | -0.1400      | True            | The athlete's performance exceeded all expectations, setting a new record.
[CORRECT]     | -0.1237      | True            | The company's financial statements reflected a period of unprecedented growth.
[CORRECT]     | -0.1167      | True            | The forecast predicted the storm's path with uncanny accuracy.
[CORRECT]     | -0.1166      | True            | The judge's ruling was based on established legal precedent.
[CORRECT]     | -0.1135      | True            | The witness's testimony remained consistent throughout the investigation.
[CORRECT]     | -0.0868      | True            | The poem's imagery resonated deeply, capturing the essence of the moment.
[CORRECT]     | -0.0862      | True            | The story unfolded exactly as the ancient prophecy foretold.
[CORRECT]     | -0.0831      | True            | Based on the data, the conclusion seemed inevitable.
[CORRECT]     | -0.0818      | True            | The scientist's findings revolutionized the field of medicine.
[CORRECT]     | -0.0606      | True            | The restoration brought the painting back to its original splendor.
---------

23:51:16 - FINAL_ACCURACY:100.00% (40/40)






---------
VALIDATION REPORT for Dimension: Identity (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Same
Pole B (Positive Score): Different
---------
Overall Accuracy: 75.00% (30/40)
---------





---------
VALIDATION REPORT for Dimension: Condition (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Possible
Pole B (Positive Score): Impossible
---------
Overall Accuracy: 82.50% (33/40)
---------







---------
VALIDATION REPORT for Dimension: Disgust (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Attraction
Pole B (Positive Score): Disgust
---------
Overall Accuracy: 100.00% (40/40)
---------


---------
VALIDATION REPORT for Dimension: Reaction (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Surprise
Pole B (Positive Score): Expectation
---------
Overall Accuracy: 90.00% (36/40)
---------

---------
VALIDATION REPORT for Dimension: Analysis (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Subjective
Pole B (Positive Score): Objective
---------
Overall Accuracy: 62.50% (25/40)
---------
--- Training Pairs Used to Generate Vector ---




---------
VALIDATION REPORT for Dimension: Size (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Small
Pole B (Positive Score): Large
---------
Overall Accuracy: 95.00% (38/40)
---------


---------
VALIDATION REPORT for Dimension: Direction (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Up
Pole B (Positive Score): Down
---------
Overall Accuracy: 82.50% (33/40)
---------


---------
VALIDATION REPORT for Dimension: Distance (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Far
Pole B (Positive Score): Near
---------
Overall Accuracy: 67.50% (27/40)
---------



---------
VALIDATION REPORT for Dimension: Social (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 25 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Lonely
Pole B (Positive Score): Together
---------
Overall Accuracy: 90.00% (36/40)
---------





---------
VALIDATION REPORT for Dimension: Joy (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Sadness
Pole B (Positive Score): Joy
---------
Overall Accuracy: 100.00% (40/40)
---------


---------
VALIDATION REPORT for Dimension: Emotion (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Calm
Pole B (Positive Score): Upset
---------
Overall Accuracy: 87.50% (35/40)
---------



---------
VALIDATION REPORT for Dimension: Emotion (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Anger
Pole B (Positive Score): Acceptance
---------
Overall Accuracy: 82.50% (33/40)
---------
--- Training Pairs Used to Generate Vector ---





---------
VALIDATION REPORT for Dimension: Emotion (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Fear
Pole B (Positive Score): Safety
---------
Overall Accuracy: 100.00% (40/40)
---------




---------
VALIDATION REPORT for Dimension: Information (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Signal
Pole B (Positive Score): Noise
---------
Overall Accuracy: 70.00% (28/40)
-------------------------------------

---------
VALIDATION REPORT for Dimension: Light (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Dark
Pole B (Positive Score): Light
---------
Overall Accuracy: 100.00% (40/40)
---------






VALIDATION REPORT for Dimension: State (Out-of-Sample)
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Open
Pole B (Positive Score): Closed

Overall Accuracy: 82.50% (33/40)






---------
VALIDATION REPORT for Dimension: State (Out-of-Sample)
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Resolved
Pole B (Positive Score): Unresolved

Overall Accuracy: 92.50% (37/40)







---------
VALIDATION REPORT for Dimension: Energy (Out-of-Sample)
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Kinetic
Pole B (Positive Score): Static

Overall Accuracy: 100.00% (40/40)







---------
VALIDATION REPORT for Dimension: Task (Out-of-Sample)
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): To-Do
Pole B (Positive Score): Done

Overall Accuracy: 97.50% (39/40)











---------
VALIDATION REPORT for Dimension: Existence (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Life
Pole B (Positive Score): Death
---------
Overall Accuracy: 92.50% (37/40)
---------



---------
VALIDATION REPORT for Dimension: Mass (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Heavy
Pole B (Positive Score): Light
---------
Overall Accuracy: 90.00% (36/40)
---------




---------
VALIDATION REPORT for Dimension: Temperature (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Hot
Pole B (Positive Score): Cold
---------
Overall Accuracy: 90.00% (36/40)
---------



---------
VALIDATION REPORT for Dimension: Origin (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Organic
Pole B (Positive Score): Artificial
---------
Overall Accuracy: 77.50% (31/40)
---------






---------
VALIDATION REPORT for Dimension: Structure (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'kwangsuklee/gemma-3-12b-it-Q4_K_M:latest'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Whole
Pole B (Positive Score): Part
---------
Overall Accuracy: 60.00% (24/40)
---------





---------
VALIDATION REPORT for Dimension: Narrative Technique (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Vivid immersive description
Pole B (Positive Score): Direct factual exposition
---------
Overall Accuracy: 85.00% (34/40)
---------


---------
VALIDATION REPORT for Dimension: Physics (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): An unstoppable force
Pole B (Positive Score): an immovable object
---------
Overall Accuracy: 82.50% (33/40)
---------

---------
VALIDATION REPORT for Dimension: Source of Knowledge (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Scientfic Evidence
Pole B (Positive Score): Spiritual Wisdom
---------
Overall Accuracy: 82.50% (33/40)
---------


---------
VALIDATION REPORT for Dimension: Reason for visit (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Business
Pole B (Positive Score): Pleasure
---------
Overall Accuracy: 100.00% (40/40)
---------

---------
VALIDATION REPORT for Dimension: Motivation (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Have To
Pole B (Positive Score): Want To
---------
Overall Accuracy: 75.00% (30/40)
---------

---------
VALIDATION REPORT for Dimension: Creative Exploration (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Chaotic creative exploration
Pole B (Positive Score): Systematic deliberate execution
---------
Overall Accuracy: 77.50% (31/40)
---------


---------
VALIDATION REPORT for Dimension: Condition (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Sick
Pole B (Positive Score): Healthy
---------
Overall Accuracy: 97.62% (41/42)
---------


---------
VALIDATION REPORT for Dimension: State (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Controlled, in control
Pole B (Positive Score): Uncontrolled, out of control
---------
Overall Accuracy: 97.50% (39/40)
---------

---------
VALIDATION REPORT for Dimension: Emotional State (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): State of heightened emotion
Pole B (Positive Score): A neutral state devoid of any emotion
---------
Overall Accuracy: 88.10% (37/42)
---------



---------
VALIDATION REPORT for Dimension: Logic, Facts or Mathematics (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Relative
Pole B (Positive Score): Absolute
---------
Overall Accuracy: 50.00% (20/40)
---------



---------
VALIDATION REPORT for Dimension: Information (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 21 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Signal
Pole B (Positive Score): Noise
---------
Overall Accuracy: 65.00% (26/40)
---------

---------
VALIDATION REPORT for Dimension: Handling (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Brutality
Pole B (Positive Score): Tenderness
---------
Overall Accuracy: 90.00% (36/40)
---------

---------
VALIDATION REPORT for Dimension: Articles (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): News
Pole B (Positive Score): Commentary
---------
Overall Accuracy: 67.50% (27/40)
---------

---------
VALIDATION REPORT for Dimension: News (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 21 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Fact
Pole B (Positive Score): Opinion
---------
Overall Accuracy: 82.50% (33/40)
---------
---------
VALIDATION REPORT for Dimension: Thinking (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Known Fact
Pole B (Positive Score): Assumption
---------
Overall Accuracy: 62.50% (25/40)
---------

---------
VALIDATION REPORT for Dimension: Thinking (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 21 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Known Fact
Pole B (Positive Score): Pure Speculation
---------
Overall Accuracy: 65.00% (26/40)
---------



---------
VALIDATION REPORT for Dimension: Knowledge (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Something which is known with absolute certainty
Pole B (Positive Score): Something which is pure speculation or assumption
---------
Overall Accuracy: 55.00% (22/40)
---------


---------
VALIDATION REPORT for Dimension: Human Experience (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Loneliness
Pole B (Positive Score): Solitude
---------
Overall Accuracy: 77.50% (31/40)
---------


---------
VALIDATION REPORT for Dimension: Flow of Conversation or Text (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 21 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Staying on the same subject
Pole B (Positive Score): Moving to a new topic
---------
Overall Accuracy: 52.50% (21/40)
---------



---------
VALIDATION REPORT for Dimension: Political (Out-of-Sample)
---------
-- Vector Details --
Vector File: dimension_vector.json
Generated From: 20 pairs created by model 'gemma3:4b'
Embedding Model: nomic-ai/nomic-embed-text-v1.5

-- Validation Details --
Validation Samples: validation_samples.json
Pole A (Negative Score): Left-leaning
Pole B (Positive Score): right-wing
---------
Overall Accuracy: 52.50% (21/40)
---------



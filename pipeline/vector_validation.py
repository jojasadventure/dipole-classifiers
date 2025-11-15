# pipeline/vector_validation.py
import sys
import json
import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, Optional, List, Dict

from tqdm import tqdm

sys.path.append(str(Path(__file__).resolve().parent.parent))
from core.embedding import EmbeddingGenerator
from core.classifier import DimensionClassifier

if TYPE_CHECKING:
    from core.context import ExperimentContext


class _Colors:
    GREEN, RED, BLUE, YELLOW, ENDC = '\033[92m', '\033[91m', '\033[94m', '\033[93m', '\033[0m'


def _evaluate_samples(classifier: DimensionClassifier, samples: List[dict]):
    """Evaluates labeled samples using the classifier and calculates accuracy."""
    texts_to_classify = [s['text'] for s in samples]
    classification_results = classifier.classify(texts_to_classify)
    # Combine results with ground truth labels to calculate accuracy
    detailed_results = []
    correct_count = 0
    for i, res in enumerate(tqdm(classification_results, desc="Evaluating samples")):
        label = samples[i]['label']
        is_correct = (res['prediction'] == label)
        if is_correct:
            correct_count += 1        
        res['label'] = label
        res['correct'] = is_correct
        detailed_results.append(res)
        
    accuracy = (correct_count / len(samples)) * 100 if samples else 0
    return accuracy, correct_count, len(samples), detailed_results

def _evaluate_pairs(classifier: DimensionClassifier, pairs: List[dict]):
    """Evaluates contrasting pairs using the classifier."""
    pole_a_key = classifier.poles['a'].lower()
    pole_b_key = classifier.poles['b'].lower()
    
    texts_a = [p.get(pole_a_key, "") for p in pairs]
    texts_b = [p.get(pole_b_key, "") for p in pairs]
    
    results_a = classifier.classify(texts_a)
    results_b = classifier.classify(texts_b)

    detailed_results = []
    correct_count = 0
    for i in range(len(pairs)):
        score_a, score_b = results_a[i]['score'], results_b[i]['score']
        is_correct = score_b > score_a
        if is_correct:
            correct_count += 1
        
        detailed_results.append({
            "pole_a_text": texts_a[i], "pole_b_text": texts_b[i],
            "score_a": score_a, "score_b": score_b,
            "correct": is_correct
        })
        
    accuracy = (correct_count / len(pairs)) * 100 if pairs else 0
    return accuracy, correct_count, len(pairs), detailed_results


def _get_training_pairs_info(context: 'ExperimentContext') -> str:
    """Finds and formats the training pairs used to generate the vector for display."""
    try:
        pairs_artifact = context.load_artifact("pairs")
        metadata, pairs = pairs_artifact.get("metadata", {}), pairs_artifact.get("data", [])
        pole_a, pole_b = metadata.get("pole_a", "A"), metadata.get("pole_b", "B")
        pole_a_key, pole_b_key = pole_a.lower(), pole_b.lower()

        info_str = "--- Training Pairs Used to Generate Vector ---\n"
        for i, pair in enumerate(pairs[:5]):
            info_str += f"Pair {i+1}:\n  - {pole_a}: {pair.get(pole_a_key, 'N/A')}\n  - {pole_b}: {pair.get(pole_b_key, 'N/A')}\n"
        if len(pairs) > 5: info_str += f"... and {len(pairs) - 5} more pairs.\n"
        return info_str + "\n"
    except Exception as e:
        return f"  Could not load training pairs info: {e}\n"

def _strip_ansi_codes(text: str) -> str:
    return re.sub(r'\x1B\[[0-9;]*[mK]', '', text)


# --- REPORT FORMATTING ---
def _format_sample_results(report_data: dict) -> str:
    lines = []
    pole_a_name, pole_b_name = report_data['pole_a_name'], report_data['pole_b_name']
    lines.append("="*80)
    lines.append(f"VALIDATION REPORT for Dimension: {_Colors.YELLOW}{report_data['dimension_name']}{_Colors.ENDC} (Out-of-Sample)")
    lines.append("="*80)
    lines.append(f"-- Vector Details --")
    lines.append(f"Vector File: {report_data['vector_file']}")
    lines.append(f"Generated From: {report_data['num_pairs_used']} pairs created by model '{report_data['generation_model']}'")
    lines.append(f"Embedding Model: {report_data['embedding_model']}")
    lines.append(f"\n-- Validation Details --")
    lines.append(f"Validation Samples: {report_data['validation_data_file']}")
    lines.append(f"Pole A (Negative Score): {pole_a_name}")
    lines.append(f"Pole B (Positive Score): {pole_b_name}")
    lines.append("-" * 80)
    summary_color = _Colors.GREEN if report_data['accuracy'] >= 90 else _Colors.YELLOW if report_data['accuracy'] >= 75 else _Colors.RED
    lines.append(f"Overall Accuracy: {summary_color}{report_data['accuracy']:.2f}%{_Colors.ENDC} ({report_data['correct_count']}/{report_data['total_count']})")
    lines.append("-" * 80)
    lines.append(report_data['training_pairs_info'])
    lines.append("--- Validation Sample Results ---")
    summary_color = _Colors.GREEN if report_data['accuracy'] >= 90 else _Colors.YELLOW if report_data['accuracy'] >= 75 else _Colors.RED
    lines.append(f"Overall Accuracy: {summary_color}{report_data['accuracy']:.2f}%{_Colors.ENDC} ({report_data['correct_count']}/{report_data['total_count']})")
    lines.append("-" * 80)

    sorted_results = sorted(report_data['detailed_results'], key=lambda x: (x['label'], x['score']))
    
    current_label = None
    for res in sorted_results:
        if res['label'] != current_label:
            current_label = res['label']
            pole_type = "Pole A" if current_label == pole_a_name else "Pole B"
            pole_color = _Colors.BLUE if pole_type == "Pole A" else _Colors.YELLOW
            lines.append(f"{pole_color}--- Results for {pole_type}: {current_label} ---{_Colors.ENDC}")
            lines.append(f"{'RESULT':<12} | {'SCORE':<12} | {'PREDICTION':<15} | TEXT")
            lines.append("." * 40)

        result_str = f"{_Colors.GREEN}[CORRECT]{_Colors.ENDC}" if res['correct'] else f"{_Colors.RED}[INCORRECT]{_Colors.ENDC}"
        score_str = f"{res['score']:+.4f}"
        lines.append(f"{result_str:<22} | {score_str:<12} | {res['prediction']:<15} | {res['text']}")
        
    lines.append("="*80)
    return "\n".join(lines)

def _format_pair_results(report_data: dict) -> str:
    lines = []
    pole_a_name, pole_b_name = report_data['pole_a_name'], report_data['pole_b_name']
    lines.append("="*80)
    lines.append(f"VALIDATION REPORT for Dimension: {_Colors.YELLOW}{report_data['dimension_name']}{_Colors.ENDC} (In-Sample)")
    lines.append("="*80)
    lines.append(f"-- Vector Details --")
    lines.append(f"Vector File: {report_data['vector_file']}")
    lines.append(f"Generated From: {report_data['num_pairs_used']} pairs created by model '{report_data['generation_model']}'")
    lines.append(f"Embedding Model: {report_data['embedding_model']}")
    lines.append(f"\n-- Validation Details --")
    lines.append(f"Validation Pairs: {report_data['validation_data_file']}")
    lines.append(f"Pole A (Negative Direction): {pole_a_name}")
    lines.append(f"Pole B (Positive Direction): {pole_b_name}")
    lines.append("-" * 80)
    summary_color = _Colors.GREEN if report_data['accuracy'] >= 95 else _Colors.YELLOW
    lines.append(f"Overall Accuracy: {summary_color}{report_data['accuracy']:.2f}%{_Colors.ENDC} ({report_data['correct_count']}/{report_data['total_count']})")
    lines.append("-" * 80)

    lines.append(report_data['training_pairs_info'])
    lines.append("--- Validation Pair Results ---")
    summary_color = _Colors.GREEN if report_data['accuracy'] >= 95 else _Colors.YELLOW
    lines.append(f"Overall Accuracy: {summary_color}{report_data['accuracy']:.2f}%{_Colors.ENDC} ({report_data['correct_count']}/{report_data['total_count']})")
    lines.append("-" * 80)
    lines.append(f"{'RESULT':<12} | {'SEPARATION':<10} | TEXT & INDIVIDUAL PROJECTION SCORES")
    lines.append("." * 80)
    max_pole_len = max(len(pole_a_name), len(pole_b_name))
    for res in report_data['detailed_results']:
        separation, score_a, score_b = res['score_b'] - res['score_a'], res['score_a'], res['score_b']
        result_str = f"{_Colors.GREEN}[CORRECT]{_Colors.ENDC}" if res['correct'] else f"{_Colors.RED}[INCORRECT]{_Colors.ENDC}"
        sep_str = f"{_Colors.GREEN if separation > 0 else _Colors.RED}{separation:+.4f}{_Colors.ENDC}"
        pole_a_label, pole_b_label = f"{pole_a_name}:".ljust(max_pole_len + 2), f"{pole_b_name}:".ljust(max_pole_len + 2)
        lines.append(f"{result_str:<22} | {sep_str:<20} | {_Colors.BLUE}{pole_a_label}{_Colors.ENDC} {res['pole_a_text']} {_Colors.YELLOW}(Score: {score_a:+.4f}){_Colors.ENDC}")
        lines.append(f"{'':<12} | {'':<10} | {_Colors.BLUE}{pole_b_label}{_Colors.ENDC} {res['pole_b_text']} {_Colors.YELLOW}(Score: {score_b:+.4f}){_Colors.ENDC}")
        if not res['correct']: lines.append(f"{'':<12} | {'':<10} | {_Colors.RED}↳ Failed: Pole A score was not less than Pole B score.{_Colors.ENDC}")
        lines.append("." * 40)
    lines.append("="*80)
    return "\n".join(lines)



def vector_validation_logic(context: 'ExperimentContext', embed_generator: EmbeddingGenerator, validation_data_path: Path) -> Optional[str]:
    """
    Validates a dimension vector and returns a formatted report string.
    """
    try:
        vector_path = context.get_path_for('vector')
        classifier = DimensionClassifier(vector_path, embed_generator)
        
        with open(validation_data_path, 'r', encoding='utf-8') as f:
            validation_json = json.load(f)
        data_list = validation_json['data']
        validation_type = validation_json.get('metadata', {}).get('type', '')
    except Exception as e:
        logging.error(f"Failed to load required files for validation: {e}")
        return None

    try:
        if "samples" in validation_data_path.name or "samples" in validation_type:
            logging.info("Running out-of-sample validation on labeled samples.")
            accuracy, correct, total, results = _evaluate_samples(classifier, data_list)
            report_formatter = _format_sample_results
        else:
            logging.info("Running in-sample validation on pairs.")
            accuracy, correct, total, results = _evaluate_pairs(classifier, data_list)
            report_formatter = _format_pair_results
    except Exception as e:
        logging.error(f"An error occurred during the validation process: {e}", exc_info=True)
        return None

    training_pairs_info_str = _get_training_pairs_info(context)
    
    report_data = {
        "dimension_name": context.dimension_name,
        "pole_a_name": classifier.poles['a'],
        "pole_b_name": classifier.poles['b'],
        "vector_file": vector_path.name,
        "validation_data_file": validation_data_path.name,
        "embedding_model": context.args.embedding_model_id,
        "accuracy": accuracy,
        "correct_count": correct,
        "total_count": total,
        "detailed_results": results,
        "generation_model": context.metadata.get('parameters', {}).get('llm_model_name', 'N/A'),
        "num_pairs_used": context.metadata.get('num_pairs_used_for_vector', 'N/A'),
        "training_pairs_info": training_pairs_info_str
    }
    
    color_report = report_formatter(report_data)
    print("\n" + color_report + "\n")
    logging.info(f"FINAL_ACCURACY:{accuracy:.2f}% ({correct}/{total})")
    
    return _strip_ansi_codes(color_report)
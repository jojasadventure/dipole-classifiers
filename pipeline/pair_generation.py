# pipeline/pair_generation.py
import sys
import json
import logging
import re
import time
from pathlib import Path
from typing import TYPE_CHECKING, List, Tuple, Optional

# Allow the module to import from the 'core' directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from core.llm_router import LLMRouter

if TYPE_CHECKING:
    from core.context import ExperimentContext

def _clean_llm_json_output(raw_text: str) -> str:
    if not raw_text: return ""
    cleaned_text = re.sub(r'^\s*```(?:json)?\s*', '', raw_text, flags=re.MULTILINE)
    cleaned_text = re.sub(r'\s*```\s*$', '', cleaned_text, flags=re.MULTILINE)
    cleaned_text = re.sub(r'(\/\/.*?|\#.*?)(?=\n|$)', '', cleaned_text)
    cleaned_text = re.sub(r'/\*.*?\*/', '', cleaned_text, flags=re.DOTALL)
    cleaned_text = cleaned_text.strip()
    start_brace = cleaned_text.find('[')
    end_brace = cleaned_text.rfind(']')
    if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
        return cleaned_text[start_brace:end_brace+1]
    return cleaned_text

def _parse_json_stream(text: str, pole_a_key: str, pole_b_key: str) -> list:
    found_pairs = []
    for match in re.finditer(r'\{.*?\}', text, re.DOTALL):
        potential_json = match.group(0)
        try:
            obj = json.loads(potential_json)
            if isinstance(obj, dict) and pole_a_key in obj and pole_b_key in obj:
                found_pairs.append({pole_a_key: obj[pole_a_key], pole_b_key: obj[pole_b_key]})
        except json.JSONDecodeError:
            continue
    return found_pairs

def pair_generation_logic(context: 'ExperimentContext', router: LLMRouter) -> Tuple[Optional[List[dict]], Optional[str]]:
    """
    Generates contrasting pairs and returns them as a list along with the prompt template used.
    """
    dimension_name = context.dimension_name
    pole_a = context.pole_a
    pole_b = context.pole_b
    num_pairs_target = context.args.llm_num_pairs
    
    all_pairs = []
    seen_pairs_tuples = set()
    pole_a_key = pole_a.lower()
    pole_b_key = pole_b.lower()

    MAX_CONSECUTIVE_API_ERRORS = 5
    consecutive_api_errors = 0
    max_total_calls = (num_pairs_target // 5) + 20
    total_api_calls = 0
    final_prompt_for_metadata = None
    

    if hasattr(context.args, 'prompt_file') and context.args.prompt_file:
        prompt_file_path = context.args.prompt_file
        logging.info(f"Using custom prompt file: {prompt_file_path}")
    else:
        project_root = Path(__file__).resolve().parent.parent
        prompt_file_path = project_root / "prompts" / "pair_generation_prompt.txt"
        logging.info(f"Using default prompt file: {prompt_file_path}")
    
    try:
        with open(prompt_file_path, 'r') as f:
            lines = f.readlines()
            uncommented_lines = [line for line in lines if not line.strip().startswith('#')]
            base_prompt_template = "".join(uncommented_lines)
            
    except FileNotFoundError:
        logging.error(f"Prompt template not found at {prompt_file_path}")
        return None, None
    except Exception as e:
        logging.error(f"Error reading prompt template file: {e}")
        return None, None

    while len(all_pairs) < num_pairs_target:
        if total_api_calls >= max_total_calls:
            logging.error(f"Stopping: Reached maximum of {max_total_calls} API calls.")
            break
        if consecutive_api_errors >= MAX_CONSECUTIVE_API_ERRORS:
            logging.error(f"Stopping: Exceeded {MAX_CONSECUTIVE_API_ERRORS} consecutive API errors.")
            break
        
        total_api_calls += 1
        pairs_needed = num_pairs_target - len(all_pairs)
        batch_size = getattr(context.args, 'llm_batch_size', 10)
        pairs_to_request = min(batch_size, pairs_needed + 5)
        logging.info(f"--- API Call {total_api_calls}/{max_total_calls} | Target: {num_pairs_target}, Have: {len(all_pairs)} ---")
        
        current_prompt = base_prompt_template.format(
            num_pairs=pairs_to_request, 
            pole_a=pole_a, 
            dimension_name=dimension_name,
            pole_b=pole_b, 
            pole_a_key=pole_a_key, 
            pole_b_key=pole_b_key,
            extra_instructions=context.args.prompt_extra_text
        )

        if all_pairs:
            existing_pairs_json = json.dumps(all_pairs[-50:], indent=None)
            current_prompt += f"\n\nIMPORTANT: Avoid generating pairs similar to these already collected ones:\n{existing_pairs_json}\n\nContinue the JSON list below:\n["

        try:
            raw_response_text = router.generate(current_prompt, timeout=120)
            final_prompt_for_metadata = current_prompt
            
            consecutive_api_errors = 0
        except Exception as api_e:
            logging.warning(f"LLM provider exception on call {total_api_calls}: {api_e}")
            consecutive_api_errors += 1
            time.sleep(5 * consecutive_api_errors)
            continue

        if not raw_response_text or not raw_response_text.strip():
            logging.warning("LLM returned an empty response. Retrying.")
            time.sleep(5)
            continue

        cleaned_response_text = _clean_llm_json_output(raw_response_text)
        newly_received_pairs = _parse_json_stream(cleaned_response_text, pole_a_key, pole_b_key)
        
        if not newly_received_pairs:
            logging.warning("Response received, but no valid pairs could be parsed. Retrying.")
            time.sleep(2)
            continue
            
        new_pairs_added = 0
        for pair in newly_received_pairs:
            pair_tuple = (pair.get(pole_a_key, ""), pair.get(pole_b_key, ""))
            if pair_tuple not in seen_pairs_tuples:
                seen_pairs_tuples.add(pair_tuple)
                all_pairs.append(pair)
                new_pairs_added += 1
        
        logging.info(f"Parsed {len(newly_received_pairs)}, added {new_pairs_added} new unique pairs. Total is now {len(all_pairs)}.")

    if len(all_pairs) < num_pairs_target:
        logging.warning(f"Finished generation. Got {len(all_pairs)} of {num_pairs_target} requested pairs.")
    
    return all_pairs, final_prompt_for_metadata
    
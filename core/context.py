# core/context.py
import argparse
import logging
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ExperimentContext:
    """Manages the state and file paths for a single, unique pipeline run."""

    def __init__(self, args: argparse.Namespace, schema_version: str = "unknown"):
        self.args = args
        self.schema_version = schema_version
        self.start_time = datetime.now()
        self.dimension_name, self.pole_a, self.pole_b = self._parse_dimension_string(args.dimension)
        sanitized_dim = self._sanitize_filename(self.dimension_name)
        sanitized_pole_a = self._sanitize_filename(self.pole_a)
        sanitized_pole_b = self._sanitize_filename(self.pole_b)
        self.full_dimension_name = f"{sanitized_dim}_{sanitized_pole_a}_vs_{sanitized_pole_b}"        
        self.run_id = self._create_run_id()
        self.run_dir = Path("results") / self.full_dimension_name / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized ExperimentContext. Output will be in: {self.run_dir}")

        self._artifact_filenames = {
            "pairs": "pairs.json",
            "embeddings": "embeddings.json",
            "vector": "dimension_vector.json",
            "validation_samples": "validation_samples.json",
            "validation_report": "validation_report.txt",
        }

        self.metadata = self._build_master_metadata()
        self._save_context_summary()

    def _parse_dimension_string(self, dimension_string: str) -> tuple[str, str, str]:
        match = re.match(r'([^:]+):\s*(.+?)\s+vs\.?\s+(.+)', dimension_string, re.IGNORECASE)
        if not match:
            raise ValueError(f"Dimension string invalid: '{dimension_string}'. Expected 'Name: PoleA vs PoleB'")
        return match.group(1).strip(), match.group(2).strip(), match.group(3).strip()

    def _sanitize_filename(self, name: str) -> str:
        name = re.sub(r'\s+', '_', name)
        name = re.sub(r'[^\w\-_\.]', '', name)
        return name

    def _get_git_commit_hash(self) -> Optional[str]:
        try:
            return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        except Exception:
            return None

    def _create_run_id(self) -> str:
        """Creates a human-friendly, unique ID for the pipeline run."""
        time_str = self.start_time.strftime('%Y%m%d-%H%M%S')
        sanitized_llm = self._sanitize_filename(self.args.llm_model_name).replace("/", "-")        
        prompt_id = ""
        if hasattr(self.args, 'prompt_file') and self.args.prompt_file:
            if self.args.prompt_file.name != 'pair_generation_prompt.txt':
                sanitized_prompt_name = self._sanitize_filename(self.args.prompt_file.stem)
                prompt_id = f"{sanitized_prompt_name}_"
            
        return f"{sanitized_llm}_{prompt_id}{self.args.llm_num_pairs}p_{time_str}"

    def _build_master_metadata(self) -> Dict[str, Any]:
        params_to_save = {}
        for key, value in vars(self.args).items():
            if isinstance(value, Path):
                params_to_save[key] = str(value)
            else:
                params_to_save[key] = value
                
        params_to_save.pop('llm_api_key', None)

        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "run_timestamp_utc": self.start_time.isoformat(),
            "git_commit_hash": self._get_git_commit_hash(),
            "dimension_name": self.dimension_name,
            "pole_a": self.pole_a,
            "pole_b": self.pole_b,
            "parameters": params_to_save
        }

    def get_path_for(self, artifact_name: str) -> Path:
        if artifact_name not in self._artifact_filenames:
            raise ValueError(f"Unknown artifact name: '{artifact_name}'")
        return self.run_dir / self._artifact_filenames[artifact_name]

    def save_artifact(self, name: str, data: Any, is_json: bool = True):
        output_path = self.get_path_for(name)
        logger.info(f"Saving artifact '{name}' to {output_path}")
        try:
            if is_json:
                payload = {"metadata": self.metadata, "data": data}
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(payload, f, indent=2)
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(data)
        except (IOError, TypeError) as e:
            logger.error(f"Failed to save artifact '{name}': {e}")
            raise

    def load_artifact(self, name: str) -> Dict[str, Any]:
        input_path = self.get_path_for(name)
        logger.info(f"Loading artifact '{name}' from {input_path}")
        if not input_path.exists(): raise FileNotFoundError(f"Cannot load artifact '{name}': file not found at {input_path}")
        try:
            with open(input_path, 'r', encoding='utf-8') as f: return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load artifact '{name}': {e}")
            raise

    def update_metadata(self, new_info: Dict[str, Any]):
        self.metadata.update(new_info)
        self._save_context_summary()
        logger.info(f"Metadata updated with: {new_info}")

    def _save_context_summary(self):
        summary_path = self.run_dir / "_run_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2)
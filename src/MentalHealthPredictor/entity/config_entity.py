from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

@dataclass(frozen=True)
class DataIngestionConfig:
    AWS_REGION: str
    BUCKET_NAME: str
    S3_OBJECT_KEY: str
    root_dir: Path
    LOCAL_DOWNLOAD_FILE: Path 


@dataclass(frozen=True)
class DataCleaningEncodingConfig:
    input_file: Path
    output_file: Path

@dataclass(frozen=True)
class ModelTrainingConfig:
    input_file: Path
    output_dir: Path  # Changed from model_output_dir
    target_columns: List[str]
    test_size: float
    random_state: int
    hyperparam_grids: Dict
    models_dir: Path = None  # Will be set in post-init

    def __post_init__(self):
        object.__setattr__(self, 'models_dir', self.output_dir / "trained_models")
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

@dataclass(frozen=True)
class DataIngestionConfig:
    AWS_REGION: str
    BUCKET_NAME: str
    S3_OBJECT_KEY: str
    root_dir: Path
    LOCAL_DOWNLOAD_FILE: Path 




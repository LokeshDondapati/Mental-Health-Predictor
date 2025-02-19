import boto3
import os
from pathlib import Path
from ObesityPredictor import logger
from ObesityPredictor.config.configuration import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.s3_client = boto3.client("s3", region_name=self.config.AWS_REGION)

    def download_file_from_s3(self) -> str:
        """
        Download a file from AWS S3 to the local system.

        Returns:
            str: Path to the downloaded file.
        """
        try:
            bucket_name = self.config.BUCKET_NAME
            s3_object_key = self.config.S3_OBJECT_KEY
            local_download_path = Path(self.config.LOCAL_DOWNLOAD_FILE)

            # Ensure the directory exists
            os.makedirs(local_download_path.parent, exist_ok=True)

            # ✅ Fix: Use `LOCAL_DOWNLOAD_FILE` instead of `root_dir`
            logger.info(f"Downloading {s3_object_key} from S3 bucket {bucket_name} to {local_download_path}")

            # Download file from S3
            self.s3_client.download_file(bucket_name, s3_object_key, str(local_download_path))

            logger.info(f"File downloaded successfully: {local_download_path}")

            return str(local_download_path)

        except Exception as e:
            logger.error(f"Error downloading file from S3: {str(e)}")
            raise e

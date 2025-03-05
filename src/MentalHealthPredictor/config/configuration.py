from MentalHealthPredictor.constants import *
import os
from MentalHealthPredictor.utils.common import read_yaml, create_directories, save_json
from MentalHealthPredictor.entity.config_entity import DataIngestionConfig, DataCleaningEncodingConfig,ModelTrainingConfig,ModelInferenceConfig
from pathlib import Path

class ConfigurationManager:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)  # ✅ Read YAML as dictionary
        self.params = read_yaml(params_filepath)

        create_directories([self.config["artifacts_root"]])  # ✅ Ensure artifacts directory exists

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config["data_ingestion"]

        # Ensure the data ingestion directory exists
        create_directories([config["root_dir"]])

        data_ingestion_config = DataIngestionConfig(
            AWS_REGION=config["AWS_REGION"],
            BUCKET_NAME=config["BUCKET_NAME"],
            S3_OBJECT_KEY=config["S3_OBJECT_KEY"],
            root_dir=Path(config["root_dir"]),
            LOCAL_DOWNLOAD_FILE=Path(config["LOCAL_DOWNLOAD_FILE"])
        )

        return data_ingestion_config
    
    def get_data_cleaning_encoding_config(self) -> DataCleaningEncodingConfig:
            config = self.config["data_cleaning_encoding"]
            return DataCleaningEncodingConfig(
                input_file=Path(config["input_file"]),
                output_file=Path(config["output_file"])
            )
    

    

    # Add this new method for model training
    def get_model_training_config(self) -> ModelTrainingConfig:
        config = self.config["model_training"]
        
        # Create required directories
        output_dir = Path(config["output_dir"])
        models_dir = output_dir / "trained_models"
        create_directories([output_dir, models_dir])

        return ModelTrainingConfig(
            input_file=Path(config["input_file"]),
            output_dir=output_dir,
            target_columns=config["target_columns"],
            test_size=config["test_size"],
            random_state=config["random_state"],
            hyperparam_grids=config["hyperparam_grids"]
        )
    
    
    def get_model_inference_config(self) -> ModelInferenceConfig:
        config = self.config["model_inference"]
        create_directories([config["output_dir"]])
        return ModelInferenceConfig(
            model_dir=Path(config["model_dir"]),
            input_data=Path(config["input_data"]),
            output_dir=Path(config["output_dir"]),
            target_columns=config["target_columns"]
        )
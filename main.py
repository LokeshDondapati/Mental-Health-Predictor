from MentalHealthPredictor import logger
from MentalHealthPredictor.config.configuration import ConfigurationManager
from MentalHealthPredictor.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from MentalHealthPredictor.pipeline.stage_02_data_cleaning_encoding import DataCleaningEncodingPipeline

import pandas as pd
from MentalHealthPredictor.utils.common import remove_pycache

# Remove cached files before running
remove_pycache()

def run_pipeline(stage_name, pipeline_class):
    """Generic function to execute a pipeline stage with logging."""
    try:
        logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
        pipeline = pipeline_class()
        
        # Check if pipeline has `run()`, else use `main()`
        if hasattr(pipeline, "run"):
            pipeline.run()  # ✅ Call `run()` if it exists
        elif hasattr(pipeline, "main"):
            pipeline.main()  # ✅ Call `main()` if it exists
        else:
            raise AttributeError(f"{pipeline_class.__name__} has neither `run()` nor `main()` method.")
        
        logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

# **Execute Data Pipeline Stages**
run_pipeline("Data Ingestion Stage", DataIngestionTrainingPipeline)
run_pipeline("Data Cleaning and Encoding Stage", DataCleaningEncodingPipeline)
# src/MentalHealthPredictor/pipeline/stage_03_model_training.py
from MentalHealthPredictor.config.configuration import ConfigurationManager
from MentalHealthPredictor.components.model_training import ModelTraining
from MentalHealthPredictor import logger

STAGE_NAME = "Model Training Stage"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_training_config = config.get_model_training_config()
        model_training = ModelTraining(config=model_training_config)
        model_training.train()

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
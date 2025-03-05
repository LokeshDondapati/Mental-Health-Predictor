from MentalHealthPredictor.config.configuration import ConfigurationManager
from MentalHealthPredictor.components.inference import Inference
from MentalHealthPredictor import logger

STAGE_NAME = "Model Inference Stage"

class InferencePipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        inference_config = config.get_model_inference_config()
        inference = Inference(config=inference_config)
        inference.predict()

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        obj = InferencePipeline()
        obj.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
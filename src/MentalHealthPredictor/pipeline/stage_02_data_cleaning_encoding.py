from MentalHealthPredictor.config.configuration import ConfigurationManager
from MentalHealthPredictor.components.data_cleaning_encoding import DataCleaningEncoding
from MentalHealthPredictor import logger

STAGE_NAME = "Data cleaning and encoding stage"


class DataCleaningEncodingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_cleaning_encoding_config = config.get_data_cleaning_encoding_config()
        data_cleaning_encoding = DataCleaningEncoding(config=data_cleaning_encoding_config)
        data_cleaning_encoding.run()




if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataCleaningEncoding()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
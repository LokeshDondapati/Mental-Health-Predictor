import os
from MentalHealthPredictor import logger
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from MentalHealthPredictor.config.configuration import DataCleaningEncodingConfig
import pandas as pd

class DataCleaningEncoding:
    def __init__(self, config: DataCleaningEncodingConfig):
        self.config = config

    def load_data(self):
        '''
        Load the ingested file from file path stored in config.yaml file
        '''
        try:
            logger.info(f"Loading data from {self.config.input_file}")
            df = pd.read_csv(self.config.input_file)
            logger.info(f"Data loaded successfully with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise e
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform data cleaning steps such as handling missing values and feature engineering.No cleaning process involved in this data
        """
        try:
            logger.info("Cleaning data...")
            logger.info(f"Data cleaned, new shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error during data cleaning: {str(e)}")
            raise e
        
    def encode_data(self, df: pd.DataFrame):
        try:
            # Initialize one-hot encoder
            one_hot_encoder = OneHotEncoder()
            
            # Fit and transform the data, converting the output to a dense array
            categorical_columns = ['Gender', 'Occupation', 'Country', 'Mental_Health_Condition', 'Consultation_History']
            one_hot_encoded = one_hot_encoder.fit_transform(df[categorical_columns]).toarray()
            
            # Create DataFrame for one-hot encoded columns
            one_hot_df = pd.DataFrame(one_hot_encoded, columns=one_hot_encoder.get_feature_names_out(categorical_columns))

            # Map ordinal columns
            severity_mapping = {'None': 0, 'Low': 1, 'Medium': 2, 'High': 3}
            stress_level_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
            df['Severity'] = df['Severity'].map(severity_mapping)
            df['Stress_Level'] = df['Stress_Level'].map(stress_level_mapping)

            # Normalize Numerical Data
            scaler = StandardScaler()
            numerical_cols = ['Age', 'Sleep_Hours', 'Work_Hours', 'Physical_Activity_Hours']
            df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

            # Concatenate all processed parts of the dataset
            processed_df = pd.concat([df.drop(categorical_columns, axis=1), one_hot_df], axis=1)

            return processed_df
        except Exception as e:
            logger.error(f"Error during the data encoding: {str(e)}")
            raise e

        
    def save_data(self, df: pd.DataFrame):
        """
        Save the cleaned and encoded data to the specified output file.
        """
        try:
            output_dir = self.config.output_file.parent
            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"Directory {output_dir} checked/created successfully.")

            output_file_path = str(self.config.output_file)
            logger.info(f"Saving data to {output_file_path}")  # Debugging info

            # Test save with a simple DataFrame
            test_df = pd.DataFrame({'test': [1, 2, 3]})
            test_path = os.path.join(output_dir, 'test_file.csv')
            test_df.to_csv(test_path, index=False)
            logger.info(f"Test file saved to {test_path}")  # Confirm test file save

            df.to_csv(output_file_path, index=False)
            logger.info(f"Data saved successfully to {output_file_path}")
        except Exception as e:
            logger.error(f"Error during saving data: {str(e)}", exc_info=True)
            raise

        
    def run(self):
        """
        Execute the data cleaning and encoding pipeline.
        """
        df = self.load_data()
        df = self.clean_data(df)
        df = self.encode_data(df)
        df = self.save_data(df)
import pandas as pd
import joblib
from pathlib import Path
from MentalHealthPredictor import logger
from MentalHealthPredictor.config.configuration import ModelInferenceConfig

class Inference:
    def __init__(self, config: ModelInferenceConfig):
        self.config = config
        self.models = {}
        self.load_models()

    def load_models(self):
        """Load all trained models from directory"""
        try:
            model_files = list(self.config.model_dir.glob("*.pkl"))
            if not model_files:
                raise FileNotFoundError("No model files found in directory")
            
            for model_path in model_files:
                model_name = model_path.stem
                self.models[model_name] = joblib.load(model_path)
                logger.info(f"Loaded model: {model_name}")
                
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise

    def preprocess_input(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add placeholder columns for expected features"""
        required_features = [
            'Age', 'Sleep_Hours', 'Work_Hours', 'Physical_Activity_Hours',
            'Gender_Female', 'Gender_Male', 'Gender_Non-binary', 
            'Gender_Prefer not to say', 'Occupation_Education',
            'Occupation_Engineering', 'Occupation_Finance', 'Occupation_Healthcare',
            'Occupation_IT', 'Occupation_Other', 'Occupation_Sales',
            'Country_Australia', 'Country_Canada', 'Country_Germany',
            'Country_India', 'Country_Other', 'Country_UK', 'Country_USA'
        ]
        
        # Add missing columns with default values
        for col in required_features:
            if col not in data.columns:
                data[col] = 0
                
        return data[required_features]
    
    
    def predict(self):
        """Run predictions for all loaded models"""
        try:
            # Load and prepare data
            df = pd.read_csv(self.config.input_data)
            processed_df = self.preprocess_input(df)
            results = processed_df.copy()
            
            # Generate predictions
            for target in self.config.target_columns:
                for model_name, model in self.models.items():
                    if target in model_name:
                        # Extract features used by the model
                        try:
                            preds = model.predict(processed_df)
                            results[f"{model_name}_prediction"] = preds
                            logger.info(f"Generated predictions for {model_name}")
                        except Exception as e:
                            logger.error(f"Prediction failed for {model_name}: {str(e)}")
            
            # Save results
            output_path = self.config.output_dir / "inference_results.csv"
            results.to_csv(output_path, index=False)
            logger.info(f"Saved inference results to {output_path}")
            
            return results
        
        except Exception as e:
            logger.error(f"Inference failed: {str(e)}")
            raise
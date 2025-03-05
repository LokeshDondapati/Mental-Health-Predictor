import pandas as pd
import joblib
from pathlib import Path
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score
from sklearn.model_selection import RandomizedSearchCV
from MentalHealthPredictor import logger
from MentalHealthPredictor.config.configuration import ModelTrainingConfig

class ModelTraining:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config
        self.models = {
            'LogisticRegression': Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('classifier', LogisticRegression(max_iter=1000))
            ]),
            'DecisionTree': Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('classifier', DecisionTreeClassifier())
            ]),
            'SVC': Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('classifier', SVC(probability=True))
            ]),
            'RandomForest': Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('classifier', RandomForestClassifier())
            ]),
            'GradientBoosting': Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('classifier', GradientBoostingClassifier())
            ]),
            'KNeighbors': Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('classifier', KNeighborsClassifier())
            ]),
            'NaiveBayes': Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('classifier', GaussianNB())
            ])
        }

    def _convert_params(self, param_grid):
        """Convert scientific notation strings to floats"""
        converted = {}
        for param, values in param_grid.items():
            new_values = []
            for val in values:
                if isinstance(val, str) and 'e' in val.lower():
                    try:
                        new_values.append(float(val))
                    except ValueError:
                        new_values.append(val)
                else:
                    new_values.append(val)
            converted[param] = new_values
        return converted

    def train(self):
        try:
            # Load and clean data
            df = pd.read_csv(self.config.input_file)
            logger.info(f"Data shape before cleaning: {df.shape}")
            
            # Drop rows with missing targets
            for target in self.config.target_columns:
                if target not in df.columns:
                    raise KeyError(f"Target column {target} not found in dataset")
                df = df.dropna(subset=[target])
            
            logger.info(f"Data shape after cleaning: {df.shape}")
            results = []
            
            # Create models directory
            self.config.models_dir.mkdir(parents=True, exist_ok=True)
            
            for target in self.config.target_columns:
                logger.info(f"\n{'='*40}")
                logger.info(f"Training models for target: {target}")
                logger.info(f"{'='*40}")
                
                # Prepare features and target
                base_drop_columns = [
                    'Mental_Health_Condition_No',  # Corrected column name
                    'Consultation_History_No',
                    'Consultation_History_Yes',
                    'User_ID'
                ]
                
                # Exclude other targets from features
                other_targets = [t for t in self.config.target_columns if t != target]
                X = df.drop(columns=base_drop_columns + other_targets)
                y = df[target]
                
                # Check for remaining NaNs
                logger.info(f"Missing values in features: {X.isna().sum().sum()}")
                logger.info(f"Missing values in target: {y.isna().sum()}")
                
                # Stratified train-test split
                sss = StratifiedShuffleSplit(n_splits=1, 
                                            test_size=self.config.test_size,
                                            random_state=self.config.random_state)
                train_index, test_index = next(sss.split(X, y))
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                y_train, y_test = y.iloc[train_index], y.iloc[test_index]
                
                # Reduced training set for tuning
                X_train_sample, _, y_train_sample, _ = train_test_split(
                    X_train, y_train, 
                    train_size=0.5, 
                    random_state=self.config.random_state
                )
                
                # Train each model
                for model_name, pipeline in self.models.items():
                    logger.info(f"\n--- Tuning {model_name} ---")
                    raw_grid = self.config.hyperparam_grids[model_name]
                    param_grid = self._convert_params(raw_grid)
                    
                    # Map to pipeline parameters
                    param_grid = {f'classifier__{k}': v for k, v in param_grid.items()}
                    
                    search = RandomizedSearchCV(
                        estimator=pipeline,
                        param_distributions=param_grid,
                        n_iter=5,
                        cv=3,
                        scoring='f1_weighted',
                        n_jobs=-1,
                        random_state=self.config.random_state,
                        error_score='raise'
                    )
                    search.fit(X_train_sample, y_train_sample)
                    
                    # Evaluate best model
                    best_model = search.best_estimator_
                    preds = best_model.predict(X_test)
                    
                    # Store results
                    results.append({
                        'Target': target,
                        'Model': model_name,
                        'Accuracy': round(accuracy_score(y_test, preds), 4),
                        'Precision': round(precision_score(y_test, preds, average='weighted', zero_division=0), 4),
                        'F1-Score': round(f1_score(y_test, preds, average='weighted', zero_division=0), 4),
                        'Best_Params': str(search.best_params_)
                    })
                    
                    # Save best model
                    model_path = self.config.models_dir / f"{target}_{model_name}.pkl"
                    joblib.dump(best_model, model_path)
                    logger.info(f"Saved {model_name} for {target}")
            
            # Save all results
            results_df = pd.DataFrame(results)
            results_path = self.config.output_dir / "training_results.csv"
            results_df.to_csv(results_path, index=False)
            logger.info(f"\nSaved training results to {results_path}")
            
        except Exception as e:
            logger.error(f"Error in model training: {str(e)}")
            raise e
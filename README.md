# Mental-Health-Predictor
Building the mental health predictor for predicting the mental health of people with yes or no as final prediction.
User can select among multiple machine learning models for the prediction.


# How to run?
### STEPS:

Clone the repository

```bash
https://github.com/LokeshDondapati/Mental-Health-Predictor.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n MentalHealthPredictor python=3.12.0 -y
```

```bash
conda activate MentalHealthPredictor
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```

## **********************************************************************************************

# DEVELOPMENT STEPS

## STAGE_01-> DATA INGESTION

#### 1.Create an s3 bucket and upload the data in s3 bucket copy the key id.</br>

```bash
s3://mental-health-dataset-capstone/mental_health_dataset.csv
```

#### 2.Create an IAM user and give access to s3 on command line and download the access and secret key tokens to configure in cmd using aws configure </br>

```bash
AWS ACCESS KEY = Contact owner
```

```bash
AWS SECRET KEY = Contact owner
```
```bash
Default region name = us-east-1
```

```bash
Default output format = "Press enter for json"
```

#### 3.Update the config.yaml file with correct config parameters of the aws 
```bash
artifacts_root: artifacts

data_ingestion:
  AWS_REGION: us-east-1
  BUCKET_NAME: mental-health-dataset-capstone
  S3_OBJECT_KEY: mental_health_dataset.csv
  root_dir: artifacts/data_ingestion
  LOCAL_DOWNLOAD_FILE: artifacts/data_ingestion/mental_health_dataset.csv 

```


## STAGE_02-> DATA CLEANING AND ENCODING

#### Update the config.yaml file with correct config parameters of the aws 
```bash
artifacts_root: artifacts

data_cleaning_encoding:
  input_file: artifacts/data_ingestion/mental_health_dataset.csv  # ✅ The ingested file is used as input
  output_file: artifacts/data_cleaning_encoded/cleaned_encoded_data.csv  # ✅ Save cleaned & encoded data here


## STAGE_03-> MODEL TRAINING

#### Update the config.yaml file with correct config parameters of the aws 
```bash
model_training:
  input_file: artifacts/data_cleaning_encoded/cleaned_encoded_data.csv
  output_dir: artifacts/model_training
  target_columns:
    - Mental_Health_Condition_Yes  # Corrected column name
    - Severity
    - Stress_Level
  test_size: 0.2
  random_state: 42
  hyperparam_grids:
    LogisticRegression:
      C: [0.1, 1, 10]
    DecisionTree:
      max_depth: [null, 5]
      min_samples_split: [2, 5]
    SVC:
      C: [0.1, 1]
      kernel: [linear, rbf]
    RandomForest:
      n_estimators: [50, 100]
      max_depth: [null, 5]
    GradientBoosting:
      n_estimators: [50, 100]
      learning_rate: [0.01, 0.1]
    KNeighbors:
      n_neighbors: [3, 5]
      weights: [uniform, distance]
    NaiveBayes:
      var_smoothing: [1e-9, 1e-8]



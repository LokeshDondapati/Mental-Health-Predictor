import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from MentalHealthPredictor.config.configuration import DataCleaningEncodingConfig
from MentalHealthPredictor.components.data_cleaning_encoding import DataCleaningEncoding

@pytest.fixture
def sample_data():
    data = {
        'Age': [25, 30, 45],
        'Gender': ['Male', 'Female', 'Male'],
        'Occupation': ['Engineer', 'Doctor', 'Teacher'],
        'Country': ['USA', 'UK', 'Canada'],
        'Mental_Health_Condition': ['Anxiety', 'None', 'Depression'],
        'Consultation_History': ['Yes', 'No', 'Yes'],
        'Severity': ['High', 'None', 'Medium'],
        'Stress_Level': ['Medium', 'Low', 'High'],
        'Sleep_Hours': [7, 6, 8],
        'Work_Hours': [40, 35, 50],
        'Physical_Activity_Hours': [3, 2, 5]
    }
    return pd.DataFrame(data)

@pytest.fixture
def config(tmpdir):
    input_path = tmpdir.join("input.csv")
    output_path = tmpdir.join("processed_data.csv")
    
    # Return a DataCleaningEncodingConfig instance with temporary paths
    return DataCleaningEncodingConfig(
        input_file=Path(input_path),
        output_file=Path(output_path)
    )

def test_load_data_valid_file(config, sample_data):
    # Save sample data to the input path
    sample_data.to_csv(config.input_file, index=False)
    
    processor = DataCleaningEncoding(config)
    df = processor.load_data()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape == (3, 11)

def test_clean_data_retains_shape(sample_data, config):
    processor = DataCleaningEncoding(config)
    cleaned_df = processor.clean_data(sample_data)
    
    assert cleaned_df.shape == sample_data.shape

def test_encode_data_transformations(sample_data, config):
    processor = DataCleaningEncoding(config)
    encoded_df = processor.encode_data(sample_data)
    
    # Check one-hot encoding
    categorical_columns = ['Gender', 'Occupation', 'Country', 'Mental_Health_Condition', 'Consultation_History']
    expected_ohe_columns = 5  # 2 (Gender) + 3 (Occupation) + 3 (Country) + 3 (Mental_Health) + 2 (Consultation)
    assert encoded_df.shape[1] == (sample_data.shape[1] - len(categorical_columns)) + expected_ohe_columns
    
    # Check ordinal encoding
    assert set(encoded_df['Severity']) == {3, 0, 2}  # High=3, None=0, Medium=2
    assert set(encoded_df['Stress_Level']) == {1, 0, 2}  # Medium=1, Low=0, High=2
    
    # Check numerical standardization
    numerical_cols = ['Age', 'Sleep_Hours', 'Work_Hours', 'Physical_Activity_Hours']
    for col in numerical_cols:
        assert np.isclose(encoded_df[col].mean(), 0, atol=1e-1)
        assert np.isclose(encoded_df[col].std(), 1, atol=1e-1)

def test_save_data_creates_file(config, sample_data):
    processor = DataCleaningEncoding(config)
    processor.save_data(sample_data)
    
    assert Path(config.output_file).exists()
    saved_df = pd.read_csv(config.output_file)
    pd.testing.assert_frame_equal(sample_data, saved_df)

def test_full_pipeline_integration(config, sample_data):
    # Save sample data to input path
    sample_data.to_csv(config.input_file, index=False)
    
    processor = DataCleaningEncoding(config)
    processor.run()
    
    # Check output file exists
    assert Path(config.output_file).exists()
    
    # Load processed data and verify transformations
    processed_df = pd.read_csv(config.output_file)
    assert processed_df.shape[1] > sample_data.shape[1]  # Ensure encoding added columns
    assert 'Severity' in processed_df.columns
    assert 'Gender_Male' in processed_df.columns  # Check one of the OHE columns
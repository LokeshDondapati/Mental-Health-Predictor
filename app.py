import streamlit as st
import joblib
import pandas as pd
import os
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Mental Health Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .st-bw {
        background-color: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-text {
        font-size: 2.5rem !important;
        color: #2c3e50 !important;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .prediction-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Load available models
def load_models_list(models_dir="artifacts/model_training/trained_models"):
    models = {}
    model_files = list(Path(models_dir).glob("*.pkl"))
    
    for model_path in model_files:
        target = "_".join(model_path.stem.split("_")[:-1])
        model_name = model_path.stem.split("_")[-1]
        
        if target not in models:
            models[target] = []
        models[target].append(model_name)
    
    return models

# Main app function
def main():
    # Header Section
    with st.container():
        st.markdown('<h1 class="header-text">🧠 Mental Health Prediction Platform</h1>', unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem; color: #4a5568;">
                Predict mental health outcomes using state-of-the-art machine learning models
            </div>
        """, unsafe_allow_html=True)

    # Sidebar Configuration
    with st.sidebar:
        st.header("Model Configuration")
        models = load_models_list()
        
        # Target Selection
        selected_target = st.selectbox(
            "Select Prediction Target",
            options=list(models.keys()),
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        # Model Selection
        selected_model = st.selectbox(
            "Select ML Model",
            options=models[selected_target],
            format_func=lambda x: x.replace("_", " ").title()
        )

    # Main Input Section
    with st.container():
        with st.form("input_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("Personal Information")
                age = st.slider("Age", 18, 80, 30)
                gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
                
            with col2:
                st.subheader("Lifestyle Factors")
                sleep_hours = st.slider("Sleep Hours per Day", 3.0, 12.0, 7.0)
                work_hours = st.slider("Work Hours per Day", 4.0, 16.0, 9.0)
                physical_activity = st.slider("Physical Activity Hours", 0.0, 5.0, 1.0)
                
            with col3:
                st.subheader("Professional Details")
                occupation = st.selectbox("Occupation", [
                    "IT", "Healthcare", "Education", 
                    "Engineering", "Finance", "Sales", "Other"
                ])
                country = st.selectbox("Country", [
                    "USA", "India", "UK", 
                    "Canada", "Australia", "Germany", "Other"
                ])
            
            submitted = st.form_submit_button("Predict Mental Health Status")

    # Prediction Logic
    if submitted:
        try:
            # Create input dataframe
            input_data = pd.DataFrame([{
                'Age': age,
                'Sleep_Hours': sleep_hours,
                'Work_Hours': work_hours,
                'Physical_Activity_Hours': physical_activity,
                'Gender_Female': 1 if gender == "Female" else 0,
                'Gender_Male': 1 if gender == "Male" else 0,
                'Gender_Non-binary': 1 if gender == "Non-binary" else 0,
                'Gender_Prefer not to say': 1 if gender == "Prefer not to say" else 0,
                'Occupation_Education': 1 if occupation == "Education" else 0,
                'Occupation_Engineering': 1 if occupation == "Engineering" else 0,
                'Occupation_Finance': 1 if occupation == "Finance" else 0,
                'Occupation_Healthcare': 1 if occupation == "Healthcare" else 0,
                'Occupation_IT': 1 if occupation == "IT" else 0,
                'Occupation_Other': 1 if occupation == "Other" else 0,
                'Occupation_Sales': 1 if occupation == "Sales" else 0,
                'Country_Australia': 1 if country == "Australia" else 0,
                'Country_Canada': 1 if country == "Canada" else 0,
                'Country_Germany': 1 if country == "Germany" else 0,
                'Country_India': 1 if country == "India" else 0,
                'Country_Other': 1 if country == "Other" else 0,
                'Country_UK': 1 if country == "UK" else 0,
                'Country_USA': 1 if country == "USA" else 0
            }])

            # Load model
            model_path = Path(f"artifacts/model_training/trained_models/{selected_target}_{selected_model}.pkl")
            model = joblib.load(model_path)
            
            # Make prediction
            prediction = model.predict(input_data)[0]
            proba = model.predict_proba(input_data)[0] if hasattr(model, "predict_proba") else []

            # Display results
            with st.container():
                st.markdown("""
                    <div class="st-bw">
                        <h2 style="color: #2c3e50; margin-bottom: 1rem;">Prediction Results</h2>
                """, unsafe_allow_html=True)
                
                # Prediction Card
                st.markdown(f"""
                    <div class="prediction-card">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="font-size: 1.2rem; color: #4a5568;">Selected Target:</div>
                            <div style="margin-left: auto; font-weight: bold; color: #2c3e50;">
                                {selected_target.replace('_', ' ').title()}
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="font-size: 1.2rem; color: #4a5568;">Selected Model:</div>
                            <div style="margin-left: auto; font-weight: bold; color: #2c3e50;">
                                {selected_model.replace('_', ' ').title()}
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="font-size: 1.2rem; color: #4a5568;">Prediction:</div>
                            <div style="margin-left: auto; font-size: 1.4rem; font-weight: bold; 
                                color: {'#2ecc71' if prediction == 1 else '#e74c3c'}">
                                {'Positive' if prediction == 1 else 'Negative'}
                            </div>
                        </div>
                """, unsafe_allow_html=True)
                
                # Confidence Score
                if len(proba) > 0:
                    confidence = max(proba) * 100
                    st.markdown(f"""
                        <div style="display: flex; align-items: center;">
                            <div style="font-size: 1.2rem; color: #4a5568;">Confidence:</div>
                            <div style="margin-left: auto; font-size: 1.2rem; color: #2c3e50;">
                                {confidence:.1f}%
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")

if __name__ == "__main__":
    main()
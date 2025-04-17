import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# Redshift connection details
REDSHIFT_HOST = "mentalhealth-cluster-1.c0xzvxzrny9v.us-east-2.redshift.amazonaws.com"
REDSHIFT_PORT = 5439
REDSHIFT_DB = "dev"
REDSHIFT_USER = "lokesh"
REDSHIFT_PASSWORD = "Lokesh123#"
TABLE_NAME = "mental_health_cleaned"

def fetch_data_from_redshift():
    try:
        connection = psycopg2.connect(
            host=REDSHIFT_HOST,
            port=REDSHIFT_PORT,
            database=REDSHIFT_DB,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWORD
        )
        query = f"SELECT * FROM {TABLE_NAME};"
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data from Redshift: {e}")
        return pd.DataFrame()

def display_numerical_summary(df):
    numeric_cols = df.select_dtypes(include=['number']).columns
    if not numeric_cols.empty:
        st.subheader("📊 Numerical Summary")
        summary = df[numeric_cols].describe().transpose()
        st.write(summary)

def display_big_numbers(df):
    st.subheader("🌟 Key Metrics")
    if 'age' in df.columns:
        mean_age = df['age'].mean()
        st.metric(label="Average Age", value=f"{mean_age:.1f}", delta=f"{mean_age - df['age'].median():.1f}")

    if 'sleep_hours' in df.columns:
        mean_sleep = df['sleep_hours'].mean()
        st.metric(label="Average Sleep Hours", value=f"{mean_sleep:.1f}", delta=f"{mean_sleep - df['sleep_hours'].median():.1f}")

    if 'work_hours' in df.columns:
        mean_work = df['work_hours'].mean()
        st.metric(label="Average Work Hours", value=f"{mean_work:.1f}", delta=f"{mean_work - df['work_hours'].median():.1f}")

def plot_mental_health_condition(df):
    if 'mental_health_condition' in df.columns:
        df = df.dropna(subset=['mental_health_condition'])
        condition_counts = df['mental_health_condition'].value_counts().reset_index()
        condition_counts.columns = ['Condition', 'Count']
        fig = px.bar(condition_counts, x='Condition', y='Count', color='Condition',
                     title='Mental Health Condition Distribution')
        st.plotly_chart(fig, use_container_width=True)

def plot_age_distribution(df):
    if 'age' in df.columns:
        df = df.dropna(subset=['age'])
        fig = px.histogram(df, x='age', nbins=20, title='Age Distribution of Users', color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig, use_container_width=True)

def plot_stress_level_distribution(df):
    if 'stress_level' in df.columns:
        df = df.dropna(subset=['stress_level'])
        stress_counts = df['stress_level'].value_counts().reset_index()
        stress_counts.columns = ['Stress Level', 'Count']
        fig = px.bar(stress_counts, x='Stress Level', y='Count', color='Stress Level',
                     title='Stress Level Distribution')
        st.plotly_chart(fig, use_container_width=True)

def plot_sleep_hours_distribution(df):
    if 'sleep_hours' in df.columns:
        df = df.dropna(subset=['sleep_hours'])
        fig = px.histogram(df, x='sleep_hours', nbins=20, title='Sleep Hours Distribution', color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig, use_container_width=True)

def plot_work_hours_distribution(df):
    if 'work_hours' in df.columns:
        df = df.dropna(subset=['work_hours'])
        fig = px.histogram(df, x='work_hours', nbins=20, title='Work Hours Distribution', color_discrete_sequence=['#FFA15A'])
        st.plotly_chart(fig, use_container_width=True)

def plot_physical_activity_distribution(df):
    if 'physical_activity_hours' in df.columns:
        df = df.dropna(subset=['physical_activity_hours'])
        fig = px.histogram(df, x='physical_activity_hours', nbins=20, title='Physical Activity Hours Distribution', color_discrete_sequence=['#EF553B'])
        st.plotly_chart(fig, use_container_width=True)

def show_dashboard():
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            font-size: 32px;
        }
        .stMetric {
            font-size: 24px !important;
            font-weight: bold !important;
            margin-top: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🧠 Mental Health Data Dashboard")
    df = fetch_data_from_redshift()

    if df.empty:
        st.warning("No data found in the Redshift database.")
        return

    # Display summaries and metrics
    display_numerical_summary(df)
    display_big_numbers(df)

    with st.expander("🔍 Preview Raw Data"):
        st.dataframe(df.head())

    col1, col2 = st.columns(2)
    with col1:
        plot_mental_health_condition(df)
    with col2:
        plot_age_distribution(df)

    col3, col4 = st.columns(2)
    with col3:
        plot_stress_level_distribution(df)
    with col4:
        plot_sleep_hours_distribution(df)

    col5, col6 = st.columns(2)
    with col5:
        plot_work_hours_distribution(df)
    with col6:
        plot_physical_activity_distribution(df)

if __name__ == "__main__":
    show_dashboard()

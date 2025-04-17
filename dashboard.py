import streamlit as st
<<<<<<< HEAD
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
=======
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import pymysql

# Database connection details
RDS_HOST = "127.0.0.1"
RDS_USER = "root"
RDS_PASSWORD = "yuvi"
RDS_DB = "mental_health_db"
TABLE_NAME = "mental_health_dataset"

def fetch_data_from_mysql():
    """Fetch data from MySQL database."""
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB,
            port=3306
        )
        query = "SELECT * FROM {}".format(TABLE_NAME)
>>>>>>> 340f7f9f8181d8b612c11c1ee7210b6d5ee39f64
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except Exception as e:
<<<<<<< HEAD
        st.error(f"Error fetching data from Redshift: {e}")
        return pd.DataFrame()

def display_numerical_summary(df):
    # Select numeric columns only
    numeric_cols = df.select_dtypes(include=['number']).columns
    if not numeric_cols.empty:
        st.subheader("📊 Numerical Summary")
        summary = df[numeric_cols].describe().transpose()
        st.write(summary)

def display_big_numbers(df):
    # Show specific big numbers (e.g., mean of age, work hours, etc.)
    st.subheader("🌟 Key Metrics")
    
    mean_age = df['age'].mean()
    st.metric(label="Average Age", value=f"{mean_age:.1f}", delta=f"{mean_age - df['age'].median():.1f}")

    mean_sleep = df['sleep_hours'].mean()
    st.metric(label="Average Sleep Hours", value=f"{mean_sleep:.1f}", delta=f"{mean_sleep - df['sleep_hours'].median():.1f}")

    mean_work_hours = df['work_hours'].mean()
    st.metric(label="Average Work Hours", value=f"{mean_work_hours:.1f}", delta=f"{mean_work_hours - df['work_hours'].median():.1f}")

def plot_mental_health_condition(df):
    df = df.dropna(subset=['mental_health_condition'])
    condition_counts = df['mental_health_condition'].value_counts().reset_index()
    condition_counts.columns = ['Condition', 'Count']
    fig = px.bar(condition_counts, x='Condition', y='Count', color='Condition',
                 title='Mental Health Condition Distribution')
    st.plotly_chart(fig, use_container_width=True)

def plot_age_distribution(df):
    df = df.dropna(subset=['age'])
    fig = px.histogram(df, x='age', nbins=20, title='Age Distribution of Users', color_discrete_sequence=['#636EFA'])
    st.plotly_chart(fig, use_container_width=True)

def plot_stress_level_distribution(df):
    df = df.dropna(subset=['stress_level'])
    stress_counts = df['stress_level'].value_counts().reset_index()
    stress_counts.columns = ['Stress Level', 'Count']
    fig = px.bar(stress_counts, x='Stress Level', y='Count', color='Stress Level',
                 title='Stress Level Distribution')
    st.plotly_chart(fig, use_container_width=True)

def plot_sleep_hours_distribution(df):
    df = df.dropna(subset=['sleep_hours'])
    fig = px.histogram(df, x='sleep_hours', nbins=20, title='Sleep Hours Distribution', color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig, use_container_width=True)

def plot_work_hours_distribution(df):
    df = df.dropna(subset=['work_hours'])
    fig = px.histogram(df, x='work_hours', nbins=20, title='Work Hours Distribution', color_discrete_sequence=['#FFA15A'])
    st.plotly_chart(fig, use_container_width=True)

def plot_physical_activity_distribution(df):
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
        .css-18e3th9 {
            background-color: #ffffff !important;
        }
        .stMetric {
            color: #2c3e50;
            font-size: 32px;
            font-weight: bold;
            margin-top: 20px;
        }
        .stSubheader {
            color: #34495e;
            font-size: 28px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🧠 Mental Health Data Dashboard")
    df = fetch_data_from_redshift()

    if df.empty:
        st.warning("No data found in the Redshift database.")
        return

    # Display the numerical summary at the top
    display_numerical_summary(df)
    
    # Display key big numbers (average values)
    display_big_numbers(df)

    with st.expander("🔍 Preview Data"):
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
=======
        st.error(f"Error fetching data from MySQL: {e}")
        return pd.DataFrame()

def plot_mental_health_condition(df):
    """Plot the distribution of mental health conditions."""
    df = df.dropna(subset=['Mental_Health_Condition'])
    condition_counts = df['Mental_Health_Condition'].value_counts()
    
    if condition_counts.empty:
        st.warning("No data available for Mental Health Condition.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=condition_counts.index, y=condition_counts.values, palette='coolwarm', ax=ax)
    ax.set_xlabel('Mental Health Condition', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax.set_title('Mental Health Condition Distribution', fontsize=16, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

def plot_age_distribution(df):
    """Plot the distribution of Age."""
    df = df.dropna(subset=['Age'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Age'], bins=20, kde=True, color='skyblue', ax=ax)
    ax.set_xlabel('Age', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax.set_title('Age Distribution of Users', fontsize=16, fontweight='bold')
    st.pyplot(fig)

def plot_stress_level_distribution(df):
    """Plot the distribution of Stress Levels."""
    df = df.dropna(subset=['Stress_Level'])
    stress_counts = df['Stress_Level'].value_counts()

    if stress_counts.empty:
        st.warning("No data available for Stress Level.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=stress_counts.index, y=stress_counts.values, palette='magma', ax=ax)
    ax.set_xlabel('Stress Level', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax.set_title('Stress Level Distribution', fontsize=16, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

def plot_sleep_hours_distribution(df):
    """Plot the distribution of Sleep Hours."""
    df = df.dropna(subset=['Sleep_Hours'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Sleep_Hours'], bins=20, kde=True, color='green', ax=ax)
    ax.set_xlabel('Sleep Hours', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax.set_title('Sleep Hours Distribution', fontsize=16, fontweight='bold')
    st.pyplot(fig)

def plot_work_hours_distribution(df):
    """Plot the distribution of Work Hours."""
    df = df.dropna(subset=['Work_Hours'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Work_Hours'], bins=20, kde=True, color='orange', ax=ax)
    ax.set_xlabel('Work Hours', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax.set_title('Work Hours Distribution', fontsize=16, fontweight='bold')
    st.pyplot(fig)

def plot_physical_activity_distribution(df):
    """Plot the distribution of Physical Activity Hours."""
    df = df.dropna(subset=['Physical_Activity_Hours'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Physical_Activity_Hours'], bins=20, kde=True, color='red', ax=ax)
    ax.set_xlabel('Physical Activity Hours', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax.set_title('Physical Activity Hours Distribution', fontsize=16, fontweight='bold')
    st.pyplot(fig)

def show_dashboard():
    """Display the mental health dashboard with various plots."""
    st.title("🧠 Mental Health Data Dashboard")

    # Fetch data from MySQL
    df = fetch_data_from_mysql()
    
    if df.empty:
        st.warning("No data found in the database.")
        return

    # Create side-by-side layout using columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("💡 Mental Health Condition Distribution")
        plot_mental_health_condition(df)
        
    with col2:
        st.header("📊 Age Distribution")
        plot_age_distribution(df)

    col3, col4 = st.columns(2)

    with col3:
        st.header("📈 Stress Level Distribution")
        plot_stress_level_distribution(df)

    with col4:
        st.header("🛏️ Sleep Hours Distribution")
        plot_sleep_hours_distribution(df)

    col5, col6 = st.columns(2)

    with col5:
        st.header("⏰ Work Hours Distribution")
        plot_work_hours_distribution(df)

    with col6:
        st.header("💪 Physical Activity Hours Distribution")
        plot_physical_activity_distribution(df)
>>>>>>> 340f7f9f8181d8b612c11c1ee7210b6d5ee39f64

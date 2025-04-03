import streamlit as st
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
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except Exception as e:
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

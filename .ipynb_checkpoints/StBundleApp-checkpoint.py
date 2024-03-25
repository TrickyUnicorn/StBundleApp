import streamlit as st
import json
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="home", #name in browser tab
    page_icon="🏠",
)

def load_feedback(filename=r'feedback.json'):
    """Load feedback data from a JSON file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        st.error(f"File {filename} not found.")
        return []

def display_feedback_stats(data):
    """Display statistics based on the feedback data."""
    if not data:
        st.write("No feedback data available.")
        return
    
    # Convert data to DataFrame for easier analysis
    df = pd.DataFrame(data)
    
    # Display basic statistics
    st.write("Total feedback entries:", len(df))
    
    department_counts = df['department'].value_counts().reset_index()
    department_counts.columns = ['Department', 'Number of Feedbacks']  # Renaming columns for clarity

    fig = px.bar(department_counts, 
                 x='Department', y='Number of Feedbacks',
                 title='Number of Feedbacks per Department')
    st.plotly_chart(fig)
    
    # Display all feedback entries in a table
    st.write("All Feedback Entries:")
    st.dataframe(df[['last_name', 'department', 'problem_name', 'score']], width=700)

def app():
    """Entry point for the feedback statistics page."""
    st.title("Feedback Statistics")
    # Load feedback data
    feedback_data = load_feedback()

    # Display statistics
    display_feedback_stats(feedback_data)

    
app()

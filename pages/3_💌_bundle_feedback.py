import streamlit as st
import pandas as pd
import json
from datetime import datetime
import DataLoaders

st.set_page_config(
    page_title="edit", #name in browser tab
    page_icon="💌",
    initial_sidebar_state="collapsed",
)


# Streamlit app UI
st.title("Feedback Bundle")

# Departments list
departments = ['IT', 'Marketing', 'Sales', 'Leader', 'Finance', 'Support', 'Logistics', 'Success']

# Initialize session state variables if they don't exist
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = ''
if 'last_name' not in st.session_state:
    st.session_state['last_name'] = ''
if 'department' not in st.session_state:
    st.session_state['department'] = departments[0]  # Default to first department
if 'problem_name' not in st.session_state:
    st.session_state['problem_name'] = ''
if 'score' not in st.session_state:
    st.session_state['score'] = 5

with st.form("feedback_form", clear_on_submit=False):  # Changed to False
    st.write("Proszę uzupełnij pola poniżej:")
    # Use session_state for value and on_change to update it
    first_name = st.text_input("Imię", value=st.session_state.first_name, key='first_name')
    last_name = st.text_input("Nazwisko", value=st.session_state.last_name, key='last_name')
    department = st.selectbox("Dział", departments, index=departments.index(st.session_state.department), key='department')
    problem_name = st.text_input("Co byś zmienił w Bundle?")
    score = st.slider("Oceń jak bardzo Cię to ogranicza?", min_value=1, max_value=10, value=5)
    
    submitted = st.form_submit_button("Wyślij Feedback")
    
    if submitted:
        # Construct a dictionary with the input data
        feedback_data = {
            "first_name": first_name,
            "last_name": last_name,
            "department": department,
            "problem_name": problem_name,
            "score": score,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        #save_data_json(feedback_data)
        DataLoaders.add_row_gsheet('Feedback',feedback_data)
        st.success("Feedback saved")
        
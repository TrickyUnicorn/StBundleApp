import streamlit as st
import json
import Login

def load_feedback(filename='Bundle/feedback.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_feedback(data, filename='Bundle/feedback.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def delete_feedback(feedback_data, delete_index, filename='Bundle/feedback.json'):
    # Remove the entry at the specified index
    del feedback_data[delete_index]
    # Save the updated list back to the JSON file
    save_feedback(feedback_data, filename)

def edit_app():

    feedback_data = load_feedback()

    # Track if any deletion has occurred
    deletion_occurred = False

    for i, entry in enumerate(feedback_data):
        with st.expander(f"#{i+1}: {entry['problem_name']}"):
            first_name = st.text_input(f"First Name #{i+1}", value=entry['first_name'], key=f"first_name_{i}")           
            last_name = st.text_input(f"Last Name #{i+1}", value=entry['last_name'], key=f"last_name_{i}")
            department = st.text_input(f"Department #{i+1}", value=entry['department'], key=f"department_{i}")   
            problem_name = st.text_input(f"Problem Name #{i+1}", value=entry['problem_name'], key=f"problem_{i}")
            score = st.slider(f"Score #{i+1}", min_value=1, max_value=10, value=entry['score'], key=f"score_{i}")     


            entry['problem_name'] = problem_name
            entry['score'] = score
            entry['department'] = department
            entry['first_name'] = first_name
            entry['last_name'] = last_name

            # button container
            col1, spacer, col2 = st.columns([2, 5, 1])

            with col1: 
                if st.button('Save Changes', key=f"save_changes_{i}"):
                    save_feedback(feedback_data)
                    st.success('Feedback updated successfully.')
            # Delete Feedback button
            with col2:
                if st.button(f"Delete", type='primary', key=f"delete_{i}"):
                    # Directly call delete_feedback function here
                    delete_feedback(feedback_data, i)
                    # Use st.experimental_rerun() to refresh and reflect the deletion
                    st.experimental_rerun()



# Call the login function or page at the start
if 'username' not in st.session_state:
    login_successful = Login.login_page()  # Attempt to login
    if login_successful:
        'loginnnnndsndsnd'
        st.experimental_rerun()  # Rerun the script to reflect the login state change immediately
else:
    # Once logged in, decide what to show based on role
    if st.session_state['role'] == 'admin':
        edit_app()

    

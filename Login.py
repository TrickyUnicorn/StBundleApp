import streamlit as st
import pandas as pd
import json

# Example users with roles
users_with_roles = {
    'admin': {'password': 'adminpass', 'role': 'admin'},
    'user': {'password': 'userpass', 'role': 'user'}
}

# Simple login function
def login(username, password):
    user_info = users_with_roles.get(username, None)
    if user_info and user_info['password'] == password:
        st.session_state['username'] = username
        st.session_state['role'] = user_info['role']
        return True
    return False



# TEST below#
st.session_state

# Login UI
def login_page():
    if 'username' not in st.session_state:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username, password):
                st.success("Logged in successfully.")
                return True
            else:
                st.error("Login failed.")
 
#login_page()
"""
# Example of conditional page access after login
if 'username' in st.session_state:
    # Display different content based on the user's role
    if st.session_state['role'] == 'admin':
        st.write("Admin content here")
    elif st.session_state['role'] == 'user':
        st.write("User content here")
    # Logout button
    if st.button("Logout"):
        del st.session_state['username']
        del st.session_state['role']
        """
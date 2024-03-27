import streamlit as st
import pandas as pd
import json
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import time

# Function to save data to JSON
def save_data_json(data, filename=r'Bundle\feedback.json'):
    try:
        with open(filename, 'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data
            file_data.append(data)
            # Sets file's current position at offset.
            file.seek(0)
            # Convert back to json.
            json.dump(file_data, file, indent=4)
    except FileNotFoundError:
        with open(filename, 'w') as file:
            # If file does not exist, create a new file and write data
            json.dump([data], file, indent=4)
          


      
        
def read_data_gsheet(worksheet_name):
    conn = st.connection("gsheets", type =GSheetsConnection )
    data = conn.read(worksheet=worksheet_name, ttl=1)
    # Filter out columns whose names start with 'Unnamed'
    filtered_data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    return filtered_data

def save_data_gsheet(worksheet_name, updated_data):
       # Initialize the loading bar
        my_bar = st.progress(0)
        
        for percent_complete in range(100):
            time.sleep(0.01)  # Simulate processing time
            my_bar.progress(percent_complete + 1)
        
        conn = st.connection("gsheets", type =GSheetsConnection )
        time.sleep(10)
        conn.update(worksheet=worksheet_name, data=updated_data)
        data =  conn.read(worksheet=worksheet_name, ttl=1)
    
        conn.clear(worksheet=worksheet_name)
    
        filtered_data_row = data.dropna(how='all')
        filtered_data_col = filtered_data_row.loc[:, ~filtered_data_row.columns.str.contains('^Unnamed')]
    
        conn.update(worksheet=worksheet_name, data = filtered_data_col)
    
        #st.success("data updated")
        return True
    

def add_row_gsheet(worksheet_name, new_row):
    data = read_data_gsheet(worksheet_name)
    # Ensure new_data_row is in the form of a DataFrame for consistency
    new_row_df = pd.DataFrame([new_row])
    new_data = pd.concat([data, new_row_df], ignore_index=True)
    save_data_gsheet(worksheet_name, new_data)
    return True


def delete_row_gsheet(worksheet_name, row_idx):
    data = read_data_gsheet(worksheet_name)
    
    row_idx_int =row_idx
    
    new_data = data.drop(data.index[row_idx_int])
    filtered_data = new_data.dropna(how='all')
    
     # Reset the index to account for the dropped row, if necessary
    filtered_data.reset_index(drop=True, inplace=True)

    st.cache_data.clear()
    save_data_gsheet(worksheet_name, filtered_data)
    #st.cache_data.clear()
    #st.experimental_rerun()  

    return filtered_data
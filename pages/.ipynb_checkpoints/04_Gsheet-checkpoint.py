import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

conn = st.connection("gsheets", type =GSheetsConnection)

json_data= pd.read_json('feedback.json')
st.dataframe(json_data)

data = conn.read(worksheet='Feedback')

st.title("Read Google Sheet as DataFrame")

st.write(data.head())

st.dataframe(data)

if st.button("Refill worksheet"):
    conn.update(worksheet='Feedback', data = json_data)
    st.success("data updated")
    
if st.button("Clear worksheet"):
    data_1 =  conn.read(worksheet='Feedback', ttl=1)
    
    conn.clear(worksheet='Feedback')
    
    filtered_data = data_1.dropna(how='all')
    
    conn.update(worksheet='Feedback', data = filtered_data)
    
    st.success("data updated")
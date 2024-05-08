# app.py
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json


st.set_page_config(
    page_title="sheets", #name in browser tab
    page_icon="📑",
)


# Example sheet_relations_col (replace with your actual data)
data_path = 'SheetRelationCol.json'

with open(data_path, 'r') as file:
    sheet_relations_col = json.load(file)
    json_data = json.dumps(sheet_relations_col, indent=4)

# Function to draw the graph
def draw_graph(sheet_name):
    G = nx.DiGraph()

    for source, targets in sheet_relations_col.items():
        if source == sheet_name:
            G.add_node(source)  # Ensure all sources are added as nodes
            for col, linked_sheets in targets.items():
                # Assuming col represents the simplified target name
                simplified_target = col
                # Join linked sheet names with newline characters
                edge_label = '\n'.join(linked_sheets)
                G.add_edge(source, simplified_target, label=edge_label)

    # Draw the graph
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42)  # Consistent layout

    nx.draw(G, pos, with_labels=True, arrows=True, node_size=7000, node_color='#1bd09b', font_size=10, font_weight='bold')

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(sheet_name)
    st.pyplot(plt)

def btn_b_callback():
    st.session_state['show_graph'] = False
    st.session_state['show_hide_button']=False   
    
    
# Streamlit app
st.title('Sheet relationship')


# Initialization
if 'show_graph' not in st.session_state:
    st.session_state['show_graph'] = False
if 'show_hide_button' not in st.session_state:
    st.session_state['show_hide_button']=False
    

# Dropdown to select sheet name
selected_sheet_name = st.selectbox('Select Sheet Name', options=list(sheet_relations_col.keys()))

# button container
col1, spacer, col2 = st.columns([2, 5, 1])
# Button to draw graph
with col1:
    if st.button('Draw Graph'):
        st.session_state['show_graph'] = True
        st.session_state['show_hide_button'] = True
        
with col2:    
    if st.button('Hide', type='primary', disabled=not st.session_state['show_graph'], on_click=btn_b_callback):
        pass
        #st.experimental_rerun()
    
if st.session_state['show_graph'] == True:
    draw_graph(selected_sheet_name)
    
with st.expander("See Sheet Relationships Bar Chart", expanded= not st.session_state['show_graph']):
    # Convert data to a format suitable for a bar chart
    data = {sheet: len(targets) for sheet, targets in sheet_relations_col.items()}
    df = pd.DataFrame(list(data.items()), columns=['Sheet', 'Number of Links'])

    # Sort the DataFrame in descending order by the number of links
    # Note: For bar_chart, sort ascending to have the largest bar at the top
    df = df.sort_values('Number of Links', ascending=True)

    # Streamlit app
    st.title('Sheet Relationships Bar Chart')

    # Display the bar chart
    st.bar_chart(df,  x='Sheet', color='#d01b50')

import streamlit as st
import pandas as pd
import DataLoaders
from html_table_generator import HtmlTableGenerator

# Sample DataFrame for demonstration
data = {
    'acronym': ['WILD', 'WILD', 'WILD', 'BEBRPL', 'BEBRPL'],
    'ver': ['WILD_01', 'WILD_02', 'WILD_03', 'BEBRPL_01', 'BEBRPL_02']
}


df = pd.DataFrame(data)

# Two columns layout
col1, col2 = st.columns(2)



with col1:
    # Selectbox for choosing an acronym
    acronym_selectbox = st.selectbox(
        "Select acronym",
        [None, "WILD", "BEBRPL", "LMFASH"],  # Added None for no selection
        index=0,  # Default to showing None as the selected value
        format_func=lambda x: "Select an acronym" if x is None else x  # Display text for None value
    )
    versions = df[df['acronym'] == acronym_selectbox]['ver'].tolist() if acronym_selectbox else []
    
    standard_checkbox_disabled = acronym_selectbox is None
    standard_checkbox_tick = False
    
    if not versions:
        standard_checkbox_tick = True
        standard_checkbox_disabled = True

    standard_checkbox = st.checkbox("Create new based on standard version", key="disabled", disabled=standard_checkbox_disabled, value=standard_checkbox_tick)

        

with col2:
    # If an acronym is chosen, filter versions for that acronym

    # Determine the disabled state
    disabled_state = standard_checkbox or not acronym_selectbox

    # Version selectbox, disabled if no acronym is selected
    version = st.selectbox(
        "Select version",
        versions,
        disabled=disabled_state,
        help="Select an acronym first" if not acronym_selectbox else None  # Optional help text
    )

if acronym_selectbox:
    st.button("Save offer")
    if st.button("Modify offer"):
        st.session_state['acronym'] = acronym_selectbox
        st.session_state['standard_version'] = standard_checkbox
        st.session_state['version'] = version
        #open modify page            
        st.switch_page('pages/7_modify_offer.py')
        

        
    pirce_list_df = DataLoaders.read_data_gsheet("OnePagerSampleData") 
    pirce_list_df['Category'] = pirce_list_df['Pozycja'].str.split('-').str[0]
    # HTML table generation
    html_generator = HtmlTableGenerator()
    img_url='https://omnipack.com/build/images/_fullfillment/icon-magazynowanie.d5867cc4.svg'

    categories = pirce_list_df['Category'].unique()
    pdf_html = ""

    for category in categories:
        category_df = pirce_list_df[pirce_list_df['Category']==category]
        category_df = category_df.drop('Category', axis=1)
        html_content = html_generator.generate_table(category_df, category, img_url)
        pdf_html += html_content
        st.markdown(html_content, unsafe_allow_html=True)
    
    
    

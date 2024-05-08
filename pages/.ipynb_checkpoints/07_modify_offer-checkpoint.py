import streamlit as st
import pandas as pd
import DataLoaders




# Function to return styled HTML table
def generate_html_header_go_1(df):
    # Start of the HTML table, adjust styling as needed
    # header <th> #181434 rows <tr> color #d0e4f4 or #DCE6F1
    html = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap');
    
    /* Ensures borders between cells are visible */
    table {
        width: 100%;
        font-family: 'Poppins', sans-serif;
        border-collapse: collapse; /* Adjusts table borders to collapse into a single border */
    }
    
    th, td {
        padding: 8px;
        text-align: center;
        font-size: 14px; /* Adjusted font size for data rows */
        border: 1px solid white !important; /* White border for cells */


    }   
    th {
        background-color: #181434; /* Dark background for headers */
        color: white;
        font-size: 16px; /* Adjusted font size for headers */
        font-weight: normal; /* Ensures headers are not bold */
        border: 1px #181434 !important;

    }   
    </style>
    """
    
    html += '<table>'
    html += '<tr>' + ''.join(f'<th>{col}</th>' for col in df.columns) + '</tr>'  # Table headers

    # Table rows
    html += '</table>'
    return html


def editable_table_1(df, category_name):
    # Display headers
    col1, col2 = st.columns(2)
    with col1:
        generate_html_header(category_name)
        html_content = generate_html_header(category_name)
        st.markdown(html_content, unsafe_allow_html=True)
    with col2: 
        st.radio( "Pick the tier",  [":rainbow[A]", "***B***", "C", "D", "E", "F"], key=category+"_ratio", horizontal=True,)
    
    #D isplay Data Grid
    with st.expander("Expand Category", expanded= False):
        #st.markdown(generate_html_header_go_1(df), unsafe_allow_html=True)
        #df = df.set_index(df.columns[0])
        df["enable"] = True
        df = df[["enable", "Pozycja", "Current", "New"]]
        edited_df = st.data_editor(df, num_rows= "flex",  use_container_width=True, key=category_name, hide_index=True,
                                  disabled=("Pozycja", "Current"))
        #favorite_command = edited_df.loc[edited_df["Price"].idxmax()]["Product"]
        #st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
    
    return 

def generate_html_header(category_name):
    html = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap');
    
    .category-header {
        background-color: #181434; /* Dark background for the header */
        color: white;
        font-family: 'Poppins', sans-serif;
        font-size: 18px; /* Size of the category name */
        text-align: center;
        padding: 8px; /* Padding around the text for spacing */
        margin: 8px 0; /* Margin around the header block for spacing from other elements */
        border-radius: 0px; /* Optional: adds rounded corners to the header block */
    }
    </style>
    """
    
    # Adding the category name within a styled div
    html += f'<div class="category-header">{category_name}</div>'
    
    return html



# Function to display and handle the form
def add_category_form(df):
    with st.form("add_category_form"):
        # Form fields
        new_product = st.text_input("Product Name")
        new_price = st.number_input("Price", min_value=0.0, format="%.2f")
        new_stock = st.number_input("Stock", min_value=0, step=1)
        new_category = st.text_input("Category")
        
        # Form submission button
        submitted = st.form_submit_button("Add Product")
        if submitted:
            # Add the new entry to the DataFrame
            new_entry = {'Product': new_product, 'Price': new_price, 'Stock': new_stock, 'Category': new_category}
            updated_df = df.append(new_entry, ignore_index=True)
            st.success("Product added successfully!")
            return updated_df
    return df




# Page title and informations
st.title("Modify Offer")
    
# Display the previously selected values, now for modification
st.write(f"**{st.session_state.get('acronym', '')}** ver: {st.session_state.get('version', 'standard_version')}", unsafe_allow_html=True)



data = DataLoaders.read_data_gsheet("OnePagerSampleData")

df = pd.DataFrame(data)
df['Category'] = df['Pozycja'].str.split('-').str[0]
df=df.dropna()

categories = df['Category'].unique()


for category in categories:
    category_df = df[df['Category']==category]
    category_df = category_df.drop('Category', axis=1)
    editable_table_1(category_df, category)

if st.button('Save', type = 'primary'):
    pass

# Update the DataFrame based on the form input
#if st.button('Add Form'):
#    df = add_category_form(df)
#    # Display the updated DataFrame
#    st.write("Updated DataFrame:")
#    st.dataframe(df)




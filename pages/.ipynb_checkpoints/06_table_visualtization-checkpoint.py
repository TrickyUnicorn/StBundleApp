import streamlit as st
import pandas as pd
import DataLoaders
import pdfkit
from tempfile import NamedTemporaryFile



# Function to return styled HTML table
def generate_html_table_go_1(df):
    # Start of the HTML table, adjust styling as needed
    # header <th> #181434 rows <tr> color #d0e4f4 or #DCE6F1
    html = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap');
    
    /* Ensures borders between cells are visible */
    table {
        width: 120%;
        font-family: 'Poppins', sans-serif;
        border-collapse: collapse; /* Adjusts table borders to collapse into a single border */


    }
    
    th, td {
        padding: 8px;
        text-align: center;
        font-size: 14px; /* Adjusted font size for data rows */
        border: 1px solid white !important; /* White border for cells */


    }
    
    tr:nth-child(even) {
        background-color: #DCE6F1; /* Light blue background for even rows */
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
    for index, row in df.iterrows():
        html += '<tr>' + ''.join(f'<td>{row[col]}</td>' for col in df.columns) + '</tr>'
    html += '</table>'
    return html



def generate_html_table_go_2(df, category):
    # Start of the HTML table, adjust styling as needed
    # header <th> #181434 rows <tr> color #d0e4f4 or #DCE6F1
    html = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap');
    
    /* Ensures borders between cells are visible */
    table {
        width: 120%;
        font-family: 'Poppins', sans-serif;
        border-collapse: collapse; /* Adjusts table borders to collapse into a single border */


    }
    
    th, td {
        padding: 8px;
        text-align: center;
        font-size: 14px; /* Adjusted font size for data rows */
        border: 1px solid white !important; /* White border for cells */


    }
    
    tr:nth-child(even) {
        background-color: #DCE6F1; /* Light blue background for even rows */
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
    for index, row in df.iterrows():
        html += '<tr>' + ''.join(f'<td>{row[col]}</td>' for col in df.columns) + '</tr>'
    html += '</table>'




def generate_html_table_go_2(df, category_name):
    # Start of the HTML table, adjust styling as needed
    html = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap');
       
    .table-container {{
        margin-bottom: 40px; /* Adds space below the table */
    }}
    table {{
        width: 120%;
        font-family: 'Poppins', sans-serif;
        border-collapse: separate;
        border-spacing: 8px 0; /* Adjusts spacing between rows */
    }}
    th, td {{
        padding: 8px;
        text-align: center;
        font-size: 14px;
        border: 0px solid white !important;
    }}
    tr:nth-child(even) {{
        background-color: #DCE6F1;
    }}
    th {{
        background-color: #181434;
        color: white;
        font-size: 16px;
        font-weight: normal;
    }}
    .category-header {{
        background-color: #181434; /* Matching the header style */
        color: white;
        font-size: 24px;
        writing-mode: vertical-lr; /* Makes text vertical */
        transform: rotate(180deg); /* Adjusts text direction */
        white-space: nowrap; /* Ensures text stays in one line */
        width: 28px;
    }}
    </style>
    """

    # Modifying the table to include vertical text in the category column
    html += '<div class="table-container">'
    html += '<table>'
    category_icon_class="https://openclipart.org/download/231068/3D-Isometric-Cardboard-Box.svg"
    # Adjust rowspan to include all data rows plus one for the header
    html += f'<tr><th class="category-header" rowspan="{len(df)+1}">{category_name}</th>' + ''.join(f'<th>{col}</th>' for col in df.columns) + '</tr>'

    for index, row in df.iterrows():
        html += '<tr>' + ''.join(f'<td>{row[col]}</td>' for col in df.columns) + '</tr>'
    html += '</table>'
    html += '</div>' # Close the div here
    return html




def generate_html_table_go_3(df, category_name, img_url):
    # Start of the HTML table, adjust styling as needed
    html = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap');
    
    .table-container {{
        margin-bottom: 40px; /* Adds space below the table */
    }}   
    table {{
        width: 130%;
        font-family: 'Poppins', sans-serif;
        border-collapse: separate;
        border-spacing: 8px 0; /* Adjusts spacing between rows */
    }}
    th, td {{
        padding: 8px;
        text-align: center;
        font-size: 12px;
        border: 0px solid white !important;
    }}
    tr:nth-child(even) {{
        background-color: #DCE6F1;
    }}
    th {{
        background-color: #181434;
        color: white;
        font-size: 16px;
        font-weight: normal;
    }}
    .category-header {{
        background-color: #181434; /* Matching the header style */
        color: white;
        font-size: 24px;
        writing-mode: vertical-lr; /* Makes text vertical */
        transform: rotate(180deg); /* Adjusts text direction */
        white-space: nowrap; /* Ensures text stays in one line */
        width: 28px;
    }}
    </style>
    """

    # Modifying the table to include vertical text in the category column
    html += '<div class="table-container">'
    html += '<table>'
    # Adjust rowspan to include all data rows plus one for the header
    html += f'<tr><th class="category-header" rowspan="{len(df)+1}">{category_name}</th>' + ''.join(f'<th>{col}</th>' for col in df.columns) + f'<th class="category-header" rowspan="{len(df)+1}"><img src="{img_url}" width="80" height="80" ></img></th>' + '</tr>'

    for index, row in df.iterrows():
        html += '<tr>' + ''.join(f'<td>{row[col]}</td>' for col in df.columns) + '</tr>'
    html += '</table>'
    html += '</div>' # Close the div here
    return html



def generate_and_download_pdf(html_content):
    # Generate PDF from the HTML content
    options = {
   # 'no-images': None,
    'disable-external-links': None
}
    pdf = pdfkit.from_string(html_content, False,  options=options)
    
    # Create a temporary file to save the PDF
    with NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
        tmpfile.write(pdf)
        tmpfile.seek(0)
        # Use Streamlit's download button to offer the PDF for download
        st.download_button(
            label="Download PDF",
            data=tmpfile.read(),
            file_name="table.pdf",
            mime="application/octet-stream"
        )

pdf_html = ''

html_content = """
<div>
    <h1>Some table visualizations</h1>
</div>
"""
pdf_html += html_content
st.markdown(html_content, unsafe_allow_html=True)

#st.title("Some table visualizations")
        
        
# Sample DataFrame for demonstration
data = {'Product': ['Product XA', 'Product XB', 'Product XC', 'Product XD', 'Product QA', 'Product QB', 'Product QC'],
        'Price': [10.99, 20.99, 30.99, 20.99, 30.99, 9.99, 11.99],
        'Stock': [100, 50, 75, 50, 75, 23, 12],
        'Pozycja': ['Category X', 'Category X', 'Category X', 'Category X', 'Category Y', 'Category Y', 'Category Y']}
df = pd.DataFrame(data)

data = DataLoaders.read_data_gsheet("OnePagerSampleData")

df = pd.DataFrame(data)
df['Category'] = df['Pozycja'].str.split('-').str[0]


categories = df['Category'].unique()


html_content=''
img='https://omnipack.com/build/images/_fullfillment/icon-magazynowanie.d5867cc4.svg'
for category in categories:
    category_df = df[df['Category']==category]
    category_df = category_df.drop('Category', axis=1)
    html_content = generate_html_table_go_3(category_df, category, img)
    pdf_html += html_content
    st.markdown(html_content, unsafe_allow_html=True)

# Example usage
#html_content = generate_html_table_go_2(df, 'Category X')
#pdf_html += html_content
#st.markdown(html_content, unsafe_allow_html=True)

#img='https://openclipart.org/download/231068/3D-Isometric-Cardboard-Box.svg'
#img='https://omnipack.com/build/images/_fullfillment/icon-magazynowanie.d5867cc4.svg'
#html_content = generate_html_table_go_3(df, 'Category All', img)
#pdf_html += html_content
#st.markdown(html_content, unsafe_allow_html=True)


#config = pdfkit.configuration(wkhtmltopdf='/Lib/site-packages/wkhtmltopdf')


generate_and_download_pdf(pdf_html)

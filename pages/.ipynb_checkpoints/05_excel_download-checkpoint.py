import streamlit as st
import pandas as pd
import io


st.set_page_config(
    page_title="excel", #name in browser tab
    #page_icon="💌",
    #initial_sidebar_state="collapsed",
)




# Function to create Excel file
def create_excel():
    data = {'Product': ['Product A', 'Product B'],
            'Price': [10.99, 20.99],
            'Stock': [100, 50]}
    df = pd.DataFrame(data)

    # Create a BytesIO buffer to save file in memory
    output = io.BytesIO()
    
    # Use XlsxWriter as the engine
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Convert the dataframe to an XlsxWriter Excel object
        df.to_excel(writer, sheet_name='Sheet1', index=False)

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Set the column width for clarity
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 10)

        # Add some cell formats
        format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                       'font_color': '#9C0006'})
        format2 = workbook.add_format({'bg_color': '#C6EFCE',
                                       'font_color': '#006100'})

        # Apply conditional formatting based on values
        worksheet.conditional_format('B2:B3', {'type': 'cell',
                                               'criteria': '>=',
                                               'value': 15,
                                               'format': format1})
        worksheet.conditional_format('B2:B3', {'type': 'cell',
                                               'criteria': '<',
                                               'value': 15,
                                               'format': format2})

    # Seek to the beginning of the stream
    output.seek(0)

    return output

# Streamlit app
def app():
    st.title('Download Excel File Example')

    # Button to create and download Excel file
    if st.button('Generate Excel File'):
        file = create_excel()
        file_name_input = st.text_input("Enter File Name", value ='example_file_v01')
        file_name = file_name_input + '.xlsx'
        
        # Use the 'download_button' to offer file for download
        st.download_button(label='Download Excel',
                           data=file,
                           type='primary',
                           file_name=file_name,
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Call the Streamlit app function
app()
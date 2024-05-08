'''
import streamlit as st
import pandas as pd
#import DataLoaders
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
#from html_table_generator import HtmlTableGenerator
import time
import logging

import DB_conf as conf


st.write('import conf')

cannstring = "DRIVER={ODBC Driver 17 for SQL Server};"
cannstring += "SERVER=" + conf.DB_HOST + ";"
cannstring += "DATABASE=" + conf.DB_NAME + ";"

if conf.DB_Trusted_Connection == True:
    cannstring += "Trusted_Connection=yes;"
else:
    cannstring += "UID=" + conf.DB_USER + ";PWD=" + conf.DB_PASS + ";"
    
    
sql = "SELECT * FROM dbo.TestABC "
logging.info(f"Connect to MSSQL end execute SQL= \"{sql}\"")
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": cannstring})
engine = create_engine(connection_url)
df = pd.read_sql(sql, engine)
logging.info(f"Append {df.shape[0]} rows to PraceDodatkowe.Inserty ")

st.write(df)
'''



#St way
import streamlit as st
import pyodbc
import json
import pandas as pd
import DataLoaders
import hashlib


def generate_create_raw_table_statement(dest_table, columns_nr):
    # Start the INSERT INTO statement with the initial column name
    create_statement = f"IF OBJECT_ID(N'[{dest_table}_raw]', N'U') IS NULL BEGIN "
    create_statement += "CREATE TABLE [" + dest_table + "_raw] (ROW_INDEX int NOT NULL "
    # Generate column names based on columns_nr, starting from 1
    for i in range(1, columns_nr+1):  # start from 1 as ROW_INDEX is already added
        create_statement += ", COLUMN_" + "{:02}".format(i) + ' varchar(max) NULL ' # formatting numbers to ensure sorting
    create_statement+=", row_hash varchar(8000) NULL); END; \n"
    return create_statement

def generate_create_arch_table_statement(dest_table, columns_nr):
    # Start the INSERT INTO statement with the initial column name
    create_statement = f"IF OBJECT_ID(N'[{dest_table}_arch]', N'U') IS NULL BEGIN "
    create_statement += "CREATE TABLE [" + dest_table+'_arch]' + " (id int identity not null, ROW_INDEX int NOT NULL "
    # Generate column names based on columns_nr, starting from 1
    for i in range(1, columns_nr+1):  # start from 1 as ROW_INDEX is already added
        create_statement += ", COLUMN_" + "{:02}".format(i) + ' varchar(max) NULL ' # formatting numbers to ensure sorting
    create_statement+=", row_hash varchar(max) NULL, sheet_hash varbinary(8000) NOT NULL,  insert_date DATETIME DEFAULT GETDATE()); END; \n"
    return create_statement

def generate_create_dest_table_statement(dest_table):
    # Start the INSERT INTO statement with the initial column name
    create_statement = f"IF OBJECT_ID(N'[{dest_table}]', N'U') IS NULL BEGIN "
    create_statement += "CREATE TABLE [" + dest_table+']' + " (id int identity not null, Country varchar(255) NULL, ServiceType varchar(800) NULL, Service varchar(800) NOT NULL, Price float NOT NULL, date_from datetime NULL, date_to datetime NULL, insert_date datetime NOT NULL,  sheet_name varchar(255) NOT NULL); END; \n "
    return create_statement


def generate_insert_statement(dest_table, columns_nr):
    # Start the INSERT INTO statement with the initial column name
    insert_statement = "INSERT INTO [" + dest_table + "_raw] (ROW_INDEX"

    # Generate column names based on columns_nr, starting from 1
    for i in range(1, columns_nr+1):  # start from 1 as ROW_INDEX is already added
        insert_statement += ", COLUMN_" + "{:02}".format(i)   # formatting numbers to ensure sorting
    insert_statement += ", row_hash) VALUES( ?"
    for i in range(1, columns_nr+2):  # start from 1 as ROW_INDEX is already added
        insert_statement += ", ?"   # formatting numbers to ensure sorting
    insert_statement += ")"
    return insert_statement


def generate_insert_arch_procedure(table_name, number_of_columns):
    # SQL Server doesn't have "CREATE OR REPLACE PROCEDURE" syntax, so we need to manually check
    # if the procedure exists and drop it if it does, or create a new one if it doesn't.
    procedure_name = f"[{table_name}_InsertArchProcedure]"
    tsql = f"""
IF OBJECT_ID(N'{procedure_name}', 'P') IS NOT NULL
    DROP PROCEDURE {procedure_name}
GO

CREATE PROCEDURE {procedure_name}
AS
BEGIN
    -- Variable to hold the concatenated row hashes
    DECLARE @AllRowHashes AS NVARCHAR(MAX);

    -- Aggregate all row hashes into one large string
    SELECT @AllRowHashes = (SELECT row_hash AS [text()]
                            FROM [{table_name}_raw]
                            FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)');

    -- Compute the hash of the concatenated row hashes
    DECLARE @SheetHash AS VARBINARY(8000);
    SET @SheetHash = HASHBYTES('SHA2_256', @AllRowHashes);

    -- Check if the sheet hash already exists in the archive table
    IF NOT EXISTS (SELECT 1 FROM [{table_name}_arch] WHERE sheet_hash = @SheetHash)
    BEGIN
        -- Insert statement with computed sheet hash
        INSERT INTO [{table_name}_arch]
            (ROW_Index, {", ".join(f"COLUMN_{str(i).zfill(2)}" for i in range(1, number_of_columns + 1))}, row_hash, sheet_hash)
        SELECT ROW_Index, {", ".join(f"COLUMN_{str(i).zfill(2)}" for i in range(1, number_of_columns + 1))}, row_hash, @SheetHash
        FROM [{table_name}_raw];
    END;
END
GO
"""
    return tsql

def generate_insert_dest_procedure(conn, table_name, number_of_columns):

    #[BundleImportConfig] 
    #init
    date_from_column_name="COLUMN_02"
    date_from_row_index = 0
    data_start_row_index = 2
    data_end_row_index = 10000
    country_column_name= "COLUMN_01"
    type_column_name= "''"
    service_column_name= "COLUMN_03"
    price_column_name= "COLUMN_04"
    with conn.cursor() as cur:
            # Execute a query to fetch configuration from the database
            cur.execute(f"""
                SELECT 
                    SheetName, ValidFromColumnName, ValidFromRowIndex, 
                    DataStartsRowIndex, DataEndsRowIndex, CountryColumnName, 
                    ServiceTypeColumnName, ServiceColumnName, PriceColumnName 
                FROM [BundleImportConfig]
                WHERE SheetName = '{table_name}'
            """)
            # Fetch all the results
            results = cur.fetchall()
            st.write(results)
            # Optionally handle multiple configurations, here we just take the first one if available
            if results:
                result = results[0]
                date_from_column_name = result[1] 
                date_from_row_index = result[2] 
                data_start_row_index = result[3] 
                if result[4] is not None: data_end_row_index = result[4] 
                country_column_name = result[5] 
                if result[6] is not None: type_column_name = result[6]  
                else: type_column_name =  "''"
                service_column_name = result[7] 
                price_column_name = result[8] 

    procedure_name = f"[{table_name}_InsertProcedure]"
 

    tsql = f"""
IF OBJECT_ID(N'{procedure_name}', 'P') IS NOT NULL
    DROP PROCEDURE {procedure_name}
GO

CREATE PROCEDURE {procedure_name}
AS
BEGIN

    -- Variable to hold the latest timestamp insert date
    DECLARE @LastInsertDate AS datetime;
    
    SELECT @LastInsertDate = (SELECT max(insert_date) 
                            FROM [{table_name}_arch]);
                            
    -- Variable to hold the date from pricelist date
    DECLARE @DateFrom AS datetime;
    
    SELECT  @DateFrom = (SELECT CONVERT(varchar, CONVERT(date,{date_from_column_name}, 105), 23) 
                            FROM [{table_name}_arch]
                            WHERE ROW_INDEX={date_from_row_index}
                            AND insert_date = @LastInsertDate);

    DELETE FROM [{table_name}] WHERE date_from = @DateFrom;
    
    INSERT INTO [{table_name}]
            ( Country, ServiceType, Service, Price, date_from, insert_date, sheet_name)
    SELECT {country_column_name}, {type_column_name}, {service_column_name}, {price_column_name},  @DateFrom, @LastInsertDate, '{table_name}'
    FROM [{table_name}_arch]
    WHERE ROW_Index BETWEEN {data_start_row_index} AND {data_end_row_index}
    AND insert_date = @LastInsertDate
    AND {service_column_name} IS NOT NULL;

    -- Calculate the next different date_from using a self-exclusion join
    ;WITH RankedDates AS (
        SELECT
            a.date_from,
            a.date_to,
            DATEADD(day, -1, MIN(b.date_from)) AS next_date_from
        FROM
            dbo.[{table_name}] a
        LEFT JOIN
            dbo.[{table_name}] b ON a.date_from < b.date_from
        GROUP BY
            a.date_from, a.date_to
    )
    -- Update the date_to column with the next different date_from or '9999-01-01' if none exists
    UPDATE dbo.[{table_name}]
    SET date_to = ISNULL(r.next_date_from, '9999-01-01')
    FROM
        dbo.[{table_name}]
    INNER JOIN
        RankedDates r ON dbo.[{table_name}].date_from = r.date_from;
END;
GO
"""
    return tsql


def bulid_raw_structures(conn, table_name, number_of_columns, reset = False):
    
    tsql_table=generate_create_raw_table_statement(table_name, number_of_columns)
    tsql_table+=generate_create_arch_table_statement(table_name,number_of_columns)
    tsql_table+=generate_create_dest_table_statement(table_name)
    tsql_procedure=generate_insert_arch_procedure(table_name, columns_nr)  
    tsql_procedure+=generate_insert_dest_procedure(conn, table_name, number_of_columns)

        # Execute the SQL insert command
    with conn.cursor() as cur:
        if reset is True:
             cur.execute(f"DROP TABLE [{table_name}_raw]")
             cur.execute(f"DROP TABLE [{table_name}_arch]")
             conn.commit()
            
        cur.execute(tsql_table)
        conn.commit()
        # Execute procedure creation in a separate batch
        for statement in tsql_procedure.split('GO'):
            if statement.strip():
                cur.execute(statement)
                conn.commit()
    
    return st.success("Structures rebuilded")



def hash_row(row):
    # Replace None with a placeholder ('_NONE_')
    row = ['_NONE_' if x is None else x for x in row]
    # Create a hash object
    hash_obj = hashlib.sha256()
    # Update the hash object with the string representation of the row
    hash_obj.update(str(tuple(row)).encode('utf-8'))
    # Return the hexadecimal digest of the hash
    return hash_obj.hexdigest()




# Initialize connection.
# Uses st.cache_resource to only run once.

@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["mssql_server"]
        + ";DATABASE="
        + st.secrets["mssql_database"]
        + ";Trusted_Connection="
        +  st.secrets["mssql_trusted_conn"]
        + ";UID="
        + st.secrets["mssql_username"]
        + ";PWD="
        + st.secrets["mssql_password"]
    )


# Perform query.
def insert_stage_data_to_db( conn, df, dest_table, truncate=True, clean=True):
    # Generate the SQL insert statement based on the number of columns in the DataFrame
    columns_nr = df.shape[1]  # Get the number of columns
    insert_sql = generate_insert_statement(dest_table, columns_nr)
    
    # Find the last row index where not all values are NaN and slice the data up to this row
    cleaned_df = df.dropna(how='all')
    last_row_index = cleaned_df.index[-1]
    df = df.iloc[:last_row_index + 1]

    # Convert DataFrame to string, replace NaN with 'nan'
    #df = df.fillna('nan').astype(str)
    # Convert NaN values to None before inserting into the database
    df = df.where(pd.notnull(df), None)
    
    # Apply the hash function to each row
    df['row_hash'] = df.apply(hash_row, axis=1)
    
    # Convert columns explicitly to the desired data type, and handle NaN properly
    for column in df.columns:
        if df[column].dtype == float :
            # Convert NaN to None, which is properly understood as SQL NULL
            df[column] = df[column].apply(lambda x: None if pd.isna(x) else float(x))
        elif df[column].dtype == int:
            df[column] = df[column].apply(lambda x: None if pd.isna(x) else int(x))

    # Convert all float64 columns to object
    for column in df.columns:
        if df[column].dtype == 'float64':
            df[column] = df[column].astype('string')
           # Replace pandas' NA with None which is compatible with SQL NULL
            df[column] = df[column].apply(lambda x: None if pd.isna(x) else x)
    # Convert DataFrame to list of tuples, which is what pyodbc expects for executemany
    data_tuples = [tuple(x) for x in df.reset_index().to_numpy()]

    # Execute the SQL insert command
    with conn.cursor() as cur:
        if truncate is True:
             cur.execute(f"TRUNCATE TABLE [{dest_table}_raw]")
        cur.executemany(insert_sql, data_tuples)
        conn.commit()  # Commit the transaction
        cur.execute(f"EXECUTE [{dest_table}_InsertArchProcedure]")
        conn.commit()
        cur.execute(f"EXECUTE [{dest_table}_InsertProcedure]")
        conn.commit()

    return "Data successfully inserted into database."


def insert_config_data_to_db( conn, df, dest_table):
    df = df.astype(str)
    stacked = df.stack()
    #od
    date_valid_from = stacked[stacked.str.contains("OD", case=False)]
    if not date_valid_from.empty:
        date_valid_from_row_index=date_valid_from.index[0][0]
        date_valid_from_column_index=date_valid_from.index[0][1] + 2 # index starts from 1 not 0 and we choose one column next
    else:
        return
    #CENA ALL IN
    cena_all_in = stacked[stacked.str.contains("CENA ALL IN", case=False)]
    # Check if any "CENA ALL IN" found and get the row index
    if not cena_all_in.empty:
        cena_all_in_row_index = cena_all_in.index[0][0]
        cena_all_in_column_index=cena_all_in.index[0][1]+1
        data_start_row_index=cena_all_in_row_index +1
    
        # Search for "KRAJ" in the same row identified above, case-insensitive
        kraj = stacked[(stacked.index.get_level_values(0) == cena_all_in_row_index) & 
                       stacked.str.contains("KRAJ", case=False)]
    
        # Extract the indices if "KRAJ" is found
        if not kraj.empty:
            kraj_row_index = kraj.index[0][0]
            kraj_column_index = kraj.index[0][1]+1
        else:
            st.write("No 'KRAJ' found in the specified row.")
        
        # Search for "WAGA" in the same row identified above, case-insensitive
        waga = stacked[(stacked.index.get_level_values(0) == cena_all_in_row_index) & 
                       (stacked.str.upper() == "WAGA")]
    
        # Extract the indices if "WAGA" is found
        if not waga.empty:
            waga_row_index = waga.index[0][0]
            waga_column_index = waga.index[0][1]+1
        else:
            st.write("No 'WAGA' found in the specified row.")
  

        # Search for "TYP USŁUGI" in the same row identified above, case-insensitive
        typ_uslugi = stacked[(stacked.index.get_level_values(0) == cena_all_in_row_index) & 
                       (stacked.str.upper() == "TYP USŁUGI")]
    
        # Extract the indices if "TYP USŁUGI" is found
        if not typ_uslugi.empty:
            typ_uslugi_row_index = typ_uslugi.index[0][0]
            typ_uslugi_column_index = typ_uslugi.index[0][1]+1
        else:
            st.write("No 'TYP USŁUGI' found in the specified row.")
            

        # Search for "Strefa" in the same row identified above, case-insensitive
        strefa = stacked[(stacked.index.get_level_values(0) == cena_all_in_row_index) & 
                       stacked.str.contains("STREFA", case=False)]
    
        # Extract the indices if "KRAJ" is found
        if not strefa.empty:
            strefa_row_index = strefa.index[0][0]
            strefa_column_index = strefa.index[0][1]+1
        else:
            st.write("No 'STREFA' found in the specified row.")  
            
              
        # Search for "USŁUGA" in the same row identified above, case-insensitive
        usluga = stacked[(stacked.index.get_level_values(0) == cena_all_in_row_index) & 
                       stacked.str.contains("USŁUGA", case=False)]
    
        # Extract the indices if "USŁUGA" is found
        if not usluga.empty:
            usluga_row_index = usluga.index[0][0]
            usluga_column_index = usluga.index[0][1]+1
        else:
            st.write("No 'USŁUGA' found in the specified row.")
    else:
        st.write("No 'CENA ALL IN' found.")
        # raise and return TODO
 
    # overwrite waga column index if empty
    if waga.empty and not usluga.empty:
        waga_column_index = usluga_column_index       
    # overwrite typ uslugi column index if empty
    if typ_uslugi.empty and not strefa.empty:
        typ_uslugi_column_index = strefa_column_index
    else: typ_uslugi_column_index = ""

    
    # Execute the SQL insert command
    with conn.cursor() as cur:
        cur.execute(f"SELECT AutoConfig FROM  [BundleImportConfig] WHERE SheetName = '{dest_table}'")
        results = cur.fetchall()
        if results: 
            if results[0][0] == 0: 
                return
        cur.execute(f"DELETE FROM  [BundleImportConfig] WHERE SheetName = '{dest_table}' AND AutoConfig = 1")
        conn.commit()  # Commit the transaction
        sql_query = """
INSERT INTO [BundleImportConfig] 
    (SheetName, ValidFromColumnName, ValidFromRowIndex, DataStartsRowIndex, CountryColumnName, ServiceTypeColumnName, ServiceColumnName, PriceColumnName)
VALUES
    ('{0}', 'COLUMN_{1:02}', '{2}', '{3}', 'COLUMN_{4:02}', 'COLUMN_{5:02}', 'COLUMN_{6:02}', 'COLUMN_{7:02}');
 
UPDATE [BundleImportConfig] set ServiceTypeColumnName = NULL WHERE ServiceTypeColumnName ='COLUMN_00' OR ServiceTypeColumnName='';
""".format(
    dest_table,
    date_valid_from_column_index,
    date_valid_from_row_index,
    data_start_row_index,
    kraj_column_index,
    typ_uslugi_column_index,            
    waga_column_index,
    cena_all_in_column_index
)  # Apply format here to zero-pad the column indices
        cur.execute(sql_query)           
                    #WHERE NOT EXISTS ( SELECT 1 FROM [BundleImportConfig] SheetName = '{dest_table}' AND AutoConfig = 1)")
        conn.commit()

    return "Data successfully inserted into database."



# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    # Use pandas to read sql query directly into DataFrame
    return pd.read_sql(query, conn)


conn = init_connection()

#dest_table = "dbo.TestBundlePacketa"

#df = run_query("SELECT * from dbo.TestABC;")


columns_nr=64
worksheets= DataLoaders.get_all_sheet_names("TODO")


# Selectbox for choosing an acronym
worksheet_selectbox = st.selectbox(
        "Select worsheet",
        worksheets,
        index=0,  # Default to showing None as the selected value
        format_func=lambda x: "Select worksheet" if x is None else x  # Display text for None value
    )
    
standard_checkbox_disabled = worksheet_selectbox is None



dest_table="Bundle"+worksheet_selectbox
config_table = run_query(f"SELECT * from dbo.[BundleImportConfig] WHERE SheetName = '{dest_table}'")
dest_table = run_query(f"SELECT * from dbo.[{dest_table}] ")



if st.button ("bulid structures",  disabled=standard_checkbox_disabled):
    bulid_raw_structures(conn, dest_table, columns_nr, reset=False)
    
#show google sheet data
with st.expander("Expand google sheet data", expanded= False):
    data = DataLoaders.read_all_data_gsheet(worksheet_selectbox)
    df = pd.DataFrame(data)
    st.write(df)
#show google sheet data
with st.expander("Expand import config", expanded= False):
    data = config_table
    df = pd.DataFrame(data)
    st.table(df)
    # TODO edit function
st.table(dest_table)
#insert_config_data_to_db( conn, df, dest_table)

# Write data to the database
if st.button("insert data", disabled=standard_checkbox_disabled):
    result = insert_stage_data_to_db(conn, df, dest_table)
    st.write(result)
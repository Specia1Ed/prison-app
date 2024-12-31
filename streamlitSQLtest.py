import streamlit as st
import mysql.connector 
import pandas as pd

connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='test2'
)
# Print results.
print('connected')
cursor = connection.cursor()
cursor.execute("SELECT * FROM prisoner")
data= cursor.fetchall()
print(cursor.column_names)
st.title("Streamlit MySQL Cnnection")
df = pd.DataFrame(data,columns=cursor.column_names)
st.dataframe(df)
#print(cursor.fetchall())
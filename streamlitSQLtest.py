import streamlit as st
import mysql.connector 

connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='test2'
)
# Print results.
print('connected')
cursor = connection.cursor()
cursor.execute("Select * from cell")
print(cursor.fetchall())
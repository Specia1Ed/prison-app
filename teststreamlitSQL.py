# streamlit_app.py
from sqlalchemy.sql import text
import streamlit as st
import numpy
# Initialize connection.
#conn = st.connection('mysql', type='sql')
conn = st.connection(
    "sql",
    dialect="mysql",
    host="localhost",
    port = 3306,
    database="test2",
    username="root",
    password="",
)
def query_database(quer,args={}):
    global conn
    with conn.session as session:
        #session.execute("INSERT INTO numbers (val) VALUES (:n);", {"n": n})
        session.execute(quer,args)
        session.commit()
# Perform query.
df = conn.query('SELECT * FROM prisoner;', ttl=600)

# Print results.
print(df.to_numpy()[0][0])
query_database("INSERT INTO employee (name, role) VALUES (?, ?)", ("namesss", "rolesss"))
for row in df.itertuples():
    st.write(f"{row.Name} has a :{row.CellID}:")
import streamlit as st
import pandas as pd
import mysql.connector 
from sqlalchemy.sql import text

#Database connection
@st.cache_resource

def get_connection():
    conn = st.connection(
    "sql",
    dialect="mysql",
    host="localhost",
    port = 3306,
    database="test2",
    username="root",
    password="",
)
    return conn

def query_database(quer):
    conn = get_connection()
    with conn.session as session:
        #session.execute("INSERT INTO numbers (val) VALUES (:n);", {"n": n})
        session.execute(quer)
        session.commit()

def fetch_data(query,dfflag=0,params=()):
    conn = get_connection()
    df=conn.query(query,ttl=600,params=params)
    if dfflag:
        return df
    else:
        return df.to_numpy()

# Login page
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("Prison Management System")
    pin = st.text_input("Enter PIN", type="password")
    if st.button("Login"):
        if pin == "5555":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect PIN")

if not st.session_state.authenticated:
    login()
else:
    # Sidebar navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Dashboard", "Manage Prisoners", "Manage Staff", "Manage Cells", "Reports", "Logout"])

    if menu == "Logout":
        st.session_state.authenticated = False
        st.rerun()

    elif menu == "Dashboard":
        st.title("Dashboard")
        prisoner_count = fetch_data("SELECT COUNT(*) FROM prisoner")[0][0]
        staff_count = fetch_data("SELECT COUNT(*) FROM employee")[0][0]
        available_cells = fetch_data("SELECT COUNT(*) FROM cell ")[0][0]
        st.metric("Total Prisoners", prisoner_count)
        st.metric("Total Staff", staff_count)
        st.metric("Available Cells", available_cells)

    elif menu == "Manage Prisoners":
        st.title("Manage Prisoners")
        prisoners = fetch_data("SELECT * FROM prisoner",1)
        st.dataframe(prisoners)

        with st.expander("Add New Prisoner"):
            name = st.text_input("Name")
            cell = st.number_input("Cell ID", min_value=1)
            id = st.number_input("ID", min_value=1000)
            crime = st.text_input("Crime Commited")
            sentence = st.number_input("Sentence", min_value=1)
            if st.button("Add Prisoner"):
                query_database(text(f"INSERT INTO prisoner (id,name, cellid, CrimeCommited, SentenceDuration) VALUES ('{id}','{name}', '{cell}', '{crime}', '{sentence}')"))
                st.success("Prisoner added successfully!")

    elif menu == "Manage Staff":
        st.title("Manage Staff")
        staff = fetch_data("SELECT * FROM employee",1)
        st.dataframe(staff)

        with st.expander("Add New Staff"):
            name = st.text_input("Name")
            role = st.text_input("Role")
            salary = st.number_input("Salary",min_value=500)
            if st.button("Add Staff"):
                #query_database("INSERT INTO employee (name, role) VALUES (?, ?)", (name, role))
                query_database(text(f"INSERT INTO employee (name,salary,Job_type) VALUES ('{name}','{salary}', '{role}')"))

                st.success("Staff added successfully!")

    elif menu == "Manage Cells":
        st.title("Manage Cells")
        cells = fetch_data("SELECT * FROM cell",1)
        st.dataframe(cells)


    elif menu == "Reports":
        st.title("Reports")
        report_type = st.selectbox("Select Report Type", ["Prisoners", "Staff", "Cells"])
        if report_type == "Prisoners":
            prisoners = fetch_data("SELECT * FROM prisoner",1)
            st.dataframe(prisoners)
        elif report_type == "Staff":
            staff = fetch_data("SELECT * FROM employee",1)
            st.dataframe(staff)
        elif report_type == "Cells":
            cells = fetch_data("SELECT * FROM cell",1)
            st.dataframe(cells)
     

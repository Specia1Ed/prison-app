import streamlit as st
import pandas as pd
import mysql.connector 


#Database connection
@st.cache_resource
def get_connection():
    connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='test2'
    )
    return connection

def query_database(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    return cursor

def fetch_data(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()

# Login page
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("Prison Management System")
    pin = st.text_input("Enter PIN", type="password")
    if st.button("Login"):
        if pin == "5555":
            st.session_state.authenticated = True
            st.experimental_rerun()
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
        #st.experimental_rerun()

    elif menu == "Dashboard":
        st.title("Dashboard")
        prisoner_count = fetch_data("SELECT COUNT(*) FROM prisoners")[0][0]
        staff_count = fetch_data("SELECT COUNT(*) FROM staff")[0][0]
        available_cells = fetch_data("SELECT COUNT(*) FROM cells WHERE occupancy < capacity")[0][0]
        st.metric("Total Prisoners", prisoner_count)
        st.metric("Total Staff", staff_count)
        st.metric("Available Cells", available_cells)

    elif menu == "Manage Prisoners":
        st.title("Manage Prisoners")
        prisoners = pd.DataFrame(fetch_data("SELECT * FROM prisoners"), columns=["ID", "Name", "Cell", "Crime", "Sentence"])
        st.dataframe(prisoners)

        with st.expander("Add New Prisoner"):
            name = st.text_input("Name")
            cell = st.number_input("Cell", min_value=1)
            crime = st.text_input("Crime")
            sentence = st.text_input("Sentence")
            if st.button("Add Prisoner"):
                query_database("INSERT INTO prisoners (name, cell, crime, sentence) VALUES (?, ?, ?, ?)", (name, cell, crime, sentence))
                st.success("Prisoner added successfully!")

    elif menu == "Manage Staff":
        st.title("Manage Staff")
        staff = pd.DataFrame(fetch_data("SELECT * FROM staff"), columns=["ID", "Name", "Role"])
        st.dataframe(staff)

        with st.expander("Add New Staff"):
            name = st.text_input("Name")
            role = st.text_input("Role")
            if st.button("Add Staff"):
                query_database("INSERT INTO staff (name, role) VALUES (?, ?)", (name, role))
                st.success("Staff added successfully!")

    elif menu == "Manage Cells":
        st.title("Manage Cells")
        cells = pd.DataFrame(fetch_data("SELECT * FROM cells"), columns=["ID", "Occupancy", "Capacity"])
        st.dataframe(cells)


    elif menu == "Reports":
        st.title("Reports")
        report_type = st.selectbox("Select Report Type", ["Prisoners", "Staff", "Cells", "Guns"])
        if report_type == "Prisoners":
            prisoners = pd.DataFrame(fetch_data("SELECT * FROM prisoners"), columns=["ID", "Name", "Cell", "Crime", "Sentence"])
            st.dataframe(prisoners)
        elif report_type == "Staff":
            staff = pd.DataFrame(fetch_data("SELECT * FROM staff"), columns=["ID", "Name", "Role"])
            st.dataframe(staff)
        elif report_type == "Cells":
            cells = pd.DataFrame(fetch_data("SELECT * FROM cells"), columns=["ID", "Occupancy", "Capacity"])
            st.dataframe(cells)
     

import streamlit as st
import pandas as pd

# Placeholder DataFrames for demonstration
prisoners_data = pd.DataFrame({
    "Prisoner ID": [101, 102],
    "Name": ["John Doe", "Jane Smith"],
    "Cell": [12, 14],
    "Crime": ["Theft", "Fraud"],
    "Sentence": ["2 years", "3 years"]
})

staff_data = pd.DataFrame({
    "Staff ID": [1, 2],
    "Name": ["Officer Brown", "Officer Green"],
    "Role": ["Warden", "Guard"]
})

cells_data = pd.DataFrame({
    "Cell ID": [12, 14, 16],
    "Occupancy": [1, 1, 0],
    "Capacity": [2, 2, 2]
})

# Sidebar navigation
st.sidebar.title("Prison Management System")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Manage Prisoners", "Manage Staff", "Manage Cells", "Reports"])

if menu == "Dashboard":
    st.title("Dashboard")
    st.write("### Overview")
    st.metric("Total Prisoners", len(prisoners_data))
    st.metric("Total Staff", len(staff_data))
    st.metric("Available Cells", len(cells_data[cells_data["Occupancy"] < cells_data["Capacity"]]))

elif menu == "Manage Prisoners":
    st.title("Manage Prisoners")
    st.write("### Prisoner Records")
    st.dataframe(prisoners_data)

    with st.expander("Add New Prisoner"):
        prisoner_id = st.text_input("Prisoner ID")
        name = st.text_input("Name")
        cell = st.number_input("Cell", min_value=1)
        crime = st.text_input("Crime")
        sentence = st.text_input("Sentence")
        if st.button("Add Prisoner"):
            st.success(f"Prisoner {name} added successfully!")

elif menu == "Manage Employees":
    st.title("Manage Employees")
    st.write("### Employees Records")
    st.dataframe(staff_data)

    with st.expander("Add New Employees"):
        staff_id = st.text_input("Employees ID")
        name = st.text_input("Name")
        role = st.text_input("Role")
        if st.button("Add Staff"):
            st.success(f"Staff {name} added successfully!")

elif menu == "Manage Cells":
    st.title("Manage Cells")
    st.write("### Cell Records")
    st.dataframe(cells_data)

elif menu == "Reports":
    st.title("Reports")
    st.write("### Generate Reports")
    report_type = st.selectbox("Select Report Type", ["Prisoners", "Staff", "Cells"])
    if report_type == "Prisoners":
        st.write("### Prisoner Report")
        st.dataframe(prisoners_data)
    elif report_type == "Staff":
        st.write("### Staff Report")
        st.dataframe(staff_data)
    elif report_type == "Cells":
        st.write("### Cell Report")
        st.dataframe(cells_data)

import streamlit as st
import pandas as pd

# Initialize session state
if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=["ID", "Name", "Age", "Gender"])

if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(columns=["Patient ID", "Patient Name", "Doctor", "Date"])

st.title("🏥 Hospital Appointment Management System")

menu = st.sidebar.selectbox("Menu", ["Add Patient", "View Patients", "Book Appointment", "View Appointments"])

# Add Patient
if menu == "Add Patient":
    st.header("Add Patient")
    
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    if st.button("Add"):
        new_id = len(st.session_state.patients) + 1
        
        new_patient = pd.DataFrame([[new_id, name, age, gender]],
                                   columns=["ID", "Name", "Age", "Gender"])
        
        st.session_state.patients = pd.concat([st.session_state.patients, new_patient], ignore_index=True)
        st.success("Patient added successfully!")

# View Patients
elif menu == "View Patients":
    st.header("Patient List")
    st.dataframe(st.session_state.patients)

# Book Appointment
elif menu == "Book Appointment":
    st.header("Book Appointment")
    
    if st.session_state.patients.empty:
        st.warning("Add patients first!")
    else:
        patient_names = st.session_state.patients["Name"].tolist()
        selected_name = st.selectbox("Select Patient", patient_names)
        
        doctor = st.text_input("Doctor Name")
        date = st.date_input("Appointment Date")
        
        if st.button("Book"):
            patient_row = st.session_state.patients[
                st.session_state.patients["Name"] == selected_name
            ].iloc[0]
            
            new_appointment = pd.DataFrame([[
                patient_row["ID"], selected_name, doctor, date
            ]], columns=["Patient ID", "Patient Name", "Doctor", "Date"])
            
            st.session_state.appointments = pd.concat(
                [st.session_state.appointments, new_appointment],
                ignore_index=True
            )
            
            st.success("Appointment booked successfully!")

# View Appointments
elif menu == "View Appointments":
    st.header("Appointments")
    st.dataframe(st.session_state.appointments)

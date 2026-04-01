import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Hospital System", layout="wide")

# Custom CSS (Frontend styling)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=["ID", "Name", "Age", "Gender"])

if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(columns=["Patient ID", "Patient Name", "Doctor", "Date"])

# Sidebar
st.sidebar.title("🏥 Hospital System")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Add Patient", "Patients", "Book Appointment", "Appointments"])

# Dashboard
if menu == "Dashboard":
    st.title("📊 Dashboard")
    
    col1, col2 = st.columns(2)
    
    col1.markdown(f"""
        <div class="card">
            <h3>Total Patients</h3>
            <h1>{len(st.session_state.patients)}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    col2.markdown(f"""
        <div class="card">
            <h3>Total Appointments</h3>
            <h1>{len(st.session_state.appointments)}</h1>
        </div>
    """, unsafe_allow_html=True)

# Add Patient
elif menu == "Add Patient":
    st.title("➕ Add Patient")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=0)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        if st.button("Add Patient"):
            new_id = len(st.session_state.patients) + 1
            
            new_patient = pd.DataFrame([[new_id, name, age, gender]],
                                       columns=["ID", "Name", "Age", "Gender"])
            
            st.session_state.patients = pd.concat(
                [st.session_state.patients, new_patient],
                ignore_index=True
            )
            
            st.success("✅ Patient added successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# View Patients
elif menu == "Patients":
    st.title("👨‍⚕️ Patient List")
    st.dataframe(st.session_state.patients, use_container_width=True)

# Book Appointment
elif menu == "Book Appointment":
    st.title("📅 Book Appointment")
    
    if st.session_state.patients.empty:
        st.warning("⚠️ Add patients first!")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        patient_names = st.session_state.patients["Name"].tolist()
        selected_name = st.selectbox("Select Patient", patient_names)
        
        doctor = st.text_input("Doctor Name")
        date = st.date_input("Appointment Date")
        
        if st.button("Book Appointment"):
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
            
            st.success("✅ Appointment booked!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# View Appointments
elif menu == "Appointments":
    st.title("📋 Appointments")
    st.dataframe(st.session_state.appointments, use_container_width=True)

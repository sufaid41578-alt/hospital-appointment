import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Hospital System", layout="wide")

# ---------------- STYLING ----------------
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- DUMMY USERS ----------------
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "doctor": {"password": "doc123", "role": "Doctor"},
    "patient": {"password": "pat123", "role": "Patient"}
}

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=["ID", "Name", "Age", "Gender"])

if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(
        columns=["Patient ID", "Patient Name", "Doctor", "Date"]
    )

# ---------------- LOGIN FUNCTION ----------------
def login():
    st.title("🔐 Hospital Login")

    role = st.selectbox("Login as", ["Admin", "Doctor", "Patient"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            if users[username]["role"] == role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Role mismatch!")
        else:
            st.error("Invalid credentials!")

# ---------------- LOGIN CHECK ----------------
if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏥 Hospital System")
st.sidebar.write(f"👤 Logged in as: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

# ---------------- ROLE-BASED MENU ----------------
if st.session_state.role == "Admin":
    menu = st.sidebar.radio("Menu", ["Dashboard", "Add Patient", "Patients", "Appointments"])

elif st.session_state.role == "Doctor":
    menu = st.sidebar.radio("Menu", ["Appointments"])

elif st.session_state.role == "Patient":
    menu = st.sidebar.radio("Menu", ["Book Appointment"])

# ---------------- DASHBOARD (ADMIN) ----------------
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

# ---------------- ADD PATIENT (ADMIN) ----------------
elif menu == "Add Patient":
    st.title("➕ Add Patient")

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

# ---------------- VIEW PATIENTS (ADMIN) ----------------
elif menu == "Patients":
    st.title("👨‍⚕️ Patient List")
    st.dataframe(st.session_state.patients, use_container_width=True)

# ---------------- BOOK APPOINTMENT (PATIENT) ----------------
elif menu == "Book Appointment":
    st.title("📅 Book Appointment")

    if st.session_state.patients.empty:
        st.warning("⚠️ No patients available!")
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

# ---------------- VIEW APPOINTMENTS (ALL ROLES) ----------------
elif menu == "Appointments":
    st.title("📋 Appointments")
    st.dataframe(st.session_state.appointments, use_container_width=True)

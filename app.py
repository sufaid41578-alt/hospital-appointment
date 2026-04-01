import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hospital System", layout="wide")

# ---------------- STYLING ----------------
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# ---------------- USERS ----------------
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "admin123", "role": "Admin"}
    }

# ---------------- DATA ----------------
if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=["ID", "Name", "Age", "Gender"])

if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(
        columns=["Patient ID", "Patient Name", "Doctor", "Date"]
    )

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

def login():
    st.title("🔐 Hospital Login")

    role = st.selectbox("Login as", ["Admin", "Doctor"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users:
            user = st.session_state.users[username]
            if user["password"] == password and user["role"] == role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials!")
        else:
            st.error("User not found!")

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏥 Hospital System")
st.sidebar.write(f"👤 {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- ROLE MENU ----------------
if st.session_state.role == "Admin":
    menu = st.sidebar.radio("Menu", [
        "Dashboard", "Add Patient", "Patients",
        "Appointments", "Add Doctor"
    ])

elif st.session_state.role == "Doctor":
    menu = st.sidebar.radio("Menu", ["Appointments"])

# ---------------- DASHBOARD ----------------
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

# ---------------- ADD PATIENT ----------------
elif menu == "Add Patient":
    st.title("➕ Add Patient")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    if st.button("Add"):
        new_id = len(st.session_state.patients) + 1
        new_patient = pd.DataFrame([[new_id, name, age, gender]],
                                  columns=["ID", "Name", "Age", "Gender"])
        st.session_state.patients = pd.concat(
            [st.session_state.patients, new_patient], ignore_index=True)
        st.success("Patient added!")

# ---------------- VIEW & DELETE PATIENT ----------------
elif menu == "Patients":
    st.title("👨‍⚕️ Patients")

    if not st.session_state.patients.empty:
        st.dataframe(st.session_state.patients)

        patient_ids = st.session_state.patients["ID"].tolist()
        delete_id = st.selectbox("Select Patient ID to Delete", patient_ids)

        if st.button("Delete Patient"):
            st.session_state.patients = st.session_state.patients[
                st.session_state.patients["ID"] != delete_id
            ]
            st.success("Patient deleted!")
    else:
        st.warning("No patients available")

# ---------------- APPOINTMENTS ----------------
elif menu == "Appointments":
    st.title("📋 Appointments")

    if not st.session_state.appointments.empty:
        st.dataframe(st.session_state.appointments)

        # Admin delete option
        if st.session_state.role == "Admin":
            index = st.selectbox("Select Appointment Index to Delete",
                                 st.session_state.appointments.index)

            if st.button("Delete Appointment"):
                st.session_state.appointments = st.session_state.appointments.drop(index)
                st.success("Appointment deleted!")
    else:
        st.warning("No appointments")

# ---------------- ADD DOCTOR ----------------
elif menu == "Add Doctor":
    st.title("➕ Add Doctor")

    username = st.text_input("Doctor Username")
    password = st.text_input("Doctor Password", type="password")

    if st.button("Add Doctor"):
        if username in st.session_state.users:
            st.error("Username already exists!")
        else:
            st.session_state.users[username] = {
                "password": password,
                "role": "Doctor"
            }
            st.success("Doctor added successfully!")

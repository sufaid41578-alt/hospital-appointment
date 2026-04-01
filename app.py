import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hospital System", layout="wide")

# ---------------- USERS ----------------
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "admin123", "role": "Admin"}
    }

# ---------------- DATA ----------------
if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=["ID", "Name", "Age", "Gender", "Username"])

if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(
        columns=["Patient Username", "Patient Name", "Doctor", "Date"]
    )

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

# ---------------- LOGIN / SIGNUP ----------------
def auth_page():
    st.title("🔐 Hospital Login System")

    role = st.selectbox("Select Role", ["Admin", "Doctor", "Patient"])
    action = st.radio("Action", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # -------- LOGIN --------
    if action == "Login":
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

    # -------- SIGNUP (PATIENT ONLY) --------
    elif action == "Sign Up":
        if role != "Patient":
            st.warning("Only patients can sign up!")
        else:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=0)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

            if st.button("Create Account"):
                if username in st.session_state.users:
                    st.error("Username already exists!")
                else:
                    # Add to users
                    st.session_state.users[username] = {
                        "password": password,
                        "role": "Patient"
                    }

                    # Add to patients table
                    new_id = len(st.session_state.patients) + 1
                    new_patient = pd.DataFrame([[
                        new_id, name, age, gender, username
                    ]], columns=["ID", "Name", "Age", "Gender", "Username"])

                    st.session_state.patients = pd.concat(
                        [st.session_state.patients, new_patient],
                        ignore_index=True
                    )

                    st.success("Account created! Please login.")

# ---------------- CHECK LOGIN ----------------
if not st.session_state.logged_in:
    auth_page()
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏥 Hospital System")
st.sidebar.write(f"👤 {st.session_state.role} ({st.session_state.username})")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- ROLE MENU ----------------
if st.session_state.role == "Admin":
    menu = st.sidebar.radio("Menu", [
        "Dashboard", "Patients", "Appointments", "Add Doctor"
    ])

elif st.session_state.role == "Doctor":
    menu = st.sidebar.radio("Menu", ["Appointments"])

elif st.session_state.role == "Patient":
    menu = st.sidebar.radio("Menu", ["Book Appointment", "My Appointments"])

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.title("📊 Dashboard")

    col1, col2 = st.columns(2)

    col1.metric("Total Patients", len(st.session_state.patients))
    col2.metric("Total Appointments", len(st.session_state.appointments))

# ---------------- PATIENTS (ADMIN) ----------------
elif menu == "Patients":
    st.title("👨‍⚕️ Patients")

    st.dataframe(st.session_state.patients)

    if not st.session_state.patients.empty:
        delete_id = st.selectbox("Delete Patient ID", st.session_state.patients["ID"])
        if st.button("Delete Patient"):
            st.session_state.patients = st.session_state.patients[
                st.session_state.patients["ID"] != delete_id
            ]
            st.success("Deleted!")

# ---------------- APPOINTMENTS ----------------
elif menu == "Appointments":
    st.title("📋 Appointments")

    st.dataframe(st.session_state.appointments)

    if st.session_state.role == "Admin" and not st.session_state.appointments.empty:
        index = st.selectbox("Delete Appointment", st.session_state.appointments.index)
        if st.button("Delete Appointment"):
            st.session_state.appointments = st.session_state.appointments.drop(index)
            st.success("Deleted!")

# ---------------- ADD DOCTOR ----------------
elif menu == "Add Doctor":
    st.title("➕ Add Doctor")

    username = st.text_input("Doctor Username")
    password = st.text_input("Password", type="password")

    if st.button("Add Doctor"):
        if username in st.session_state.users:
            st.error("Username exists!")
        else:
            st.session_state.users[username] = {
                "password": password,
                "role": "Doctor"
            }
            st.success("Doctor added!")

# ---------------- BOOK APPOINTMENT (PATIENT) ----------------
elif menu == "Book Appointment":
    st.title("📅 Book Appointment")

    doctor = st.text_input("Doctor Name")
    date = st.date_input("Date")

    if st.button("Book"):
        patient_row = st.session_state.patients[
            st.session_state.patients["Username"] == st.session_state.username
        ].iloc[0]

        new_appointment = pd.DataFrame([[
            st.session_state.username,
            patient_row["Name"],
            doctor,
            date
        ]], columns=["Patient Username", "Patient Name", "Doctor", "Date"])

        st.session_state.appointments = pd.concat(
            [st.session_state.appointments, new_appointment],
            ignore_index=True
        )

        st.success("Appointment booked!")

# ---------------- MY APPOINTMENTS ----------------
elif menu == "My Appointments":
    st.title("📋 My Appointments")

    user_apps = st.session_state.appointments[
        st.session_state.appointments["Patient Username"] == st.session_state.username
    ]

    st.dataframe(user_apps)

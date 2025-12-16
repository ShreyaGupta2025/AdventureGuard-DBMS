import streamlit as st
import pandas as pd
import mysql.connector
import datetime
import config

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(page_title="Add Data", page_icon="➕", layout="wide")

# ------------------------------------------------------
# DB CONNECTION
# ------------------------------------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            port=config.DB_PORT
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        return None

conn = get_db_connection()
if not conn:
    st.stop()


# Helper functions
def execute_query(sql, params=None):
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        return True
    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
        return False


def get_table(sql):
    return pd.read_sql(sql, conn)


# ======================================================
# PAGE TITLE
# ======================================================
st.title("➕ Add Data")
st.caption("Use this panel to insert Participants, Activities, Instructors, Injuries, Equipment, and Maintenance Logs.")
st.write("---")


# ======================================================
# FORM 1 — Add Participant
# ======================================================
st.header("🧍 Add Participant")
with st.form("add_participant_form"):
    p_name = st.text_input("Full Name")
    p_dob = st.date_input("Date of Birth")
    p_contact = st.text_input("Contact Number (10 digits)")
    p_emg_name = st.text_input("Emergency Contact Name")
    p_emg_contact = st.text_input("Emergency Contact Number (10 digits)")

    submitted = st.form_submit_button("Add Participant")

    if submitted:
        if len(p_contact) != 10 or len(p_emg_contact) != 10:
            st.error("❌ Contact numbers must be 10 digits.")
        else:
            success = execute_query("""
                INSERT INTO Participant (Name, DOB, ContactNumber, EmergencyContactName, EmergencyContactNumber)
                VALUES (%s, %s, %s, %s, %s)
            """, (p_name, p_dob, p_contact, p_emg_name, p_emg_contact))

            if success:
                st.success("✅ Participant added successfully!")

st.write("---")


# ======================================================
# FORM 2 — Add Instructor
# ======================================================
st.header("🧑‍🏫 Add Instructor")
with st.form("add_instructor_form"):
    i_name = st.text_input("Instructor Name")
    i_contact = st.text_input("Contact Number (10 digits)")
    i_exp = st.number_input("Experience (years)", min_value=0, max_value=50)
    i_expertise = st.text_area("Expertise (comma-separated)")

    submitted = st.form_submit_button("Add Instructor")

    if submitted:
        if len(i_contact) != 10:
            st.error("❌ Contact number must be 10 digits.")
        else:
            success = execute_query("""
                INSERT INTO Instructor (Name, ContactNumber, ExperienceYears, Expertise)
                VALUES (%s, %s, %s, %s)
            """, (i_name, i_contact, i_exp, i_expertise))

            if success:
                st.success("✅ Instructor added successfully!")

st.write("---")


# ======================================================
# FORM 3 — Add Activity
# ======================================================
st.header("🧗 Add Activity")

instructors = get_table("SELECT InstructorID, Name FROM Instructor")

with st.form("add_activity_form"):
    a_name = st.text_input("Activity Name")
    a_type = st.text_input("Activity Type")

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date")
        start_time = st.time_input("Start Time")

    with col2:
        end_date = st.date_input("End Date")
        end_time = st.time_input("End Time")

    # Combine to datetime
    a_start = datetime.datetime.combine(start_date, start_time)
    a_end = datetime.datetime.combine(end_date, end_time)

    a_fees = st.number_input("Fees (₹)", min_value=0.0)
    a_inst = st.selectbox("Assign Instructor", instructors["Name"])

    submitted = st.form_submit_button("Add Activity")

    if submitted:
        inst_id = int(instructors[instructors["Name"] == a_inst]["InstructorID"].values[0])

        success = execute_query("""
            INSERT INTO Activity (ActivityName, ActivityType, StartDate, EndDate, Fees, InstructorID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (a_name, a_type, a_start, a_end, a_fees, inst_id))

        if success:
            st.success("✅ Activity added successfully!")

st.write("---")


# ======================================================
# FORM 4 — Add Equipment
# ======================================================
st.header("🛠 Add Equipment")

equipment_list = get_table("SELECT EquipmentID, EquipmentType FROM Equipment")

with st.form("add_equipment_form"):
    e_type = st.text_input("Equipment Type")
    e_status = st.selectbox("Status", ["Working", "Under Maintenance", "Broken"])
    e_warranty = st.date_input("Warranty Expiry")

    e_depends = st.selectbox(
        "Depends on Equipment (optional)",
        ["None"] + equipment_list["EquipmentType"].tolist()
    )

    submitted = st.form_submit_button("Add Equipment")

    if submitted:
        dep_id = None
        if e_depends != "None":
            dep_id = int(equipment_list[equipment_list["EquipmentType"] == e_depends]["EquipmentID"].values[0])

        success = execute_query("""
            INSERT INTO Equipment (EquipmentType, Status, WarrantyExpiry, DependsOnEquipmentID)
            VALUES (%s, %s, %s, %s)
        """, (e_type, e_status, e_warranty, dep_id))

        if success:
            st.success("✅ Equipment added successfully!")

st.write("---")


# ======================================================
# FORM 5 — Add Maintenance Log
# ======================================================
st.header("🛠 Add Maintenance Log")

equipment_list = get_table("SELECT EquipmentID, EquipmentType FROM Equipment")

with st.form("add_maintenance_form"):
    m_eq = st.selectbox("Equipment", equipment_list["EquipmentType"])
    m_date = st.date_input("Maintenance Date")
    m_desc = st.text_area("Description")
    m_tech = st.text_input("Technician Name")
    m_cost = st.number_input("Cost (₹)", min_value=0.0)

    submitted = st.form_submit_button("Add Maintenance Log")

    if submitted:
        eq_id = int(equipment_list[equipment_list["EquipmentType"] == m_eq]["EquipmentID"].values[0])

        success = execute_query("""
            INSERT INTO MaintenanceLog (EquipmentID, MaintDate, Description, Technician, Cost)
            VALUES (%s, %s, %s, %s, %s)
        """, (eq_id, m_date, m_desc, m_tech, m_cost))

        if success:
            st.success("✅ Maintenance log added successfully! Trigger will update equipment status.")

st.write("---")


# ======================================================
# FORM 6 — Add Injury
# ======================================================
st.header("🩹 Add Injury")

participants = get_table("SELECT ParticipantID, Name FROM Participant")
activities = get_table("SELECT ActivityID, ActivityName FROM Activity")

with st.form("add_injury_form"):
    p_select = st.selectbox("Participant", participants["Name"])
    a_select = st.selectbox("Activity", activities["ActivityName"])

    injury_name = st.text_input("Injury Name")
    injury_date = st.date_input("Injury Date")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    treatment = st.text_input("Treatment")

    submitted = st.form_submit_button("Add Injury")

    if submitted:
        pid = int(participants[participants["Name"] == p_select]["ParticipantID"].values[0])
        aid = int(activities[activities["ActivityName"] == a_select]["ActivityID"].values[0])

        success = execute_query("""
            INSERT INTO Injury (ParticipantID, ActivityID, InjuryName, InjuryDate, Severity, Treatment)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (pid, aid, injury_name, injury_date, severity, treatment))

        if success:
            st.success("✅ Injury added successfully! (Triggers validated the entry)")

st.write("---")
st.success("All forms loaded successfully. Add your data now!")

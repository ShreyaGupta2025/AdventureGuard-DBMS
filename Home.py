import streamlit as st
import pandas as pd
import mysql.connector
import config

# ===========================================
# MUST BE FIRST STREAMLIT COMMAND
# ===========================================
st.set_page_config(
    page_title="AdventureGuard",
    page_icon="🎽",
    layout="wide"
)

# ===========================================
# DARK MODE + SIDEBAR CSS
# ===========================================
dark_mode_css = """
<style>

    .stApp {
        background-color: #0E1117 !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #111418 !important;
        padding-top: 10px !important;
        padding-left: 18px !important;
        padding-right: 12px !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] div {
        margin-bottom: 6px !important;
        line-height: 1.35 !important;
        font-size: 0.95rem !important;
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        margin-top: 12px !important;
        margin-bottom: 6px !important;
        color: white !important;
    }

</style>
"""
st.markdown(dark_mode_css, unsafe_allow_html=True)


# ===========================================
# 🎨 SIDEBAR (AeroSwift Style)
# ===========================================
st.sidebar.markdown(
    """
    <div style='text-align: center; margin-bottom: 10px;'>
        <h2>🎽 <span style="color:#00B4D8;">AdventureGuard</span></h2>
        <p style='font-size:14px; color:#bbbbbb; margin-top:-10px;'>
            Safe • Managed • Adventure-Ready
        </p>
        <hr style='margin:10px 0;'>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar sections
st.sidebar.header("📦 Operations")
st.sidebar.markdown("""
- 🏠 Home  
- 🎽 Dashboard  
- 🧍 Participants  
- 🧑‍🏫 Instructors  
- 🧗 Activities  
""")

st.sidebar.header("📊 Data & Reports")
st.sidebar.markdown("""
- 🩹 Injuries  
- 🛠 Maintenance Logs  
- ⭐ Ratings  
- 📈 Analytics & Reports  
""")

st.sidebar.header("ℹ️ About")
st.sidebar.markdown("""
- 📘 Project Overview  
""")

st.sidebar.markdown("---")
st.sidebar.caption("Developed by **Shreya Gupta** | BITS Pilani Hyderabad Campus")



# ===========================================
# DATABASE CONNECTION (YOUR VERSION)
# ===========================================
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




# Helper to get values
def get_value(sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        cur.close()
        return row[0] if row else 0
    except:
        return 0



# ===========================================
# PAGE TITLE
# ===========================================
st.title("🎽 AdventureGuard – Adventure Sports Safety & Management System")
st.caption("A Data-Driven Adventure Sports DBMS Project")
st.write("---")



# ===========================================
# 🌍 MINI-WORLD SCENARIO
# ===========================================
st.header("🌍 Mini-World Scenario")

st.markdown("""
AdventureGuard supports an organization that runs adventure sports such as rock climbing,
kayaking, yoga, and swimming. It manages participants, their emergency contacts, and the instructors
who conduct each session. Participants can join multiple activities and provide ratings to instructors,
ensuring continuous improvement and safety.

Behind the scenes, AdventureGuard tracks equipment such as ropes, harnesses, kayaks, and paddles —
including maintenance history and dependencies. Injuries are recorded with severity and treatment,
helping improve safety measures over time. With structured data, triggers, and automated rules, 
AdventureGuard keeps every adventure thrilling, safe, and well-managed.
""")

st.write("---")



# ===========================================
# ⚙️ SYSTEM OVERVIEW
# ===========================================
st.header("⚙️ System Overview")

st.markdown("""
- **Participant Management** — Emergency contacts, age, activity registrations  
- **Instructor Management** — expertise, ratings, experience  
- **Activity Scheduling** — timings, fees, instructors, participant count  
- **Equipment Tracking** — status, maintenance logs, dependencies  
- **Injury Logging** — severity, treatment, activity linkage  
- **Maintenance System** — technician logs, repair costs, automatic status update  
""")

st.write("---")



# ===========================================
# 🔄 AUTOMATED WORKFLOW
# ===========================================
st.header("🔄 Automated Workflow")

st.markdown("""
- 🧍 **Registration** — participants register with emergency details  
- 📅 **Activity Enrollment** — participant counts update via triggers  
- 🛠 **Maintenance Logs** — automatically update equipment status  
- 🩹 **Injury Logging** — verified by triggers for date + severity  
- ⭐ **Instructor Ratings** — averages calculated using SQL functions  
- 📊 **Safety Insights** — injury + maintenance analysis guides improvements  
""")

st.write("---")



# ===========================================
# 📊 SYSTEM PERFORMANCE SNAPSHOT
# ===========================================
st.header("📊 System Performance Snapshot")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Participants", get_value("SELECT COUNT(*) FROM Participant"))
col2.metric("Activities", get_value("SELECT COUNT(*) FROM Activity"))
col3.metric("Instructors", get_value("SELECT COUNT(*) FROM Instructor"))
col4.metric("Equipment Items", get_value("SELECT COUNT(*) FROM Equipment"))
col5.metric("Injuries Logged", get_value("SELECT COUNT(*) FROM Injury"))

st.caption("(Counts live from MySQL — growth numbers hidden for accuracy.)")

st.write("---")

st.success("Use the sidebar to explore Database Tables, Dashboard, Backend Implementation, and Project Overview.")

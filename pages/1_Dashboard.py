import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import config

# =========================================================
# PAGE SETTINGS
# =========================================================
st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

# =========================================================
# DB CONNECTION FUNCTION (your version)
# =========================================================
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


# Open connection once
conn = get_db_connection()



# =========================================================
# HELPER FUNCTION (safe value getter)
# =========================================================
def get_value(query):
    try:
        df = pd.read_sql(query, conn)
        return df.iloc[0, 0]
    except:
        return 0


# =========================================================
# TITLE
# =========================================================
st.title("🏠 AdventureGuard Dashboard")
st.write("A Live Snapshot of Adventure Sports, Safety & Operations")
st.markdown("---")


# =========================================================
# SUMMARY METRICS
# =========================================================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🧍 Participants", get_value("SELECT COUNT(*) FROM Participant"))
col2.metric("🧗 Activities", get_value("SELECT COUNT(*) FROM Activity"))
col3.metric("🧑‍🏫 Instructors", get_value("SELECT COUNT(*) FROM Instructor"))
col4.metric("🩹 Injuries Logged", get_value("SELECT COUNT(*) FROM Injury"))
col5.metric("🛠 Equipment Items", get_value("SELECT COUNT(*) FROM Equipment"))

st.markdown("<hr>", unsafe_allow_html=True)


# =========================================================
# INJURY SEVERITY CHART
# =========================================================
st.subheader("📊 Injury Severity Overview")

inj_df = pd.read_sql(
    "SELECT Severity, COUNT(*) AS Count FROM Injury GROUP BY Severity",
    conn
)

if not inj_df.empty:
    fig = px.bar(
        inj_df,
        x="Severity",
        y="Count",
        color="Severity",
        template="plotly_dark",
        title="Injury Distribution by Severity",
        text="Count"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No injuries recorded yet.")

st.markdown("---")


# =========================================================
# EQUIPMENT STATUS CHART
# =========================================================
st.subheader("🔧 Equipment Status Distribution")

eq_df = pd.read_sql(
    "SELECT Status, COUNT(*) AS Count FROM Equipment GROUP BY Status",
    conn
)

if not eq_df.empty:
    fig = px.pie(
        eq_df,
        names="Status",
        values="Count",
        title="Equipment Condition Overview",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No equipment available to display.")

st.markdown("---")


# =========================================================
# PARTICIPANTS PER ACTIVITY
# =========================================================
st.subheader("🧍 Participants per Activity")

act_df = pd.read_sql("""
    SELECT a.ActivityName, COUNT(r.ParticipantID) AS ParticipantCount
    FROM Activity a
    LEFT JOIN Registers r ON a.ActivityID = r.ActivityID
    GROUP BY a.ActivityID, a.ActivityName;
""", conn)

if not act_df.empty:
    fig = px.bar(
        act_df,
        x="ActivityName",
        y="ParticipantCount",
        template="plotly_dark",
        title="Participant Distribution Across Activities",
        text="ParticipantCount"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No participants registered yet.")

st.markdown("---")


# =========================================================
# RECENT INSIGHTS: INJURIES & MAINTENANCE
# =========================================================
st.subheader("📅 Recent Activity & Safety Insights")

colA, colB = st.columns(2)

# Recent Injuries
with colA:
    st.markdown("### 🩹 Latest Injuries")
    inj_recent = pd.read_sql("""
        SELECT ParticipantID, ActivityID, InjuryName, Severity, InjuryDate
        FROM Injury
        ORDER BY InjuryDate DESC
        LIMIT 5;
    """, conn)
    st.dataframe(inj_recent, use_container_width=True)

# Recent Maintenance Logs
with colB:
    st.markdown("### 🛠 Recent Maintenance Logs")
    maint_recent = pd.read_sql("""
        SELECT EquipmentID, MaintDate, Technician, Cost
        FROM MaintenanceLog
        ORDER BY MaintDate DESC
        LIMIT 5;
    """, conn)
    st.dataframe(maint_recent, use_container_width=True)

st.markdown("---")
st.success("Dashboard loaded successfully!")


import streamlit as st
import pandas as pd
import mysql.connector
import config

# --------------------------------------------
# PAGE CONFIG
# --------------------------------------------
st.set_page_config(page_title="Complex SQL Queries", page_icon="🧠", layout="wide")

st.title("🧠 Complex SQL Queries (Advanced Reports)")
st.caption("This page demonstrates complex SQL operations such as nested queries, aggregation, grouping, and multi-table joins.")

st.write("---")

# --------------------------------------------
# DB CONNECTION
# --------------------------------------------
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
    except:
        st.error("Database connection failed.")
        return None

conn = get_db_connection()
if not conn:
    st.stop()

def run_query(sql):
    try:
        df = pd.read_sql(sql, conn)
        return df
    except Exception as e:
        st.error(f"Query Error: {e}")
        return None


# ================================================
# QUERY 1 — Top Activities by Paid Participants
# ================================================
with st.expander("📌 Query 1: Top Activities by Paid Participants (GROUP BY + HAVING)"):
    st.write("This query lists activities with more than **2 paid participants**, using grouping + filtering.")

    query1 = """
    SELECT a.ActivityName, COUNT(r.ParticipantID) AS PaidCount
    FROM Activity a
    JOIN Registers r ON a.ActivityID = r.ActivityID
    WHERE r.PaymentStatus = 'Yes'
    GROUP BY a.ActivityName
    HAVING COUNT(r.ParticipantID) > 2
    ORDER BY PaidCount DESC;
    """

    st.code(query1, language="sql")

    if st.button("Run Query 1"):
        df = run_query(query1)
        if df is not None:
            st.dataframe(df, use_container_width=True)


# ================================================
# QUERY 2 — Most Injury-Prone Participants
# ================================================
with st.expander("📌 Query 2: Most Injury-Prone Participants (Nested Query + Count)"):
    st.write("Shows participants with more injuries than the **average injury count**.")

    query2 = """
    SELECT p.Name, COUNT(i.InjuryName) AS InjuryCount
    FROM Participant p
    JOIN Injury i ON p.ParticipantID = i.ParticipantID
    GROUP BY p.Name
    HAVING InjuryCount > (
        SELECT AVG(cnt)
        FROM (
            SELECT COUNT(*) AS cnt
            FROM Injury
            GROUP BY ParticipantID
        ) AS injury_stats
    );
    """

    st.code(query2, language="sql")

    if st.button("Run Query 2"):
        df = run_query(query2)
        if df is not None:
            st.dataframe(df, use_container_width=True)


# ================================================
# QUERY 3 — Equipment with Highest Maintenance Cost
# ================================================
with st.expander("📌 Query 3: Highest Maintenance Cost Equipment (Aggregation + Join)"):
    st.write("Finds equipment items with total maintenance cost > 500.")

    query3 = """
    SELECT e.EquipmentType, SUM(m.Cost) AS TotalCost
    FROM Equipment e
    JOIN MaintenanceLog m ON e.EquipmentID = m.EquipmentID
    GROUP BY e.EquipmentType
    HAVING TotalCost > 500
    ORDER BY TotalCost DESC;
    """

    st.code(query3, language="sql")

    if st.button("Run Query 3"):
        df = run_query(query3)
        if df is not None:
            st.dataframe(df, use_container_width=True)


# ================================================
# QUERY 4 — Instructor Ratings Summary
# ================================================
with st.expander("📌 Query 4: Instructor Rating Summary (AVG + JOIN + Grouping)"):
    st.write("Shows instructors with average rating ≥ 4.")

    query4 = """
    SELECT i.Name AS Instructor, ROUND(AVG(r.RatingValue), 2) AS AvgRating
    FROM Instructor i
    JOIN Rating r ON i.InstructorID = r.InstructorID
    GROUP BY i.Name
    HAVING AvgRating >= 4
    ORDER BY AvgRating DESC;
    """

    st.code(query4, language="sql")

    if st.button("Run Query 4"):
        df = run_query(query4)
        if df is not None:
            st.dataframe(df, use_container_width=True)


# ================================================
# QUERY 5 — Activities without Any Injuries
# ================================================
with st.expander("📌 Query 5: Activities with Zero Injuries (LEFT JOIN + NULL CHECK)"):
    st.write("Shows safe activities with **no injuries recorded**.")

    query5 = """
    SELECT a.ActivityName
    FROM Activity a
    LEFT JOIN Injury i ON a.ActivityID = i.ActivityID
    WHERE i.InjuryName IS NULL;
    """

    st.code(query5, language="sql")

    if st.button("Run Query 5"):
        df = run_query(query5)
        if df is not None:
            st.dataframe(df, use_container_width=True)


st.write("---")
st.success("All complex SQL queries loaded successfully!")

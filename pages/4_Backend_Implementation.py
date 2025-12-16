import streamlit as st
import mysql.connector
import config
import textwrap


# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="Backend Implementation", page_icon="⚙️", layout="wide")

st.title("⚙️ Backend Implementation (SQL)")
st.write("""
This page automatically displays all backend SQL objects (Constraints, Triggers, Procedures, Functions) 
directly from your **ADVENTURE** database.  
It ensures your DBMS project demonstration shows **live, real SQL** running behind the system.
""")
st.write("---")


# ======================================================
# DATABASE CONNECTION
# ======================================================
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            port=config.DB_PORT,
            autocommit=False
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        return None


conn = get_db_connection()
if not conn:
    st.stop()


# ======================================================
# Explanation Helper
# ======================================================
def short_explanation(name, obj_type):
    name_low = name.lower()

    if obj_type == "TRIGGER":
        if "equip" in name_low:
            return "Keeps equipment status synced with maintenance logs."
        if "participant" in name_low or "total" in name_low:
            return "Updates total participants on registration."
        if "injury" in name_low:
            return "Validates injury severity and date logic."
        if "rating" in name_low:
            return "Ensures rating values stay between 1–5."
        return "Trigger enforcing important safety/business rules."

    if obj_type == "PROCEDURE":
        if "report" in name_low:
            return "Generates activity reports for admin use."
        if "add" in name_low:
            return "Safely inserts validated records into the database."
        if "update" in name_low:
            return "Updates existing records with validation."
        if "maintenance" in name_low:
            return "Summarizes maintenance logs & total cost."
        return "Multi-step backend automation routine."

    if obj_type == "FUNCTION":
        if "maintenance" in name_low:
            return "Returns total cost of all maintenance for equipment."
        if "age" in name_low:
            return "Computes age of a participant from DOB."
        if "rating" in name_low:
            return "Returns average rating of an instructor."
        if "participant" in name_low:
            return "Counts participants in an activity."
        if "injury" in name_low:
            return "Counts number of injuries for a participant."
        return "Reusable SQL function returning a computed value."

    return ""


# ======================================================
# PRIMARY & FOREIGN KEYS + ENUMS
# ======================================================
st.header("🔐 Constraints & Integrity Rules")

with st.expander("📌 Primary Keys & Foreign Keys"):
    try:
        cur = conn.cursor(dictionary=True)

        # Primary keys
        cur.execute("""
            SELECT TABLE_NAME, GROUP_CONCAT(COLUMN_NAME) AS cols
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA=%s AND CONSTRAINT_NAME='PRIMARY'
            GROUP BY TABLE_NAME;
        """, (config.DB_NAME,))
        pks = cur.fetchall()

        st.subheader("Primary Keys")
        for row in pks:
            st.markdown(f"**{row['TABLE_NAME']}** → `{row['cols']}`")

        st.write("")

        # Foreign keys
        st.subheader("Foreign Keys")
        cur.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA=%s AND REFERENCED_TABLE_NAME IS NOT NULL;
        """, (config.DB_NAME,))
        fks = cur.fetchall()

        for fk in fks:
            st.markdown(
                f"**{fk['TABLE_NAME']}.{fk['COLUMN_NAME']}** → "
                f"{fk['REFERENCED_TABLE_NAME']}.{fk['REFERENCED_COLUMN_NAME']}"
            )

        cur.close()

    except Exception as e:
        st.error(f"Error loading constraints: {e}")


with st.expander("📌 ENUM Fields / Domain Constraints"):
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA=%s AND COLUMN_TYPE LIKE 'enum(%%)';
        """, (config.DB_NAME,))
        enums = cur.fetchall()
        for en in enums:
            st.markdown(f"**{en['TABLE_NAME']}.{en['COLUMN_NAME']}** — `{en['COLUMN_TYPE']}`")
        cur.close()
    except Exception as e:
        st.error(f"Error loading enums: {e}")

st.write("---")


# ======================================================
# TRIGGERS (SEPARATE SECTION)
# ======================================================
st.header("🧨 Triggers (Live from DB)")

try:
    cur = conn.cursor(dictionary=True)
    cur.execute(f"SHOW TRIGGERS FROM `{config.DB_NAME}`;")
    triggers = cur.fetchall()
    cur.close()

    if triggers:
        for trg in triggers:
            name = trg["Trigger"]
            timing = trg["Timing"]
            event = trg["Event"]
            tbl = trg["Table"]
            sql_stmt = trg["Statement"]

            explanation = short_explanation(name, "TRIGGER")

            with st.expander(f"🔁 {name} — {timing} {event} ON {tbl}"):
                if explanation:
                    st.write(explanation)
                st.code(textwrap.dedent(sql_stmt).strip(), language="sql")
    else:
        st.info("No triggers found.")

except Exception as e:
    st.error(f"Error fetching triggers: {e}")

st.write("---")


# ======================================================
# STORED PROCEDURES (SEPARATE SECTION)
# ======================================================
st.header("📜 Stored Procedures (Live from DB)")

try:
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT ROUTINE_NAME FROM information_schema.ROUTINES
        WHERE ROUTINE_SCHEMA=%s AND ROUTINE_TYPE='PROCEDURE'
        ORDER BY ROUTINE_NAME;
    """, (config.DB_NAME,))
    procedures = cur.fetchall()
    cur.close()

    if procedures:
        for proc in procedures:
            name = proc["ROUTINE_NAME"]

            try:
                c = conn.cursor()
                c.execute(f"SHOW CREATE PROCEDURE `{config.DB_NAME}`.`{name}`;")
                res = c.fetchone()
                sql_text = res[2]
                c.close()
            except:
                sql_text = "-- Could not load procedure"

            explanation = short_explanation(name, "PROCEDURE")

            with st.expander(f"🛠 PROCEDURE — {name}"):
                if explanation:
                    st.write(explanation)
                st.code(textwrap.dedent(sql_text).strip(), language="sql")

    else:
        st.info("No stored procedures found.")

except Exception as e:
    st.error(f"Error loading procedures: {e}")

st.write("---")


# ======================================================
# FUNCTIONS (SEPARATE SECTION)
# ======================================================
st.header("🧮 SQL Functions (Live from DB)")

try:
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT ROUTINE_NAME FROM information_schema.ROUTINES
        WHERE ROUTINE_SCHEMA=%s AND ROUTINE_TYPE='FUNCTION'
        ORDER BY ROUTINE_NAME;
    """, (config.DB_NAME,))
    functions = cur.fetchall()
    cur.close()

    if functions:
        for fn in functions:
            name = fn["ROUTINE_NAME"]

            try:
                c = conn.cursor()
                c.execute(f"SHOW CREATE FUNCTION `{config.DB_NAME}`.`{name}`;")
                res = c.fetchone()
                sql_text = res[2]
                c.close()
            except:
                sql_text = "-- Could not load function"

            explanation = short_explanation(name, "FUNCTION")

            with st.expander(f"📐 FUNCTION — {name}"):
                if explanation:
                    st.write(explanation)
                st.code(textwrap.dedent(sql_text).strip(), language="sql")

    else:
        st.info("No SQL functions found.")

except Exception as e:
    st.error(f"Error loading functions: {e}")

st.write("---")


# ======================================================
# Quick Debug Tools
# ======================================================
st.header("🧪 Quick DB Checks")

col1, col2 = st.columns(2)

with col1:
    if st.button("Show Tables"):
        cur = conn.cursor()
        cur.execute("SHOW TABLES;")
        rows = cur.fetchall()
        cur.close()
        st.write(rows)

with col2:
    if st.button("Count Triggers & Routines"):
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA=%s", (config.DB_NAME,))
        tcount = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA=%s", (config.DB_NAME,))
        rcount = c.fetchone()[0]
        c.close()
        st.write(f"Triggers: {tcount}, Procedures/Functions: {rcount}")


st.success("Backend implementation loaded successfully.")

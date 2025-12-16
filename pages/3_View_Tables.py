import streamlit as st
import pandas as pd
import mysql.connector
import config

# -------------------------------------------
#  STREAMLIT PAGE CONFIG
# -------------------------------------------
st.set_page_config(page_title="View Tables", layout="wide")

st.title("📄 View Database Tables")

# -------------------------------------------
#  CONNECT TO DATABASE
# -------------------------------------------
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


# -------------------------------------------
#  FETCH TABLE NAMES
# -------------------------------------------
def get_tables():
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    return tables


tables = get_tables()

selected_table = st.selectbox("Select a table to view:", tables)

# -------------------------------------------
#  FETCH AND DISPLAY DATA FROM SELECTED TABLE
# -------------------------------------------
def fetch_table_data(table_name):
    try:
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error reading table '{table_name}': {e}")
        return None


df = fetch_table_data(selected_table)

if df is not None:
    st.subheader(f"🗂️ Showing data from: **{selected_table}**")

    if df.empty:
        st.warning("⚠️ No data available in this table.")
    else:
        st.dataframe(df, use_container_width=True)


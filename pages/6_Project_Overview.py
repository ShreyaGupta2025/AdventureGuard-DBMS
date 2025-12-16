import streamlit as st

st.set_page_config(page_title="Project Overview", page_icon="📘", layout="wide")

st.title("📘 Project Overview – AdventureGuard DBMS")
st.write("""
AdventureGuard is a data-driven Adventure Sports Safety & Management System designed to 
streamline participant registration, monitor instructor performance, track equipment status, 
and ensure safety during adventure activities. The system integrates **automated triggers, 
procedures, relational modeling, and a Streamlit-MySQL interface** to simulate how a real 
adventure sports organisation operates.
""")

st.write("---")

# -------------------------------------
# MINI WORLD
# -------------------------------------
st.header("🌍 Mini-World Description")
st.markdown("""
AdventureGuard manages an organisation that hosts adventure sports such as **rock climbing, 
kayaking, yoga, and swimming**. The system tracks:

- **Participants** — registered users, their emergency contacts, and injuries.
- **Activities** — scheduled adventure events with type, timing, fees, and instructor assignment.
- **Instructors** — experienced professionals conducting activities, rated by participants.
- **Equipment** — all items used in activities (ropes, kayaks, harnesses), along with their condition, warranty and dependencies.
- **Maintenance Logs** — technician records ensuring equipment safety.
- **Injuries** — weak entity recording severity, treatment, and associated activity.

The system ensures **safety, automation, and tracking** of all operations.
""")

st.write("---")

# -------------------------------------
# BUSINESS RULES
# -------------------------------------
st.header("📜 Business Rules")

st.subheader("👥 Participant Rules")
st.markdown("""
- Each participant has a unique ID.  
- Must provide valid emergency contact details.  
- Can register for multiple activities.  
- May have zero or more injuries.  
""")

st.subheader("🎯 Activity Rules")
st.markdown("""
- Each activity has a unique ID, schedule, fees, and instructor.  
- TotalParticipants is a **derived attribute**, computed automatically.  
""")

st.subheader("🧑‍🏫 Instructor Rules")
st.markdown("""
- Each instructor has a unique ID and expertise areas.  
- Can conduct multiple activities.  
- Rated by participants (one rating per participant per instructor).  
""")

st.subheader("🩹 Injury Rules")
st.markdown("""
- Injury is a **weak entity** dependent on Participant + Activity.  
- Records severity, date, treatment.  
- Severity validated using triggers.  
""")

st.subheader("🛠 Equipment Rules")
st.markdown("""
- Equipment has unique ID, status, maintenance info, and dependencies.  
- Status automatically updates via triggers when maintenance occurs.  
""")

st.subheader("🧾 Maintenance Log Rules")
st.markdown("""
- Each log is linked to an equipment item.  
- Tracks date, description, technician, and cost.  
""")

st.write("---")

# -------------------------------------
# RELATIONSHIPS
# -------------------------------------
st.header("🔗 Key Relationships & Cardinalities")
st.markdown("""
- **Participant ↔ Registers ↔ Activity**: M:N  
- **Instructor ↔ Conducts ↔ Activity**: 1:N  
- **Equipment ↔ UsedIn ↔ Activity**: M:N  
- **Participant ↔ Suffers ↔ Injury**: 1:N (Injury weak entity)  
- **Equipment ↔ MaintenanceLog**: 1:N  
- **Equipment ↔ DependsOn ↔ Equipment**: Recursive relationship  
""")

st.write("---")

# -------------------------------------
# TEAM SECTION
# -------------------------------------
st.header("🧑‍🤝‍🧑 Team Members – Group G14")

st.table({
    "Team Member ID": [
        "2023A3PS0348H (Leader)",
        "2023A3PS0399H",
        "2023A3PS0418H",
        "2023A3PS0002H",
        "2023A3PS1068H"
    ],
    "Name": [
        "Vaibhav Malik",
        "Shreya Gupta",
        "Harsh Vaishya",
        "Parth Sethi",
        "Siddharth Malawat"
    ]
})

st.success("This completes the Project Overview section.")

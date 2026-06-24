import streamlit as st
import datetime

# 1. Page Configuration & Title
st.set_page_config(page_title="Smart Task Tracker", page_icon="🎯", layout="centered")
st.title("🎯 Smart Task & Goal Tracker")
st.write("Welcome! Track your goals, set priorities, and watch your progress grow.")

# 2. Initialize Data Storage
# Streamlit reruns the whole script on every click. 
# 'session_state' acts like a memory to keep your tasks saved while the app is open.
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 3. Sidebar for Inputting New Tasks
st.sidebar.header("➕ Add New Task")
task_name = st.sidebar.text_input("What is the task/goal?")
task_priority = st.sidebar.selectbox("Priority Level", ["Low", "Medium", "High"])
task_date = st.sidebar.date_input("Target Deadline", datetime.date.today())

if st.sidebar.button("Add Task"):
    if task_name.strip() != "":
        # Save the task as a dictionary inside our list
        st.session_state.tasks.append({
            "name": task_name,
            "priority": task_priority,
            "date": task_date,
            "completed": False
        })
        st.sidebar.success(f"Added: {task_name}")
    else:
        st.sidebar.error("Task name cannot be empty!")

# 4. Progress Dashboard & Analytics
st.header("📊 Your Dashboard")
total_tasks = len(st.session_state.tasks)
completed_tasks = sum(1 for t in st.session_state.tasks if t["completed"])

if total_tasks > 0:
    progress_percentage = completed_tasks / total_tasks
    st.metric(label="Completion Rate", value=f"{int(progress_percentage * 100)}%")
    st.progress(progress_percentage)
else:
    st.info("No tasks added yet. Use the sidebar to get started!")

# 5. Displaying the Tasks
st.header("📝 Active Tasks")

# We loop through the list backwards so newest tasks appear at the top
for index, task in enumerate(st.session_state.tasks):
    # Create a nice visual box for each task
    with st.container():
        col1, col2, col3 = st.columns([1, 4, 2])
        
        # Checkbox to mark complete
        with col1:
            # If checked, update the task status
            is_checked = st.checkbox("Done", value=task["completed"], key=f"check_{index}")
            st.session_state.tasks[index]["completed"] = is_checked
            
        # Task Details
        with col2:
            if is_checked:
                st.write(f"~~{task['name']}~~ (Completed)")
            else:
                st.write(f"**{task['name']}**")
                
        # Priority Badge & Date
        with col3:
            st.write(f"⚠️ {task['priority']} | 📅 {task['date']}")
        
        st.divider()

# 6. Housekeeping: Clear Completed Tasks
if total_tasks > 0:
    if st.button("🧹 Clear Completed Tasks"):
        # Keep only the tasks that are NOT completed
        st.session_state.tasks = [t for t in st.session_state.tasks if not t["completed"]]
        st.rerun()
        
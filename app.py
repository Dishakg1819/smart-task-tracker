import streamlit as st
import datetime
import json
import os
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Ultimate Task Dashboard", page_icon="🚀", layout="wide")
st.title("🚀 Ultimate Goal & Task Dashboard")

# --- FEATURE 1: PERSISTENT STORAGE ---
# We save tasks to a file named 'tasks_data.json' so they stay saved forever.
DB_FILE = "tasks_data.json"

def load_tasks():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                # Convert the text file back into a Python list
                tasks = json.load(f)
                # Convert date strings back to actual date objects
                for t in tasks:
                    t["date"] = datetime.datetime.strptime(t["date"], "%Y-%m-%d").date()
                return tasks
            except:
                return []
    return []

def save_tasks(tasks):
    # Convert date objects to strings so they can be saved as text JSON
    serializable_tasks = []
    for t in tasks:
        task_copy = t.copy()
        task_copy["date"] = str(t["date"])
        serializable_tasks.append(task_copy)
    with open(DB_FILE, "w") as f:
        json.dump(serializable_tasks, f, indent=4)

# Load data into session state once when app starts
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()


# --- STEP 3: SIDEBAR INPUT ---
st.sidebar.header("➕ Add New Task")
task_name = st.sidebar.text_input("What is the task/goal?")
task_priority = st.sidebar.selectbox("Priority Level", ["Low", "Medium", "High"])

# FEATURE 2: CATEGORIZATION
task_category = st.sidebar.selectbox("Category", ["Personal", "Work", "Studies", "Health/Fitness"])
task_date = st.sidebar.date_input("Target Deadline", datetime.date.today())

if st.sidebar.button("Add Task"):
    if task_name.strip() != "":
        st.session_state.tasks.append({
            "name": task_name,
            "priority": task_priority,
            "category": task_category,
            "date": task_date,
            "completed": False
        })
        save_tasks(st.session_state.tasks)  # Save immediately to file
        st.sidebar.success(f"Added to {task_category}!")
        st.preload = True
        st.rerun()
    else:
        st.sidebar.error("Task name cannot be empty!")


# --- STEP 4: LAYOUT SPLIT (Dashboard & Analytics) ---
# We split the screen into two columns: Left for list, Right for charts
left_col, right_col = st.columns([5, 4], gap="large")

total_tasks = len(st.session_state.tasks)
completed_tasks = sum(1 for t in st.session_state.tasks if t["completed"])

with left_col:
    st.header("📝 Your Tasks")
    
    # FEATURE 2: FILTERING SYSTEM
    if total_tasks > 0:
        filter_option = st.selectbox("🔍 Filter list by category:", ["All Tasks", "Personal", "Work", "Studies", "Health/Fitness"])
    
        # Display tasks
        for index, task in enumerate(st.session_state.tasks):
            # Skip task if it doesn't match our filter selection
            if filter_option != "All Tasks" and task["category"] != filter_option:
                continue
                
            with st.container():
                c1, c2, c3 = st.columns([1, 4, 3])
                with c1:
                    is_checked = st.checkbox("", value=task["completed"], key=f"chk_{index}")
                    if is_checked != task["completed"]:
                        st.session_state.tasks[index]["completed"] = is_checked
                        save_tasks(st.session_state.tasks) # Save completion change
                        st.rerun()
                with c2:
                    if task["completed"]:
                        st.write(f"~~{task['name']}~~")
                    else:
                        st.write(f"**{task['name']}**")
                with c3:
                    st.caption(f"📁 {task['category']} | ⚠️ {task['priority']} | 📅 {task['date']}")
                st.divider()
                
        if st.button("🧹 Clear Completed Tasks"):
            st.session_state.tasks = [t for t in st.session_state.tasks if not t["completed"]]
            save_tasks(st.session_state.tasks) # Save cleared state
            st.rerun()
    else:
        st.info("Your task tracker is empty! Add a task via the sidebar.")

with right_col:
    st.header("📊 Analytics")
    if total_tasks > 0:
        # Standard Metrics
        progress_percentage = completed_tasks / total_tasks
        st.metric(label="Overall Completion Rate", value=f"{int(progress_percentage * 100)}%")
        st.progress(progress_percentage)
        
        st.write("---")
        
        # FEATURE 3: VISUAL CHARTS (Plotly Pie Chart)
        st.subheader("Tasks Breakdown by Category")
        
        # Count tasks per category
        categories_count = {}
        for t in st.session_state.tasks:
            cat = t["category"]
            categories_count[cat] = categories_count.get(cat, 0) + 1
            
        # Convert dictionary to data arrays for plotting
        cat_names = list(categories_count.keys())
        cat_values = list(categories_count.values())
        
        # Build the interactive pie chart
        fig = px.pie(names=cat_names, values=cat_values, hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Add some items to generate a live visual data report here.")
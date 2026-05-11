import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

# ----------------- Configuration & Styling -----------------
st.set_page_config(page_title="University DB App", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Database Connection -----------------
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root', # Password found!
        database='UniversityDB'
    )

def execute_query(query, params=None, fetch=True):
    try:
        conn = get_connection()
        # Ping the connection and reconnect if necessary
        conn.ping(reconnect=True, attempts=3, delay=1)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Database Error: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()

# ----------------- UI Layout -----------------
st.markdown('<p class="big-font">🎓 University Database Management Dashboard</p>', unsafe_allow_html=True)

menu = ["📊 Dashboard", "🗂️ View Students", "➕ Add Student", "📚 View Courses", "🏢 View Departments"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "📊 Dashboard":
    st.subheader("System Overview")
    
    # Fetch metrics
    student_count = execute_query("SELECT COUNT(*) as count FROM students")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if student_count:
            st.metric(label="Total Students", value=student_count[0]['count'])
        else:
            st.metric(label="Total Students", value=0)

    course_count = execute_query("SELECT COUNT(*) as count FROM courses")
    with col2:
        if course_count:
            st.metric(label="Total Courses", value=course_count[0]['count'])
        else:
            st.metric(label="Total Courses", value=0)
            
    instructor_count = execute_query("SELECT COUNT(*) as count FROM instructors")
    with col3:
        if instructor_count:
            st.metric(label="Total Instructors", value=instructor_count[0]['count'])
        else:
            st.metric(label="Total Instructors", value=0)
            
    enroll_count = execute_query("SELECT COUNT(*) as count FROM enrollments")
    with col4:
        if enroll_count:
            st.metric(label="Total Enrollments", value=enroll_count[0]['count'])
        else:
            st.metric(label="Total Enrollments", value=0)

    st.markdown("---")
    st.info("👈 Use the left sidebar to navigate the application and manage the DB records. If the dashboard is showing zeros, ensure your MySQL XAMPP/Service is running and you have loaded the `sql/load_data.sql` correctly.")

elif choice == "🗂️ View Students":
    st.subheader("Registered Students")
    students = execute_query("""
        SELECT s.student_id as 'ID', 
               CONCAT(s.first_name, ' ', s.last_name) as 'Full Name', 
               s.email as 'Email', 
               DATE_FORMAT(s.enrollment_date, '%Y-%m-%d') as 'Enrollment',
               d.dept_name as 'Department'
        FROM students s 
        LEFT JOIN departments d ON s.dept_id = d.dept_id
    """)
    if students:
        st.dataframe(pd.DataFrame(students), use_container_width=True)
    else:
        st.warning("No students found in the database.")

elif choice == "➕ Add Student":
    st.subheader("Enroll a New Student")
    
    deps = execute_query("SELECT dept_id, dept_name FROM departments")
    if deps:
        dep_options = {d['dept_name']: d['dept_id'] for d in deps}
        
        with st.form("add_student", clear_on_submit=True):
            col1, col2 = st.columns(2)
            first_name = col1.text_input("First Name", placeholder="e.g. John")
            last_name = col2.text_input("Last Name", placeholder="e.g. Doe")
            
            email = st.text_input("Email Address", placeholder="e.g. jdoe@university.edu")
            
            col_date, col_dep = st.columns(2)
            enroll_date = col_date.date_input("Enrollment Date", value=date.today())
            selected_dep = col_dep.selectbox("Department", list(dep_options.keys()))

            submit = st.form_submit_button("Register Student", use_container_width=True)

            if submit:
                if not first_name or not last_name or not email:
                    st.warning("⚠️ Please fill in all fields.")
                else:
                    success = execute_query(
                        """INSERT INTO students (first_name, last_name, email, enrollment_date, dept_id) 
                           VALUES (%s, %s, %s, %s, %s)""", 
                        (first_name, last_name, email, enroll_date, dep_options[selected_dep]), 
                        fetch=False
                    )
                    if success:
                        st.success("✅ Student successfully registered!")
    else:
        st.error("No departments found. Please setup the database first.")

elif choice == "📚 View Courses":
    st.subheader("Available Courses")
    courses = execute_query("""
        SELECT c.course_code as 'Code', 
               c.course_title as 'Title', 
               c.credits as 'Credits',
               CONCAT(i.first_name, ' ', i.last_name) as 'Instructor'
        FROM courses c
        LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
    """)
    if courses:
        st.dataframe(pd.DataFrame(courses), use_container_width=True)
    else:
        st.warning("No courses found.")

elif choice == "🏢 View Departments":
    st.subheader("University Departments")
    departments = execute_query("SELECT dept_id as 'ID', dept_name as 'Department', building as 'Building' FROM departments")
    if departments:
        st.dataframe(pd.DataFrame(departments), use_container_width=True)
    else:
        st.warning("No departments found.")

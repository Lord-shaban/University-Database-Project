import streamlit as st
import mysql.connector
import pandas as pd

# ----------------- Database Configuration -----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # Change this to your mysql password
    'database': 'UniversityDB'
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# ----------------- UI Structure -----------------
st.set_page_config(page_title="University DB App", layout="wide")
st.title("🎓 University Database Management")

menu = ["View Students", "Add Student", "View Courses", "View Departments"]
choice = st.sidebar.selectbox("Navigation", menu)

conn = get_connection()
if conn:
    cursor = conn.cursor(dictionary=True)

    if choice == "View Students":
        st.subheader("Students List")
        cursor.execute("""
            SELECT s.student_id, s.first_name, s.last_name, s.email, d.dept_name 
            FROM students s 
            LEFT JOIN departments d ON s.dept_id = d.dept_id
        """)
        students = cursor.fetchall()
        df = pd.DataFrame(students)
        st.dataframe(df)

    elif choice == "Add Student":
        st.subheader("Add a New Student")
        with st.form("add_student"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            date = st.date_input("Enrollment Date")
            
            # Get departments for dropdown
            cursor.execute("SELECT dept_id, dept_name FROM departments")
            deps = cursor.fetchall()
            dep_options = {d['dept_name']: d['dept_id'] for d in deps}
            selected_dep = st.selectbox("Department", list(dep_options.keys()))

            submit = st.form_submit_button("Add Student")

            if submit:
                try:
                    query = "INSERT INTO students (first_name, last_name, email, enrollment_date, dept_id) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (first_name, last_name, email, date, dep_options[selected_dep]))
                    conn.commit()
                    st.success("Student added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif choice == "View Courses":
        st.subheader("Courses List")
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        st.dataframe(pd.DataFrame(courses))

    elif choice == "View Departments":
        st.subheader("Departments List")
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
        st.dataframe(pd.DataFrame(departments))

    conn.close()
else:
    st.warning("Please ensure MySQL is running and credentials are correct in the script.")

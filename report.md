# University Database Project Report

## 1. Conceptual Design
### Entities and Attributes
- **Department:** `dept_id` (PK), `dept_name`, `building`
- **Student:** `student_id` (PK), `first_name`, `last_name`, `email`, `enrollment_date`, `dept_id` (FK)
- **Instructor:** `instructor_id` (PK), `first_name`, `last_name`, `email`, `dept_id` (FK)
- **Course:** `course_id` (PK), `course_code`, `course_title`, `credits`, `instructor_id` (FK)
- **Enrollment:** `enrollment_id` (PK), `student_id` (FK), `course_id` (FK), `semester`, `grade`

## 2. ER Diagram
* **Department 1:N Student**: A department has many students; a student belongs to one department.
* **Department 1:N Instructor**: A department employs many instructors.
* **Instructor 1:N Course**: An instructor can teach multiple courses.
* **Student N:M Course**: A student can enroll in multiple courses, and a course has many students. (Resolved by `Enrollment` as an associative entity with additional attributes: `semester` and `grade`).

## 3. Relational Schema
- `departments(dept_id, dept_name, building)`
- `students(student_id, first_name, last_name, email, enrollment_date, dept_id)`
  - FK: `dept_id` → `departments(dept_id)` ON DELETE SET NULL
- `instructors(instructor_id, first_name, last_name, email, dept_id)`
  - FK: `dept_id` → `departments(dept_id)` ON DELETE SET NULL
- `courses(course_id, course_code, course_title, credits, instructor_id)`
  - FK: `instructor_id` → `instructors(instructor_id)` ON DELETE SET NULL
  - CHECK: `credits > 0`
  - UNIQUE: `course_code`
- `enrollments(enrollment_id, student_id, course_id, semester, grade)`
  - FK: `student_id` → `students(student_id)` ON DELETE CASCADE
  - FK: `course_id` → `courses(course_id)` ON DELETE CASCADE
  - CHECK: `grade >= 0 AND grade <= 100`
  - UNIQUE: `(student_id, course_id, semester)`

## 4. DDL & DML
- **DDL:** Located in `/sql/create_tables.sql` — creates 5 tables with proper constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK).
- **DML:** Located in `/sql/load_data.sql` — inserts sample data: 4 departments, 10 students, 4 instructors, 5 courses, 10 enrollments.
- **Queries:** Located in `/sql/queries.sql` — includes JOIN queries, aggregation (AVG), and UPDATE statements.

## 5. Test Data
Included in `/sql/load_data.sql`. Summary:

| Table | Records | Sample Data |
|-------|---------|-------------|
| departments | 4 | Computer Science, Information Systems, Mathematics, Physics |
| students | 10 | Ahmed Ali, Sara Hassan, Mohamed Sayed, etc. |
| instructors | 4 | Dr. Ibrahim Mansour, Dr. Fatma Gad, etc. |
| courses | 5 | CS101, CS202, IS101, MATH101, CS303 |
| enrollments | 10 | Various student-course pairs with grades 65–95 |

## 6. Design Choices & Explanation
- **Cascading Deletes:** Deleting a student cascades to remove their enrollments (ON DELETE CASCADE) to prevent orphaned records. Deleting a department sets student/instructor `dept_id` to NULL (ON DELETE SET NULL).
- **Surrogate Keys:** All tables use `AUTO_INCREMENT` integer primary keys for consistent indexing and easier referencing.
- **Data Integrity:** CHECK constraints ensure valid grade ranges (0–100) and positive credit values. UNIQUE constraints prevent duplicate course codes and duplicate enrollment per student per course per semester.

## 7. Triggers
The trigger `before_enrollment_insert` (in `sql/triggers.sql`) validates grades before insertion:
- Fires BEFORE INSERT on the `enrollments` table.
- Rejects any grade outside the 0–100 range with a custom error message.
- Purpose: Ensures data integrity at the database level, independent of the application layer.

## 8. Bonus: Web Application UI
A full-featured Streamlit web application (`src/app.py`) provides:

- **Dashboard:** Real-time statistics, bar charts (students per department, average grades), and recent enrollment history.
- **Full CRUD for all 5 tables:**
  - **View:** Data tables with search, filters, and card-based displays.
  - **Add:** Forms with validation and auto-refresh.
  - **Edit:** Select a record, modify fields (pre-populated), and save.
  - **Delete:** Select and confirm deletion with cascade warnings.
- **Design:** Premium dark theme with Inter font, glassmorphic cards, indigo accent color, and responsive layout.
- **Tech Stack:** Python, Streamlit, MySQL Connector, Pandas.

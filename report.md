# University Database Project Report

## 1. Conceptual Design
### Entities and Attributes
- **Department:** `dept_id` (PK), `dept_name`, `building`
- **Student:** `student_id` (PK), `first_name`, `last_name`, `email`, `enrollment_date`, `dept_id` (FK)
- **Instructor:** `instructor_id` (PK), `first_name`, `last_name`, `email`, `dept_id` (FK)
- **Course:** `course_id` (PK), `course_code`, `course_title`, `credits`, `instructor_id` (FK)
- **Enrollment:** `enrollment_id` (PK), `student_id` (FK), `course_id` (FK), `semester`, `grade`

## 2. ER Diagram
* **Department 1:N Student**: A department has many students, and a student belongs to one department.
* **Department 1:N Instructor**: A department employs many instructors.
* **Instructor 1:N Course**: An instructor can teach multiple courses.
* **Student N:M Course**: A student can enroll in multiple courses, and a course has many students. (Resolved by `Enrollment` table as an associative entity).

## 3. Relational Schema
- `departments(dept_id, dept_name, building)`
- `students(student_id, first_name, last_name, email, enrollment_date, dept_id)`
  - FK: `dept_id` references `departments(dept_id)`
- `instructors(instructor_id, first_name, last_name, email, dept_id)`
  - FK: `dept_id` references `departments(dept_id)`
- `courses(course_id, course_code, course_title, credits, instructor_id)`
  - FK: `instructor_id` references `instructors(instructor_id)`
- `enrollments(enrollment_id, student_id, course_id, semester, grade)`
  - FK: `student_id` references `students(student_id)`
  - FK: `course_id` references `courses(course_id)`

## 4. DDL & DML
Located in `/sql/create_tables.sql` and `/sql/load_data.sql`. We used standard constraints such as `CHECK (credits > 0)` and `UNIQUE (student_id, course_id, semester)`.

## 5. Test Data
Included in `/sql/load_data.sql`. Each table has sufficient records, such as 10 students, 5 courses, 10 enrollments, to properly simulate retrieval and table relationships.

## 6. Design Choices & Explanation
- **Cascading Deletes:** Deleting a student cascades to remove their enrollments to prevent orphaned records. Deleting a department sets references to `NULL`.
- **Primary & Foreign Keys:** Consistent numeric surrogate keys (`id`) with `AUTO_INCREMENT` ensure easier indexing.

## 7. Triggers
The trigger (in `triggers.sql`) is designed to capture updates to a student's grade or log course registration counts. 
*(See `sql/triggers.sql` for exact implementation).*

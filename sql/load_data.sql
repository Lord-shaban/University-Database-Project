USE UniversityDB;

-- إدخال بيانات الأقسام (Departments)
INSERT INTO departments (dept_name, building) VALUES
('Computer Science', 'Building A'),
('Information Systems', 'Building A'),
('Mathematics', 'Building B'),
('Physics', 'Building B');

-- إدخال بيانات الطلاب (Students)
INSERT INTO students (first_name, last_name, email, enrollment_date, dept_id) VALUES
('Ahmed', 'Ali', 'ahmed.ali@university.edu', '2023-09-01', 1),
('Sara', 'Hassan', 'sara.h@university.edu', '2023-09-01', 1),
('Mohamed', 'Sayed', 'm.sayed@university.edu', '2023-09-01', 2),
('Mona', 'Zaki', 'mona.z@university.edu', '2024-02-01', 2),
('Omar', 'Khaled', 'omar.k@university.edu', '2024-02-01', 3),
('Laila', 'Samy', 'laila.s@university.edu', '2024-02-01', 1),
('Youssef', 'Amr', 'youssef.a@university.edu', '2023-09-01', 3),
('Nour', 'Eldin', 'nour.e@university.edu', '2023-09-01', 4),
('Hoda', 'Mahmoud', 'hoda.m@university.edu', '2024-02-01', 4),
('Ziad', 'Tarek', 'ziad.t@university.edu', '2024-02-01', 1);

-- إدخال بيانات الأساتذة (Instructors)
INSERT INTO instructors (first_name, last_name, email, dept_id) VALUES
('Dr. Ibrahim', 'Mansour', 'ibrahim@university.edu', 1),
('Dr. Fatma', 'Gad', 'fatma@university.edu', 1),
('Dr. Tamer', 'Ashraf', 'tamer@university.edu', 2),
('Dr. Salma', 'Nabil', 'salma@university.edu', 3);

-- إدخال بيانات المواد (Courses)
INSERT INTO courses (course_code, course_title, credits, instructor_id) VALUES
('CS101', 'Introduction to CS', 3, 1),
('CS202', 'Data Structures', 4, 1),
('IS101', 'Database Management', 3, 3),
('MATH101', 'Calculus I', 3, 4),
('CS303', 'Big Data Analytics', 4, 2);

-- إدخال بيانات التسجيل والدرجات (Enrollments)
INSERT INTO enrollments (student_id, course_id, semester, grade) VALUES
(1, 1, 'Fall 2025', 85.5),
(1, 2, 'Spring 2026', 91.0),
(2, 1, 'Fall 2025', 78.0),
(2, 3, 'Spring 2026', 88.5),
(3, 3, 'Fall 2025', 92.0),
(4, 3, 'Spring 2026', 65.0),
(5, 4, 'Fall 2025', 74.0),
(6, 1, 'Fall 2025', 95.0),
(6, 5, 'Spring 2026', 89.0),
(7, 4, 'Spring 2026', 83.0);
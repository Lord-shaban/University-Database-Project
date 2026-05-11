-- إنشاء قاعدة البيانات
CREATE DATABASE IF NOT EXISTS UniversityDB;
USE UniversityDB;

-- 1. جدول الأقسام
CREATE TABLE IF NOT EXISTS departments (
    dept_id INT AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    building VARCHAR(50),
    CONSTRAINT pk_departments PRIMARY KEY (dept_id)
);

-- 2. جدول الطلاب
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    enrollment_date DATE NOT NULL,
    dept_id INT,
    CONSTRAINT pk_students PRIMARY KEY (student_id),
    CONSTRAINT fk_students_dept FOREIGN KEY (dept_id) 
        REFERENCES departments(dept_id) ON DELETE SET NULL
);

-- 3. جدول الأساتذة
CREATE TABLE IF NOT EXISTS instructors (
    instructor_id INT AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    dept_id INT,
    CONSTRAINT pk_instructors PRIMARY KEY (instructor_id),
    CONSTRAINT fk_instructors_dept FOREIGN KEY (dept_id) 
        REFERENCES departments(dept_id) ON DELETE SET NULL
);

-- 4. جدول المواد الدراسية
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    course_title VARCHAR(100) NOT NULL,
    credits INT NOT NULL CHECK (credits > 0),
    instructor_id INT,
    CONSTRAINT pk_courses PRIMARY KEY (course_id),
    CONSTRAINT fk_courses_inst FOREIGN KEY (instructor_id) 
        REFERENCES instructors(instructor_id) ON DELETE SET NULL
);

-- 5. جدول التسجيل والدرجات
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INT AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    semester VARCHAR(20) NOT NULL,
    grade DECIMAL(5,2) DEFAULT NULL CHECK (grade >= 0 AND grade <= 100),
    CONSTRAINT pk_enrollments PRIMARY KEY (enrollment_id),
    CONSTRAINT fk_enroll_student FOREIGN KEY (student_id) 
        REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_enroll_course FOREIGN KEY (course_id) 
        REFERENCES courses(course_id) ON DELETE CASCADE,
    CONSTRAINT uq_student_course UNIQUE (student_id, course_id, semester)
);
# 📘 شرح ملف create_tables.sql — إنشاء الجداول

## نظرة عامة
هذا الملف يحتوي على أوامر DDL (Data Definition Language) لإنشاء قاعدة البيانات وجميع الجداول الخمسة.

---

## 1. إنشاء قاعدة البيانات

```sql
CREATE DATABASE IF NOT EXISTS UniversityDB;
USE UniversityDB;
```

- `CREATE DATABASE IF NOT EXISTS` → ينشئ قاعدة بيانات اسمها `UniversityDB` فقط إذا لم تكن موجودة مسبقاً.
- `USE UniversityDB` → يحدد أن كل الأوامر التالية ستُنفذ داخل هذه القاعدة.

---

## 2. جدول الأقسام (departments)

```sql
CREATE TABLE IF NOT EXISTS departments (
    dept_id INT AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    building VARCHAR(50),
    CONSTRAINT pk_departments PRIMARY KEY (dept_id)
);
```

| العمود | النوع | الشرح |
|--------|-------|-------|
| `dept_id` | INT AUTO_INCREMENT | مفتاح أساسي يتزايد تلقائياً (1, 2, 3, ...) |
| `dept_name` | VARCHAR(100) NOT NULL | اسم القسم — لا يمكن أن يكون فارغاً |
| `building` | VARCHAR(50) | اسم المبنى — اختياري |

- **PRIMARY KEY**: `dept_id` — يضمن أن كل قسم له رقم فريد.

---

## 3. جدول الطلاب (students)

```sql
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
```

| العمود | النوع | الشرح |
|--------|-------|-------|
| `student_id` | INT AUTO_INCREMENT | مفتاح أساسي |
| `first_name` | VARCHAR(50) NOT NULL | الاسم الأول — مطلوب |
| `last_name` | VARCHAR(50) NOT NULL | الاسم الأخير — مطلوب |
| `email` | VARCHAR(100) UNIQUE NOT NULL | البريد الإلكتروني — فريد ومطلوب |
| `enrollment_date` | DATE NOT NULL | تاريخ التسجيل |
| `dept_id` | INT | رقم القسم (مفتاح أجنبي) |

### القيود (Constraints):
- **PRIMARY KEY** (`student_id`): كل طالب له ID فريد.
- **UNIQUE** (`email`): لا يمكن لطالبين مشاركة نفس البريد.
- **FOREIGN KEY** (`dept_id` → `departments.dept_id`): يربط الطالب بقسمه.
- **ON DELETE SET NULL**: إذا حُذف القسم، يصبح `dept_id` للطالب `NULL` بدلاً من حذف الطالب.

---

## 4. جدول الأساتذة (instructors)

```sql
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
```

- نفس بنية جدول الطلاب تقريباً.
- **ON DELETE SET NULL**: حذف قسم → الأستاذ يبقى لكن بدون قسم.

---

## 5. جدول المواد الدراسية (courses)

```sql
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
```

| القيد | الشرح |
|-------|-------|
| `UNIQUE (course_code)` | كل مادة لها كود فريد مثل CS101 |
| `CHECK (credits > 0)` | الساعات المعتمدة يجب أن تكون أكبر من صفر |
| `ON DELETE SET NULL` | حذف أستاذ → المادة تبقى لكن بدون أستاذ |

---

## 6. جدول التسجيل والدرجات (enrollments)

```sql
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
```

### النقاط المهمة:
- **ON DELETE CASCADE**: حذف طالب أو مادة → حذف التسجيلات المرتبطة تلقائياً.
- **CHECK (grade >= 0 AND grade <= 100)**: الدرجة بين 0 و 100 فقط.
- **UNIQUE (student_id, course_id, semester)**: منع تسجيل نفس الطالب في نفس المادة في نفس الفصل مرتين.
- **DECIMAL(5,2)**: يسمح بدرجات عشرية مثل 85.50.
- **DEFAULT NULL**: الدرجة تكون NULL (فارغة) حتى يتم إدخالها.

---

## ملخص العلاقات بين الجداول

```
departments ──1:N──→ students      (قسم واحد فيه طلاب كثير)
departments ──1:N──→ instructors   (قسم واحد فيه أساتذة كثير)
instructors ──1:N──→ courses       (أستاذ واحد يدرّس مواد كثيرة)
students    ──N:M──→ courses       (عبر جدول enrollments)
```

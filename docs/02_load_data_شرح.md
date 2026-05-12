# 📘 شرح ملف load_data.sql — إدخال البيانات

## نظرة عامة
هذا الملف يحتوي على أوامر DML (Data Manipulation Language) لإدخال بيانات تجريبية في الجداول الخمسة.

> ⚠️ **مهم:** يجب تنفيذ `create_tables.sql` أولاً قبل هذا الملف.

---

## 1. بيانات الأقسام (4 سجلات)

```sql
INSERT INTO departments (dept_name, building) VALUES
('Computer Science', 'Building A'),
('Information Systems', 'Building A'),
('Mathematics', 'Building B'),
('Physics', 'Building B');
```

- لم نحدد `dept_id` لأنه `AUTO_INCREMENT` — MySQL يعطيه قيم 1, 2, 3, 4 تلقائياً.
- قسمان في Building A وقسمان في Building B.

---

## 2. بيانات الطلاب (10 سجلات)

```sql
INSERT INTO students (first_name, last_name, email, enrollment_date, dept_id) VALUES
('Ahmed', 'Ali', 'ahmed.ali@university.edu', '2023-09-01', 1),
('Sara', 'Hassan', 'sara.h@university.edu', '2023-09-01', 1),
...
```

### ملاحظات:
- **`dept_id = 1`** يعني القسم الأول (Computer Science).
- بعض الطلاب سُجلوا في `2023-09-01` والبعض في `2024-02-01` (فصلين مختلفين).
- كل طالب له بريد إلكتروني فريد (UNIQUE constraint).

---

## 3. بيانات الأساتذة (4 سجلات)

```sql
INSERT INTO instructors (first_name, last_name, email, dept_id) VALUES
('Dr. Ibrahim', 'Mansour', 'ibrahim@university.edu', 1),
('Dr. Fatma', 'Gad', 'fatma@university.edu', 1),
('Dr. Tamer', 'Ashraf', 'tamer@university.edu', 2),
('Dr. Salma', 'Nabil', 'salma@university.edu', 3);
```

- أستاذان في CS (dept_id=1)، واحد في IS، وواحد في Math.
- قسم Physics ليس له أستاذ (هذا طبيعي — يمكن إضافته لاحقاً).

---

## 4. بيانات المواد (5 سجلات)

```sql
INSERT INTO courses (course_code, course_title, credits, instructor_id) VALUES
('CS101', 'Introduction to CS', 3, 1),
('CS202', 'Data Structures', 4, 1),
('IS101', 'Database Management', 3, 3),
('MATH101', 'Calculus I', 3, 4),
('CS303', 'Big Data Analytics', 4, 2);
```

| الكود | المادة | الساعات | الأستاذ |
|-------|--------|---------|---------|
| CS101 | Introduction to CS | 3 | Dr. Ibrahim (id=1) |
| CS202 | Data Structures | 4 | Dr. Ibrahim (id=1) |
| IS101 | Database Management | 3 | Dr. Tamer (id=3) |
| MATH101 | Calculus I | 3 | Dr. Salma (id=4) |
| CS303 | Big Data Analytics | 4 | Dr. Fatma (id=2) |

---

## 5. بيانات التسجيل والدرجات (10 سجلات)

```sql
INSERT INTO enrollments (student_id, course_id, semester, grade) VALUES
(1, 1, 'Fall 2025', 85.5),
(1, 2, 'Spring 2026', 91.0),
(2, 1, 'Fall 2025', 78.0),
...
```

### شرح كل سطر:
| الطالب | المادة | الفصل | الدرجة |
|--------|--------|-------|--------|
| Ahmed (1) | CS101 (1) | Fall 2025 | 85.5 |
| Ahmed (1) | CS202 (2) | Spring 2026 | 91.0 |
| Sara (2) | CS101 (1) | Fall 2025 | 78.0 |
| Sara (2) | IS101 (3) | Spring 2026 | 88.5 |
| Mohamed (3) | IS101 (3) | Fall 2025 | 92.0 |
| Mona (4) | IS101 (3) | Spring 2026 | 65.0 |
| Omar (5) | MATH101 (4) | Fall 2025 | 74.0 |
| Laila (6) | CS101 (1) | Fall 2025 | 95.0 |
| Laila (6) | CS303 (5) | Spring 2026 | 89.0 |
| Youssef (7) | MATH101 (4) | Spring 2026 | 83.0 |

### ملاحظات:
- Ahmed مسجل في مادتين (CS101 و CS202).
- Laila مسجلة في مادتين (CS101 و CS303).
- الدرجات تتراوح بين 65 و 95.
- لا يوجد طالبان مسجلان في نفس المادة في نفس الفصل مرتين (بسبب UNIQUE constraint).

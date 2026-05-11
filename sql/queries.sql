USE UniversityDB;

-- 1. استرجاع جميع الطلاب المسجلين في كورس معين (مثال: CS101) مع درجاتهم
SELECT s.student_id, s.first_name, s.last_name, e.grade
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
WHERE c.course_code = 'CS101';

-- 2. حساب المتوسط العام للدرجات لكل كورس
SELECT c.course_code, c.course_title, AVG(e.grade) AS average_grade
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_code, c.course_title;

-- 3. تحديث درجة طالب في مادة معينة
UPDATE enrollments 
SET grade = 94.5 
WHERE student_id = 1 AND course_id = 1;
# 📘 شرح ملف queries.sql — الاستعلامات

## نظرة عامة
هذا الملف يحتوي على استعلامات SQL لاسترجاع وتحديث البيانات.

---

## الاستعلام 1: طلاب مادة معينة مع درجاتهم

```sql
SELECT s.student_id, s.first_name, s.last_name, e.grade
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
WHERE c.course_code = 'CS101';
```

### الشرح سطر بسطر:
1. **SELECT**: نختار أعمدة (ID, الاسم الأول, الأخير, الدرجة).
2. **FROM students s**: نبدأ من جدول الطلاب (اختصرناه بـ `s`).
3. **JOIN enrollments e ON ...**: نربط الطلاب بالتسجيلات عبر `student_id`.
4. **JOIN courses c ON ...**: نربط التسجيلات بالمواد عبر `course_id`.
5. **WHERE c.course_code = 'CS101'**: نُصفّي فقط المادة CS101.

### النتيجة المتوقعة:
| student_id | first_name | last_name | grade |
|------------|------------|-----------|-------|
| 1 | Ahmed | Ali | 85.5 |
| 2 | Sara | Hassan | 78.0 |
| 6 | Laila | Samy | 95.0 |

### لماذا JOIN وليس WHERE؟
- `JOIN` هو الطريقة القياسية والأوضح لربط الجداول.
- يربط السجلات التي تتطابق في العمود المشترك فقط.

---

## الاستعلام 2: متوسط الدرجات لكل مادة

```sql
SELECT c.course_code, c.course_title, AVG(e.grade) AS average_grade
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_code, c.course_title;
```

### الشرح:
1. **LEFT JOIN**: نستخدم LEFT JOIN (وليس JOIN عادي) لنظهر حتى المواد التي ليس فيها تسجيلات (ستظهر بمتوسط NULL).
2. **AVG(e.grade)**: دالة تجميعية تحسب المتوسط الحسابي للدرجات.
3. **AS average_grade**: نسمي العمود الناتج "average_grade" للوضوح.
4. **GROUP BY**: نجمّع النتائج حسب كل مادة (كل مادة سطر واحد).

### الفرق بين JOIN و LEFT JOIN:
| النوع | السلوك |
|-------|--------|
| `JOIN` (INNER) | يُرجع فقط السجلات المتطابقة في الجدولين |
| `LEFT JOIN` | يُرجع كل سجلات الجدول الأيسر + المطابقات (أو NULL) |

---

## الاستعلام 3: تحديث درجة طالب

```sql
UPDATE enrollments
SET grade = 94.5
WHERE student_id = 1 AND course_id = 1;
```

### الشرح:
- **UPDATE**: أمر تعديل (DML).
- **SET grade = 94.5**: نغير الدرجة إلى 94.5.
- **WHERE**: نحدد بالضبط أي سجل (الطالب 1 في المادة 1).

> ⚠️ بدون WHERE، سيتم تحديث جميع السجلات في الجدول!

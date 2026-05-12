# شرح triggers.sql

## الكود

```sql
DELIMITER //
CREATE TRIGGER before_enrollment_insert
BEFORE INSERT ON enrollments
FOR EACH ROW
BEGIN
    IF NEW.grade < 0 OR NEW.grade > 100 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Grade must be between 0 and 100';
    END IF;
END;
//
DELIMITER ;
```

## شرح سطر بسطر

- **DELIMITER //** → يغير الفاصل مؤقتاً لأن جسم الـ Trigger يحتوي على `;`
- **CREATE TRIGGER** → ينشئ trigger اسمه `before_enrollment_insert`
- **BEFORE INSERT ON enrollments** → يُنفذ قبل كل عملية INSERT على جدول enrollments
- **FOR EACH ROW** → يعمل مرة لكل سجل
- **NEW.grade** → يمثل قيمة الدرجة في السجل الجديد
- **IF ... THEN** → يتحقق: هل الدرجة خارج النطاق 0-100؟
- **SIGNAL SQLSTATE '45000'** → يُصدر خطأ مخصص ويمنع الإدخال
- **DELIMITER ;** → يُعيد الفاصل الطبيعي

## أمثلة

| العملية | النتيجة |
|---------|---------|
| INSERT grade = 85 | ✅ ينجح |
| INSERT grade = 105 | ❌ يُرفض |
| INSERT grade = -5 | ❌ يُرفض |
| INSERT grade = NULL | ✅ ينجح (NULL مقبول) |

## لماذا Trigger مع CHECK؟
- طبقة حماية مزدوجة
- بعض إصدارات MySQL القديمة لا تدعم CHECK

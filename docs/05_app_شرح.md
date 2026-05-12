# شرح app.py — تطبيق Streamlit

## نظرة عامة
ملف `app.py` هو تطبيق ويب مبني بـ **Streamlit** يتصل بقاعدة بيانات MySQL ويوفر واجهة كاملة (CRUD) لإدارة بيانات الجامعة.

---

## 1. المكتبات المستخدمة

```python
import streamlit as st          # إطار عمل الواجهة
import mysql.connector          # للاتصال بـ MySQL
import pandas as pd             # لعرض البيانات في جداول
from datetime import date       # للتعامل مع التواريخ
```

| المكتبة | الوظيفة |
|---------|---------|
| `streamlit` | يبني واجهة ويب تفاعلية بدون HTML/JS |
| `mysql.connector` | يتصل بـ MySQL وينفذ SQL |
| `pandas` | يحول نتائج SQL لجداول قابلة للعرض |

---

## 2. إعدادات الصفحة

```python
st.set_page_config(page_title="UniversityDB", page_icon="🎓",
                   layout="wide", initial_sidebar_state="expanded")
```

- `layout="wide"` → يستخدم عرض الشاشة الكامل
- `initial_sidebar_state="expanded"` → القائمة الجانبية مفتوحة افتراضياً

---

## 3. التصميم (CSS)

```python
st.markdown("""<style>...</style>""", unsafe_allow_html=True)
```

- نستخدم CSS مخصص لتغيير شكل التطبيق (ثيم داكن، خطوط، ألوان...)
- `unsafe_allow_html=True` → يسمح بإدخال HTML/CSS مباشرة

### عناصر التصميم الرئيسية:
- **خلفية داكنة**: `#0c0c14`
- **لون أساسي (Accent)**: `#6366f1` (Indigo)
- **خط**: Inter من Google Fonts
- **بطاقات**: خلفية `#16161f` مع حواف شفافة

---

## 4. الاتصال بقاعدة البيانات

```python
@st.cache_resource
def get_conn():
    return mysql.connector.connect(
        host='localhost', user='root',
        password='root', database='UniversityDB'
    )
```

- `@st.cache_resource` → يحفظ الاتصال في الذاكرة ولا يعيد إنشاءه مع كل تحديث
- يتصل بـ MySQL على `localhost` بمستخدم `root`

---

## 5. دالة تنفيذ الاستعلامات

```python
def q(sql, p=None, fetch=True):
    try:
        c = get_conn()
        c.ping(reconnect=True, attempts=3, delay=1)
        cur = c.cursor(dictionary=True)
        cur.execute(sql, p or ())
        if fetch: return cur.fetchall()
        c.commit(); return True
    except Exception as e:
        st.error(f"DB Error: {e}"); return None
    finally:
        if 'cur' in locals(): cur.close()
```

### شرح:
- **`c.ping(reconnect=True)`** → يتحقق أن الاتصال نشط، وإذا انقطع يعيد الاتصال
- **`dictionary=True`** → النتائج ترجع كـ dict (مثل `{'ID': 1, 'Name': 'Ahmed'}`)
- **`fetch=True`** → للاستعلامات (SELECT) — يرجع النتائج
- **`fetch=False`** → لعمليات التعديل (INSERT/UPDATE/DELETE) — يعمل commit
- **`finally`** → يغلق الـ cursor دائماً حتى لو حصل خطأ

---

## 6. دالة العد

```python
def cnt(t):
    r = q(f"SELECT COUNT(*) AS n FROM {t}")
    return r[0]['n'] if r else 0
```

- تحسب عدد السجلات في أي جدول
- تُستخدم في Dashboard لعرض الإحصائيات

---

## 7. القائمة الجانبية (Sidebar)

```python
with st.sidebar:
    st.markdown('<div class="brand">...</div>', unsafe_allow_html=True)
    pages = ["📊 Dashboard", "👥 Students", ...]
    choice = st.radio("Nav", pages, label_visibility="collapsed")
```

- `st.sidebar` → كل شيء بداخله يظهر في القائمة الجانبية
- `st.radio` → أزرار اختيار للتنقل بين الصفحات
- `label_visibility="collapsed"` → يخفي عنوان "Nav"

---

## 8. صفحة Dashboard

### الإحصائيات:
```python
s, c, i, e = cnt("students"), cnt("courses"), cnt("instructors"), cnt("enrollments")
```
تعرض 4 بطاقات بعدد الطلاب والمواد والأساتذة والتسجيلات.

### الرسوم البيانية:
```python
st.bar_chart(pd.DataFrame(dd).set_index("Dept"), color="#6366f1")
```
- `pd.DataFrame(dd)` → يحول النتائج لجدول pandas
- `.set_index("Dept")` → يجعل أسماء الأقسام على المحور الأفقي
- `st.bar_chart` → يرسم رسم بياني عمودي

---

## 9. عمليات CRUD لكل جدول

كل قسم (Students, Instructors, Courses, Departments, Enrollments) يحتوي على 4 تبويبات:

### 📋 View All — عرض البيانات
```python
res = q("SELECT ... FROM students ...")
st.dataframe(pd.DataFrame(res), use_container_width=True, hide_index=True)
```

### ➕ Add New — إضافة سجل جديد
```python
with st.form("add_stu", clear_on_submit=True):
    fn = st.text_input("First Name")
    # ... باقي الحقول
    if st.form_submit_button("✅ Register"):
        q("INSERT INTO students ... VALUES (%s, ...)", (fn, ...), fetch=False)
        st.rerun()  # تحديث الصفحة
```
- `st.form` → يجمع كل الحقول في نموذج واحد
- `clear_on_submit=True` → يمسح الحقول بعد الإرسال
- `%s` → placeholder يمنع SQL Injection

### ✏️ Edit — تعديل سجل
```python
sel = st.selectbox("Select student to edit", ...)
cur = q("SELECT * FROM students WHERE student_id=%s", (id,))
# يعرض فورم بالقيم الحالية
fn = st.text_input("First Name", value=cur['first_name'])
q("UPDATE students SET first_name=%s ... WHERE student_id=%s", ...)
```

### 🗑️ Delete — حذف سجل
```python
sel = st.selectbox("Select student to delete", ...)
if st.button("🗑️ Delete"):
    q("DELETE FROM students WHERE student_id=%s", (id,), fetch=False)
    st.rerun()
```

---

## 10. مفاهيم Streamlit المهمة

| المفهوم | الشرح |
|---------|-------|
| `st.columns(2)` | يقسم الصفحة لعمودين |
| `st.tabs(["A","B"])` | تبويبات أفقية |
| `st.form()` | نموذج إدخال |
| `st.selectbox()` | قائمة منسدلة |
| `st.dataframe()` | عرض جدول |
| `st.bar_chart()` | رسم بياني |
| `st.rerun()` | يعيد تحميل الصفحة |
| `st.success/warning/error()` | رسائل تنبيه |
| `st.balloons()` | حركة بصرية احتفالية |

---

## 11. مصطلحات مهمة للمناقشة

| المصطلح | الشرح |
|---------|-------|
| DDL | Data Definition Language — أوامر إنشاء الجداول |
| DML | Data Manipulation Language — أوامر الإدخال والتعديل |
| CRUD | Create, Read, Update, Delete |
| FK | Foreign Key — مفتاح أجنبي يربط بين جدولين |
| PK | Primary Key — مفتاح أساسي فريد |
| JOIN | ربط جدولين عبر عمود مشترك |
| Trigger | كود يُنفذ تلقائياً عند حدوث عملية معينة |
| CASCADE | حذف تلقائي للسجلات المرتبطة |
| SET NULL | جعل القيمة NULL عند حذف المرجع |

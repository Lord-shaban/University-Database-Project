# University Database Project 🎓

## Project Overview
This project involves the design and implementation of a relational database for a university system. The database (`UniversityDB`) tracks **departments**, **students**, **instructors**, **courses**, and **student enrollments** with full CRUD (Create, Read, Update, Delete) operations through a modern web-based dashboard.

## Repository Structure

```
├─ /README.md                ← This file
├─ /report.md                ← Written report (markdown version)
├─ /report.docx              ← Written report (Word document)
├─ /presentation.pptx        ← Slide deck for video walkthrough
├─ /video_link.txt           ← Public YouTube/MS Stream URL
├─ /sql/
│    ├─ create_tables.sql    ← DDL for schema creation (5 tables)
│    ├─ load_data.sql        ← INSERT scripts (10+ records/table)
│    ├─ queries.sql          ← Sample retrieval & update queries
│    └─ triggers.sql         ← Database triggers (grade validation)
└─ /src/
     └─ app.py               ← Streamlit Web App (Bonus UI)
```

## Database Schema

| Table | Description | Key Relationships |
|-------|-------------|-------------------|
| `departments` | Academic departments | — |
| `students` | Student records | FK → `departments` |
| `instructors` | Instructor records | FK → `departments` |
| `courses` | Course catalog | FK → `instructors` |
| `enrollments` | Student-course registrations & grades | FK → `students`, `courses` |

## How to Run

### 1. Database Setup
1. Install [MySQL](https://www.mysql.com/) (or use XAMPP).
2. Execute the SQL scripts in `/sql/` in this order:
   ```
   create_tables.sql → load_data.sql → triggers.sql → queries.sql
   ```

### 2. Application UI (Bonus)
The application provides a full-featured dashboard to browse, add, edit, and delete data.

1. Ensure Python is installed.
2. Install dependencies:
   ```bash
   pip install streamlit mysql-connector-python pandas
   ```
3. Update your database credentials in `src/app.py` (default: `root`/`root`).
4. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## Application Features

| Page | View | Add | Edit | Delete |
|------|------|-----|------|--------|
| 📊 **Dashboard** | Stats, charts, recent enrollments | — | — | — |
| 👥 **Students** | Table with search & filter | ✅ | ✅ | ✅ |
| 👨‍🏫 **Instructors** | Cards with course count | ✅ | ✅ | ✅ |
| 📚 **Courses** | Cards with enrollment count | ✅ | ✅ | ✅ |
| 🏢 **Departments** | Cards with student/instructor stats | ✅ | ✅ | ✅ |
| 📝 **Enrollments** | Table with semester filter | ✅ | ✅ (Grade) | ✅ |

### Design Highlights
- Premium dark theme with Inter font
- Glassmorphic card layouts
- Interactive bar charts (students per dept, avg grade per course)
- Search & filter capabilities
- Real-time data refresh after every operation

---

© 2026 🐱 برعاية تيم القطة المشمشية

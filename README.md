# University Database Project

## Project Overview
This project involves the design and implementation of a relational database for a university system. The database (`UniversityDB`) tracks departments, students, instructors, courses, and student enrollments.

## Repository Structure

```
├─ /README.md             ← This file
├─ /report.docx           ← Written report (see report.md as well)
├─ /presentation.pptx     ← Slide deck
├─ /video_link.txt        ← Public YouTube/MS Stream URL
├─ /sql/
│    ├─ create_tables.sql ← DDL for schema creation
│    ├─ load_data.sql     ← INSERT scripts (min 10 records/table)
│    ├─ queries.sql       ← Sample retrieval/update queries
│    └─ triggers.sql      ← Database triggers
└─ /src/                  ← UI/application source code (Streamlit Web App)
```

## How to Run

### 1. Database Setup
1. Install [MySQL](https://www.mysql.com/) or a compatible SQL database server.
2. Execute the SQL scripts in the `/sql/` directory in the following order:
   - `create_tables.sql`
   - `load_data.sql`
   - `triggers.sql`
   - `queries.sql` (to test and view results)

### 2. Application UI (Bonus)
The application provides a simple UI to browse and insert data into our database.

1. Ensure you have Python installed.
2. Navigate to the `/src/` folder: `cd src`
3. Install dependencies:
   ```bash
   pip install streamlit mysql-connector-python
   ```
4. Update your database configuration (username and password) in `app.py`.
5. Run the application:
   ```bash
   streamlit run app.py
   ```

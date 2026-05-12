import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

st.set_page_config(page_title="UniversityDB", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*,html,body,[class*="css"]{font-family:'Inter',sans-serif!important}
span[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-icons{font-family:'Material Symbols Rounded','Material Icons'!important;font-size:1.2rem!important}
#MainMenu,footer{visibility:hidden}

/* ── Sidebar toggle button ── */
button[data-testid="stBaseButton-headerNoPadding"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="collapsedControl"],
button[kind="headerNoPadding"] {
    visibility: visible !important;
    display: flex !important;
    color: #a0a0b8 !important;
    background: #16161f !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    border-radius: 8px !important;
    width: 36px !important;
    height: 36px !important;
    align-items: center;
    justify-content: center;
    margin: 0.5rem !important;
    z-index: 999999 !important;
    position: relative !important;
}
button[data-testid="stBaseButton-headerNoPadding"]:hover,
button[data-testid="baseButton-headerNoPadding"]:hover,
button[kind="headerNoPadding"]:hover {
    background: #1e1e2e !important;
    border-color: rgba(99,102,241,.4) !important;
    color: #818cf8 !important;
}
button[data-testid="stBaseButton-headerNoPadding"] svg,
button[data-testid="baseButton-headerNoPadding"] svg,
button[kind="headerNoPadding"] svg {
    fill: currentColor !important;
    stroke: currentColor !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
    visibility: visible !important;
}

.stApp{background:#0c0c14}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{background:#111119!important;border-right:1px solid rgba(255,255,255,.06)!important}
section[data-testid="stSidebar"] label,section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span{color:#a0a0b8!important}
section[data-testid="stSidebar"] .stRadio>div{gap:4px}
section[data-testid="stSidebar"] .stRadio>div>label{border-radius:10px;padding:.6rem 1rem!important;transition:all .15s;margin:2px 0}
section[data-testid="stSidebar"] .stRadio>div>label:hover{background:rgba(99,102,241,.08)}
section[data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"],
section[data-testid="stSidebar"] button[kind="headerNoPadding"]{
    color:#a0a0b8!important;background:transparent!important;border:none!important;
}

.brand{padding:1.5rem .6rem 1.2rem;border-bottom:1px solid rgba(255,255,255,.06);margin-bottom:.6rem;text-align:center}
.brand h1{font-size:1.2rem;font-weight:700;color:#ebebf5;margin:0}.brand p{font-size:.72rem;color:#55556b;margin:.2rem 0 0}
.ph{margin-bottom:1.6rem}.ph h1{font-size:1.65rem;font-weight:700;color:#ebebf5;margin:0}.ph p{font-size:.88rem;color:#6b6b82;margin:.25rem 0 0}
.sg{display:grid;grid-template-columns:repeat(4,1fr);gap:.9rem;margin-bottom:1.8rem}
.sc{background:#16161f;border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:1.2rem 1.3rem;position:relative;overflow:hidden;transition:border-color .2s}
.sc:hover{border-color:rgba(99,102,241,.3)}
.sc .ic{position:absolute;top:1rem;right:1.1rem;font-size:1.5rem;opacity:.25}
.sc .lb{font-size:.72rem;font-weight:600;color:#6b6b82;text-transform:uppercase;letter-spacing:.6px;margin-bottom:.4rem}
.sc .vl{font-size:2rem;font-weight:800;color:#ebebf5}
.cp{background:#16161f;border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:1.3rem 1.4rem;margin-bottom:1.1rem}
.cp h3{font-size:.92rem;font-weight:600;color:#ebebf5;margin:0 0 .9rem;display:flex;align-items:center;gap:.4rem}
.ec{background:#16161f;border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:1.15rem 1.3rem;margin-bottom:.85rem;transition:border-color .2s}
.ec:hover{border-color:rgba(99,102,241,.25)}
.ec .t{font-size:1rem;font-weight:600;color:#ebebf5}.ec .s{font-size:.8rem;color:#6b6b82;margin:.15rem 0 .5rem}
.bd{display:inline-block;font-size:.7rem;font-weight:600;padding:.2rem .55rem;border-radius:6px;margin-right:.35rem}
.bd-p{background:rgba(99,102,241,.12);color:#818cf8}.bd-n{background:rgba(255,255,255,.06);color:#8888a0}
.ec .mt{font-size:.78rem;color:#6b6b82;margin-top:.5rem}
.tip{background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.15);border-radius:12px;padding:.85rem 1.1rem;font-size:.82rem;color:#9090ad;line-height:1.6}
.tip b{color:#818cf8}
.cnt{font-size:.8rem;color:#6b6b82;margin-bottom:.6rem}
.stDataFrame{border-radius:12px!important;overflow:hidden}
.stDataFrame [data-testid="stDataFrameResizable"]{border:1px solid rgba(255,255,255,.06)!important;border-radius:12px!important}
.stFormSubmitButton button,.stButton button{background:linear-gradient(135deg,#6366f1,#4f46e5)!important;color:#fff!important;border:none!important;border-radius:10px!important;font-weight:600!important;font-size:.88rem!important;padding:.6rem 1.8rem!important;transition:all .2s!important;box-shadow:0 4px 14px rgba(99,102,241,.25)!important}
.stFormSubmitButton button:hover,.stButton button:hover{transform:translateY(-1px)!important;box-shadow:0 6px 20px rgba(99,102,241,.35)!important}
.stTextInput input,.stNumberInput input,.stDateInput input{background:rgba(255,255,255,.04)!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:10px!important;color:#ebebf5!important}
.stTextInput input:focus,.stNumberInput input:focus,.stDateInput input:focus{border-color:#6366f1!important;box-shadow:0 0 0 3px rgba(99,102,241,.15)!important}
.stSelectbox [data-baseweb="select"]{border-radius:10px!important}
.stTextInput label,.stNumberInput label,.stDateInput label,.stSelectbox label{color:#a0a0b8!important}

/* ── Tabs with proper spacing ── */
.stTabs [data-baseweb="tab-list"]{gap:8px;border-bottom:1px solid rgba(255,255,255,.06);background:transparent;padding-bottom:0}
.stTabs [data-baseweb="tab"]{color:#6b6b82!important;font-weight:500!important;font-size:.88rem!important;border-bottom:2px solid transparent!important;padding:.65rem 1.2rem!important;margin-bottom:-1px}
.stTabs [aria-selected="true"]{color:#818cf8!important;border-bottom-color:#6366f1!important}

.stSuccess,.stWarning,.stError,.stInfo{border-radius:10px!important}
@media(max-width:768px){.sg{grid-template-columns:repeat(2,1fr)}}
</style>""", unsafe_allow_html=True)

# ═══════════ DB ═══════════
@st.cache_resource
def get_conn():
    return mysql.connector.connect(host='localhost',user='root',password='root',database='UniversityDB')

def q(sql,p=None,fetch=True):
    try:
        c=get_conn();c.ping(reconnect=True,attempts=3,delay=1);cur=c.cursor(dictionary=True);cur.execute(sql,p or())
        if fetch:return cur.fetchall()
        c.commit();return True
    except Exception as e:st.error(f"DB Error: {e}");return None
    finally:
        if 'cur' in locals():cur.close()

def cnt(t):
    r=q(f"SELECT COUNT(*) AS n FROM {t}");return r[0]['n'] if r else 0

# ═══════════ SIDEBAR ═══════════
with st.sidebar:
    st.markdown('<div class="brand"><h1>🎓 UniversityDB</h1><p>Management System</p></div>',unsafe_allow_html=True)
    pages=["📊 Dashboard","👥 Students","👨‍🏫 Instructors","📚 Courses","🏢 Departments","📝 Enrollments"]
    choice=st.radio("Nav",pages,label_visibility="collapsed")
    st.markdown("---")
    st.caption("© 2026 🐱 برعاية تيم القطة المشمشية")

# ═══════════ DASHBOARD ═══════════
if choice=="📊 Dashboard":
    st.markdown('<div class="ph"><h1>📊 Dashboard</h1><p>Real-time overview of your university database</p></div>',unsafe_allow_html=True)
    s,c,i,e=cnt("students"),cnt("courses"),cnt("instructors"),cnt("enrollments")
    d_cnt=cnt("departments")
    st.markdown(f"""<div class="sg">
        <div class="sc"><span class="ic">👥</span><div class="lb">Students</div><div class="vl">{s}</div></div>
        <div class="sc"><span class="ic">📚</span><div class="lb">Courses</div><div class="vl">{c}</div></div>
        <div class="sc"><span class="ic">👨‍🏫</span><div class="lb">Instructors</div><div class="vl">{i}</div></div>
        <div class="sc"><span class="ic">📝</span><div class="lb">Enrollments</div><div class="vl">{e}</div></div>
    </div>""",unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="cp"><h3>📈 Students per Department</h3></div>',unsafe_allow_html=True)
        dd=q("SELECT d.dept_name AS Dept,COUNT(s.student_id) AS Students FROM departments d LEFT JOIN students s ON d.dept_id=s.dept_id GROUP BY d.dept_id,d.dept_name ORDER BY Students DESC")
        if dd:st.bar_chart(pd.DataFrame(dd).set_index("Dept"),color="#6366f1")
    with c2:
        st.markdown('<div class="cp"><h3>📊 Avg Grade per Course</h3></div>',unsafe_allow_html=True)
        gd=q("SELECT c.course_code AS Course,ROUND(AVG(e.grade),1) AS Average FROM courses c JOIN enrollments e ON c.course_id=e.course_id WHERE e.grade IS NOT NULL GROUP BY c.course_id,c.course_code")
        if gd:st.bar_chart(pd.DataFrame(gd).set_index("Course"),color="#6366f1")

    st.markdown('<div class="cp"><h3>🕐 Recent Enrollments</h3></div>',unsafe_allow_html=True)
    rc=q("SELECT CONCAT(s.first_name,' ',s.last_name) AS Student,c.course_title AS Course,e.semester AS Semester,COALESCE(CAST(e.grade AS CHAR),'Pending') AS Grade FROM enrollments e JOIN students s ON e.student_id=s.student_id JOIN courses c ON e.course_id=c.course_id ORDER BY e.enrollment_id DESC LIMIT 5")
    if rc:st.dataframe(pd.DataFrame(rc),use_container_width=True,hide_index=True)

    st.markdown('<div class="tip">💡 <b>Tip:</b> Use the sidebar to navigate. Ensure MySQL is running and <code>load_data.sql</code> executed.</div>',unsafe_allow_html=True)

# ═══════════ STUDENTS ═══════════
elif choice=="👥 Students":
    st.markdown('<div class="ph"><h1>👥 Students</h1><p>Manage student records</p></div>',unsafe_allow_html=True)
    tab1,tab2,tab3,tab4=st.tabs(["📋 View All","➕ Add New","✏️ Edit","🗑️ Delete"])

    with tab1:
        fc1,fc2=st.columns([3,1])
        search=fc1.text_input("🔍",placeholder="Search by name or email...",label_visibility="collapsed",key="ss")
        deps=q("SELECT dept_id,dept_name FROM departments")
        dn=["All"]+([d['dept_name'] for d in deps] if deps else [])
        df=fc2.selectbox("Dept",dn,label_visibility="collapsed",key="sd")
        sql="SELECT s.student_id AS ID,CONCAT(s.first_name,' ',s.last_name) AS Name,s.email AS Email,DATE_FORMAT(s.enrollment_date,'%%Y-%%m-%%d') AS Enrolled,COALESCE(d.dept_name,'—') AS Department FROM students s LEFT JOIN departments d ON s.dept_id=d.dept_id WHERE 1=1"
        p=[]
        if search:sql+=" AND (s.first_name LIKE %s OR s.last_name LIKE %s OR s.email LIKE %s)";p+=[f"%{search}%"]*3
        if df!="All":sql+=" AND d.dept_name=%s";p.append(df)
        sql+=" ORDER BY s.student_id"
        res=q(sql,p)
        if res:
            st.markdown(f'<div class="cnt">{len(res)} student(s)</div>',unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(res),use_container_width=True,hide_index=True)
        else:st.info("No students found.")

    with tab2:
        deps=q("SELECT dept_id,dept_name FROM departments")
        if deps:
            dm={d['dept_name']:d['dept_id'] for d in deps}
            with st.form("add_stu",clear_on_submit=True):
                r1,r2=st.columns(2)
                fn=r1.text_input("First Name",placeholder="e.g. Ahmed")
                ln=r2.text_input("Last Name",placeholder="e.g. Ali")
                em=st.text_input("Email",placeholder="e.g. ahmed@university.edu")
                r3,r4=st.columns(2)
                ed=r3.date_input("Enrollment Date",value=date.today())
                dp=r4.selectbox("Department",list(dm.keys()))
                if st.form_submit_button("✅ Register Student",use_container_width=True):
                    if not fn or not ln or not em:st.warning("⚠️ Fill all fields.")
                    else:
                        ok=q("INSERT INTO students(first_name,last_name,email,enrollment_date,dept_id)VALUES(%s,%s,%s,%s,%s)",(fn,ln,em,ed,dm[dp]),fetch=False)
                        if ok:st.success(f"✅ {fn} {ln} registered!");st.rerun()
        else:st.error("No departments. Set up DB first.")

    with tab3:
        sl=q("SELECT student_id,CONCAT(student_id,' — ',first_name,' ',last_name) AS label FROM students ORDER BY student_id")
        if sl:
            sm3={s['label']:s['student_id'] for s in sl}
            sel=st.selectbox("Select student to edit",list(sm3.keys()),key="edit_stu_sel")
            cur=q("SELECT * FROM students WHERE student_id=%s",(sm3[sel],))
            if cur:
                c=cur[0]
                deps2=q("SELECT dept_id,dept_name FROM departments")
                dm2={d['dept_name']:d['dept_id'] for d in deps2} if deps2 else {}
                with st.form("edit_stu"):
                    r1,r2=st.columns(2)
                    fn=r1.text_input("First Name",value=c['first_name'],key="esfn")
                    ln=r2.text_input("Last Name",value=c['last_name'],key="esln")
                    em=st.text_input("Email",value=c['email'],key="esem")
                    dp_names=list(dm2.keys())
                    cur_idx=dp_names.index(next((k for k,v in dm2.items() if v==c['dept_id']),dp_names[0])) if dp_names and c['dept_id'] else 0
                    dp=st.selectbox("Department",dp_names,index=cur_idx,key="esdp")
                    if st.form_submit_button("✏️ Save Changes",use_container_width=True):
                        ok=q("UPDATE students SET first_name=%s,last_name=%s,email=%s,dept_id=%s WHERE student_id=%s",(fn,ln,em,dm2[dp],sm3[sel]),fetch=False)
                        if ok:st.success("✅ Student updated!");st.rerun()
        else:st.info("No students to edit.")

    with tab4:
        stu_list=q("SELECT student_id,CONCAT(student_id,' — ',first_name,' ',last_name,' (',email,')') AS label FROM students ORDER BY student_id")
        if stu_list:
            sm={s['label']:s['student_id'] for s in stu_list}
            sel=st.selectbox("Select student to delete",list(sm.keys()),key="del_stu")
            st.warning("⚠️ Deleting a student will also remove all their enrollments.")
            if st.button("🗑️ Delete Student",use_container_width=True,key="del_stu_btn"):
                ok=q("DELETE FROM students WHERE student_id=%s",(sm[sel],),fetch=False)
                if ok:st.success("✅ Student deleted!");st.rerun()
        else:st.info("No students to delete.")

# ═══════════ INSTRUCTORS ═══════════
elif choice=="👨‍🏫 Instructors":
    st.markdown('<div class="ph"><h1>👨‍🏫 Instructors</h1><p>Manage instructor records</p></div>',unsafe_allow_html=True)
    tab1,tab2,tab3,tab4=st.tabs(["📋 View All","➕ Add New","✏️ Edit","🗑️ Delete"])

    with tab1:
        ins=q("""SELECT i.instructor_id AS ID,CONCAT(i.first_name,' ',i.last_name) AS Name,
               i.email AS Email,COALESCE(d.dept_name,'—') AS Department,
               COUNT(c.course_id) AS Courses
               FROM instructors i LEFT JOIN departments d ON i.dept_id=d.dept_id
               LEFT JOIN courses c ON i.instructor_id=c.instructor_id
               GROUP BY i.instructor_id,i.first_name,i.last_name,i.email,d.dept_name
               ORDER BY i.instructor_id""")
        if ins:
            st.markdown(f'<div class="cnt">{len(ins)} instructor(s)</div>',unsafe_allow_html=True)
            cols=st.columns(2)
            for idx,x in enumerate(ins):
                with cols[idx%2]:
                    st.markdown(f"""<div class="ec">
                        <div class="t">{x['Name']}</div>
                        <div class="s">✉️ {x['Email']}</div>
                        <div><span class="bd bd-p">{x['Department']}</span><span class="bd bd-n">{x['Courses']} course(s)</span></div>
                    </div>""",unsafe_allow_html=True)
        else:st.info("No instructors found.")

    with tab2:
        deps=q("SELECT dept_id,dept_name FROM departments")
        if deps:
            dm={d['dept_name']:d['dept_id'] for d in deps}
            with st.form("add_ins",clear_on_submit=True):
                r1,r2=st.columns(2)
                fn=r1.text_input("First Name",placeholder="e.g. Dr. Ibrahim",key="ifn")
                ln=r2.text_input("Last Name",placeholder="e.g. Mansour",key="iln")
                em=st.text_input("Email",placeholder="e.g. ibrahim@university.edu",key="iem")
                dp=st.selectbox("Department",list(dm.keys()),key="idp")
                if st.form_submit_button("✅ Add Instructor",use_container_width=True):
                    if not fn or not ln or not em:st.warning("⚠️ Fill all fields.")
                    else:
                        ok=q("INSERT INTO instructors(first_name,last_name,email,dept_id)VALUES(%s,%s,%s,%s)",(fn,ln,em,dm[dp]),fetch=False)
                        if ok:st.success(f"✅ {fn} {ln} added!");st.rerun()
        else:st.error("No departments. Set up DB first.")

    with tab3:
        il2=q("SELECT instructor_id,CONCAT(instructor_id,' — ',first_name,' ',last_name) AS label FROM instructors ORDER BY instructor_id")
        if il2:
            im3={i['label']:i['instructor_id'] for i in il2}
            sel=st.selectbox("Select instructor to edit",list(im3.keys()),key="edit_ins_sel")
            cur=q("SELECT * FROM instructors WHERE instructor_id=%s",(im3[sel],))
            if cur:
                c=cur[0]
                deps2=q("SELECT dept_id,dept_name FROM departments")
                dm2={d['dept_name']:d['dept_id'] for d in deps2} if deps2 else {}
                with st.form("edit_ins"):
                    r1,r2=st.columns(2)
                    fn=r1.text_input("First Name",value=c['first_name'],key="eifn")
                    ln=r2.text_input("Last Name",value=c['last_name'],key="eiln")
                    em=st.text_input("Email",value=c['email'],key="eiem")
                    dp_names=list(dm2.keys())
                    cur_idx=dp_names.index(next((k for k,v in dm2.items() if v==c['dept_id']),dp_names[0])) if dp_names and c['dept_id'] else 0
                    dp=st.selectbox("Department",dp_names,index=cur_idx,key="eidp")
                    if st.form_submit_button("✏️ Save Changes",use_container_width=True):
                        ok=q("UPDATE instructors SET first_name=%s,last_name=%s,email=%s,dept_id=%s WHERE instructor_id=%s",(fn,ln,em,dm2[dp],im3[sel]),fetch=False)
                        if ok:st.success("✅ Instructor updated!");st.rerun()
        else:st.info("No instructors to edit.")

    with tab4:
        il=q("SELECT instructor_id,CONCAT(instructor_id,' — ',first_name,' ',last_name,' (',email,')') AS label FROM instructors ORDER BY instructor_id")
        if il:
            im2={i['label']:i['instructor_id'] for i in il}
            sel=st.selectbox("Select instructor to delete",list(im2.keys()),key="del_ins")
            st.warning("⚠️ Deleting an instructor will unassign their courses.")
            if st.button("🗑️ Delete Instructor",use_container_width=True,key="del_ins_btn"):
                ok=q("DELETE FROM instructors WHERE instructor_id=%s",(im2[sel],),fetch=False)
                if ok:st.success("✅ Instructor deleted!");st.rerun()
        else:st.info("No instructors to delete.")

# ═══════════ COURSES ═══════════
elif choice=="📚 Courses":
    st.markdown('<div class="ph"><h1>📚 Courses</h1><p>Manage course catalog</p></div>',unsafe_allow_html=True)
    tab1,tab2,tab3,tab4=st.tabs(["📋 View All","➕ Add New","✏️ Edit","🗑️ Delete"])

    with tab1:
        cr=q("""SELECT c.course_code AS code,c.course_title AS title,c.credits AS credits,
              COALESCE(CONCAT(i.first_name,' ',i.last_name),'TBA') AS instructor,
              COUNT(e.enrollment_id) AS enrolled
              FROM courses c LEFT JOIN instructors i ON c.instructor_id=i.instructor_id
              LEFT JOIN enrollments e ON c.course_id=e.course_id
              GROUP BY c.course_id,c.course_code,c.course_title,c.credits,i.first_name,i.last_name""")
        if cr:
            st.markdown(f'<div class="cnt">{len(cr)} course(s)</div>',unsafe_allow_html=True)
            cols=st.columns(2)
            for idx,x in enumerate(cr):
                with cols[idx%2]:
                    st.markdown(f"""<div class="ec">
                        <div class="t">{x['title']}</div>
                        <div class="s">{x['code']}</div>
                        <div><span class="bd bd-p">{x['credits']} credits</span><span class="bd bd-n">{x['enrolled']} enrolled</span></div>
                        <div class="mt">👨‍🏫 {x['instructor']}</div>
                    </div>""",unsafe_allow_html=True)
        else:st.info("No courses found.")

    with tab2:
        ins=q("SELECT instructor_id,CONCAT(first_name,' ',last_name) AS name FROM instructors")
        if ins:
            im={i['name']:i['instructor_id'] for i in ins}
            with st.form("add_crs",clear_on_submit=True):
                r1,r2=st.columns(2)
                cc=r1.text_input("Course Code",placeholder="e.g. CS101",key="cc")
                ct=r2.text_input("Course Title",placeholder="e.g. Intro to CS",key="ct")
                r3,r4=st.columns(2)
                cr_n=r3.number_input("Credits",min_value=1,max_value=6,value=3,key="ccr")
                si=r4.selectbox("Instructor",list(im.keys()),key="ci")
                if st.form_submit_button("✅ Add Course",use_container_width=True):
                    if not cc or not ct:st.warning("⚠️ Fill all fields.")
                    else:
                        ok=q("INSERT INTO courses(course_code,course_title,credits,instructor_id)VALUES(%s,%s,%s,%s)",(cc,ct,cr_n,im[si]),fetch=False)
                        if ok:st.success(f"✅ {cc} — {ct} added!");st.rerun()
        else:st.error("No instructors. Add instructors first.")

    with tab3:
        cl2=q("SELECT course_id,CONCAT(course_code,' — ',course_title) AS label FROM courses ORDER BY course_id")
        if cl2:
            cm3={c['label']:c['course_id'] for c in cl2}
            sel=st.selectbox("Select course to edit",list(cm3.keys()),key="edit_crs_sel")
            cur=q("SELECT * FROM courses WHERE course_id=%s",(cm3[sel],))
            if cur:
                c=cur[0]
                ins2=q("SELECT instructor_id,CONCAT(first_name,' ',last_name) AS name FROM instructors")
                im2={i['name']:i['instructor_id'] for i in ins2} if ins2 else {}
                with st.form("edit_crs"):
                    r1,r2=st.columns(2)
                    cc=r1.text_input("Course Code",value=c['course_code'],key="eccc")
                    ct=r2.text_input("Course Title",value=c['course_title'],key="ecct")
                    r3,r4=st.columns(2)
                    cr_n=r3.number_input("Credits",min_value=1,max_value=6,value=c['credits'],key="eccr")
                    i_names=list(im2.keys())
                    cur_idx=i_names.index(next((k for k,v in im2.items() if v==c['instructor_id']),i_names[0])) if i_names and c['instructor_id'] else 0
                    si=r4.selectbox("Instructor",i_names,index=cur_idx,key="ecci")
                    if st.form_submit_button("✏️ Save Changes",use_container_width=True):
                        ok=q("UPDATE courses SET course_code=%s,course_title=%s,credits=%s,instructor_id=%s WHERE course_id=%s",(cc,ct,cr_n,im2[si],cm3[sel]),fetch=False)
                        if ok:st.success("✅ Course updated!");st.rerun()
        else:st.info("No courses to edit.")

    with tab4:
        cl=q("SELECT course_id,CONCAT(course_code,' — ',course_title) AS label FROM courses ORDER BY course_id")
        if cl:
            cm2={c['label']:c['course_id'] for c in cl}
            sel=st.selectbox("Select course to delete",list(cm2.keys()),key="del_crs")
            st.warning("⚠️ Deleting a course will also remove all its enrollments.")
            if st.button("🗑️ Delete Course",use_container_width=True,key="del_crs_btn"):
                ok=q("DELETE FROM courses WHERE course_id=%s",(cm2[sel],),fetch=False)
                if ok:st.success("✅ Course deleted!");st.rerun()
        else:st.info("No courses to delete.")

# ═══════════ DEPARTMENTS ═══════════
elif choice=="🏢 Departments":
    st.markdown('<div class="ph"><h1>🏢 Departments</h1><p>Manage academic departments</p></div>',unsafe_allow_html=True)
    tab1,tab2,tab3,tab4=st.tabs(["📋 View All","➕ Add New","✏️ Edit","🗑️ Delete"])

    with tab1:
        dp=q("""SELECT d.dept_name AS name,d.building AS building,
              COUNT(DISTINCT s.student_id) AS students,COUNT(DISTINCT i.instructor_id) AS instructors
              FROM departments d LEFT JOIN students s ON d.dept_id=s.dept_id
              LEFT JOIN instructors i ON d.dept_id=i.dept_id
              GROUP BY d.dept_id,d.dept_name,d.building""")
        if dp:
            cols=st.columns(2)
            for idx,d in enumerate(dp):
                with cols[idx%2]:
                    st.markdown(f"""<div class="ec">
                        <div class="t">{d['name']}</div>
                        <div class="s">🏗️ {d['building']}</div>
                        <div><span class="bd bd-p">{d['students']} students</span><span class="bd bd-n">{d['instructors']} instructors</span></div>
                    </div>""",unsafe_allow_html=True)
        else:st.info("No departments found.")

    with tab2:
        with st.form("add_dep",clear_on_submit=True):
            dn=st.text_input("Department Name",placeholder="e.g. Computer Science",key="ddn")
            db=st.text_input("Building",placeholder="e.g. Building A",key="ddb")
            if st.form_submit_button("✅ Add Department",use_container_width=True):
                if not dn or not db:st.warning("⚠️ Fill all fields.")
                else:
                    ok=q("INSERT INTO departments(dept_name,building)VALUES(%s,%s)",(dn,db),fetch=False)
                    if ok:st.success(f"✅ {dn} added!");st.rerun()

    with tab3:
        dl2=q("SELECT dept_id,CONCAT(dept_id,' — ',dept_name) AS label FROM departments ORDER BY dept_id")
        if dl2:
            dm3={d['label']:d['dept_id'] for d in dl2}
            sel=st.selectbox("Select department to edit",list(dm3.keys()),key="edit_dep_sel")
            cur=q("SELECT * FROM departments WHERE dept_id=%s",(dm3[sel],))
            if cur:
                c=cur[0]
                with st.form("edit_dep"):
                    dn2=st.text_input("Department Name",value=c['dept_name'],key="eddn")
                    db2=st.text_input("Building",value=c['building'],key="eddb")
                    if st.form_submit_button("✏️ Save Changes",use_container_width=True):
                        ok=q("UPDATE departments SET dept_name=%s,building=%s WHERE dept_id=%s",(dn2,db2,dm3[sel]),fetch=False)
                        if ok:st.success("✅ Department updated!");st.rerun()
        else:st.info("No departments to edit.")

    with tab4:
        dl=q("SELECT dept_id,CONCAT(dept_id,' — ',dept_name,' (',building,')') AS label FROM departments ORDER BY dept_id")
        if dl:
            dm2={d['label']:d['dept_id'] for d in dl}
            sel=st.selectbox("Select department to delete",list(dm2.keys()),key="del_dep")
            st.warning("⚠️ Deleting a department will unassign its students and instructors.")
            if st.button("🗑️ Delete Department",use_container_width=True,key="del_dep_btn"):
                ok=q("DELETE FROM departments WHERE dept_id=%s",(dm2[sel],),fetch=False)
                if ok:st.success("✅ Department deleted!");st.rerun()
        else:st.info("No departments to delete.")

# ═══════════ ENROLLMENTS ═══════════
elif choice=="📝 Enrollments":
    st.markdown('<div class="ph"><h1>📝 Enrollments</h1><p>Manage student enrollments and grades</p></div>',unsafe_allow_html=True)
    tab1,tab2,tab3,tab4=st.tabs(["📋 View All","➕ New Enrollment","✏️ Update Grade","🗑️ Delete"])

    # Predefined semester options
    semester_options=["Fall 2024","Spring 2025","Summer 2025","Fall 2025","Spring 2026","Summer 2026","Fall 2026"]

    with tab1:
        sem_filter=st.selectbox("Filter by Semester",["All Semesters"]+[r['semester'] for r in (q("SELECT DISTINCT semester FROM enrollments ORDER BY semester") or [])],key="ef")
        sql="SELECT e.enrollment_id AS ID,CONCAT(s.first_name,' ',s.last_name) AS Student,c.course_code AS Code,c.course_title AS Course,e.semester AS Semester,COALESCE(CAST(e.grade AS CHAR),'—') AS Grade FROM enrollments e JOIN students s ON e.student_id=s.student_id JOIN courses c ON e.course_id=c.course_id"
        p=[]
        if sem_filter!="All Semesters":sql+=" WHERE e.semester=%s";p.append(sem_filter)
        sql+=" ORDER BY e.enrollment_id DESC"
        en=q(sql,p)
        if en:
            st.markdown(f'<div class="cnt">{len(en)} enrollment(s)</div>',unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(en),use_container_width=True,hide_index=True)
        else:st.info("No enrollments found.")

    with tab2:
        stu=q("SELECT student_id,CONCAT(first_name,' ',last_name) AS name FROM students")
        crs=q("SELECT course_id,CONCAT(course_code,' — ',course_title) AS name FROM courses")
        if stu and crs:
            sm={s['name']:s['student_id'] for s in stu}
            cm={c['name']:c['course_id'] for c in crs}
            with st.form("add_enr",clear_on_submit=True):
                r1,r2=st.columns(2)
                ss=r1.selectbox("Student",list(sm.keys()),key="es")
                sc=r2.selectbox("Course",list(cm.keys()),key="ec")
                r3,r4=st.columns(2)
                sem=r3.selectbox("Semester",semester_options,key="esm")
                gr=r4.number_input("Grade (0 = no grade yet)",min_value=0.0,max_value=100.0,value=0.0,step=0.5,key="eg")
                if st.form_submit_button("✅ Enroll",use_container_width=True):
                    g=gr if gr>0 else None
                    ok=q("INSERT INTO enrollments(student_id,course_id,semester,grade)VALUES(%s,%s,%s,%s)",(sm[ss],cm[sc],sem,g),fetch=False)
                    if ok:
                        st.success("✅ Enrollment recorded!")
                        st.rerun()
        else:st.info("Add students and courses first.")

    with tab3:
        en_list=q("""SELECT e.enrollment_id,
                     CONCAT(s.first_name,' ',s.last_name,' → ',c.course_code,' (',e.semester,') — Grade: ',COALESCE(CAST(e.grade AS CHAR),'N/A')) AS label
                     FROM enrollments e JOIN students s ON e.student_id=s.student_id
                     JOIN courses c ON e.course_id=c.course_id ORDER BY e.enrollment_id DESC""")
        if en_list:
            em={e['label']:e['enrollment_id'] for e in en_list}
            with st.form("upd_gr",clear_on_submit=True):
                sel=st.selectbox("Select Enrollment",list(em.keys()),key="ug_sel")
                ng=st.number_input("New Grade",min_value=0.0,max_value=100.0,value=0.0,step=0.5,key="ug_gr")
                if st.form_submit_button("✏️ Update Grade",use_container_width=True):
                    if ng<=0:st.warning("⚠️ Enter a valid grade (1–100).")
                    else:
                        ok=q("UPDATE enrollments SET grade=%s WHERE enrollment_id=%s",(ng,em[sel]),fetch=False)
                        if ok:
                            st.success(f"✅ Grade updated to {ng}!")
                            st.rerun()
        else:st.info("No enrollments to update.")

    with tab4:
        del_list=q("""SELECT e.enrollment_id,
                      CONCAT(s.first_name,' ',s.last_name,' → ',c.course_code,' (',e.semester,') — Grade: ',COALESCE(CAST(e.grade AS CHAR),'N/A')) AS label
                      FROM enrollments e JOIN students s ON e.student_id=s.student_id
                      JOIN courses c ON e.course_id=c.course_id ORDER BY e.enrollment_id DESC""")
        if del_list:
            em2={e['label']:e['enrollment_id'] for e in del_list}
            sel=st.selectbox("Select enrollment to delete",list(em2.keys()),key="del_enr")
            st.warning("⚠️ This will permanently remove this enrollment record.")
            if st.button("🗑️ Delete Enrollment",use_container_width=True,key="del_enr_btn"):
                ok=q("DELETE FROM enrollments WHERE enrollment_id=%s",(em2[sel],),fetch=False)
                if ok:st.success("✅ Enrollment deleted!");st.rerun()
        else:st.info("No enrollments to delete.")

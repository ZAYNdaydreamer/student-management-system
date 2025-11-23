import streamlit as st
import pandas as pd
from typing import Tuple
from models.student import Student

def validate_student_input(name: str, age: int, grade: str, email: str, gpa: float) -> Tuple[bool, str]:
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters."
    if not isinstance(age, int) or age < 3 or age > 120:
        return False, "Age must be an integer between 3 and 120."
    if not grade or len(grade.strip()) == 0:
        return False, "Grade is required."
    if email and "@" not in email:
        return False, "Email must be valid if provided."
    if not isinstance(gpa, (int, float)) or gpa < 0.0 or gpa > 4.0:
        return False, "GPA must be between 0.0 and 4.0."
    return True, ""

def render_sidebar():
    st.sidebar.header("Actions")
    action = st.sidebar.radio("Choose action", ("List", "Add", "Update", "Delete", "Search"))
    return action

def render_main(action: str, manager):
    if action == "List":
        students = manager.list_students()
        df = pd.DataFrame([s.to_dict() for s in students])
        st.subheader("All students")
        st.dataframe(df)
        st.success(f"Total students: {len(df)}")

    elif action == "Add":
        st.subheader("Add student")
        with st.form("add_form"):
            name = st.text_input("Full name")
            age = st.number_input("Age", min_value=3, max_value=120, value=18, step=1)
            grade = st.text_input("Grade (e.g., 10, A-level)")
            email = st.text_input("Email (optional)")
            gpa = st.number_input("GPA", min_value=0.0, max_value=4.0, value=0.0, step=0.1, format="%.2f")
            notes = st.text_area("Notes (optional)")
            submitted = st.form_submit_button("Add")
            if submitted:
                ok, msg = validate_student_input(name, int(age), grade, email, float(gpa))
                if not ok:
                    st.error(msg)
                else:
                    student = manager.add_student({
                        "name": name.strip(),
                        "age": int(age),
                        "grade": grade.strip(),
                        "email": email.strip() or None,
                        "gpa": float(gpa),
                        "notes": notes.strip() or None
                    })
                    st.success(f"Student added with ID {student.id}")

    elif action == "Update":
        st.subheader("Update student")
        sid = st.number_input("Student ID to update", min_value=1, step=1)
        if st.button("Load"):
            s = manager.get_student(int(sid))
            if not s:
                st.error("Student not found.")
            else:
                with st.form("update_form"):
                    name = st.text_input("Full name", value=s.name)
                    age = st.number_input("Age", min_value=3, max_value=120, value=s.age, step=1)
                    grade = st.text_input("Grade", value=s.grade)
                    email = st.text_input("Email", value=s.email or "")
                    gpa = st.number_input("GPA", min_value=0.0, max_value=4.0, value=s.gpa, step=0.01, format="%.2f")
                    notes = st.text_area("Notes", value=s.notes or "")
                    submitted = st.form_submit_button("Update")
                    if submitted:
                        ok, msg = validate_student_input(name, int(age), grade, email, float(gpa))
                        if not ok:
                            st.error(msg)
                        else:
                            updated = manager.update_student(s.id, {
                                "name": name.strip(),
                                "age": int(age),
                                "grade": grade.strip(),
                                "email": email.strip() or None,
                                "gpa": float(gpa),
                                "notes": notes.strip() or None
                            })
                            if updated:
                                st.success("Student updated.")
                            else:
                                st.error("Update failed.")

    elif action == "Delete":
        st.subheader("Delete student")
        sid = st.number_input("Student ID to delete", min_value=1, step=1)
        if st.button("Delete"):
            ok = manager.delete_student(int(sid))
            if ok:
                st.success("Student deleted.")
            else:
                st.error("Student not found.")

    elif action == "Search":
        st.subheader("Search & Filter")
        cols = st.columns(4)
        q = cols[0].text_input("Keyword (name or id)")
        grade = cols[1].text_input("Grade")
        min_age = cols[2].number_input("Min age", min_value=0, value=0, step=1)
        max_age = cols[3].number_input("Max age", min_value=0, value=0, step=1)
        cols2 = st.columns(2)
        min_gpa = cols2[0].number_input("Min GPA", min_value=0.0, max_value=4.0, value=0.0, step=0.01, format="%.2f")
        max_gpa = cols2[1].number_input("Max GPA", min_value=0.0, max_value=4.0, value=4.0, step=0.01, format="%.2f")
        if st.button("Run search"):
            min_age_val = None if min_age == 0 else int(min_age)
            max_age_val = None if max_age == 0 else int(max_age)
            results = manager.search(q=q, grade=grade, min_age=min_age_val, max_age=max_age_val,
                                     min_gpa=min_gpa, max_gpa=max_gpa)
            df = pd.DataFrame([r.to_dict() for r in results])
            st.dataframe(df)
            st.success(f"Found {len(df)} result(s).")
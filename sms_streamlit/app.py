import streamlit as st
from ui.components import render_sidebar, render_main
from services.manager import StudentManager

DATA_FILE = "data/students.json"

def main():
    st.set_page_config(page_title="Student Management System", layout="wide")
    st.title("📚 Student Management System")
    manager = StudentManager(DATA_FILE)

    action = render_sidebar()
    render_main(action, manager)

if __name__ == "__main__":
    main()
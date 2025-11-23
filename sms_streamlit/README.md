# Student Management System (Streamlit + Python OOP)

## Overview
This is a simple Student Management System built with Python OOP principles and a Streamlit UI.
It supports CRUD operations, JSON storage, search/filtering, and input validation.

## Project structure
- `app.py` - Streamlit entry point
- `models/student.py` - Student dataclass model
- `services/manager.py` - StudentManager for CRUD + storage (JSON)
- `ui/components.py` - Streamlit UI components and validation
- `data/students.json` - Sample data file
- `requirements.txt` - Python dependencies

## Setup
1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```

## Notes
- Data is stored in `data/students.json`. The manager creates the file if it does not exist.
- Code is modular under `models`, `services`, and `ui`.
- Input validation is implemented in `ui/components.py`.
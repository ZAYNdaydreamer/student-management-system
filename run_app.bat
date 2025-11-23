@echo off
REM ===========================
REM Student Management System Run Script
REM ===========================

REM Change directory to the folder of this script
cd /d "%~dp0"

REM Run Streamlit app
"C:\Program Files\Python311\python.exe" -m streamlit run app.py

pause

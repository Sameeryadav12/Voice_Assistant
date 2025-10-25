@echo off
:: Quick Launch Script for Jarvis Voice Assistant Professional UI
:: Double-click this file to run the assistant!

echo ====================================
echo Jarvis Voice Assistant - Professional Edition
echo ====================================
echo.
echo Starting the assistant...
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
python main_professional_ui.py

pause


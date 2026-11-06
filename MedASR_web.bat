@echo off
title MedASR Web Dictation
cd /d C:\medasr
call env\Scripts\activate.bat
python dictate_web.py
echo.
pause

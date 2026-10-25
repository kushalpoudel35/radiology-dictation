@echo off
title MedASR Dictation
cd /d C:\medasr
call env\Scripts\activate.bat
python dictate.py
echo.
pause

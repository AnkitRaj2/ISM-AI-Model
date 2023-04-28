@echo off
:loop
python linear_regression.py
timeout /t 15 >nul
goto loop
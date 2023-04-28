@echo off
:loop
python linear_regression.py
timeout /t 5 >nul
goto loop
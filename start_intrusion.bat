@echo off

rem Path to your virtual environment activation script (adjust as needed)
set venv_activate="C:\Users\mitch\onedrive\opencv\opencv_for_beginners\opencv-env\Scripts\activate"

:loop
echo Starting Intrusion_Detection.py at %time%

call %venv_activate%  
python Intrusion_Detection.py

timeout /t 60

rem Get the PID (process ID) of the Intrusion_Detection.py process
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV ^| findstr "Intrusion_Detection.py"') do set PID=%%a

rem Kill the app.py process using its PID
taskkill /f /pid %PID% >nul 2>&1

echo Intrusion_Detection.py stopped at %time%
deactivate

goto loop
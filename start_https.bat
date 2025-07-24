@echo off
echo.
echo ===============================================
echo  🔐 Norshel Secure Servers Startup
echo  (HTTPS + HTTP Redirect)
echo ===============================================
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Activate virtual environment and start both servers
call venv\Scripts\activate.bat
python start_secure_servers.py

pause 
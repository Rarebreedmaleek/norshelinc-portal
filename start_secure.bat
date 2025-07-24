@echo off
echo.
echo ===============================================
echo  🔐 Norshel Secure Servers
echo ===============================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo 🔒 Starting HTTPS server on port 8443...
start "HTTPS Server" cmd /k "venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8443 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem --reload"

echo 🔄 Waiting 5 seconds for HTTPS server to start...
timeout /t 5 /nobreak >nul

echo 🔄 Starting HTTP redirect server on port 8000...
start "HTTP Redirect" cmd /k "venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

echo.
echo ✅ Both servers are starting in separate windows:
echo    🔒 HTTPS: https://localhost:8443
echo    🔄 HTTP:  http://localhost:8000 (redirects to HTTPS)
echo.
echo ⚠️  Browser Security Notice:
echo    Your browser will show a security warning for the self-signed certificate.
echo    Click 'Advanced' and 'Proceed to localhost' to continue.
echo.
echo 📋 Available pages:
echo    • https://localhost:8443/ (Home)
echo    • https://localhost:8443/login (Parent Login)
echo    • https://localhost:8443/dashboard (Dashboard)
echo.
echo Close this window or press any key to continue...
pause >nul 
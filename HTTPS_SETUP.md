# 🔐 HTTPS Setup for Norshel Web Application

## Overview
Your Norshel web application now supports secure HTTPS connections with automatic HTTP to HTTPS redirection.

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)
Double-click the `start_secure.bat` file in the project root. This will:
- Generate SSL certificates if needed
- Start HTTPS server on port 8443
- Start HTTP redirect server on port 8000

### Option 2: Manual Setup

1. **Activate Virtual Environment**
   ```cmd
   venv\Scripts\activate.bat
   ```

2. **Start HTTPS Server** (in first terminal)
   ```cmd
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8443 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem --reload
   ```

3. **Start HTTP Redirect Server** (in second terminal)
   ```cmd
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```

## 🔗 Access URLs

- **HTTPS (Primary)**: https://localhost:8443
- **HTTP (Redirects to HTTPS)**: http://localhost:8000

### Available Pages:
- 🏠 **Home**: https://localhost:8443/
- 🔐 **Login**: https://localhost:8443/login
- 📊 **Dashboard**: https://localhost:8443/dashboard
- 📋 **Programs**: https://localhost:8443/programs
- 📞 **Contact**: https://localhost:8443/contact

## ⚠️ Browser Security Warning

Since we use self-signed certificates for development, your browser will show a security warning:

1. Click **"Advanced"**
2. Click **"Proceed to localhost (unsafe)"**
3. Your site will then load securely with HTTPS! 🔒

## 🔧 Security Features

✅ **SSL/TLS Encryption**: All data encrypted in transit  
✅ **HTTP → HTTPS Redirect**: Automatic redirect for security  
✅ **Security Headers**: XSS, CSRF, and clickjacking protection  
✅ **Content Security Policy**: Prevents code injection attacks  
✅ **Strict Transport Security**: Forces HTTPS connections  

## 🛠️ Troubleshooting

### Port Already in Use
If you get a "port already in use" error:
```cmd
# Kill any existing Python processes
taskkill /F /IM python.exe

# Or find and kill specific process
netstat -ano | findstr :8443
taskkill /F /PID [PID_NUMBER]
```

### Certificate Issues
If SSL certificates are missing or corrupted:
```cmd
# Delete existing certificates
rmdir /s certs

# Run the server - it will regenerate certificates automatically
python start_https_server.py
```

### Testing HTTP Redirect
1. Open browser to http://localhost:8000
2. You should automatically be redirected to https://localhost:8443
3. Check the address bar - it should show HTTPS with a lock icon

## 📝 Login Credentials

For testing the parent dashboard:
- **Email**: parent1@norshel.com
- **Password**: norshel

## 🔒 Production Deployment

For production deployment:
1. Obtain a real SSL certificate from a Certificate Authority (Let's Encrypt, etc.)
2. Update the certificate paths in the configuration
3. Use a reverse proxy like Nginx for better performance
4. Enable firewall rules for ports 80 (HTTP) and 443 (HTTPS)

## 🆘 Support

If you encounter any issues:
1. Check that both servers are running on their respective ports
2. Verify SSL certificates exist in the `certs/` directory
3. Ensure virtual environment is activated
4. Check firewall/antivirus isn't blocking the ports

---
**Your Norshel web application is now secure with HTTPS! 🎉** 
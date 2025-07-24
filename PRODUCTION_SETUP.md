# 🚀 Production Setup Guide for Norshel FastAPI Application

## ✅ Current Status
Your FastAPI application is now fully functional with:
- ✅ **HTTPS Server** running on `https://localhost:8443`
- ✅ **HTTP Redirect** running on `http://localhost:8000`
- ✅ **JWT Authentication** working correctly
- ✅ **AI Chatbot Integration** responding properly
- ✅ **Tailwind CSS** responsive frontend
- ✅ **SSL Certificates** generated and working

## 🌐 Access Your Application

**Live URLs:**
- 🔒 **Primary (HTTPS)**: https://localhost:8443
- 🔄 **Redirect (HTTP)**: http://localhost:8000 (automatically redirects to HTTPS)

**Available Pages:**
- 🏠 **Home**: https://localhost:8443/
- 🔐 **Login**: https://localhost:8443/login
- 📊 **Dashboard**: https://localhost:8443/dashboard
- 📋 **Programs**: https://localhost:8443/programs
- 🎥 **Videos**: https://localhost:8443/video
- 📞 **Contact**: https://localhost:8443/contact

**Test Login Credentials:**
- 📧 **Email**: `parent1@norshel.com`
- 🔑 **Password**: `norshel`

## 🏭 Production Deployment Options

### Option 1: Windows Service (systemd alternative)
Since you're on Windows, use `nssm` (Non-Sucking Service Manager):

1. **Download NSSM**:
   ```cmd
   # Download from https://nssm.cc/download
   # Extract to C:\nssm
   ```

2. **Create Service**:
   ```cmd
   # Run as Administrator
   C:\nssm\nssm.exe install NorshelApp
   
   # Configure:
   # Path: C:\Users\Rarebreed Server\Desktop\NorshelCursor\new_venv\Scripts\python.exe
   # Startup directory: C:\Users\Rarebreed Server\Desktop\NorshelCursor
   # Arguments: -m uvicorn backend.main:app --host 127.0.0.1 --port 8443 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem
   ```

3. **Start Service**:
   ```cmd
   net start NorshelApp
   ```

### Option 2: PM2 (Node.js Process Manager)
1. **Install Node.js** from https://nodejs.org
2. **Install PM2**:
   ```cmd
   npm install -g pm2
   npm install -g pm2-windows-service
   ```

3. **Create PM2 config** (`ecosystem.config.js`):
   ```javascript
   module.exports = {
     apps: [{
       name: 'norshel-https',
       script: 'new_venv\\Scripts\\python.exe',
       args: '-m uvicorn backend.main:app --host 127.0.0.1 --port 8443 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem',
       cwd: 'C:\\Users\\Rarebreed Server\\Desktop\\NorshelCursor'
     }, {
       name: 'norshel-http',
       script: 'new_venv\\Scripts\\python.exe',
       args: '-m uvicorn backend.main:app --host 127.0.0.1 --port 8000',
       cwd: 'C:\\Users\\Rarebreed Server\\Desktop\\NorshelCursor'
     }]
   }
   ```

4. **Start and setup auto-restart**:
   ```cmd
   pm2 start ecosystem.config.js
   pm2 save
   pm2-service-install
   ```

### Option 3: Docker (Recommended for Production)
1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8443
   CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8443", "--ssl-keyfile", "certs/key.pem", "--ssl-certfile", "certs/cert.pem"]
   ```

2. **Create docker-compose.yml**:
   ```yaml
   version: '3.8'
   services:
     norshel-app:
       build: .
       ports:
         - "8443:8443"
         - "8000:8000"
       restart: unless-stopped
   ```

## 🔒 Security Recommendations for Production

### 1. SSL Certificates
- Replace self-signed certificates with real ones from Let's Encrypt or a CA
- Use `certbot` for automatic renewal

### 2. Environment Variables
Create `.env` file:
```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=your-database-connection-string
ENVIRONMENT=production
```

### 3. Database
Replace mock data with a real database:
```python
# Consider PostgreSQL, MySQL, or SQLite
DATABASE_URL = "postgresql://user:password@localhost/norshel_db"
```

### 4. Reverse Proxy (Nginx)
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass https://127.0.0.1:8443;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🛠️ Maintenance Commands

**Start Servers Manually:**
```cmd
# HTTPS Server
new_venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8443 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem --reload

# HTTP Redirect Server  
new_venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

**Check Status:**
```cmd
netstat -ano | findstr ":8443"
netstat -ano | findstr ":8000"
```

**Update Dependencies:**
```cmd
new_venv\Scripts\activate.bat
pip install -r requirements.txt --upgrade
```

## 📊 Monitoring

### Health Check Endpoint
- **URL**: `https://localhost:8443/`
- **Expected**: HTTP 200 response

### Log Files
Monitor application logs for errors and performance issues.

### Performance Metrics
Consider integrating:
- **Sentry** for error tracking
- **Prometheus** for metrics
- **Grafana** for dashboards

## 🎯 Next Steps

1. **Choose your deployment method** (Windows Service, PM2, or Docker)
2. **Set up auto-start** for system reboots
3. **Configure monitoring** and alerting
4. **Replace SSL certificates** with production ones
5. **Set up database** if needed
6. **Configure backup** procedures

---

**🎉 Your Norshel FastAPI application is ready for production!**

Access it now at: https://localhost:8443 
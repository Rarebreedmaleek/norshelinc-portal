# 🚀 Deploy to Railway - Step by Step Guide

## 📋 Prerequisites
- GitHub account
- Railway account (free at [railway.app](https://railway.app))

## 🎯 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. **Go to GitHub** and create a new repository
2. **Name it**: `norshel-parent-portal`
3. **Make it public** (Railway works better with public repos)
4. **Don't initialize** with README (we already have files)

### Step 2: Push Your Code to GitHub

```bash
# In your project directory, run these commands:
git init
git add .
git commit -m "Initial commit - Norshel Parent Portal"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/norshel-parent-portal.git
git push -u origin main
```

### Step 3: Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**: `norshel-parent-portal`
6. **Railway will automatically detect** it's a Python app
7. **Click "Deploy"**

### Step 4: Configure Environment Variables

In Railway dashboard:
1. **Go to your project**
2. **Click "Variables" tab**
3. **Add these environment variables**:

```env
ENVIRONMENT=production
SECRET_KEY=your-super-secret-production-key-here-make-it-long-and-random
```

### Step 5: Get Your Live URL

1. **Railway will provide a URL** like: `https://your-app-name.railway.app`
2. **Test your application** by visiting the URL
3. **Verify all features work**:
   - Home page loads
   - Login works
   - Dashboard displays
   - Chatbot responds

## 🔧 Troubleshooting

### If deployment fails:

1. **Check logs** in Railway dashboard
2. **Common issues**:
   - Missing dependencies in `requirements.txt`
   - Wrong Python version in `runtime.txt`
   - Import errors in code

### If app doesn't start:

1. **Check Procfile** is correct
2. **Verify port configuration** uses `$PORT`
3. **Check environment variables** are set

## 🌐 Custom Domain (Optional)

1. **In Railway dashboard**, go to "Settings"
2. **Click "Domains"**
3. **Add your custom domain**
4. **Update DNS** to point to Railway's servers

## 📊 Monitoring

1. **Check Railway dashboard** for:
   - Uptime status
   - Response times
   - Error logs
2. **Set up alerts** for downtime

## 🎉 Success!

Your Norshel Parent Portal is now live at:
**https://your-app-name.railway.app**

### Test Credentials:
- **Email**: `parent1@norshel.com`
- **Password**: `norshel`

---

**Need help?** Check Railway's documentation or contact their support! 
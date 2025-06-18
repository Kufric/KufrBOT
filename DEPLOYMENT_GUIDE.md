# Quick Deployment Guide for KufrBOT

## Step 1: Download Your Project
1. In Replit, click the three dots menu (⋯) at top left
2. Click "Download as ZIP"
3. Extract the ZIP file on your computer

## Step 2: Upload to GitHub
1. Go to [github.com](https://github.com) and sign in (create account if needed)
2. Click the green "New" button to create a new repository
3. Name it "kufrbot" or any name you like
4. Make it Public (required for free Railway deployment)
5. Click "Create repository"
6. On the next page, scroll down to "uploading an existing file"
7. Drag and drop ALL your project files (or click "choose your files")
8. Important files to include:
   - main.py
   - bot.py
   - config.py
   - railway.json
   - Procfile
   - requirements.txt
   - runtime.txt
   - templates/ folder
   - static/ folder
9. Write commit message: "Initial KufrBOT setup"
10. Click "Commit new files"

## Step 3: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Click "New Project"
4. Click "Deploy from GitHub repo"
5. Select your kufrbot repository
6. Railway will automatically detect it's a Python project
7. After deployment starts, click on your project
8. Go to "Variables" tab
9. Add these environment variables:
   - Key: `TWITCH_TOKEN` Value: `oauth:your_token_here`
   - Key: `APEX_API_KEY` Value: `your_api_key_here`
10. Click "Deploy" 

## Step 4: Get Your Bot URL
- Railway will give you a URL like `https://kufrbot-production.up.railway.app`
- Your bot will be running 24/7 at this URL
- The dashboard will be accessible via the web

## Troubleshooting
- If deployment fails, check the logs in Railway dashboard
- Make sure both environment variables are set correctly
- Your Twitch token should start with "oauth:"

Your bot will automatically restart if it crashes and stay online 24/7!
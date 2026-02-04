# Deployment Guide

## ⚠️ Important Note on Vercel

You requested to deploy this project to **Vercel**. However, this is a **Streamlit** application, which requires a persistent server (WebSocket connection). 

**Vercel is designed for serverless functions and static sites.** It does not natively support long-running Python processes like Streamlit. While technical workarounds exist, they are often unstable, slow, or have timeout issues (Vercel functions time out after 10-60 seconds).

## ✅ Recommended Alternatives

We recommend deploying to platforms that support Docker or persistent Python apps:
- **Streamlit Cloud** (Easiest, free tier available)
- **Railway** (Recommended, automated)
- **Render** (Good alternative)
- **Fly.io**

## Option 1: Railway (Recommended)

Railway automatically detects the `Dockerfile` we created.

1. Create an account at [railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select this repository.
4. Add your Environment Variables:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY` (if used)
5. Deploy.

## Option 2: Render

1. Create an account at [render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repo.
4. Select **Docker** as the Runtime (it will auto-detect the Dockerfile).
5. Add Environment Variables.
6. Deploy.

## Option 3: Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Connect your GitHub account.
3. Select this repository.
4. Main file path: `app.py`
5. Click **Advanced Settings** to add secrets (`OPENAI_API_KEY`).
6. Deploy.

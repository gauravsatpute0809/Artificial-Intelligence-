# 🚀 Deployment Guide for Engineering Hospital System

This project is now ready to be deployed on **Render**. Follow these steps:

## Prerequisites
1. Push your code to a **GitHub** or **GitLab** repository.
2. Sign up for a [Render](https://render.com) account.

## Option 1: Automatic Deployment (Recommended)
Render supports **Blueprints**, which use the included `render.yaml` file to configure everything for you.

1. Go to your [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub repository.
4. Render will automatically detect the `render.yaml` and set up the Web Service.

## Option 2: Manual Deployment
If you prefer to set it up manually:

1. Click **New +** and select **Web Service**.
2. Connect your repository.
3. Select **Python** as the Runtime.
4. Set the following configurations:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn --chdir backend app:app`
5. Add an **Environment Variable**:
   - `PORT`: `5000` (or any port you prefer)

## What's Changed for Deployment?
- **Unified Serving:** The Flask backend now serves the built frontend files from `frontend/dist`.
- **Relative URLs:** API calls in the frontend now use relative paths (e.g., `/chat` instead of `http://localhost:5000/chat`), so it works on any domain.
- **Build Script:** Provided `build.sh` which installs both Python and Node.js dependencies and builds the UI.
- **Database:** The SQLite database is automatically initialized during the build process.

## Local Testing (After the changes)
You can still run the app locally using your `run_all.py` script as before.
If you want to test the production build locally:
1. `cd frontend && npm run build`
2. `cd .. && python backend/app.py`
3. Open `http://localhost:5000`

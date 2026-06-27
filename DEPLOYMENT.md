# 🚀 Deployment Guide

This guide walks you through deploying the **AI Cooking To-Do List** app to production. We cover two popular platforms — **Railway** and **Render** — with step-by-step instructions.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] You have a **Google Gemini API key** (get one at [Google AI Studio](https://aistudio.google.com/apikey))
- [ ] The app runs locally (`python main.py` → visit `http://localhost:8000`)
- [ ] All 23 tests pass (`python -m pytest tests/ -v`)
- [ ] No API keys or secrets are committed to your code
- [ ] The `.env` file is in your `.gitignore` (never deploy secrets in code!)

---

## 📦 Prepare Your Repository

### 1. Initialize Git (if not already done)

```bash
cd cooking-todo-app
git init
```

### 2. Create a `.gitignore`

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
*.egg-info/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Tool versions
.tool-versions
EOF
```

### 3. Commit Your Code

```bash
git add .
git commit -m "Initial commit: AI Cooking To-Do List"
```

### 4. Push to GitHub

```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/cooking-todo-app.git
git branch -M main
git push -u origin main
```

---

## 🚂 Option A: Deploy to Railway

[Railway](https://railway.app) offers fast deployments with a generous free tier.

### Step 1 — Create an Account

1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account

### Step 2 — Create a New Project

1. Click **"New Project"** on the dashboard
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your repository
4. Select your `cooking-todo-app` repository

### Step 3 — Configure Environment Variables

1. In your project, go to the **"Variables"** tab
2. Click **"+ New Variable"**
3. Add the following:

   | Variable | Value |
   |----------|-------|
   | `GEMINI_API_KEY` | `your_actual_gemini_api_key` |

   > ⚠️ **Never put your real API key in code!** Always use environment variables.

### Step 4 — Configure Build Settings

Railway auto-detects Python projects. Verify these settings under **"Settings"**:

| Setting | Value |
|---------|-------|
| **Builder** | Nixpacks (default) |
| **Start Command** | Automatically reads from `Procfile` |
| **Root Directory** | `/` (default) |

The `Procfile` already contains:
```
web: uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### Step 5 — Deploy

1. Railway will automatically trigger a deployment
2. Watch the build logs for any errors
3. Once deployed, Railway provides a public URL (e.g., `https://your-app.up.railway.app`)

### Step 6 — Verify

1. Open your Railway-provided URL in a browser
2. Fill in the form and click **"Generate Meal Plan"**
3. Confirm the meal plan, grocery list, substitutions, and budget breakdown all render correctly

---

## 🎨 Option B: Deploy to Render

[Render](https://render.com) offers free tier web services with automatic deploys.

### Step 1 — Create an Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account

### Step 2 — Create a New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select your `cooking-todo-app` repository

### Step 3 — Configure Build & Deploy Settings

Fill in the following:

| Setting | Value |
|---------|-------|
| **Name** | `ai-cooking-todo-list` (or your choice) |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free (or your choice) |

### Step 4 — Set Environment Variables

1. Scroll down to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Add:

   | Key | Value |
   |-----|-------|
   | `GEMINI_API_KEY` | `your_actual_gemini_api_key` |
   | `PYTHON_VERSION` | `3.12.0` |

### Step 5 — Deploy

1. Click **"Create Web Service"**
2. Render will build and deploy your app
3. The build typically takes 2-3 minutes

### Step 6 — Verify

1. Render provides a URL like `https://ai-cooking-todo-list.onrender.com`
2. Open it and test all features
3. Check the **"Logs"** tab if anything isn't working

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| **App loads but no styles** | Static file path issue | Ensure `static/` folder is included in the deployment |
| **"Internal Server Error" on generate** | Missing or invalid API key | Check that `GEMINI_API_KEY` is set correctly in environment variables |
| **Build fails** | Python version mismatch | Set `PYTHON_VERSION=3.12.0` in environment variables |
| **App shows blank page** | Missing `static/index.html` | Verify all files in `static/` are committed to git |
| **Timeout errors** | Gemini API latency | The app has a 30-second timeout; this is normal for the first request |

### Checking Logs

**Railway:**
- Go to your project → **"Logs"** tab
- Filter by **"Service"** to see application logs

**Render:**
- Go to your service → **"Logs"** tab
- Check for Python exceptions or HTTP errors

### Health Check

Both platforms support health checks. The app provides a health endpoint:

```bash
curl https://your-app-url.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AI Cooking To-Do List",
  "timestamp": "2026-06-27T05:30:00+00:00"
}
```

---

## 🔒 Security Notes

1. **Never commit `.env` files** — They contain your API key
2. **API key rotation** — If you suspect your key is compromised, regenerate it at [Google AI Studio](https://aistudio.google.com/apikey)
3. **CORS** — The app currently allows all origins (`*`). For production, restrict to your deployment domain:
   
   In `main.py`, change:
   ```python
   allow_origins=["*"]
   ```
   To:
   ```python
   allow_origins=["https://your-app.up.railway.app"]
   ```

4. **Rate limiting** — Consider adding rate limiting for production to prevent API abuse

---

## ✅ Post-Deployment Verification

After deploying, verify these critical items:

- [ ] The app loads at the deployment URL
- [ ] The dark-mode UI renders with all styles and animations
- [ ] Submitting the form generates a meal plan
- [ ] The grocery list table populates correctly
- [ ] Substitutions cards are displayed
- [ ] Budget breakdown progress bar animates
- [ ] The health check endpoint returns `"healthy"`
- [ ] No API keys are visible in the browser's DevTools (Network tab)

> ⚠️ **Critical**: If your deployed link is not working, you will be disqualified from PromptWars regardless of your score!

---

## 📝 Need Help?

- **Gemini API Issues**: Check [Google AI documentation](https://ai.google.dev/docs)
- **Railway Issues**: Visit [Railway docs](https://docs.railway.app)
- **Render Issues**: Visit [Render docs](https://docs.render.com)

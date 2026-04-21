# 🔧 Fix Render Deployment - Force Docker Runtime

## The Problem

Render is detecting your app as a Python app (because of `app/Runtime.txt` and `app/requirements.txt`) and trying to use Python 3.14, which causes the matplotlib build error.

## ✅ Solution: Force Docker Runtime

### Option 1: Delete and Recreate Service (Recommended)

1. **Delete the existing service** on Render dashboard
2. **Create a new Web Service**
3. **IMPORTANT**: When creating, select **"Docker"** as the runtime
4. Connect your GitHub repo: `Bitan-2125/Crop_monitoring_system`
5. Render will detect the `Dockerfile` automatically
6. Add environment variables:
   - `WEATHER_API_KEY`
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`
7. Deploy!

### Option 2: Use render.yaml (Blueprint)

1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will detect `render.yaml` and use Docker runtime
5. Add environment variables in the dashboard
6. Deploy!

### Option 3: Manual Configuration Change

If you don't want to delete the service:

1. Go to your service on Render dashboard
2. Go to "Settings"
3. Look for "Build & Deploy" section
4. Change "Build Command" to: (leave empty)
5. Change "Start Command" to: (leave empty)
6. Under "Docker", ensure:
   - Dockerfile Path: `./Dockerfile`
   - Docker Context: `.`
7. Save changes
8. Trigger manual deploy

## 🎯 Correct Render Configuration

Your `render.yaml` file is now configured correctly:

```yaml
services:
  - type: web
    name: harvestify
    runtime: docker  # ← This forces Docker runtime
    dockerfilePath: ./Dockerfile
    dockerContext: .
    plan: free
```

## 🚨 Common Mistakes to Avoid

1. ❌ **Don't select "Python" runtime** when creating the service
2. ❌ **Don't use the old render.yaml** (the one without `runtime: docker`)
3. ❌ **Don't ignore the Dockerfile** - make sure Render sees it
4. ✅ **Do select "Docker" runtime** explicitly
5. ✅ **Do use the render.yaml** (Blueprint method)
6. ✅ **Do verify** the Dockerfile path is correct

## 📋 Step-by-Step: Correct Deployment

### Method 1: Using Render Dashboard (Easiest)

1. **Delete existing service** (if you created one already)
   - Go to your service → Settings → Delete Service

2. **Create new Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub: `Bitan-2125/Crop_monitoring_system`
   - **IMPORTANT**: Select **"Docker"** (not Python!)
   
3. **Configure**
   - Name: `harvestify`
   - Region: Choose closest to you
   - Branch: `main`
   - Dockerfile Path: `./Dockerfile` (should auto-detect)
   - Docker Build Context: `.` (should auto-detect)

4. **Add Environment Variables**
   ```
   WEATHER_API_KEY=your_key
   GROQ_API_KEY=your_key
   TAVILY_API_KEY=your_key
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes

### Method 2: Using Blueprint (render.yaml)

1. **Go to Render Dashboard**
   - Click "New +" → "Blueprint"

2. **Connect Repository**
   - Select your GitHub repo
   - Render will detect `render.yaml`

3. **Review Configuration**
   - Verify it shows "Docker" runtime
   - Verify environment variables

4. **Add Secrets**
   - Add your API keys in the dashboard

5. **Deploy**
   - Click "Apply"
   - Wait 5-10 minutes

## 🔍 How to Verify Docker is Being Used

After deployment starts, check the logs. You should see:

✅ **Correct (Docker):**
```
==> Building...
==> Downloading base image
==> Running: docker build -t ...
Step 1/10 : FROM python:3.11.9-slim
```

❌ **Wrong (Python buildpack):**
```
==> Building...
==> Downloading Python 3.14
==> Installing dependencies from requirements.txt
```

If you see the wrong output, **stop the deployment** and follow Option 1 above.

## 🎯 Why This Happens

Render auto-detects the runtime based on files in your repo:
- Sees `app/Runtime.txt` → Thinks it's a Python app
- Sees `app/requirements.txt` → Confirms Python app
- Uses Python 3.14 (latest) → Causes matplotlib error

**Solution**: Explicitly tell Render to use Docker by:
1. Selecting "Docker" when creating the service, OR
2. Using `render.yaml` with `runtime: docker`

## 📝 Files Updated

- ✅ `render.yaml` - Now correctly specifies Docker runtime
- ✅ `Dockerfile` - Already correct
- ✅ `docker-compose.yml` - For local testing

## 🚀 After Fixing

Once you've recreated the service with Docker runtime:

1. Deployment should take 5-10 minutes
2. You'll see Docker build steps in logs
3. No matplotlib build errors
4. App will be live!

## 🆘 Still Having Issues?

### Check 1: Verify Dockerfile exists
```bash
ls -la Dockerfile
```

### Check 2: Verify render.yaml
```bash
cat render.yaml
# Should show "runtime: docker"
```

### Check 3: Test Docker build locally
```bash
docker build -t harvestify:test .
# Should complete without errors
```

### Check 4: Render logs
- Look for "docker build" in the logs
- If you see "pip install", you're using Python runtime (wrong!)

## 💡 Pro Tip

To avoid confusion, you can temporarily rename or remove these files:
- `app/Runtime.txt` (only needed for Python buildpack)
- `app/Procfile` (only needed for Python buildpack)

But keep them for reference. With Docker runtime, these files are ignored.

## ✅ Summary

1. **Delete** the existing Render service
2. **Create new** Web Service
3. **Select "Docker"** runtime (not Python!)
4. **Add** environment variables
5. **Deploy** and wait

Your app will deploy successfully with Docker! 🎉

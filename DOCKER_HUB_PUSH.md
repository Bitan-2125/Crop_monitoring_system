# 🐳 Push to Docker Hub Registry

## Step-by-Step Guide

### 1. Check Your Docker Hub Username

Go to https://hub.docker.com/ and note your username.

### 2. Tag Your Image

Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username:

```bash
# Tag the image
docker tag harvestify-master-web:latest YOUR_DOCKERHUB_USERNAME/harvestify:latest

# Optional: Also tag with version
docker tag harvestify-master-web:latest YOUR_DOCKERHUB_USERNAME/harvestify:v1.0.0
```

### 3. Push to Docker Hub

```bash
# Push latest tag
docker push YOUR_DOCKERHUB_USERNAME/harvestify:latest

# Push version tag (if you created it)
docker push YOUR_DOCKERHUB_USERNAME/harvestify:v1.0.0
```

### 4. Verify

Go to https://hub.docker.com/r/YOUR_DOCKERHUB_USERNAME/harvestify to see your image!

## 📋 Complete Commands (Copy & Paste)

Replace `YOUR_DOCKERHUB_USERNAME` with your username:

```bash
# 1. Login (already done)
docker login

# 2. Tag the image
docker tag harvestify-master-web:latest YOUR_DOCKERHUB_USERNAME/harvestify:latest

# 3. Push to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/harvestify:latest
```

## 🎯 Example

If your Docker Hub username is `johndoe`:

```bash
docker tag harvestify-master-web:latest johndoe/harvestify:latest
docker push johndoe/harvestify:latest
```

## 🚀 After Pushing

### Pull from Any Machine

Anyone can now pull your image:

```bash
docker pull YOUR_DOCKERHUB_USERNAME/harvestify:latest
```

### Run from Docker Hub

```bash
docker run -d \
  -p 8000:8000 \
  -e WEATHER_API_KEY=your_key \
  -e GROQ_API_KEY=your_key \
  -e TAVILY_API_KEY=your_key \
  YOUR_DOCKERHUB_USERNAME/harvestify:latest
```

### Deploy to Cloud Platforms

Now you can deploy using your Docker Hub image:

#### Render
```yaml
services:
  - type: web
    name: harvestify
    runtime: docker
    image:
      url: docker.io/YOUR_DOCKERHUB_USERNAME/harvestify:latest
```

#### Railway
```bash
railway run docker pull YOUR_DOCKERHUB_USERNAME/harvestify:latest
```

#### Fly.io
Update `fly.toml`:
```toml
[build]
  image = "YOUR_DOCKERHUB_USERNAME/harvestify:latest"
```

## 📊 Image Information

Your image contains:
- Python 3.11.9
- Flask 3.0.3
- PyTorch 2.2.0 (CPU)
- All ML models
- Complete application code

**Image Size**: ~1.5 GB (due to PyTorch and models)

## 🔒 Make Repository Private (Optional)

1. Go to https://hub.docker.com/
2. Navigate to your repository
3. Settings → Make Private

## 🏷️ Tagging Best Practices

```bash
# Latest (always points to newest)
docker tag harvestify-master-web:latest YOUR_USERNAME/harvestify:latest

# Version tags
docker tag harvestify-master-web:latest YOUR_USERNAME/harvestify:v1.0.0
docker tag harvestify-master-web:latest YOUR_USERNAME/harvestify:v1.0
docker tag harvestify-master-web:latest YOUR_USERNAME/harvestify:v1

# Environment tags
docker tag harvestify-master-web:latest YOUR_USERNAME/harvestify:production
docker tag harvestify-master-web:latest YOUR_USERNAME/harvestify:staging
```

## 🔄 Update Your Image

When you make changes:

```bash
# 1. Rebuild
docker-compose build

# 2. Tag new version
docker tag harvestify-master-web:latest YOUR_USERNAME/harvestify:v1.1.0
docker tag harvestify-master-web:latest YOUR_USERNAME/harvestify:latest

# 3. Push both tags
docker push YOUR_USERNAME/harvestify:v1.1.0
docker push YOUR_USERNAME/harvestify:latest
```

## 📝 Create Docker Hub Repository Description

Add this to your Docker Hub repository description:

```markdown
# Harvestify - AI-Powered Agricultural Platform

Smart farming application with ML-based crop recommendations, disease detection, and market insights.

## Features
- 🌾 Crop Recommendation (ML-based)
- 🦠 Plant Disease Detection (CNN)
- 🧪 Fertilizer Suggestions
- 💰 Market Price Insights
- 📅 Smart Crop Planning

## Quick Start

docker run -d -p 8000:8000 \
  -e WEATHER_API_KEY=your_key \
  -e GROQ_API_KEY=your_key \
  -e TAVILY_API_KEY=your_key \
  YOUR_USERNAME/harvestify:latest

## Environment Variables
- `WEATHER_API_KEY` - OpenWeatherMap API key
- `GROQ_API_KEY` - Groq AI API key
- `TAVILY_API_KEY` - Tavily search API key

## Documentation
https://github.com/Bitan-2125/Crop_monitoring_system

## Tags
- `latest` - Latest stable version
- `v1.0.0` - Version 1.0.0
```

## 🆘 Troubleshooting

### "denied: requested access to the resource is denied"
```bash
# Make sure you're logged in
docker login

# Check your username
docker info | grep Username
```

### "no basic auth credentials"
```bash
# Logout and login again
docker logout
docker login
```

### Push is slow
The image is ~1.5 GB. First push will take time. Subsequent pushes are faster (only changed layers).

### Want to reduce image size?
Use multi-stage builds or Alpine base image (advanced).

## ✅ Verification

After pushing, verify:

1. **Check Docker Hub**: https://hub.docker.com/r/YOUR_USERNAME/harvestify
2. **Pull and test**:
   ```bash
   docker pull YOUR_USERNAME/harvestify:latest
   docker run -p 8000:8000 YOUR_USERNAME/harvestify:latest
   ```

## 🎉 Success!

Your Docker image is now publicly available and can be deployed anywhere!

Share your image:
```
docker pull YOUR_DOCKERHUB_USERNAME/harvestify:latest
```

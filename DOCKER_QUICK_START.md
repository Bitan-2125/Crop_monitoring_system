# 🐳 Docker Quick Start Guide

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Your API keys ready:
  - OpenWeatherMap API Key
  - Groq API Key
  - Tavily API Key

## 🚀 Quick Start (3 Steps)

### Step 1: Set Up Environment Variables

Create or edit `app/.env` file:

```bash
# On Linux/Mac
cp app/.env.example app/.env
nano app/.env

# On Windows
copy app\.env.example app\.env
notepad app\.env
```

Add your API keys:
```env
WEATHER_API_KEY=your_weather_api_key_here
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Step 2: Build and Run

**Option A: Using Quick Start Script (Recommended)**

Linux/Mac:
```bash
chmod +x start-docker.sh
./start-docker.sh
```

Windows:
```cmd
start-docker.bat
```

**Option B: Using Docker Compose**

```bash
docker-compose up -d
```

**Option C: Manual Docker Commands**

```bash
# Build
docker build -t harvestify:latest .

# Run
docker run -d \
  --name harvestify-app \
  -p 8000:8000 \
  --env-file app/.env \
  harvestify:latest
```

### Step 3: Access Your App

Open your browser: **http://localhost:8000**

## 📋 Common Commands

```bash
# View logs
docker logs -f harvestify-app

# Stop the app
docker stop harvestify-app

# Start the app
docker start harvestify-app

# Restart the app
docker restart harvestify-app

# Remove the container
docker rm -f harvestify-app

# View running containers
docker ps

# View all containers
docker ps -a

# Check container stats
docker stats harvestify-app

# Execute command inside container
docker exec -it harvestify-app bash
```

## 🌐 Deploy to Cloud

### Deploy to Render (Docker)

1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" → "Web Service"
4. Connect your repository
5. Select "Docker" as runtime
6. Add environment variables
7. Deploy!

### Deploy to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up

# Set environment variables
railway variables set WEATHER_API_KEY=your_key
railway variables set GROQ_API_KEY=your_key
railway variables set TAVILY_API_KEY=your_key
```

### Deploy to Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch (creates fly.toml)
fly launch

# Set secrets
fly secrets set WEATHER_API_KEY=your_key
fly secrets set GROQ_API_KEY=your_key
fly secrets set TAVILY_API_KEY=your_key

# Deploy
fly deploy
```

### Deploy to DigitalOcean

1. Push to GitHub
2. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
3. Create new app from GitHub
4. Select Dockerfile
5. Add environment variables
6. Deploy!

## 🔧 Troubleshooting

### Port 8000 already in use

```bash
# Use different port
docker run -d -p 8080:8000 --name harvestify-app --env-file app/.env harvestify:latest
# Access at http://localhost:8080
```

### Container won't start

```bash
# Check logs
docker logs harvestify-app

# Check if environment variables are set
docker exec harvestify-app env | grep API_KEY
```

### Out of memory

```bash
# Run with memory limit
docker run -d -p 8000:8000 --memory="2g" --name harvestify-app --env-file app/.env harvestify:latest
```

### Permission denied (Linux)

```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again
```

### Image build fails

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t harvestify:latest .
```

## 📊 Monitoring

### View Resource Usage

```bash
docker stats harvestify-app
```

### View Health Status

```bash
docker inspect --format='{{json .State.Health}}' harvestify-app | python -m json.tool
```

### View Container Details

```bash
docker inspect harvestify-app
```

## 🔒 Security Best Practices

1. ✅ Never commit `.env` files with real API keys
2. ✅ Use Docker secrets for production
3. ✅ Regularly update base images
4. ✅ Scan images for vulnerabilities:
   ```bash
   docker scan harvestify:latest
   ```
5. ✅ Run containers as non-root user (already configured)
6. ✅ Use specific version tags, not `latest` in production

## 🎯 Production Deployment Checklist

- [ ] Environment variables set correctly
- [ ] Health checks configured
- [ ] Logging configured
- [ ] Resource limits set
- [ ] Backup strategy in place
- [ ] Monitoring setup (e.g., Prometheus, Grafana)
- [ ] SSL/TLS certificates configured
- [ ] Domain name configured
- [ ] Auto-scaling configured (if needed)
- [ ] CI/CD pipeline setup

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Render Docker Deployment](https://render.com/docs/docker)
- [Railway Documentation](https://docs.railway.app/)
- [Fly.io Documentation](https://fly.io/docs/)

## 💡 Tips

- Use `docker-compose` for local development
- Use cloud platforms (Render, Railway, Fly.io) for production
- Monitor logs regularly
- Set up alerts for errors
- Keep Docker images updated
- Use multi-stage builds for smaller images
- Implement proper logging and monitoring

## 🆘 Need Help?

Check the detailed guide: `DOCKER_DEPLOYMENT.md`

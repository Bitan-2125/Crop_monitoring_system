# 🎯 Quick Command Reference

## 🐳 Docker Commands

### Build & Run
```bash
# Build image
docker build -t harvestify:latest .

# Run container
docker run -d --name harvestify-app -p 8000:8000 --env-file app/.env harvestify:latest

# Run with Docker Compose
docker-compose up -d
```

### Manage Containers
```bash
# View logs
docker logs -f harvestify-app

# Stop container
docker stop harvestify-app

# Start container
docker start harvestify-app

# Restart container
docker restart harvestify-app

# Remove container
docker rm -f harvestify-app

# View running containers
docker ps

# View all containers
docker ps -a
```

### Debugging
```bash
# Execute bash in container
docker exec -it harvestify-app bash

# Check environment variables
docker exec harvestify-app env

# View container stats
docker stats harvestify-app

# Inspect container
docker inspect harvestify-app

# Check health status
docker inspect --format='{{json .State.Health}}' harvestify-app
```

### Cleanup
```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove everything (careful!)
docker system prune -a
```

## 🚀 Deployment Commands

### Render
```bash
# Just push to GitHub
git add .
git commit -m "Deploy to Render"
git push

# Then use web UI at dashboard.render.com
```

### Railway
```bash
# Install CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Set environment variables
railway variables set WEATHER_API_KEY=your_key
railway variables set GROQ_API_KEY=your_key
railway variables set TAVILY_API_KEY=your_key

# Deploy
railway up

# View logs
railway logs

# Open in browser
railway open
```

### Fly.io
```bash
# Install CLI (Linux/Mac)
curl -L https://fly.io/install.sh | sh

# Install CLI (Windows)
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Login
fly auth login

# Launch app
fly launch

# Set secrets
fly secrets set WEATHER_API_KEY=your_key
fly secrets set GROQ_API_KEY=your_key
fly secrets set TAVILY_API_KEY=your_key

# Deploy
fly deploy

# View logs
fly logs

# Open in browser
fly open

# SSH into app
fly ssh console

# Check status
fly status
```

### Heroku
```bash
# Install CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create harvestify-app

# Set buildpack
heroku stack:set container

# Set environment variables
heroku config:set WEATHER_API_KEY=your_key
heroku config:set GROQ_API_KEY=your_key
heroku config:set TAVILY_API_KEY=your_key

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Open in browser
heroku open
```

### DigitalOcean
```bash
# Install CLI
curl -sL https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-linux-amd64.tar.gz | tar -xzv
sudo mv doctl /usr/local/bin

# Login
doctl auth init

# Create app (use web UI for easier setup)
# Or use CLI:
doctl apps create --spec .do/app.yaml
```

## 📦 Git Commands

### Basic Workflow
```bash
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

### Branch Management
```bash
# Create new branch
git checkout -b feature-name

# Switch branch
git checkout main

# Merge branch
git merge feature-name

# Delete branch
git branch -d feature-name
```

### Undo Changes
```bash
# Discard local changes
git checkout -- filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

## 🔧 Environment Setup

### Create .env file
```bash
# Linux/Mac
cp app/.env.example app/.env
nano app/.env

# Windows
copy app\.env.example app\.env
notepad app\.env
```

### Check Python version
```bash
python --version
python3 --version
```

### Install dependencies locally
```bash
cd app
pip install -r requirements.txt
```

### Run locally (without Docker)
```bash
cd app
python app.py
# Or with gunicorn
gunicorn app:app --bind 0.0.0.0:8000
```

## 🧪 Testing Commands

### Test Docker build
```bash
docker build -t harvestify:test .
```

### Test container locally
```bash
docker run -p 8000:8000 --env-file app/.env harvestify:test
```

### Check if app is running
```bash
curl http://localhost:8000
```

### Test with different port
```bash
docker run -p 8080:8000 --env-file app/.env harvestify:latest
```

## 📊 Monitoring Commands

### View Docker logs
```bash
# Follow logs
docker logs -f harvestify-app

# Last 100 lines
docker logs --tail 100 harvestify-app

# Logs since 10 minutes ago
docker logs --since 10m harvestify-app
```

### Check resource usage
```bash
# Container stats
docker stats harvestify-app

# System-wide stats
docker stats

# Disk usage
docker system df
```

### Health check
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' harvestify-app

# Full health details
docker inspect --format='{{json .State.Health}}' harvestify-app | python -m json.tool
```

## 🔍 Troubleshooting Commands

### Check if port is in use
```bash
# Linux/Mac
lsof -i :8000
netstat -tuln | grep 8000

# Windows
netstat -ano | findstr :8000
```

### Kill process on port
```bash
# Linux/Mac
kill -9 $(lsof -t -i:8000)

# Windows
# Find PID first with netstat, then:
taskkill /PID <PID> /F
```

### Check Docker daemon
```bash
# Check if Docker is running
docker info

# Restart Docker (Linux)
sudo systemctl restart docker

# Restart Docker (Mac)
# Use Docker Desktop UI

# Restart Docker (Windows)
# Use Docker Desktop UI or:
Restart-Service docker
```

### View Docker version
```bash
docker --version
docker-compose --version
```

## 🎯 Quick Start Scripts

### Linux/Mac
```bash
chmod +x start-docker.sh
./start-docker.sh
```

### Windows
```cmd
start-docker.bat
```

### Docker Compose
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up -d --build
```

## 💾 Backup Commands

### Export Docker image
```bash
docker save harvestify:latest > harvestify-backup.tar
```

### Import Docker image
```bash
docker load < harvestify-backup.tar
```

### Backup container data
```bash
docker cp harvestify-app:/app/Data ./backup/
```

## 🔐 Security Commands

### Scan image for vulnerabilities
```bash
docker scan harvestify:latest
```

### Check for outdated packages
```bash
docker run --rm harvestify:latest pip list --outdated
```

### Update base image
```bash
docker pull python:3.11.9-slim
docker build --no-cache -t harvestify:latest .
```

## 📝 Notes

- Replace `harvestify-app` with your container name if different
- Replace `harvestify:latest` with your image name if different
- Always test locally before deploying to production
- Keep your API keys secure and never commit them to Git
- Monitor logs regularly for errors
- Update dependencies regularly for security

## 🆘 Need Help?

- Docker issues: `docker logs harvestify-app`
- Deployment issues: Check platform-specific logs
- Build issues: `docker build --no-cache -t harvestify:latest .`
- Port issues: Use different port with `-p 8080:8000`

## 📚 More Information

- `DOCKER_QUICK_START.md` - Quick start guide
- `DOCKER_DEPLOYMENT.md` - Detailed deployment guide
- `DEPLOYMENT_COMPARISON.md` - Platform comparison
- `DEPLOYMENT_SUMMARY.md` - Complete summary

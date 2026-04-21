# Docker Deployment Guide

## Quick Start

### 1. Build and Run Locally

```bash
# Build the Docker image
docker build -t harvestify:latest .

# Run the container
docker run -p 8000:8000 \
  -e WEATHER_API_KEY=your_weather_api_key \
  -e GROQ_API_KEY=your_groq_api_key \
  -e TAVILY_API_KEY=your_tavily_api_key \
  harvestify:latest
```

Access your app at: http://localhost:8000

### 2. Using Docker Compose (Recommended)

```bash
# Make sure app/.env file exists with your API keys
# Or set environment variables in your shell

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## Environment Variables

Create `app/.env` file with:

```env
WEATHER_API_KEY=your_weather_api_key_here
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Deploy to Cloud Platforms

### Deploy to Render (Docker)

1. Create `render.yaml` for Docker deployment:

```yaml
services:
  - type: web
    name: harvestify
    runtime: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: WEATHER_API_KEY
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: TAVILY_API_KEY
        sync: false
```

2. Push to GitHub and connect to Render
3. Add environment variables in Render dashboard
4. Deploy!

### Deploy to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables
railway variables set WEATHER_API_KEY=your_key
railway variables set GROQ_API_KEY=your_key
railway variables set TAVILY_API_KEY=your_key

# Deploy
railway up
```

### Deploy to Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app (creates fly.toml)
fly launch

# Set secrets
fly secrets set WEATHER_API_KEY=your_key
fly secrets set GROQ_API_KEY=your_key
fly secrets set TAVILY_API_KEY=your_key

# Deploy
fly deploy
```

### Deploy to Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/harvestify

# Deploy to Cloud Run
gcloud run deploy harvestify \
  --image gcr.io/YOUR_PROJECT_ID/harvestify \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars WEATHER_API_KEY=your_key,GROQ_API_KEY=your_key,TAVILY_API_KEY=your_key
```

### Deploy to AWS ECS/Fargate

```bash
# Build and push to ECR
aws ecr create-repository --repository-name harvestify
docker tag harvestify:latest YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/harvestify:latest
docker push YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/harvestify:latest

# Create task definition and service using AWS Console or CLI
# Set environment variables in task definition
```

### Deploy to Azure Container Instances

```bash
# Create resource group
az group create --name harvestify-rg --location eastus

# Create container registry
az acr create --resource-group harvestify-rg --name harvestifyacr --sku Basic

# Build and push
az acr build --registry harvestifyacr --image harvestify:latest .

# Deploy
az container create \
  --resource-group harvestify-rg \
  --name harvestify \
  --image harvestifyacr.azurecr.io/harvestify:latest \
  --dns-name-label harvestify-app \
  --ports 8000 \
  --environment-variables \
    WEATHER_API_KEY=your_key \
    GROQ_API_KEY=your_key \
    TAVILY_API_KEY=your_key
```

### Deploy to DigitalOcean App Platform

1. Push your code to GitHub
2. Go to DigitalOcean App Platform
3. Create new app from GitHub repository
4. Select Dockerfile deployment
5. Add environment variables
6. Deploy!

## Docker Commands Reference

```bash
# Build image
docker build -t harvestify:latest .

# Run container
docker run -d -p 8000:8000 --name harvestify-app harvestify:latest

# View logs
docker logs -f harvestify-app

# Stop container
docker stop harvestify-app

# Remove container
docker rm harvestify-app

# Remove image
docker rmi harvestify:latest

# Execute command in running container
docker exec -it harvestify-app bash

# View container stats
docker stats harvestify-app
```

## Optimization Tips

### Reduce Image Size

The current Dockerfile uses `python:3.11.9-slim` which is already optimized. For even smaller size:

```dockerfile
FROM python:3.11.9-alpine
# Note: Alpine requires additional build dependencies for some packages
```

### Multi-stage Build (Advanced)

```dockerfile
# Build stage
FROM python:3.11.9-slim as builder
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
```

### Production Best Practices

1. Use specific version tags, not `latest`
2. Run as non-root user
3. Use secrets management for API keys
4. Enable health checks
5. Set resource limits
6. Use multi-stage builds
7. Scan images for vulnerabilities

## Troubleshooting

### Container won't start
```bash
docker logs harvestify-app
```

### Out of memory
Increase Docker memory limit or optimize model loading

### Port already in use
```bash
# Use different port
docker run -p 8080:8000 harvestify:latest
```

### Permission denied
```bash
# Run with sudo or add user to docker group
sudo usermod -aG docker $USER
```

## Health Check

The Dockerfile includes a health check. Monitor it:

```bash
docker inspect --format='{{json .State.Health}}' harvestify-app
```

## Security Notes

- Never commit `.env` files with real API keys
- Use Docker secrets or environment variables for sensitive data
- Regularly update base images for security patches
- Scan images with `docker scan harvestify:latest`

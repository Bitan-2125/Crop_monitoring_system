# Makefile for Harvestify Docker deployment

.PHONY: help build run stop logs clean test deploy-render deploy-railway deploy-fly

help:
	@echo "Harvestify Docker Commands:"
	@echo "  make build          - Build Docker image"
	@echo "  make run            - Run container locally"
	@echo "  make dev            - Run with docker-compose"
	@echo "  make stop           - Stop all containers"
	@echo "  make logs           - View container logs"
	@echo "  make clean          - Remove containers and images"
	@echo "  make test           - Test the application"
	@echo "  make deploy-render  - Deploy to Render"
	@echo "  make deploy-railway - Deploy to Railway"
	@echo "  make deploy-fly     - Deploy to Fly.io"

build:
	@echo "Building Docker image..."
	docker build -t harvestify:latest .

run:
	@echo "Running container..."
	docker run -d -p 8000:8000 --name harvestify-app \
		--env-file app/.env \
		harvestify:latest
	@echo "App running at http://localhost:8000"

dev:
	@echo "Starting development environment..."
	docker-compose up --build

dev-bg:
	@echo "Starting development environment in background..."
	docker-compose up -d --build
	@echo "App running at http://localhost:8000"

stop:
	@echo "Stopping containers..."
	docker-compose down
	-docker stop harvestify-app
	-docker rm harvestify-app

logs:
	@echo "Showing logs..."
	docker-compose logs -f

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	-docker stop harvestify-app
	-docker rm harvestify-app
	-docker rmi harvestify:latest
	@echo "Cleanup complete!"

test:
	@echo "Testing application..."
	@curl -f http://localhost:8000 || echo "App not running. Start with 'make run' or 'make dev'"

deploy-render:
	@echo "Deploying to Render..."
	@echo "1. Make sure your code is pushed to GitHub"
	@echo "2. Go to https://dashboard.render.com"
	@echo "3. Create new Web Service"
	@echo "4. Select Docker runtime"
	@echo "5. Add environment variables"
	git add .
	git commit -m "Deploy to Render" || true
	git push

deploy-railway:
	@echo "Deploying to Railway..."
	railway up

deploy-fly:
	@echo "Deploying to Fly.io..."
	fly deploy

shell:
	@echo "Opening shell in container..."
	docker exec -it harvestify-app bash

rebuild:
	@echo "Rebuilding without cache..."
	docker-compose build --no-cache
	docker-compose up -d

status:
	@echo "Container status:"
	@docker ps -a | grep harvestify || echo "No containers running"
	@echo "\nImages:"
	@docker images | grep harvestify || echo "No images found"

@echo off
REM Harvestify Docker Quick Start Script for Windows

echo Starting Harvestify with Docker...

REM Check if .env file exists
if not exist "app\.env" (
    echo Warning: app\.env file not found!
    if exist "app\.env.example" (
        echo Creating from app\.env.example...
        copy "app\.env.example" "app\.env"
        echo Created app\.env - Please edit it with your API keys
        exit /b 1
    ) else (
        echo app\.env.example not found. Please create app\.env manually
        exit /b 1
    )
)

REM Build Docker image
echo Building Docker image...
docker build -t harvestify:latest .

if %ERRORLEVEL% neq 0 (
    echo Docker build failed!
    exit /b 1
)

echo Docker image built successfully!

REM Stop and remove existing container if running
docker ps -aq -f name=harvestify-app >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Stopping existing container...
    docker stop harvestify-app
    docker rm harvestify-app
)

REM Run the container
echo Starting container...
docker run -d --name harvestify-app -p 8000:8000 --env-file app\.env --restart unless-stopped harvestify:latest

if %ERRORLEVEL% equ 0 (
    echo Container started successfully!
    echo.
    echo Access your app at: http://localhost:8000
    echo.
    echo Useful commands:
    echo   View logs:    docker logs -f harvestify-app
    echo   Stop app:     docker stop harvestify-app
    echo   Restart app:  docker restart harvestify-app
    echo   Remove app:   docker rm -f harvestify-app
    echo.
    echo Showing logs (Ctrl+C to exit)...
    timeout /t 2 >nul
    docker logs -f harvestify-app
) else (
    echo Failed to start container!
    exit /b 1
)

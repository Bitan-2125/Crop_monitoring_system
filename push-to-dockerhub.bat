@echo off
REM Push Harvestify to Docker Hub

echo ========================================
echo   Push Harvestify to Docker Hub
echo ========================================
echo.

REM Get Docker Hub username
set /p DOCKER_USERNAME="Enter your Docker Hub username: "

echo.
echo Tagging image as %DOCKER_USERNAME%/harvestify:latest...
docker tag harvestify-master-web:latest %DOCKER_USERNAME%/harvestify:latest

if %ERRORLEVEL% neq 0 (
    echo Failed to tag image!
    pause
    exit /b 1
)

echo.
echo Tagging image as %DOCKER_USERNAME%/harvestify:v1.0.0...
docker tag harvestify-master-web:latest %DOCKER_USERNAME%/harvestify:v1.0.0

echo.
echo Pushing %DOCKER_USERNAME%/harvestify:latest to Docker Hub...
docker push %DOCKER_USERNAME%/harvestify:latest

if %ERRORLEVEL% neq 0 (
    echo Failed to push latest tag!
    pause
    exit /b 1
)

echo.
echo Pushing %DOCKER_USERNAME%/harvestify:v1.0.0 to Docker Hub...
docker push %DOCKER_USERNAME%/harvestify:v1.0.0

if %ERRORLEVEL% neq 0 (
    echo Failed to push v1.0.0 tag!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Your image is now available at:
echo   docker pull %DOCKER_USERNAME%/harvestify:latest
echo.
echo View on Docker Hub:
echo   https://hub.docker.com/r/%DOCKER_USERNAME%/harvestify
echo.
pause

# Push Harvestify to Docker Hub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Push Harvestify to Docker Hub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get Docker Hub username
$DOCKER_USERNAME = Read-Host "Enter your Docker Hub username"

Write-Host ""
Write-Host "Tagging image as $DOCKER_USERNAME/harvestify:latest..." -ForegroundColor Yellow
docker tag harvestify-master-web:latest "$DOCKER_USERNAME/harvestify:latest"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to tag image!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Tagging image as $DOCKER_USERNAME/harvestify:v1.0.0..." -ForegroundColor Yellow
docker tag harvestify-master-web:latest "$DOCKER_USERNAME/harvestify:v1.0.0"

Write-Host ""
Write-Host "Pushing $DOCKER_USERNAME/harvestify:latest to Docker Hub..." -ForegroundColor Yellow
docker push "$DOCKER_USERNAME/harvestify:latest"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to push latest tag!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Pushing $DOCKER_USERNAME/harvestify:v1.0.0 to Docker Hub..." -ForegroundColor Yellow
docker push "$DOCKER_USERNAME/harvestify:v1.0.0"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to push v1.0.0 tag!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SUCCESS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your image is now available at:" -ForegroundColor Cyan
Write-Host "  docker pull $DOCKER_USERNAME/harvestify:latest" -ForegroundColor White
Write-Host ""
Write-Host "View on Docker Hub:" -ForegroundColor Cyan
Write-Host "  https://hub.docker.com/r/$DOCKER_USERNAME/harvestify" -ForegroundColor White
Write-Host ""

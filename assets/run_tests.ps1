$dockerfile = "Dockerfile.tests"
$imageName = "pytest-runner"

Write-Host "Building Docker image: $imageName"
docker build -f $dockerfile -t $imageName .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed." -ForegroundColor Red
    exit 1
}

Write-Host "Running pytest in Docker container..."
docker run --rm $imageName

if ($LASTEXITCODE -eq 0) {
    Write-Host "Tests passed." -ForegroundColor Green
} else {
    Write-Host "Tests failed." -ForegroundColor Red
    exit 1
}

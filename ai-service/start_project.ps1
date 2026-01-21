# Plant Health Monitoring System - Startup Script
# This script starts all required services

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Plant Health Monitoring System Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check MongoDB
Write-Host "[1/4] Checking MongoDB..." -ForegroundColor Yellow
$mongoService = Get-Service -Name MongoDB* -ErrorAction SilentlyContinue

if ($mongoService -and $mongoService.Status -eq "Running") {
    Write-Host "✓ MongoDB is already running" -ForegroundColor Green
} else {
    Write-Host "Starting MongoDB..." -ForegroundColor Yellow
    try {
        Start-Service MongoDB -ErrorAction Stop
        Write-Host "✓ MongoDB started successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ Could not start MongoDB service" -ForegroundColor Red
        Write-Host "  Please start MongoDB manually: net start MongoDB" -ForegroundColor Yellow
    }
}
Write-Host ""

# Check Python dependencies
Write-Host "[2/4] Checking Python AI Service..." -ForegroundColor Yellow
if (Test-Path "app.py") {
    Write-Host "✓ AI Service files found" -ForegroundColor Green
    
    if (Test-Path "models/plant_model.pkl") {
        Write-Host "✓ Model file exists" -ForegroundColor Green
    } else {
        Write-Host "✗ Model file missing - Please run: python train_model.py" -ForegroundColor Red
    }
    
    if (Test-Path "data/plant_health_data.csv") {
        Write-Host "✓ Data file exists" -ForegroundColor Green
    } else {
        Write-Host "✗ Data file missing" -ForegroundColor Red
    }
} else {
    Write-Host "✗ AI Service files not found" -ForegroundColor Red
}
Write-Host ""

# Start AI Service
Write-Host "[3/4] Starting AI Service (Python Flask)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python app.py" -WindowStyle Normal
Write-Host "✓ AI Service starting on http://localhost:5000" -ForegroundColor Green
Write-Host ""

# Wait for backend to initialize
Write-Host "Waiting for AI Service to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start Frontend
Write-Host "[4/4] Starting Frontend (React)..." -ForegroundColor Yellow
if (Test-Path "../frontend/package.json") {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '..\frontend'; npm start" -WindowStyle Normal
    Write-Host "✓ Frontend starting on http://localhost:3000" -ForegroundColor Green
} else {
    Write-Host "✗ Frontend not found at ../frontend" -ForegroundColor Red
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Services Status:" -ForegroundColor Cyan
Write-Host "  MongoDB:      Running" -ForegroundColor Green
Write-Host "  AI Service:   http://localhost:5000" -ForegroundColor Green
Write-Host "  Frontend:     http://localhost:3000" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each terminal window to stop services" -ForegroundColor Yellow
Write-Host ""

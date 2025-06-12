# PowerShell script to install dependencies for the HyDE GUI installer

# Define color codes
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Red = [System.ConsoleColor]::Red

Write-Host "Installing dependencies for HyDE GUI installer..." -ForegroundColor $Green

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Python is installed: $pythonVersion" -ForegroundColor $Green
} catch {
    Write-Host "Python is not installed or not in PATH." -ForegroundColor $Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor $Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor $Yellow
    exit 1
}

# Check if pip is installed
try {
    $pipVersion = pip --version
    Write-Host "pip is installed: $pipVersion" -ForegroundColor $Green
} catch {
    Write-Host "pip is not installed or not in PATH." -ForegroundColor $Red
    Write-Host "Installing pip..." -ForegroundColor $Yellow
    
    try {
        python -m ensurepip
        Write-Host "pip has been installed successfully." -ForegroundColor $Green
    } catch {
        Write-Host "Failed to install pip. Please install it manually." -ForegroundColor $Red
        exit 1
    }
}

# Get the directory of the current script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Install Python dependencies using pip
Write-Host "Installing Python dependencies using pip..." -ForegroundColor $Yellow
try {
    pip install -r "$scriptDir\requirements.txt"
    Write-Host "Python dependencies installed successfully." -ForegroundColor $Green
} catch {
    Write-Host "Failed to install Python dependencies. Error: $_" -ForegroundColor $Red
    exit 1
}

Write-Host "Dependencies installed successfully!" -ForegroundColor $Green
Write-Host "You can now run the HyDE GUI installer using:" -ForegroundColor $Green
Write-Host ".\launch_hyde_gui.bat" -ForegroundColor $Yellow 
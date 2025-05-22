@echo off

REM Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3 is required but not installed. Please install Python 3 first.
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is required but not installed. Please install pip first.
    exit /b 1
)

REM Install required Python packages
echo Installing required Python packages...
pip install -r "%~dp0requirements.txt"

REM Launch the GUI installer
echo Launching HyDE GUI installer...
python "%~dp0hyde-gui.py" 
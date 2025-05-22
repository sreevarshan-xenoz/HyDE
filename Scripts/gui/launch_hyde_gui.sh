#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed. Please install pip3 first."
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
pip3 install -r "$(dirname "$0")/requirements.txt"

# Launch the GUI installer
echo "Launching HyDE GUI installer..."
python3 "$(dirname "$0")/hyde-gui.py" 
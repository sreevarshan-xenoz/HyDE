#!/bin/bash

# Script to install dependencies for the HyDE GUI installer
# This script should be run with root privileges

# Define color codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Installing dependencies for HyDE GUI installer...${NC}"

# Detect package manager
if command -v pacman &> /dev/null; then
    # Arch-based system
    echo -e "${YELLOW}Arch-based system detected. Using pacman.${NC}"
    
    # Update package database
    echo -e "${YELLOW}Updating package database...${NC}"
    pacman -Sy --noconfirm
    
    # Install Python and Qt dependencies
    echo -e "${YELLOW}Installing Python and Qt dependencies...${NC}"
    pacman -S --needed --noconfirm python python-pip python-pyqt6
    
elif command -v apt-get &> /dev/null; then
    # Debian-based system
    echo -e "${YELLOW}Debian-based system detected. Using apt.${NC}"
    
    # Update package database
    echo -e "${YELLOW}Updating package database...${NC}"
    apt-get update
    
    # Install Python and Qt dependencies
    echo -e "${YELLOW}Installing Python and Qt dependencies...${NC}"
    apt-get install -y python3 python3-pip python3-pyqt6
    
elif command -v dnf &> /dev/null; then
    # Fedora-based system
    echo -e "${YELLOW}Fedora-based system detected. Using dnf.${NC}"
    
    # Update package database
    echo -e "${YELLOW}Updating package database...${NC}"
    dnf check-update
    
    # Install Python and Qt dependencies
    echo -e "${YELLOW}Installing Python and Qt dependencies...${NC}"
    dnf install -y python3 python3-pip python3-pyqt6
    
else
    echo -e "${RED}Unsupported package manager. Please install the following packages manually:${NC}"
    echo "- Python 3"
    echo "- pip for Python 3"
    echo "- PyQt6 for Python 3"
    exit 1
fi

# Install Python dependencies using pip
echo -e "${YELLOW}Installing Python dependencies using pip...${NC}"
pip install -r "$(dirname "$0")/requirements.txt"

echo -e "${GREEN}Dependencies installed successfully!${NC}"
echo -e "${GREEN}You can now run the HyDE GUI installer using:${NC}"
echo -e "${YELLOW}./launch_hyde_gui.sh${NC}" 
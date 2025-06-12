# HyDE GUI Installer and Settings Manager

This directory contains a graphical user interface (GUI) for installing and configuring the HyDE desktop environment.

## Features

- **Graphical Installer**: Easy-to-use installation wizard for HyDE
- **Theme Preview System**: Preview themes before applying them
- **Settings Manager**: Centralized settings management for all HyDE components
- **First-time Setup Wizard**: Helps new users configure their environment

## Requirements

- Python 3.6 or higher
- PyQt6
- pip (Python package manager)

## Installation

### Linux

1. Make the installation script executable:
   ```bash
   chmod +x install_dependencies.sh
   ```

2. Run the installation script with sudo:
   ```bash
   sudo ./install_dependencies.sh
   ```

3. Launch the GUI installer:
   ```bash
   ./launch_hyde_gui.sh
   ```

### Windows

1. Open PowerShell as administrator and navigate to this directory

2. Run the installation script:
   ```powershell
   .\install_dependencies.ps1
   ```

3. Launch the GUI installer:
   ```powershell
   .\launch_hyde_gui.bat
   ```

## Components

- **hyde-gui.py**: Main GUI application with installation wizard and settings manager
- **theme_previewer.py**: Theme preview generator
- **settings_manager.py**: Centralized settings manager
- **requirements.txt**: Python dependencies
- **launch_hyde_gui.sh**: Linux launcher script
- **launch_hyde_gui.bat**: Windows launcher script
- **install_dependencies.sh**: Linux dependency installer
- **install_dependencies.ps1**: Windows dependency installer

## Usage

The GUI installer guides you through the following steps:

1. **Welcome**: Introduction to HyDE
2. **Installation Options**: Select packages to install
3. **Theme Selection**: Choose and preview themes
4. **Settings**: Configure HyDE settings
5. **Installation**: Install HyDE with selected options

## Theme Preview System

The theme preview system allows you to:

- View how themes will look before applying them
- Generate real-time previews of themes
- See color palettes for each theme

## Settings Manager

The centralized settings manager provides:

- Window management settings
- Appearance settings
- Performance settings
- Notification settings
- Easy reset options for all settings

## Contributing

Contributions to improve the GUI installer are welcome. Please follow the project's contribution guidelines when submitting changes. 
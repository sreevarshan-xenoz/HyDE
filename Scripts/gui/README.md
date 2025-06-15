# HyDE GUI Installer and Settings Manager

This directory contains a graphical user interface (GUI) for installing and configuring the HyDE desktop environment.

## Features

- **Graphical Installer**: Easy-to-use installation wizard for HyDE
- **Theme Preview System**: Preview themes before applying them
- **Settings Manager**: Centralized settings management for all HyDE components
- **First-time Setup Wizard**: Helps new users configure their environment
- **AI Configuration Assistant**: Natural language interface for configuring HyDE

## Requirements

- Python 3.6 or higher
- PyQt6
- pip (Python package manager)
- OpenAI API key (for AI Assistant feature)

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
- **ai_assistant.py**: AI-powered configuration assistant
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
5. **AI Assistant**: Use natural language to configure HyDE
6. **Installation**: Install HyDE with selected options

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

## AI Configuration Assistant

The AI Configuration Assistant provides:

- Natural language interface for configuring HyDE
- Intelligent suggestions based on user preferences
- Real-time preview of configuration changes
- Conversation history for complex configuration tasks

To use the AI Assistant:
1. Enter your OpenAI API key in the settings
2. Type your configuration request in natural language
3. Review the suggested changes
4. Apply the changes to your configuration

Example requests:
- "Make my desktop more minimal"
- "Switch to a dark theme with blue accents"
- "Increase window border radius and enable transparency"
- "Optimize performance for gaming"

## Contributing

Contributions to improve the GUI installer are welcome. Please follow the project's contribution guidelines when submitting changes. 
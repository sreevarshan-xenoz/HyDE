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

The AI Configuration Assistant provides a natural language interface for configuring your HyDE desktop environment. It can understand complex requests and suggest appropriate changes to your configuration.

### Features

- Natural language interface for configuring HyDE
- Intelligent suggestions based on your preferences
- Real-time preview of configuration changes
- Conversation history for complex tasks
- Support for both OpenAI API and local models via Ollama

### Requirements

- For OpenAI API:
  - OpenAI API key
- For local models:
  - Ollama installed on your system
  - One of the following models pulled in Ollama:
    - Gemma:2B
    - Phi-3
    - Mistral

### Usage

1. Navigate to the AI Assistant page
2. Select your preferred model type (OpenAI API or Local Ollama)
3. If using OpenAI API, enter your API key
4. Type your configuration request in natural language
5. Review the suggested changes in the preview area
6. Apply the changes if you're satisfied with them

### Example Requests

- "Make my desktop more minimal with rounded corners"
- "Switch to a dark theme with blue accents"
- "Increase the border radius of windows"
- "Change the font to a more modern sans-serif"
- "Make the animations smoother"

### Local Models

The AI Assistant supports local models via Ollama, providing privacy and offline capabilities. To use local models:

1. Install Ollama on your system (https://ollama.ai/)
2. Pull the desired model using Ollama:
   ```
   ollama pull gemma:2b
   ollama pull phi
   ollama pull mistral
   ```
3. Select "Local Ollama" as the model type in the AI Assistant
4. Choose your preferred model from the dropdown

## Contributing

Contributions to improve the GUI installer are welcome. Please follow the project's contribution guidelines when submitting changes. 
#!/usr/bin/env python3

import sys
import os
import json
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                            QComboBox, QCheckBox, QScrollArea, QFrame,
                            QSplitter, QTextEdit, QMessageBox, QLineEdit,
                            QTabWidget, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QPixmap, QTextCursor

# Import our custom modules
from theme_previewer import ThemePreviewGenerator
from settings_manager import SettingsManager
from ai_assistant import AIAssistant

# Add a worker thread for AI processing
class AIWorker(QThread):
    finished = pyqtSignal(dict)
    
    def __init__(self, ai_assistant, user_input):
        super().__init__()
        self.ai_assistant = ai_assistant
        self.user_input = user_input
    
    def run(self):
        result = self.ai_assistant.process_request(self.user_input)
        self.finished.emit(result)

class HyDEGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HyDE Setup")
        self.setMinimumSize(800, 600)
        
        # Initialize components
        self.theme_previewer = ThemePreviewGenerator()
        self.settings_manager = SettingsManager()
        self.ai_assistant = AIAssistant(self.settings_manager)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Create pages
        self.create_welcome_page()
        self.create_install_page()
        self.create_theme_page()
        self.create_settings_page()
        self.create_ai_assistant_page()  # New AI Assistant page
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        layout.addLayout(nav_layout)
        
        # Connect signals
        self.prev_btn.clicked.connect(self.previous_page)
        self.next_btn.clicked.connect(self.next_page)
        
        # Initialize current page
        self.current_page = 0
        self.update_navigation()
    
    def create_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Welcome message
        welcome_label = QLabel("Welcome to HyDE Setup")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(welcome_label)
        
        # Description
        desc_label = QLabel("This wizard will help you set up your HyDE desktop environment.")
        layout.addWidget(desc_label)
        
        # Add more detailed information
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setHtml("""
        <p>HyDE (Hyprdots Desktop Environment) is a customized desktop environment for Linux based on Hyprland.</p>
        <p>This setup wizard will guide you through:</p>
        <ul>
            <li>Installing required packages</li>
            <li>Configuring your desktop environment</li>
            <li>Selecting and customizing themes</li>
            <li>Setting up your preferences</li>
        </ul>
        <p>Click 'Next' to begin the installation process.</p>
        """)
        layout.addWidget(info_text)
        
        self.stacked_widget.addWidget(page)
    
    def create_install_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Installation options
        options_label = QLabel("Installation Options")
        options_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(options_label)
        
        # Package selection
        self.core_packages = QCheckBox("Core Packages")
        self.core_packages.setChecked(True)
        layout.addWidget(self.core_packages)
        
        # Add description for core packages
        core_desc = QLabel("Essential packages required for HyDE to function properly.")
        core_desc.setStyleSheet("font-size: 11px; color: #666;")
        layout.addWidget(core_desc)
        
        self.extra_packages = QCheckBox("Extra Packages")
        layout.addWidget(self.extra_packages)
        
        # Add description for extra packages
        extra_desc = QLabel("Additional packages for enhanced functionality (recommended).")
        extra_desc.setStyleSheet("font-size: 11px; color: #666;")
        layout.addWidget(extra_desc)
        
        # NVIDIA detection
        self.nvidia_detect = QCheckBox("Auto-detect NVIDIA")
        self.nvidia_detect.setChecked(True)
        layout.addWidget(self.nvidia_detect)
        
        # Add description for NVIDIA detection
        nvidia_desc = QLabel("Automatically detect and install NVIDIA drivers if an NVIDIA GPU is present.")
        nvidia_desc.setStyleSheet("font-size: 11px; color: #666;")
        layout.addWidget(nvidia_desc)
        
        # Custom packages section
        custom_label = QLabel("Custom Packages (Optional)")
        custom_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 15px;")
        layout.addWidget(custom_label)
        
        self.custom_packages = QTextEdit()
        self.custom_packages.setPlaceholderText("Enter additional packages to install, one per line")
        self.custom_packages.setMaximumHeight(100)
        layout.addWidget(self.custom_packages)
        
        self.stacked_widget.addWidget(page)
    
    def create_theme_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Theme selection
        theme_label = QLabel("Theme Selection")
        theme_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(theme_label)
        
        # Create a splitter for theme selection and preview
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left side - theme selector
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Theme selector
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Catppuccin-Latte",
            "Catppuccin-Mocha",
            "Decay-Green",
            "Edge-Runner",
            "Frosted-Glass",
            "Graphite-Mono",
            "Gruvbox-Retro",
            "Material-Sakura",
            "Nordic-Blue",
            "Rosé-Pine",
            "Synth-Wave",
            "Tokyo-Night"
        ])
        left_layout.addWidget(QLabel("Select Theme:"))
        left_layout.addWidget(self.theme_combo)
        
        # Theme description
        self.theme_description = QTextEdit()
        self.theme_description.setReadOnly(True)
        self.theme_description.setMaximumHeight(100)
        left_layout.addWidget(QLabel("Description:"))
        left_layout.addWidget(self.theme_description)
        
        # Theme info
        self.theme_info = QLabel()
        left_layout.addWidget(self.theme_info)
        
        # Apply theme button
        self.apply_theme_btn = QPushButton("Apply Theme")
        self.apply_theme_btn.clicked.connect(self.apply_selected_theme)
        left_layout.addWidget(self.apply_theme_btn)
        
        left_layout.addStretch()
        splitter.addWidget(left_widget)
        
        # Right side - theme preview
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        right_layout.addWidget(QLabel("Preview:"))
        
        # Theme preview area
        self.theme_preview = QLabel()
        self.theme_preview.setMinimumSize(400, 300)
        self.theme_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.theme_preview.setFrameStyle(QFrame.Shape.Box)
        right_layout.addWidget(self.theme_preview)
        
        # Generate preview button
        self.generate_preview_btn = QPushButton("Refresh Preview")
        self.generate_preview_btn.clicked.connect(self.refresh_theme_preview)
        right_layout.addWidget(self.generate_preview_btn)
        
        splitter.addWidget(right_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([200, 400])
        
        # Connect theme change signal
        self.theme_combo.currentTextChanged.connect(self.update_theme_preview)
        
        # Load initial theme preview
        self.update_theme_preview(self.theme_combo.currentText())
        
        self.stacked_widget.addWidget(page)
    
    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Settings manager
        settings_label = QLabel("HyDE Settings")
        settings_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(settings_label)
        
        # Create scrollable area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Add various settings sections
        self.add_settings_section(scroll_layout, "Window Management")
        self.add_settings_section(scroll_layout, "Appearance")
        self.add_settings_section(scroll_layout, "Performance")
        self.add_settings_section(scroll_layout, "Notifications")
        
        # Add reset buttons
        reset_layout = QHBoxLayout()
        reset_section_btn = QPushButton("Reset Section")
        reset_all_btn = QPushButton("Reset All")
        
        reset_section_btn.clicked.connect(self.reset_current_section)
        reset_all_btn.clicked.connect(self.reset_all_settings)
        
        reset_layout.addWidget(reset_section_btn)
        reset_layout.addWidget(reset_all_btn)
        scroll_layout.addLayout(reset_layout)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        self.stacked_widget.addWidget(page)
    
    def add_settings_section(self, layout, title):
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.Box)
        section_layout = QVBoxLayout(section)
        
        # Section title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")
        section_layout.addWidget(title_label)
        
        # Add settings based on category
        if title == "Window Management":
            self.add_setting_checkbox(section_layout, "enable_animations", "Enable window animations")
            self.add_setting_checkbox(section_layout, "show_borders", "Show window borders")
        elif title == "Appearance":
            self.add_setting_checkbox(section_layout, "enable_transparency", "Enable transparency")
            self.add_setting_checkbox(section_layout, "show_desktop_icons", "Show desktop icons")
        elif title == "Performance":
            self.add_setting_checkbox(section_layout, "enable_compositing", "Enable compositing")
            self.add_setting_checkbox(section_layout, "reduce_animations", "Reduce animations")
        elif title == "Notifications":
            self.add_setting_checkbox(section_layout, "enable_notifications", "Enable notifications")
            self.add_setting_checkbox(section_layout, "show_badges", "Show notification badges")
        
        layout.addWidget(section)
    
    def add_setting_checkbox(self, layout, setting_key, text):
        checkbox = QCheckBox(text)
        # Get setting value from settings manager
        category = self.get_category_for_setting(setting_key)
        if category:
            value = self.settings_manager.get_setting(category, setting_key)
            checkbox.setChecked(value)
            
            # Connect change signal
            checkbox.stateChanged.connect(lambda state, c=category, k=setting_key: 
                                          self.settings_manager.set_setting(c, k, bool(state)))
        
        layout.addWidget(checkbox)
    
    def get_category_for_setting(self, setting_key):
        """Map setting keys to their categories"""
        mapping = {
            "enable_animations": "window_management",
            "show_borders": "window_management",
            "enable_transparency": "appearance",
            "show_desktop_icons": "appearance",
            "enable_compositing": "performance",
            "reduce_animations": "performance",
            "enable_notifications": "notifications",
            "show_badges": "notifications"
        }
        return mapping.get(setting_key)
    
    def reset_current_section(self):
        """Reset the current settings section"""
        # Determine which section is currently visible
        # This is a simplified implementation
        QMessageBox.information(self, "Reset Section", 
                               "This would reset the current section to default settings.")
    
    def reset_all_settings(self):
        """Reset all settings to default"""
        reply = QMessageBox.question(self, "Reset All Settings", 
                                    "Are you sure you want to reset all settings to default?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.settings_manager.reset_all()
            QMessageBox.information(self, "Settings Reset", 
                                   "All settings have been reset to default values.")
    
    def update_theme_preview(self, theme_name):
        """Update theme preview when a theme is selected"""
        # Update preview image
        preview = self.theme_previewer.get_preview(theme_name)
        if preview:
            # Scale preview to fit the label while maintaining aspect ratio
            scaled_preview = preview.scaled(self.theme_preview.size(), 
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.theme_preview.setPixmap(scaled_preview)
        
        # Update theme description and info
        self.theme_description.setText(f"Description for {theme_name} theme.")
        self.theme_info.setText(f"Author: Unknown\nVersion: 1.0")
    
    def refresh_theme_preview(self):
        """Refresh the theme preview (regenerate)"""
        theme_name = self.theme_combo.currentText()
        preview = self.theme_previewer.get_preview(theme_name, use_cache=False)
        if preview:
            scaled_preview = preview.scaled(self.theme_preview.size(), 
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.theme_preview.setPixmap(scaled_preview)
    
    def apply_selected_theme(self):
        """Apply the selected theme"""
        theme_name = self.theme_combo.currentText()
        QMessageBox.information(self, "Theme Applied", 
                               f"The {theme_name} theme would be applied to your system.")
        # TODO: Actually apply the theme
    
    def create_ai_assistant_page(self):
        """Create the AI Assistant page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Title
        title_label = QLabel("AI Configuration Assistant")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Use natural language to configure your HyDE desktop environment.")
        layout.addWidget(desc_label)
        
        # Create a splitter for the chat interface and settings preview
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left side - chat interface
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Chat history
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        left_layout.addWidget(QLabel("Chat History:"))
        left_layout.addWidget(self.chat_history)
        
        # User input
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your request here...")
        self.user_input.returnPressed.connect(self.send_ai_request)
        input_layout.addWidget(self.user_input)
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_ai_request)
        input_layout.addWidget(send_btn)
        
        left_layout.addLayout(input_layout)
        
        # Clear conversation button
        clear_btn = QPushButton("Clear Conversation")
        clear_btn.clicked.connect(self.clear_ai_conversation)
        left_layout.addWidget(clear_btn)
        
        splitter.addWidget(left_widget)
        
        # Right side - settings preview
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        right_layout.addWidget(QLabel("Settings Preview:"))
        
        # Settings preview area
        self.settings_preview = QTextEdit()
        self.settings_preview.setReadOnly(True)
        right_layout.addWidget(self.settings_preview)
        
        # Apply changes button
        self.apply_changes_btn = QPushButton("Apply Changes")
        self.apply_changes_btn.clicked.connect(self.apply_ai_changes)
        right_layout.addWidget(self.apply_changes_btn)
        
        splitter.addWidget(right_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([400, 400])
        
        # API Key section
        api_group = QGroupBox("AI API Settings")
        api_layout = QFormLayout()
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setText(self.ai_assistant.api_key)
        api_layout.addRow("OpenAI API Key:", self.api_key_input)
        
        save_key_btn = QPushButton("Save API Key")
        save_key_btn.clicked.connect(self.save_api_key)
        api_layout.addRow("", save_key_btn)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        self.stacked_widget.addWidget(page)
        
        # Add initial welcome message
        self.add_ai_message("Hello! I'm your HyDE configuration assistant. How can I help you customize your desktop environment today?")
    
    def send_ai_request(self):
        """Send a request to the AI assistant"""
        user_input = self.user_input.text().strip()
        if not user_input:
            return
        
        # Add user message to chat
        self.add_user_message(user_input)
        
        # Clear input field
        self.user_input.clear()
        
        # Show processing message
        self.add_ai_message("Processing your request...")
        
        # Create and start worker thread
        self.ai_worker = AIWorker(self.ai_assistant, user_input)
        self.ai_worker.finished.connect(self.handle_ai_response)
        self.ai_worker.start()
    
    def handle_ai_response(self, result):
        """Handle the AI response"""
        # Remove the "Processing" message
        self.chat_history.moveCursor(QTextCursor.MoveOperation.End)
        self.chat_history.moveCursor(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor)
        self.chat_history.textCursor().removeSelectedText()
        self.chat_history.textCursor().deletePreviousChar()
        
        if result["success"]:
            # Add AI response to chat
            self.add_ai_message(result["message"])
            
            # Update settings preview
            self.update_settings_preview(result["changes"])
        else:
            # Show error message
            self.add_ai_message(f"Error: {result['message']}")
    
    def add_user_message(self, message):
        """Add a user message to the chat history"""
        self.chat_history.append(f"<b>You:</b> {message}")
        self.chat_history.append("")
    
    def add_ai_message(self, message):
        """Add an AI message to the chat history"""
        self.chat_history.append(f"<b>Assistant:</b> {message}")
        self.chat_history.append("")
    
    def clear_ai_conversation(self):
        """Clear the AI conversation history"""
        self.chat_history.clear()
        self.ai_assistant.clear_conversation()
        self.add_ai_message("Hello! I'm your HyDE configuration assistant. How can I help you customize your desktop environment today?")
        self.settings_preview.clear()
    
    def update_settings_preview(self, changes):
        """Update the settings preview with the changes"""
        if not changes:
            self.settings_preview.setText("No changes were made.")
            return
        
        preview_text = "<h3>Proposed Changes:</h3><ul>"
        for change in changes:
            preview_text += f"<li><b>{change['category']}.{change['key']}</b>: {change['value']}</li>"
        preview_text += "</ul>"
        
        self.settings_preview.setHtml(preview_text)
    
    def apply_ai_changes(self):
        """Apply the AI-suggested changes"""
        # The changes are already applied in the AI assistant's process_request method
        # This is just to confirm and refresh the UI
        QMessageBox.information(self, "Changes Applied", "The suggested changes have been applied to your configuration.")
        
        # Refresh the settings page if it exists
        if hasattr(self, 'settings_page'):
            self.refresh_settings_page()
    
    def save_api_key(self):
        """Save the API key"""
        api_key = self.api_key_input.text().strip()
        if api_key:
            self.ai_assistant.save_api_key(api_key)
            QMessageBox.information(self, "API Key Saved", "Your API key has been saved successfully.")
        else:
            QMessageBox.warning(self, "Invalid API Key", "Please enter a valid API key.")
    
    def refresh_settings_page(self):
        """Refresh the settings page with current values"""
        # This method would update the settings page UI with the current settings
        # Implementation depends on how the settings page is structured
        pass
    
    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.update_navigation()
    
    def next_page(self):
        """Go to the next page"""
        if self.current_page < self.stacked_widget.count() - 1:
            self.current_page += 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.update_navigation()
        elif self.current_page == self.stacked_widget.count() - 1:
            # On the last page, the "Next" button becomes "Finish"
            self.install_hyde()
    
    def update_navigation(self):
        """Update navigation buttons based on current page"""
        self.prev_btn.setEnabled(self.current_page > 0)
        
        if self.current_page == self.stacked_widget.count() - 1:
            self.next_btn.setText("Finish")
        else:
            self.next_btn.setText("Next")
    
    def install_hyde(self):
        """Install HyDE with selected options"""
        # Gather installation options
        options = {
            "core_packages": self.core_packages.isChecked(),
            "extra_packages": self.extra_packages.isChecked(),
            "nvidia_detect": self.nvidia_detect.isChecked(),
            "custom_packages": self.custom_packages.toPlainText().split("\n"),
            "selected_theme": self.theme_combo.currentText()
        }
        
        # Show confirmation dialog
        message = f"""
        Ready to install HyDE with the following options:
        
        - Core Packages: {"Yes" if options["core_packages"] else "No"}
        - Extra Packages: {"Yes" if options["extra_packages"] else "No"}
        - NVIDIA Detection: {"Yes" if options["nvidia_detect"] else "No"}
        - Selected Theme: {options["selected_theme"]}
        """
        
        if any(pkg.strip() for pkg in options["custom_packages"]):
            message += "\nCustom Packages:\n- " + "\n- ".join(
                pkg for pkg in options["custom_packages"] if pkg.strip())
        
        reply = QMessageBox.question(self, "Confirm Installation", 
                                    message,
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # TODO: Implement actual installation
            QMessageBox.information(self, "Installation", 
                                   "HyDE installation would start now.")

def main():
    app = QApplication(sys.argv)
    window = HyDEGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3

import sys
import os
import json
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                            QComboBox, QCheckBox, QScrollArea, QFrame,
                            QSplitter, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap

# Import our custom modules
from theme_previewer import ThemePreviewGenerator
from settings_manager import SettingsManager

class HyDEGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HyDE Setup")
        self.setMinimumSize(800, 600)
        
        # Initialize components
        self.theme_previewer = ThemePreviewGenerator()
        self.settings_manager = SettingsManager()
        
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
    
    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.update_navigation()
    
    def next_page(self):
        if self.current_page < self.stacked_widget.count() - 1:
            self.current_page += 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.update_navigation()
        else:
            self.install_hyde()
    
    def update_navigation(self):
        self.prev_btn.setEnabled(self.current_page > 0)
        if self.current_page == self.stacked_widget.count() - 1:
            self.next_btn.setText("Install")
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
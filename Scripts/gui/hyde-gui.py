#!/usr/bin/env python3

import sys
import os
import json
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                            QComboBox, QCheckBox, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap

class HyDEGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HyDE Setup")
        self.setMinimumSize(800, 600)
        
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
        
        self.extra_packages = QCheckBox("Extra Packages")
        layout.addWidget(self.extra_packages)
        
        # NVIDIA detection
        self.nvidia_detect = QCheckBox("Auto-detect NVIDIA")
        self.nvidia_detect.setChecked(True)
        layout.addWidget(self.nvidia_detect)
        
        self.stacked_widget.addWidget(page)
    
    def create_theme_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Theme selection
        theme_label = QLabel("Theme Selection")
        theme_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(theme_label)
        
        # Theme preview area
        preview_frame = QFrame()
        preview_frame.setFrameStyle(QFrame.Shape.Box)
        preview_layout = QVBoxLayout(preview_frame)
        
        self.theme_preview = QLabel()
        self.theme_preview.setMinimumSize(400, 300)
        preview_layout.addWidget(self.theme_preview)
        
        layout.addWidget(preview_frame)
        
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
        self.theme_combo.currentTextChanged.connect(self.update_theme_preview)
        layout.addWidget(self.theme_combo)
        
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
        
        # Add some example settings
        if title == "Window Management":
            self.add_setting_checkbox(section_layout, "Enable window animations")
            self.add_setting_checkbox(section_layout, "Show window borders")
        elif title == "Appearance":
            self.add_setting_checkbox(section_layout, "Enable transparency")
            self.add_setting_checkbox(section_layout, "Show desktop icons")
        elif title == "Performance":
            self.add_setting_checkbox(section_layout, "Enable compositing")
            self.add_setting_checkbox(section_layout, "Reduce animations")
        elif title == "Notifications":
            self.add_setting_checkbox(section_layout, "Enable notifications")
            self.add_setting_checkbox(section_layout, "Show notification badges")
        
        layout.addWidget(section)
    
    def add_setting_checkbox(self, layout, text):
        checkbox = QCheckBox(text)
        layout.addWidget(checkbox)
    
    def update_theme_preview(self, theme_name):
        # TODO: Implement theme preview loading
        pass
    
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
        # TODO: Implement installation process
        pass

def main():
    app = QApplication(sys.argv)
    window = HyDEGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 
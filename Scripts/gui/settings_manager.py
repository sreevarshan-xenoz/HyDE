#!/usr/bin/env python3

import os
import json
from pathlib import Path

class SettingsManager:
    def __init__(self):
        self.config_dir = Path("~/.config/hyde").expanduser()
        self.settings_file = self.config_dir / "settings.json"
        self.settings = {}
        self.load_settings()
    
    def load_settings(self):
        """Load settings from JSON file"""
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = self.get_default_settings()
            self.save_settings()
    
    def save_settings(self):
        """Save settings to JSON file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get_default_settings(self):
        """Get default settings"""
        return {
            "window_management": {
                "enable_animations": True,
                "show_borders": True,
                "border_width": 2,
                "border_radius": 8
            },
            "appearance": {
                "enable_transparency": True,
                "show_desktop_icons": True,
                "icon_theme": "Papirus",
                "cursor_theme": "Bibata-Modern-Classic"
            },
            "performance": {
                "enable_compositing": True,
                "reduce_animations": False,
                "vsync": True,
                "tearing": False
            },
            "notifications": {
                "enable_notifications": True,
                "show_badges": True,
                "notification_timeout": 5000,
                "notification_position": "top-right"
            }
        }
    
    def get_setting(self, category, key):
        """Get a specific setting value"""
        return self.settings.get(category, {}).get(key)
    
    def set_setting(self, category, key, value):
        """Set a specific setting value"""
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value
        self.save_settings()
    
    def get_category_settings(self, category):
        """Get all settings for a specific category"""
        return self.settings.get(category, {})
    
    def reset_category(self, category):
        """Reset all settings in a category to default"""
        default_settings = self.get_default_settings()
        if category in default_settings:
            self.settings[category] = default_settings[category]
            self.save_settings()
    
    def reset_all(self):
        """Reset all settings to default"""
        self.settings = self.get_default_settings()
        self.save_settings()
    
    def apply_settings(self):
        """Apply current settings to the system"""
        # TODO: Implement settings application
        # This would involve applying the settings to various
        # system components and configuration files
        pass 
#!/usr/bin/env python3

import os
import json
from pathlib import Path

class ThemePreview:
    def __init__(self):
        self.theme_dir = Path("Source/themes")
        self.preview_dir = Path("Source/assets/previews")
        self.current_theme = None
        self.theme_config = {}
    
    def get_theme_preview(self, theme_name):
        """Get the preview image path for a theme"""
        preview_path = self.preview_dir / f"{theme_name.lower()}.png"
        if preview_path.exists():
            return str(preview_path)
        return None
    
    def load_theme_config(self, theme_name):
        """Load theme configuration from JSON file"""
        config_path = self.theme_dir / theme_name / "theme.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.theme_config = json.load(f)
                self.current_theme = theme_name
                return self.theme_config
        return None
    
    def get_theme_colors(self, theme_name):
        """Get the color palette for a theme"""
        config = self.load_theme_config(theme_name)
        if config and 'colors' in config:
            return config['colors']
        return None
    
    def get_theme_info(self, theme_name):
        """Get theme information including name, description, and author"""
        config = self.load_theme_config(theme_name)
        if config:
            return {
                'name': config.get('name', theme_name),
                'description': config.get('description', ''),
                'author': config.get('author', ''),
                'version': config.get('version', '1.0.0')
            }
        return None
    
    def apply_theme_preview(self, theme_name):
        """Apply theme preview to the current session"""
        config = self.load_theme_config(theme_name)
        if not config:
            return False
        
        # TODO: Implement theme preview application
        # This would involve temporarily applying the theme
        # to show how it would look without permanently changing
        # the system configuration
        return True
    
    def get_available_themes(self):
        """Get list of available themes"""
        themes = []
        if self.theme_dir.exists():
            for theme_dir in self.theme_dir.iterdir():
                if theme_dir.is_dir() and (theme_dir / "theme.json").exists():
                    themes.append(theme_dir.name)
        return sorted(themes) 
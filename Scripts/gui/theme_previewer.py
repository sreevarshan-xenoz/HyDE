#!/usr/bin/env python3

import os
import sys
import json
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QFrame, QPushButton, QApplication)
from PyQt6.QtGui import QPixmap, QColor, QPainter, QBrush, QPen
from PyQt6.QtCore import Qt, QRect, QSize

class ThemePreviewGenerator:
    def __init__(self, themes_dir=None, preview_cache_dir=None):
        # Set default directories if not provided
        self.themes_dir = Path(themes_dir) if themes_dir else Path("Source/themes")
        self.preview_cache_dir = Path(preview_cache_dir) if preview_cache_dir else Path("Source/assets/previews")
        
        # Create cache directory if it doesn't exist
        self.preview_cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_theme_colors(self, theme_name):
        """Extract colors from theme configuration"""
        theme_config_path = self.themes_dir / theme_name / "theme.json"
        
        # Default colors in case theme file doesn't exist or is missing colors
        default_colors = {
            "background": "#282c34",
            "foreground": "#abb2bf",
            "accent": "#61afef",
            "secondary": "#c678dd",
            "tertiary": "#98c379",
            "inactive": "#5c6370",
            "warning": "#e5c07b",
            "error": "#e06c75"
        }
        
        if theme_config_path.exists():
            try:
                with open(theme_config_path, 'r') as f:
                    config = json.load(f)
                    colors = config.get("colors", {})
                    
                    # Merge with defaults for any missing colors
                    for key, value in default_colors.items():
                        if key not in colors:
                            colors[key] = value
                    
                    return colors
            except (json.JSONDecodeError, IOError):
                pass
        
        # If we couldn't load from file, use defaults
        return default_colors
    
    def generate_preview(self, theme_name, width=600, height=400):
        """Generate a preview image for a theme"""
        colors = self.get_theme_colors(theme_name)
        
        # Create a QPixmap and paint the preview
        pixmap = QPixmap(width, height)
        painter = QPainter(pixmap)
        
        # Fill background
        painter.fillRect(0, 0, width, height, QColor(colors["background"]))
        
        # Draw window frame
        self._draw_window(painter, colors, 20, 20, 560, 200)
        
        # Draw panel
        self._draw_panel(painter, colors, 20, 240, 560, 60)
        
        # Draw color swatches
        self._draw_color_swatches(painter, colors, 20, 320, 560, 60)
        
        painter.end()
        
        # Save preview to cache
        cache_path = self.preview_cache_dir / f"{theme_name.lower()}.png"
        pixmap.save(str(cache_path))
        
        return pixmap
    
    def _draw_window(self, painter, colors, x, y, width, height):
        """Draw a window with titlebar and content"""
        # Window background
        painter.fillRect(x, y, width, height, QColor(colors["background"]))
        
        # Window border
        pen = QPen(QColor(colors["accent"]))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(x, y, width, height)
        
        # Titlebar
        painter.fillRect(x, y, width, 30, QColor(colors["accent"]))
        
        # Window controls
        painter.setBrush(QBrush(QColor(colors["error"])))
        painter.drawEllipse(x + width - 80, y + 15, 10, 10)
        
        painter.setBrush(QBrush(QColor(colors["warning"])))
        painter.drawEllipse(x + width - 60, y + 15, 10, 10)
        
        painter.setBrush(QBrush(QColor(colors["tertiary"])))
        painter.drawEllipse(x + width - 40, y + 15, 10, 10)
        
        # Window content
        painter.setPen(QPen(QColor(colors["foreground"])))
        painter.drawText(x + 20, y + 70, "Window Title")
        
        # Draw some text lines
        painter.drawText(x + 20, y + 100, "This is a preview of the theme.")
        painter.drawText(x + 20, y + 120, "Text uses the foreground color.")
        
        # Draw accent text
        painter.setPen(QPen(QColor(colors["accent"])))
        painter.drawText(x + 20, y + 150, "Accent colored text")
        
        # Draw secondary text
        painter.setPen(QPen(QColor(colors["secondary"])))
        painter.drawText(x + 20, y + 170, "Secondary colored text")
    
    def _draw_panel(self, painter, colors, x, y, width, height):
        """Draw a panel with buttons"""
        # Panel background
        painter.fillRect(x, y, width, height, QColor(colors["background"]))
        
        # Panel border
        pen = QPen(QColor(colors["inactive"]))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(x, y, width, height)
        
        # Draw buttons
        button_width = 100
        button_height = 30
        button_spacing = 20
        
        # Primary button
        self._draw_button(painter, colors["accent"], colors["background"],
                         x + button_spacing, y + 15, 
                         button_width, button_height, "Primary")
        
        # Secondary button
        self._draw_button(painter, colors["secondary"], colors["background"],
                         x + button_width + button_spacing * 2, y + 15, 
                         button_width, button_height, "Secondary")
        
        # Tertiary button
        self._draw_button(painter, colors["tertiary"], colors["background"],
                         x + button_width * 2 + button_spacing * 3, y + 15, 
                         button_width, button_height, "Tertiary")
        
        # Warning button
        self._draw_button(painter, colors["warning"], colors["background"],
                         x + button_width * 3 + button_spacing * 4, y + 15, 
                         button_width, button_height, "Warning")
    
    def _draw_button(self, painter, bg_color, text_color, x, y, width, height, text):
        """Draw a button with text"""
        painter.fillRect(x, y, width, height, QColor(bg_color))
        painter.setPen(QPen(QColor(text_color)))
        
        # Center text in button
        rect = QRect(x, y, width, height)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
    
    def _draw_color_swatches(self, painter, colors, x, y, width, height):
        """Draw color swatches showing theme colors"""
        swatch_size = 40
        spacing = 10
        current_x = x + spacing
        
        # Draw each color swatch
        for name, color in colors.items():
            painter.fillRect(current_x, y + 10, swatch_size, swatch_size, QColor(color))
            
            # Draw border around swatch
            pen = QPen(QColor(colors["foreground"]))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawRect(current_x, y + 10, swatch_size, swatch_size)
            
            # Draw color name
            painter.drawText(current_x, y + swatch_size + 20, name)
            
            current_x += swatch_size + spacing
            
            # Break to next line if we run out of space
            if current_x > x + width - swatch_size:
                break
    
    def get_cached_preview(self, theme_name):
        """Get a cached preview image if it exists"""
        cache_path = self.preview_cache_dir / f"{theme_name.lower()}.png"
        if cache_path.exists():
            return QPixmap(str(cache_path))
        return None
    
    def get_preview(self, theme_name, width=600, height=400, use_cache=True):
        """Get a preview for a theme, generating if needed"""
        if use_cache:
            cached = self.get_cached_preview(theme_name)
            if cached:
                return cached
        
        return self.generate_preview(theme_name, width, height)

# For standalone testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create a simple window to display the preview
    window = QWidget()
    window.setWindowTitle("Theme Preview Test")
    layout = QVBoxLayout(window)
    
    # Create preview generator
    generator = ThemePreviewGenerator()
    
    # Generate preview for a theme (default or from command line)
    theme_name = sys.argv[1] if len(sys.argv) > 1 else "Catppuccin-Mocha"
    preview = generator.get_preview(theme_name, use_cache=False)
    
    # Display preview
    preview_label = QLabel()
    preview_label.setPixmap(preview)
    layout.addWidget(preview_label)
    
    window.show()
    sys.exit(app.exec()) 
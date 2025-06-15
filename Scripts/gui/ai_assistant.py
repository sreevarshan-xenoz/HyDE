#!/usr/bin/env python3

import os
import json
import re
from pathlib import Path
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HyDE-AI-Assistant")

class AIAssistant:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.config_dir = Path("~/.config/hyde").expanduser()
        self.api_key_file = self.config_dir / "ai_api_key.txt"
        self.api_key = self._load_api_key()
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"  # Default model
        self.conversation_history = []
        
    def _load_api_key(self):
        """Load API key from file or environment variable"""
        if self.api_key_file.exists():
            with open(self.api_key_file, 'r') as f:
                return f.read().strip()
        return os.environ.get("OPENAI_API_KEY", "")
    
    def save_api_key(self, api_key):
        """Save API key to file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.api_key_file, 'w') as f:
            f.write(api_key)
        self.api_key = api_key
    
    def set_model(self, model_name):
        """Set the AI model to use"""
        self.model = model_name
    
    def process_request(self, user_input):
        """Process a natural language request and return a response"""
        if not self.api_key:
            return {
                "success": False,
                "message": "API key not set. Please set your OpenAI API key in the settings.",
                "changes": {}
            }
        
        # Add user input to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Prepare the system message with context about available settings
            system_message = self._get_system_message()
            
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_message},
                    *self.conversation_history
                ],
                "temperature": 0.7
            }
            
            # Make the API request
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            ai_message = result["choices"][0]["message"]["content"]
            
            # Add AI response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            
            # Extract settings changes from the response
            changes = self._extract_settings_changes(ai_message)
            
            return {
                "success": True,
                "message": ai_message,
                "changes": changes
            }
            
        except Exception as e:
            logger.error(f"Error processing AI request: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "changes": {}
            }
    
    def _get_system_message(self):
        """Generate a system message with context about available settings"""
        # Get current settings structure
        settings = self.settings_manager.settings
        
        # Create a description of available settings
        settings_description = json.dumps(settings, indent=2)
        
        return f"""
        You are an AI assistant for the HyDE desktop environment configuration system.
        Your task is to help users configure their desktop environment through natural language.
        
        The user will describe what they want to change, and you should:
        1. Understand their request
        2. Identify which settings need to be changed
        3. Provide a clear explanation of what you're changing
        4. Return a JSON object with the changes in the following format:
        
        {{
            "changes": [
                {{
                    "category": "category_name",
                    "key": "setting_key",
                    "value": "new_value"
                }},
                ...
            ]
        }}
        
        Available settings categories and options:
        {settings_description}
        
        Only include settings that need to be changed. If no changes are needed, return an empty changes array.
        """
    
    def _extract_settings_changes(self, ai_message):
        """Extract settings changes from the AI response"""
        try:
            # Look for JSON in the response
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', ai_message)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON without code block markers
                json_match = re.search(r'({[\s\S]*})', ai_message)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    return {}
            
            # Parse the JSON
            changes_data = json.loads(json_str)
            
            # Apply the changes to the settings
            if "changes" in changes_data:
                for change in changes_data["changes"]:
                    if all(k in change for k in ["category", "key", "value"]):
                        self.settings_manager.set_setting(
                            change["category"],
                            change["key"],
                            change["value"]
                        )
                return changes_data["changes"]
            
            return {}
            
        except Exception as e:
            logger.error(f"Error extracting settings changes: {str(e)}")
            return {}
    
    def clear_conversation(self):
        """Clear the conversation history"""
        self.conversation_history = [] 
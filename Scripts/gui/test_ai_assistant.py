#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from settings_manager import SettingsManager
from ai_assistant import AIAssistant

def main():
    """Test the AI Assistant functionality"""
    print("Testing HyDE AI Assistant...")
    
    # Initialize the settings manager
    settings_manager = SettingsManager()
    
    # Initialize the AI assistant
    ai_assistant = AIAssistant(settings_manager)
    
    # Check if API key is set
    if not ai_assistant.api_key:
        print("No API key found. Please set your OpenAI API key.")
        api_key = input("Enter your OpenAI API key: ")
        ai_assistant.save_api_key(api_key)
    
    # Test a simple request
    print("\nTesting with a simple request...")
    test_request = "Make my desktop more minimal with rounded corners"
    print(f"Request: {test_request}")
    
    result = ai_assistant.process_request(test_request)
    
    if result["success"]:
        print("\nAI Response:")
        print(result["message"])
        
        print("\nChanges made:")
        for change in result["changes"]:
            print(f"- {change['category']}.{change['key']}: {change['value']}")
    else:
        print(f"\nError: {result['message']}")
    
    # Test another request
    print("\nTesting with another request...")
    test_request = "Switch to a dark theme with blue accents"
    print(f"Request: {test_request}")
    
    result = ai_assistant.process_request(test_request)
    
    if result["success"]:
        print("\nAI Response:")
        print(result["message"])
        
        print("\nChanges made:")
        for change in result["changes"]:
            print(f"- {change['category']}.{change['key']}: {change['value']}")
    else:
        print(f"\nError: {result['message']}")
    
    print("\nTest completed.")

if __name__ == "__main__":
    main() 
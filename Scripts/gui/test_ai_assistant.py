#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.append(str(Path(__file__).parent.parent))

from gui.settings_manager import SettingsManager
from gui.ai_assistant import AIAssistant

def main():
    """Test the AI Assistant functionality"""
    print("Testing HyDE AI Assistant...")
    
    # Initialize settings manager and AI assistant
    settings_manager = SettingsManager()
    ai_assistant = AIAssistant(settings_manager)
    
    # Check if we have a model configuration
    if not ai_assistant.model:
        print("No model configuration found. Please select a model type and model.")
        model_type = input("Enter model type (openai/ollama): ").strip().lower()
        
        if model_type == "openai":
            # Check for API key
            if not ai_assistant.api_key:
                api_key = input("Enter your OpenAI API key: ").strip()
                if api_key:
                    ai_assistant.save_api_key(api_key)
                else:
                    print("No API key provided. Exiting.")
                    return
            
            # Set OpenAI model
            model = input("Enter OpenAI model (gpt-3.5-turbo/gpt-4): ").strip()
            ai_assistant.set_model(model, "openai")
        
        elif model_type == "ollama":
            # Check if Ollama is installed
            if not ai_assistant._is_ollama_installed():
                print("Ollama is not installed. Please install Ollama to use local models.")
                return
            
            # Set Ollama model
            model = input("Enter Ollama model (gemma:2b/phi/mistral): ").strip()
            ai_assistant.set_model(model, "ollama")
        
        else:
            print("Invalid model type. Exiting.")
            return
    
    # Test requests
    test_requests = [
        "Make my desktop more minimal with rounded corners",
        "Switch to a dark theme with blue accents"
    ]
    
    for request in test_requests:
        print(f"\nTesting request: {request}")
        response, changes = ai_assistant.process_request(request)
        
        print("\nAI Response:")
        print(response)
        
        if changes:
            print("\nChanges made:")
            for key, value in changes.items():
                print(f"  {key}: {value}")
        else:
            print("\nNo changes were made.")
    
    print("\nTest completed.")

if __name__ == "__main__":
    main() 
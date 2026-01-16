"""
Gemini API integration for Newla AI.
"""

import google.generativeai as genai
import os
from typing import Optional, List, Dict


class GeminiClient:
    """Wrapper for Gemini API calls."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google API key (defaults to env var)
            model: Gemini model to use
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
    
    def call(self, system_prompt: str, user_prompt: str) -> str:
        """
        Make a completion request to Gemini.
        
        Args:
            system_prompt: System instruction
            user_prompt: User message
            
        Returns:
            Gemini's response text
        """
        try:
            # Gemini combines system and user prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = self.model.generate_content(full_prompt)
            
            return response.text
            
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
    def call_with_history(
        self, 
        system_prompt: str, 
        messages: List[Dict[str, str]]
    ) -> str:
        """
        Make a completion request with conversation history.
        
        Args:
            system_prompt: System instruction
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            Gemini's response text
        """
        try:
            # Convert messages to Gemini format
            chat = self.model.start_chat(history=[])
            
            # Add system prompt as first message
            full_conversation = system_prompt + "\n\n"
            
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                full_conversation += f"{role}: {msg['content']}\n\n"
            
            response = self.model.generate_content(full_conversation)
            return response.text
            
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")


def call_gemini(system_prompt: str, user_prompt: str, model: str = "gemini-1.5-flash") -> str:
    """
    Convenience function for Gemini API calls.
    
    Args:
        system_prompt: System instruction
        user_prompt: User message
        model: Model to use
        
    Returns:
        Response text
    """
    client = GeminiClient(model=model)
    return client.call(system_prompt, user_prompt)
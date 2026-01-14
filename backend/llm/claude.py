"""
Claude API integration for Newla AI.
"""
import anthropic
import os
from typing import Optional, Dict, List
class ClaudeClient:
    """Wrapper for Claude API calls."""
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-haiku-20240307"):
        """
        Initialize Claude client.
        Args:
            api_key: Anthropic API key (defaults to env var)
            model: Claude model to use
        """
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("Claude API key not found. Set CLAUDE_API_KEY environment variable.")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
    def call(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        """
        Make a completion request to Claude.
        Args:
            system_prompt: System instruction
            user_prompt: User message
            max_tokens: Maximum tokens in response
            
        Returns:
            Claude's response text
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            raise RuntimeError(f"Claude API error: {str(e)}")
    def call_with_history(
        self, 
        system_prompt: str, 
        messages: List[Dict[str, str]], 
        max_tokens: int = 3000
    ) -> str:
        """
        Make a completion request with conversation history.
        
        Args:
            system_prompt: System instruction
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens in response
            
        Returns:
            Claude's response text
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages
            )
            return message.content[0].text
        except Exception as e:
            raise RuntimeError(f"Claude API error: {str(e)}")


def call_claude(system_prompt: str, user_prompt: str, model: str = "claude-3-haiku-20240307") -> str:
    """
    Convenience function for Claude API calls.
    
    Args:
        system_prompt: System instruction
        user_prompt: User message
        model: Model to use
        
    Returns:
        Response text
    """
    client = ClaudeClient(model=model)
    return client.call(system_prompt, user_prompt)
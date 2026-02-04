"""
LLM Router for Newla AI
Routes requests to Claude or Gemini based on configuration.
"""
from typing import Dict, List, Optional
from .claude import call_claude, ClaudeClient
from .gemini import call_gemini, GeminiClient
class LLMRouter:
    """Routes LLM requests to appropriate provider."""
    def __init__(self,default_provider:str="claude"):
        """
        Initialize LLM router.
        Args:
           default_provider:Default LLM provider("claude"or"gemini")
        """
        self.default_provider = default_provider
        self.claude_client = None
        self.gemini_client = None
    def get_client(self,provider:str):
        """Get or create client for specified provider."""
        if provider == "claude":
            if not self.claude_client:
                self.claude_client = ClaudeClient()
            return self.claude_client
        elif provider == "gemini":
            if not self.gemini_client:
                self.gemini_client = GeminiClient()
            return self.gemini_client
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    def call(self,system_prompt:str,user_prompt:str,provider:Optional[str]=None)->str:
        """Make an LLM completion request.
        Args:
           system_prompt: System instruction
           user_prompt : User message
           provider: LLM provider to use (defaults to default_provider)
        Returns:
           LLM response text
        """
        provider = provider or self.default_provider
        client = self.get_client(provider)
        return client.call(system_prompt,user_prompt)
    def call_with_history(self,system_prompt:str,
                          messages:List[Dict[str,str]],
                          provider:Optional[str]=None)->str:
        """Make an LLM completion request with conversation history.
        Args:
           system_prompt: System instruction
           messages : conversation history
           provider: llm provider to use
        Returns:
           LLM response text
           """
        provider = provider or self.default_provider
        client = self.get_client(provider)
        return client.call_with_history(system_prompt,messages)
    
def call_llm(provider:str,system_prompt:str,user_prompt:str)->str:
        """Convenience function to call any LLM provider.
        Args:
           provider:"claude" or "gemini"
           system_prompt: system instruction
           user_prompt:user message
        Returns:
           LLM response
           """
        if provider =="claude":
            return call_claude(system_prompt,user_prompt)
        elif provider=="gemini":
            return call_gemini(system_prompt,user_prompt)
        else:
            raise ValueError(f"Unsupported LLM provider:{provider}")
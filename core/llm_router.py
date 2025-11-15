"""
Simple LLM Router supporting multiple providers:
- Google Gemini (via google.generativeai)
- OpenAI-compatible endpoints (OpenAI, Anthropic via Messages API, etc.)
- Ollama (local models)
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LLMRouter:
    """Routes LLM requests to the appropriate provider."""
    
    def __init__(self, provider: str, model_name: str, api_key: Optional[str] = None, 
                 api_url: Optional[str] = None, temperature: float = 0.7):
        """
        Initialize the LLM router.
        
        Args:
            provider: One of 'google', 'openai', 'ollama'
            model_name: Model identifier
            api_key: API key (required for google/openai, not for ollama)
            api_url: API URL (optional for openai override, required for ollama)
            temperature: Generation temperature
        """
        self.provider = provider.lower()
        self.model_name = model_name
        self.api_key = api_key
        self.api_url = api_url
        self.temperature = temperature
        self.client = None
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate client based on provider."""
        if self.provider == 'google':
            if not self.api_key:
                raise ValueError("API key required for Google provider")
            try:
                import google.generativeai as genai
            except ImportError:
                raise ImportError("google-generativeai package required. Install with: pip install google-generativeai")
            
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model_name)
            self.genai = genai  # Store reference for later use
            logger.info(f"Initialized Google Gemini client with model: {self.model_name}")
            
        elif self.provider == 'openai':
            if not self.api_key:
                raise ValueError("API key required for OpenAI provider")
            try:
                from openai import OpenAI
            except ImportError:
                raise ImportError("openai package required. Install with: pip install openai")
            
            # Use custom URL if provided, otherwise default OpenAI
            kwargs = {"api_key": self.api_key}
            if self.api_url:
                kwargs["base_url"] = self.api_url
            
            self.client = OpenAI(**kwargs)
            logger.info(f"Initialized OpenAI client with model: {self.model_name}")
            
        elif self.provider == 'ollama':
            try:
                from openai import OpenAI
            except ImportError:
                raise ImportError("openai package required for Ollama. Install with: pip install openai")
            
            # Ollama uses OpenAI-compatible API
            api_url = self.api_url or "http://localhost:11434/v1"
            self.client = OpenAI(
                base_url=api_url,
                api_key="ollama"  # Ollama doesn't need real key but API expects one
            )
            logger.info(f"Initialized Ollama client with model: {self.model_name} at {api_url}")
            
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def generate(self, prompt: str, timeout: int = 120) -> str:
        """
        Generate text using the configured provider.
        
        Args:
            prompt: The input prompt
            timeout: Request timeout in seconds
            
        Returns:
            Generated text response
        """
        if self.provider == 'google':
            return self._generate_google(prompt, timeout)
        elif self.provider in ['openai', 'ollama']:
            return self._generate_openai_compatible(prompt, timeout)
    
    def _generate_google(self, prompt: str, timeout: int) -> str:
        """Generate using Google Gemini."""
        generation_config = self.genai.types.GenerationConfig(temperature=self.temperature)
        
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=generation_config,
                request_options={'timeout': timeout}
            )
            return response.text
        except Exception as e:
            error_msg = str(e).lower()
            if 'timeout' in error_msg or 'deadline' in error_msg:
                logger.warning("Google API call timed out")
                raise TimeoutError("API call timed out")
            elif 'quota' in error_msg or 'resource' in error_msg or 'rate' in error_msg:
                logger.warning(f"Google API resource exhausted: {e}")
                raise
            else:
                logger.error(f"Google API error: {e}")
                raise
    

    def _generate_openai_compatible(self, prompt: str, timeout: int) -> str:
        """Generate using OpenAI-compatible API (OpenAI or Ollama)."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                timeout=timeout
            )

            
            if not response.choices:
                logger.error(
                    "API Error: The response from model '%s' contained no 'choices'. Full response: %s",
                    self.model_name,
                    response.model_dump_json(indent=2)
                )
                raise ValueError("Received an empty list of choices from the API.")

            first_choice = response.choices[0]

            if first_choice.message is None or first_choice.message.content is None:
                logger.warning(
                    "API Warning: Model '%s' returned a null message or content, likely due to content filtering or refusal to answer. Finish reason: '%s'.",
                    self.model_name,
                    first_choice.finish_reason
                )
                return ""
            return first_choice.message.content

        except Exception as e:
            logger.error(f"{self.provider.upper()} API error: {e}")
            raise

    
    @staticmethod
    def list_google_models(api_key: str) -> list[str]:
        """List available Google Gemini models."""
        if not api_key or api_key == 'MISSING_API_KEY':
            logger.error("API Key is missing. Cannot fetch models.")
            return []
        
        try:
            import google.generativeai as genai
        except ImportError:
            logger.error("google-generativeai package required")
            return []
        
        try:
            genai.configure(api_key=api_key)
            available_models = []
            logger.info("Fetching list of available Gemini models...")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            logger.info(f"Found {len(available_models)} compatible models.")
            return available_models
        except Exception as e:
            error_msg = str(e).lower()
            if 'permission' in error_msg or 'auth' in error_msg:
                logger.error("Invalid API Key or permission denied.")
            else:
                logger.error(f"Failed to fetch models: {e}")
            return []
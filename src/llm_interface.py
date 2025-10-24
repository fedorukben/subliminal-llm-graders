"""
LLM Interface Layer
Provides unified interface for multiple LLM providers
"""

import os
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, model_id: str, temperature: float = 0.7, max_retries: int = 3):
        self.model_id = model_id
        self.temperature = temperature
        self.max_retries = max_retries

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate response from the LLM"""
        pass

    def generate_with_retry(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate with exponential backoff retry logic"""
        for attempt in range(self.max_retries):
            try:
                return self.generate(prompt, system_prompt)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = 2 ** attempt
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)


class OpenAIProvider(LLMProvider):
    """OpenAI API provider (GPT models)"""

    def __init__(self, model_id: str, temperature: float = 0.7, max_retries: int = 3):
        super().__init__(model_id, temperature, max_retries)
        import openai
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=self.temperature
        )
        return response.choices[0].message.content


class AnthropicProvider(LLMProvider):
    """Anthropic API provider (Claude models)"""

    def __init__(self, model_id: str, temperature: float = 0.7, max_retries: int = 3):
        super().__init__(model_id, temperature, max_retries)
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        kwargs = {
            "model": self.model_id,
            "max_tokens": 4096,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text


class GoogleProvider(LLMProvider):
    """Google AI provider (Gemini/Gemma models)"""

    def __init__(self, model_id: str, temperature: float = 0.7, max_retries: int = 3):
        super().__init__(model_id, temperature, max_retries)
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model_id)

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = self.model.generate_content(
            full_prompt,
            generation_config={"temperature": self.temperature}
        )
        return response.text


class XAIProvider(LLMProvider):
    """xAI provider (Grok models) - using OpenAI-compatible API"""

    def __init__(self, model_id: str, temperature: float = 0.7, max_retries: int = 3):
        super().__init__(model_id, temperature, max_retries)
        import openai
        self.client = openai.OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=self.temperature
        )
        return response.choices[0].message.content


class LLMFactory:
    """Factory for creating LLM provider instances"""

    PROVIDERS = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "google": GoogleProvider,
        "xai": XAIProvider,
    }

    @classmethod
    def create(cls, provider: str, model_id: str, temperature: float = 0.7) -> LLMProvider:
        """Create an LLM provider instance"""
        if provider not in cls.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(cls.PROVIDERS.keys())}")

        return cls.PROVIDERS[provider](model_id, temperature)


class LLMModel:
    """High-level wrapper for LLM interactions"""

    def __init__(self, name: str, provider: str, model_id: str, temperature: float = 0.7):
        self.name = name
        self.provider_name = provider
        self.model_id = model_id
        self.temperature = temperature
        self.provider = LLMFactory.create(provider, model_id, temperature)
        logger.info(f"Initialized {name} model: {provider}/{model_id}")

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate response with retry logic"""
        return self.provider.generate_with_retry(prompt, system_prompt)

    def __repr__(self):
        return f"LLMModel(name={self.name}, provider={self.provider_name}, model={self.model_id})"

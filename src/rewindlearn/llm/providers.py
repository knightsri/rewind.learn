"""LLM provider clients."""

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from rewindlearn.core.config import Settings
from rewindlearn.core.exceptions import LLMError


class LLMProvider:
    """Factory for LLM clients."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._clients: dict[str, BaseChatModel] = {}

    def get_client(self, model: str) -> BaseChatModel:
        """Get or create an LLM client for the specified model."""
        if model in self._clients:
            return self._clients[model]

        client = self._create_client(model)
        self._clients[model] = client
        return client

    def _create_client(self, model: str) -> BaseChatModel:
        """Create a new LLM client."""
        if model.startswith("claude"):
            api_key = self.settings.anthropic_api_key
            if not api_key:
                raise LLMError("Anthropic API key not configured")
            return ChatAnthropic(
                model=model,
                api_key=api_key,
                max_retries=self.settings.max_retries,
            )
        elif model.startswith("gpt"):
            api_key = self.settings.openai_api_key
            if not api_key:
                raise LLMError("OpenAI API key not configured")
            return ChatOpenAI(
                model=model,
                api_key=api_key,
                max_retries=self.settings.max_retries,
            )
        else:
            raise LLMError(f"Unknown model: {model}")

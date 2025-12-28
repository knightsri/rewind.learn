"""LLM provider clients."""

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from rewindlearn.core.config import Settings
from rewindlearn.core.exceptions import LLMError

# OpenRouter API base URL
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class LLMProvider:
    """Factory for LLM clients.

    Provider selection priority:
    1. OpenRouter (if model contains "/" and openrouter_api_key is set)
    2. Anthropic (if model starts with "claude" and anthropic_api_key is set)
    3. OpenAI (if model starts with "gpt" and openai_api_key is set)
    """

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
        """Create a new LLM client.

        Supports OpenRouter (provider/model format), Anthropic, and OpenAI.
        """
        # OpenRouter format: provider/model (e.g., "anthropic/claude-sonnet-4-20250514")
        if "/" in model and self.settings.openrouter_api_key:
            return ChatOpenAI(
                model=model,
                api_key=self.settings.openrouter_api_key,
                base_url=OPENROUTER_BASE_URL,
                max_retries=self.settings.max_retries,
            )
        # Direct Anthropic access
        elif model.startswith("claude") and self.settings.anthropic_api_key:
            return ChatAnthropic(
                model=model,
                api_key=self.settings.anthropic_api_key,
                max_retries=self.settings.max_retries,
            )
        # Direct OpenAI access
        elif model.startswith("gpt") and self.settings.openai_api_key:
            return ChatOpenAI(
                model=model,
                api_key=self.settings.openai_api_key,
                max_retries=self.settings.max_retries,
            )
        # Fallback error handling
        elif "/" in model:
            raise LLMError(
                f"OpenRouter API key not configured for model: {model}. "
                "Set REWINDLEARN_OPENROUTER_API_KEY"
            )
        elif model.startswith("claude"):
            raise LLMError(
                f"Anthropic API key not configured for model: {model}. "
                "Set REWINDLEARN_ANTHROPIC_API_KEY"
            )
        elif model.startswith("gpt"):
            raise LLMError(
                f"OpenAI API key not configured for model: {model}. "
                "Set REWINDLEARN_OPENAI_API_KEY"
            )
        else:
            raise LLMError(f"Unknown model format: {model}")

"""Tests for configuration module."""

import os

import pytest

from rewindlearn.core.config import Settings, get_settings


def test_settings_defaults():
    """Test that settings have sensible defaults."""
    settings = Settings()
    assert settings.default_provider == "anthropic"
    assert settings.default_model == "claude-sonnet-4-20250514"
    assert settings.max_retries == 3
    assert settings.temperature_default == 0.3


def test_settings_from_env(monkeypatch):
    """Test that settings can be loaded from environment variables."""
    monkeypatch.setenv("REWINDLEARN_ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("REWINDLEARN_DEFAULT_MODEL", "gpt-4")

    settings = Settings()
    assert settings.anthropic_api_key == "test-key"
    assert settings.default_model == "gpt-4"


def test_validate_api_keys_raises_without_keys():
    """Test that validate_api_keys raises when no keys are set."""
    settings = Settings(anthropic_api_key=None, openai_api_key=None)
    with pytest.raises(ValueError, match="No LLM API keys configured"):
        settings.validate_api_keys()


def test_validate_api_keys_passes_with_anthropic():
    """Test that validate_api_keys passes with Anthropic key."""
    settings = Settings(anthropic_api_key="test-key")
    settings.validate_api_keys()  # Should not raise


def test_validate_api_keys_passes_with_openai():
    """Test that validate_api_keys passes with OpenAI key."""
    settings = Settings(openai_api_key="test-key")
    settings.validate_api_keys()  # Should not raise


def test_get_api_key():
    """Test getting API keys by provider name."""
    settings = Settings(anthropic_api_key="anthropic-key", openai_api_key="openai-key")
    assert settings.get_api_key("anthropic") == "anthropic-key"
    assert settings.get_api_key("openai") == "openai-key"
    assert settings.get_api_key("unknown") is None

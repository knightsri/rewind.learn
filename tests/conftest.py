"""Pytest fixtures for Rewind.Learn tests."""

from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_transcript(fixtures_dir: Path) -> Path:
    """Return path to a sample transcript file."""
    return fixtures_dir / "transcripts" / "simple.txt"


@pytest.fixture
def sample_vtt(fixtures_dir: Path) -> Path:
    """Return path to a sample VTT file."""
    return fixtures_dir / "transcripts" / "with-timestamps.vtt"


@pytest.fixture
def sample_chat(fixtures_dir: Path) -> Path:
    """Return path to a sample chat file."""
    return fixtures_dir / "chats" / "zoom-chat.txt"


@pytest.fixture
def templates_dir() -> Path:
    """Return the path to the templates directory."""
    return Path(__file__).parent.parent / "templates"

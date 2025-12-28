"""Tests for file processors."""

from pathlib import Path

import pytest

from rewindlearn.processors import process_input, get_processor_for_file
from rewindlearn.processors.transcript import TranscriptProcessor
from rewindlearn.processors.chat import ChatProcessor


def test_transcript_processor_txt(sample_transcript):
    """Test processing a plain text transcript."""
    processor = TranscriptProcessor()
    result = processor.process(sample_transcript)

    assert result.raw_text
    assert len(result.raw_text) > 0
    assert result.metadata["format"] == "txt"
    assert result.metadata["has_timestamps"]


def test_transcript_processor_vtt(sample_vtt):
    """Test processing a VTT transcript."""
    processor = TranscriptProcessor()
    result = processor.process(sample_vtt)

    assert result.raw_text
    assert len(result.timestamps) > 0
    assert result.metadata["format"] == ".vtt"
    assert result.metadata["has_timestamps"]


def test_chat_processor_zoom(sample_chat):
    """Test processing a Zoom chat file."""
    processor = ChatProcessor()
    result = processor.process(sample_chat)

    assert result.raw_text
    assert result.metadata["format"] == "zoom_txt"
    assert result.metadata["message_count"] > 0


def test_process_input_transcript(sample_transcript):
    """Test process_input with transcript type."""
    result = process_input("transcript", sample_transcript)
    assert result.raw_text
    assert result.metadata["format"] == "txt"


def test_process_input_chat(sample_chat):
    """Test process_input with chat_log type."""
    result = process_input("chat_log", sample_chat)
    assert result.raw_text


def test_process_input_unknown_type(sample_transcript):
    """Test process_input with unknown type raises error."""
    with pytest.raises(ValueError, match="Unknown input type"):
        process_input("unknown", sample_transcript)


def test_get_processor_for_file_txt(sample_transcript):
    """Test getting processor for .txt file."""
    processor = get_processor_for_file(sample_transcript)
    assert processor is not None


def test_get_processor_for_file_vtt(sample_vtt):
    """Test getting processor for .vtt file."""
    processor = get_processor_for_file(sample_vtt)
    assert processor is not None


def test_transcript_add_seconds():
    """Test timestamp arithmetic."""
    processor = TranscriptProcessor()
    assert processor._add_seconds("00:00:30", 30) == "00:01:00"
    assert processor._add_seconds("00:59:30", 30) == "01:00:00"
    assert processor._add_seconds("23:59:30", 30) == "24:00:00"

"""Tests for Whisper STT engine."""

from __future__ import annotations

import numpy as np
import pytest

from src.stt.whisper_engine import WhisperConfig, WhisperEngine


def test_whisper_config_defaults() -> None:
    """Test WhisperConfig default values."""
    config = WhisperConfig()
    assert config.model == "base"
    assert config.device == "cpu"
    assert config.language == "en"
    assert config.vad_filter is True
    assert config.beam_size == 5


def test_whisper_engine_init() -> None:
    """Test WhisperEngine initialization."""
    engine = WhisperEngine()
    assert engine.is_loaded() is False
    assert engine.config.model == "base"


def test_whisper_engine_custom_config() -> None:
    """Test WhisperEngine with custom config."""
    config = WhisperConfig(model="tiny", device="cpu", language="en")
    engine = WhisperEngine(config=config)
    assert engine.config.model == "tiny"
    assert engine.config.device == "cpu"


def test_transcription_result_creation() -> None:
    """Test TranscriptionResult dataclass."""
    from src.stt.whisper_engine import TranscriptionResult

    result = TranscriptionResult(
        text="Hello world",
        confidence=0.95,
        language="en",
        duration=2.5,
    )
    assert result.text == "Hello world"
    assert result.confidence == 0.95
    assert result.language == "en"
    assert result.duration == 2.5


def test_transcribe_without_model_raises() -> None:
    """Test that transcribe raises RuntimeError when model not loaded."""
    engine = WhisperEngine()
    audio = np.zeros(16000, dtype=np.float32)

    with pytest.raises(RuntimeError, match="not loaded"):
        engine.transcribe(audio)
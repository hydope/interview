# StealthInterview - Whisper Speech-to-Text Engine
# Copyright (C) 2026 StealthInterview Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Whisper-based speech-to-text engine for real-time interview transcription."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np
import whisper

logger = logging.getLogger(__name__)


@dataclass
class TranscriptionResult:
    """Result of a speech-to-text transcription."""

    text: str
    confidence: float
    language: str
    duration: float
    timestamp: float = 0.0


@dataclass
class WhisperConfig:
    """Configuration for Whisper STT engine."""

    model: str = "base"
    device: str = "cpu"
    language: str = "en"
    compute_type: str = "int8"
    vad_filter: bool = True
    beam_size: int = 5


class WhisperEngine:
    """
    Real-time speech-to-text engine using OpenAI Whisper.

    Supports streaming transcription for live interview audio with
    voice activity detection and configurable model sizes.
    """

    def __init__(self, config: Optional[WhisperConfig] = None) -> None:
        """
        Initialize the Whisper STT engine.

        Args:
            config: Whisper configuration. Defaults to base model on CPU.
        """
        self.config = config or WhisperConfig()
        self._model: Optional[whisper.Whisper] = None
        self._is_loaded = False
        self._callback: Optional[Callable[[TranscriptionResult], None]] = None

    def load(self) -> None:
        """Load the Whisper model into memory."""
        logger.info(
            "Loading Whisper model '%s' on device '%s'",
            self.config.model,
            self.config.device,
        )
        try:
            self._model = whisper.load_model(
                self.config.model,
                device=self.config.device,
            )
            self._is_loaded = True
            logger.info("Whisper model loaded successfully")
        except Exception as exc:
            logger.error("Failed to load Whisper model: %s", exc)
            raise

    def is_loaded(self) -> bool:
        """Return whether the model is loaded."""
        return self._is_loaded

    def transcribe(self, audio: np.ndarray) -> TranscriptionResult:
        """
        Transcribe audio data to text.

        Args:
            audio: Audio data as numpy array (float32, normalized).

        Returns:
            TranscriptionResult with text, confidence, and metadata.

        Raises:
            RuntimeError: If model is not loaded.
        """
        if not self._is_loaded or self._model is None:
            raise RuntimeError("Whisper model not loaded. Call load() first.")

        logger.debug("Transcribing audio segment (%.2f seconds)", len(audio) / 16000)

        result = self._model.transcribe(
            audio,
            language=self.config.language,
            beam_size=self.config.beam_size,
            vad_filter=self.config.vad_filter,
        )

        return TranscriptionResult(
            text=result.get("text", "").strip(),
            confidence=result.get("confidence", 0.0),
            language=result.get("language", self.config.language),
            duration=len(audio) / 16000,
        )

    def set_callback(self, callback: Callable[[TranscriptionResult], None]) -> None:
        """
        Set a callback function for streaming transcription results.

        Args:
            callback: Function called with each TranscriptionResult.
        """
        self._callback = callback

    def stream_transcribe(self, audio: np.ndarray) -> None:
        """
        Transcribe audio and invoke the callback if set.

        Args:
            audio: Audio data as numpy array.
        """
        result = self.transcribe(audio)
        if self._callback:
            self._callback(result)

    def unload(self) -> None:
        """Unload the model and free memory."""
        self._model = None
        self._is_loaded = False
        logger.info("Whisper model unloaded")
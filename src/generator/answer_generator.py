# StealthInterview - AI Answer Generator
# Copyright (C) 2026 StealthInterview Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""AI answer generation engine for interview responses."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

from src.llm.ollama_client import OllamaClient
from src.stt.whisper_engine import WhisperEngine

logger = logging.getLogger(__name__)


@dataclass
class GenerationConfig:
    """Configuration for answer generation."""

    format: str = "behavioral"  # behavioral, coding, system_design
    response_speed: str = "fast"  # fast, medium, slow
    answer_length: str = "medium"  # short, medium, long
    technical_detail: str = "high"  # low, medium, high
    include_examples: bool = True
    include_code: bool = True


@dataclass
class GeneratedAnswer:
    """Generated interview answer."""

    question: str
    answer: str
    format: str
    tokens_used: int
    duration_ms: float


class AnswerGenerator:
    """
    Generates AI-powered interview answers from transcribed questions.

    Combines Whisper STT and Ollama LLM to produce contextual,
    interview-optimized responses in real time.
    """

    def __init__(
        self,
        stt: WhisperEngine,
        llm: OllamaClient,
        config: Optional[GenerationConfig] = None,
    ) -> None:
        """
        Initialize the answer generator.

        Args:
            stt: Speech-to-text engine instance.
            llm: LLM client instance.
            config: Generation configuration.
        """
        self.stt = stt
        self.llm = llm
        self.config = config or GenerationConfig()

    def _build_system_prompt(self) -> str:
        """Build the system prompt based on generation config."""
        base = (
            "You are an expert interview coach helping a candidate answer "
            "interview questions in real time. Provide concise, confident, "
            "and well-structured answers."
        )

        format_instructions = {
            "behavioral": (
                "Use the STAR method (Situation, Task, Action, Result) "
                "for behavioral questions. Focus on concrete examples "
                "and measurable outcomes."
            ),
            "coding": (
                "For coding questions, explain your approach, time/space "
                "complexity, and provide code examples when appropriate."
            ),
            "system_design": (
                "For system design questions, cover high-level architecture, "
                "scalability, data flow, and trade-offs between approaches."
            ),
        }

        length_instructions = {
            "short": "Keep answers under 60 seconds when spoken.",
            "medium": "Keep answers under 90 seconds when spoken.",
            "long": "Provide comprehensive answers up to 2 minutes when spoken.",
        }

        detail_instructions = {
            "low": "Provide a high-level overview without deep technical details.",
            "medium": "Include moderate technical detail appropriate for the role.",
            "high": "Include detailed technical explanations and implementation specifics.",
        }

        return "\n".join([
            base,
            "",
            f"Format: {self.config.format}",
            format_instructions.get(self.config.format, ""),
            "",
            f"Length: {length_instructions.get(self.config.answer_length, '')}",
            "",
            f"Technical Detail: {detail_instructions.get(self.config.technical_detail, '')}",
            "",
            "Do not mention that you are an AI. Speak directly as the candidate.",
        ])

    def generate(
        self,
        question: str,
        resume_context: Optional[str] = None,
    ) -> GeneratedAnswer:
        """
        Generate an answer to an interview question.

        Args:
            question: The interview question to answer.
            resume_context: Optional resume data for personalization.

        Returns:
            GeneratedAnswer with the AI-generated response.

        Raises:
            RuntimeError: If generation fails.
        """
        import time

        start_time = time.time()

        system_prompt = self._build_system_prompt()

        user_prompt = question
        if resume_context:
            user_prompt = (
                f"Candidate background:\n{resume_context}\n\n"
                f"Question: {question}\n\n"
                "Answer based on this background:"
            )

        logger.info("Generating answer for question: %s", question[:80])

        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        duration_ms = (time.time() - start_time) * 1000

        return GeneratedAnswer(
            question=question,
            answer=response.content,
            format=self.config.format,
            tokens_used=response.tokens_used,
            duration_ms=duration_ms,
        )

    def generate_stream(
        self,
        question: str,
        callback: callable,
        resume_context: Optional[str] = None,
    ) -> str:
        """
        Generate a streaming answer, invoking callback for each chunk.

        Args:
            question: The interview question to answer.
            callback: Function called with each text chunk.
            resume_context: Optional resume data for personalization.

        Returns:
            Full generated response string.
        """
        system_prompt = self._build_system_prompt()

        user_prompt = question
        if resume_context:
            user_prompt = (
                f"Candidate background:\n{resume_context}\n\n"
                f"Question: {question}\n\n"
                "Answer based on this background:"
            )

        return self.llm.generate_stream(
            prompt=user_prompt,
            system_prompt=system_prompt,
            callback=callback,
        )

    def transcribe_and_generate(
        self,
        audio_data,
        resume_context: Optional[str] = None,
    ) -> GeneratedAnswer:
        """
        Transcribe audio and generate an answer in one step.

        Args:
            audio_data: Audio array for transcription.
            resume_context: Optional resume data.

        Returns:
            GeneratedAnswer combining transcription and generation.
        """
        transcription = self.stt.transcribe(audio_data)
        logger.info("Transcribed: %s", transcription.text[:80])

        return self.generate(
            question=transcription.text,
            resume_context=resume_context,
        )
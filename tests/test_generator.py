"""Tests for answer generator."""

from __future__ import annotations

from unittest.mock import MagicMock

from src.generator.answer_generator import AnswerGenerator, GenerationConfig
from src.llm.ollama_client import LLMResponse, OllamaClient
from src.stt.whisper_engine import TranscriptionResult, WhisperEngine


def test_generation_config_defaults() -> None:
    """Test GenerationConfig default values."""
    config = GenerationConfig()
    assert config.format == "behavioral"
    assert config.response_speed == "fast"
    assert config.answer_length == "medium"
    assert config.technical_detail == "high"


def test_answer_generator_build_system_prompt() -> None:
    """Test system prompt generation."""
    mock_stt = MagicMock(spec=WhisperEngine)
    mock_llm = MagicMock(spec=OllamaClient)
    generator = AnswerGenerator(stt=mock_stt, llm=mock_llm)

    prompt = generator._build_system_prompt()
    assert "behavioral" in prompt.lower()
    assert "star" in prompt.lower()


def test_answer_generator_generate() -> None:
    """Test answer generation with mocked LLM."""
    mock_stt = MagicMock(spec=WhisperEngine)
    mock_llm = MagicMock(spec=OllamaClient)
    mock_llm.generate.return_value = LLMResponse(
        content="This is a test answer.",
        model="test-model",
        tokens_used=10,
    )

    generator = AnswerGenerator(stt=mock_stt, llm=mock_llm)
    result = generator.generate(question="Tell me about yourself")

    assert result.answer == "This is a test answer."
    assert result.question == "Tell me about yourself"
    assert result.format == "behavioral"
    assert result.tokens_used == 10


def test_answer_generator_with_resume_context() -> None:
    """Test generation with resume context."""
    mock_stt = MagicMock(spec=WhisperEngine)
    mock_llm = MagicMock(spec=OllamaClient)
    mock_llm.generate.return_value = LLMResponse(
        content="Based on my experience...",
        model="test-model",
    )

    generator = AnswerGenerator(stt=mock_stt, llm=mock_llm)
    result = generator.generate(
        question="What is your experience with Python?",
        resume_context="Skills: Python, Django. Experience: 3 years at Tech Corp.",
    )

    assert "Based on my experience..." in result.answer
    mock_llm.generate.assert_called_once()
    # Verify the prompt includes resume context
    call_args = mock_llm.generate.call_args
    assert "Candidate background" in call_args[1]["prompt"]
# StealthInterview - Ollama LLM Client
# Copyright (C) 2026 StealthInterview Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Ollama LLM client for AI answer generation during interviews."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Optional

import requests

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from the LLM."""

    content: str
    model: str
    tokens_used: int = 0
    duration_ms: float = 0.0


@dataclass
class OllamaConfig:
    """Configuration for Ollama client."""

    model: str = "llama3.2:3b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.7
    max_tokens: int = 512
    top_p: float = 0.9
    stream: bool = True
    timeout: int = 30


class OllamaClient:
    """
    Client for interacting with Ollama LLM API.

    Provides streaming and non-streaming chat completions for
    real-time interview answer generation.
    """

    def __init__(self, config: Optional[OllamaConfig] = None) -> None:
        """
        Initialize the Ollama client.

        Args:
            config: Ollama configuration. Defaults to llama3.2:3b.
        """
        self.config = config or OllamaConfig()
        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})

    def is_available(self) -> bool:
        """Check if the Ollama server is reachable."""
        try:
            response = self._session.get(
                f"{self.config.base_url}/api/tags",
                timeout=5,
            )
            return response.status_code == 200
        except requests.RequestException as exc:
            logger.warning("Ollama server not available: %s", exc)
            return False

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt/question.
            system_prompt: Optional system instruction.
            temperature: Override temperature for this request.
            max_tokens: Override max tokens for this request.

        Returns:
            LLMResponse with generated content.

        Raises:
            RuntimeError: If generation fails.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model,
            "messages": messages,
            "stream": False,
            "temperature": temperature if temperature is not None else self.config.temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.config.max_tokens,
            "top_p": self.config.top_p,
        }

        logger.debug("Sending request to Ollama: %s", payload)

        try:
            response = self._session.post(
                f"{self.config.base_url}/api/chat",
                json=payload,
                timeout=self.config.timeout,
            )
            response.raise_for_status()
            data = response.json()

            return LLMResponse(
                content=data.get("message", {}).get("content", ""),
                model=data.get("model", self.config.model),
                tokens_used=data.get("eval_count", 0),
            )
        except requests.RequestException as exc:
            logger.error("Ollama generation failed: %s", exc)
            raise RuntimeError(f"LLM generation failed: {exc}") from exc

    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        callback: Optional[callable] = None,
    ) -> str:
        """
        Generate a streaming response, invoking callback for each chunk.

        Args:
            prompt: User prompt/question.
            system_prompt: Optional system instruction.
            callback: Function called with each text chunk.

        Returns:
            Full generated response string.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model,
            "messages": messages,
            "stream": True,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
        }

        full_response = ""

        try:
            response = self._session.post(
                f"{self.config.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=self.config.timeout,
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            full_response += content
                            if callback:
                                callback(content)
                    except json.JSONDecodeError:
                        continue

            return full_response
        except requests.RequestException as exc:
            logger.error("Ollama streaming failed: %s", exc)
            raise RuntimeError(f"LLM streaming failed: {exc}") from exc

    def list_models(self) -> list[str]:
        """List available models on the Ollama server."""
        try:
            response = self._session.get(
                f"{self.config.base_url}/api/tags",
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return [m.get("name", "") for m in data.get("models", [])]
        except requests.RequestException as exc:
            logger.error("Failed to list Ollama models: %s", exc)
            return []
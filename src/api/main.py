# StealthInterview - REST API
# Copyright (C) 2026 StealthInterview Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""FastAPI REST API for StealthInterview integration."""

from __future__ import annotations

import logging
import uuid
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.config import load_config  # type: ignore
from src.generator.answer_generator import AnswerGenerator, GenerationConfig
from src.llm.ollama_client import OllamaClient, OllamaConfig
from src.resume.parser import ResumeParser
from src.stt.whisper_engine import WhisperEngine, WhisperConfig

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="StealthInterview API",
    description="REST API for the world's most advanced open-source AI interview copilot",
    version="0.1.0",
    license_info={
        "name": "GPLv3",
        "url": "https://www.gnu.org/licenses/gpl-3.0",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components (initialized on startup)
stt_engine: Optional[WhisperEngine] = None
llm_client: Optional[OllamaClient] = None
answer_generator: Optional[AnswerGenerator] = None
resume_parser: Optional[ResumeParser] = None


# Request/Response models
class GenerateRequest(BaseModel):
    question: str
    format: Optional[str] = "behavioral"
    answer_length: Optional[str] = "medium"
    technical_detail: Optional[str] = "high"
    resume_context: Optional[str] = None


class GenerateResponse(BaseModel):
    question: str
    answer: str
    format: str
    tokens_used: int
    duration_ms: float


class TranscribeRequest(BaseModel):
    audio_base64: str  # Base64-encoded audio data
    language: Optional[str] = "en"


class TranscribeResponse(BaseModel):
    text: str
    confidence: float
    language: str
    duration: float


class ResumeParseResponse(BaseModel):
    skills: list[str]
    experience: list[dict]
    education: list[dict]
    projects: list[dict]
    contact: dict[str, str]


class MockStartRequest(BaseModel):
    format: Optional[str] = "behavioral"
    difficulty: Optional[str] = "medium"
    num_questions: Optional[int] = 5


class MockStartResponse(BaseModel):
    session_id: str
    format: str
    difficulty: str
    num_questions: int
    questions: list[dict]


class HealthResponse(BaseModel):
    status: str
    version: str
    ollama_available: bool


# Startup/shutdown
@app.on_event("startup")
async def startup() -> None:
    """Initialize components on API startup."""
    global stt_engine, llm_client, answer_generator, resume_parser

    logger.info("Starting StealthInterview API...")

    try:
        config = load_config()

        # Initialize STT
        stt_config = WhisperConfig(
            model=config.get("stt", {}).get("model", "base"),
            device=config.get("stt", {}).get("device", "cpu"),
            language=config.get("stt", {}).get("language", "en"),
        )
        stt_engine = WhisperEngine(config=stt_config)
        stt_engine.load()
        logger.info("STT engine initialized")

        # Initialize LLM
        llm_config = OllamaConfig(
            model=config.get("llm", {}).get("model", "llama3.2:3b"),
            base_url=config.get("llm", {}).get("base_url", "http://localhost:11434"),
            temperature=config.get("llm", {}).get("temperature", 0.7),
        )
        llm_client = OllamaClient(config=llm_config)
        if not llm_client.is_available():
            logger.warning("Ollama server not available at %s", llm_config.base_url)

        # Initialize answer generator
        gen_config = GenerationConfig(
            format=config.get("generator", {}).get("format", "behavioral"),
            answer_length=config.get("generator", {}).get("answer_length", "medium"),
            technical_detail=config.get("generator", {}).get("technical_detail", "high"),
        )
        answer_generator = AnswerGenerator(
            stt=stt_engine,
            llm=llm_client,
            config=gen_config,
        )
        logger.info("Answer generator initialized")

        # Initialize resume parser
        resume_parser = ResumeParser()
        logger.info("Resume parser initialized")

        logger.info("StealthInterview API started successfully")
    except Exception as exc:
        logger.error("Failed to initialize API: %s", exc)
        raise


# Endpoints
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health() -> HealthResponse:
    """Health check endpoint."""
    ollama_available = llm_client.is_available() if llm_client else False
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        ollama_available=ollama_available,
    )


@app.post("/generate", response_model=GenerateResponse, tags=["Generation"])
async def generate_answer(request: GenerateRequest) -> GenerateResponse:
    """Generate an AI answer to an interview question."""
    if answer_generator is None:
        raise HTTPException(status_code=503, detail="Answer generator not initialized")

    # Override config for this request
    answer_generator.config.format = request.format
    answer_generator.config.answer_length = request.answer_length
    answer_generator.config.technical_detail = request.technical_detail

    result = answer_generator.generate(
        question=request.question,
        resume_context=request.resume_context,
    )

    return GenerateResponse(
        question=result.question,
        answer=result.answer,
        format=result.format,
        tokens_used=result.tokens_used,
        duration_ms=result.duration_ms,
    )


@app.post("/transcribe", response_model=TranscribeResponse, tags=["Transcription"])
async def transcribe_audio(request: TranscribeRequest) -> TranscribeResponse:
    """Transcribe base64-encoded audio to text."""
    if stt_engine is None:
        raise HTTPException(status_code=503, detail="STT engine not initialized")

    import base64
    import numpy as np

    try:
        audio_bytes = base64.b64decode(request.audio_base64)
        audio = np.frombuffer(audio_bytes, dtype=np.float32)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid audio data: {exc}")

    result = stt_engine.transcribe(audio)

    return TranscribeResponse(
        text=result.text,
        confidence=result.confidence,
        language=result.language,
        duration=result.duration,
    )


@app.post("/resume/parse", response_model=ResumeParseResponse, tags=["Resume"])
async def parse_resume(file_path: str) -> ResumeParseResponse:
    """Parse a resume file and extract structured data."""
    if resume_parser is None:
        raise HTTPException(status_code=503, detail="Resume parser not initialized")

    data = resume_parser.parse(file_path)

    return ResumeParseResponse(
        skills=data.skills,
        experience=data.experience,
        education=data.education,
        projects=data.projects,
        contact=data.contact,
    )


@app.post("/mock/start", response_model=MockStartResponse, tags=["Mock Interview"])
async def start_mock(request: MockStartRequest) -> MockStartResponse:
    """Start a new mock interview session."""
    from src.mock.simulator import MockSimulator

    sim = MockSimulator()
    session = sim.start_session(
        format=request.format,
        difficulty=request.difficulty,
        num_questions=request.num_questions,
    )

    return MockStartResponse(
        session_id=session.id,
        format=session.format,
        difficulty=session.difficulty,
        num_questions=len(session.questions),
        questions=[
            {
                "id": q.id,
                "question": q.question,
                "category": q.category,
                "difficulty": q.difficulty,
                "tags": q.tags,
            }
            for q in session.questions
        ],
    )


@app.get("/config", tags=["System"])
async def get_config() -> dict:
    """Get current API configuration."""
    return {
        "version": "0.1.0",
        "stt": {"model": stt_engine.config.model if stt_engine else None},
        "llm": {"model": llm_client.config.model if llm_client else None},
        "generator": {
            "format": answer_generator.config.format if answer_generator else None,
            "answer_length": answer_generator.config.answer_length if answer_generator else None,
            "technical_detail": answer_generator.config.technical_detail if answer_generator else None,
        },
    }


def main() -> None:
    """Run the API server."""
    import sys

    from src.config import load_config

    config = load_config()
    api_config = config.get("api", {})

    uvicorn.run(
        app,
        host=api_config.get("host", "0.0.0.0"),
        port=api_config.get("port", 8000),
        debug=api_config.get("debug", False),
    )


if __name__ == "__main__":
    main()
"""Tests for resume parser."""

from __future__ import annotations

from src.resume.parser import ResumeData, ResumeParser


def test_resume_data_defaults() -> None:
    """Test ResumeData default values."""
    data = ResumeData()
    assert data.raw_text == ""
    assert data.skills == []
    assert data.experience == []
    assert data.education == []
    assert data.contact == {}


def test_parser_init() -> None:
    """Test ResumeParser initialization."""
    parser = ResumeParser()
    assert parser is not None


def test_extract_section_basic() -> None:
    """Test basic section extraction."""
    parser = ResumeParser()
    text = """
Experience
Software Engineer at Tech Corp (2020-2023)
- Built web applications
- Led team of 5

Education
B.S. Computer Science at University X (2016-2020)
"""

    entries = parser._extract_section(text, "experience")
    assert len(entries) >= 1
    assert any("Tech Corp" in str(e) for e in entries)
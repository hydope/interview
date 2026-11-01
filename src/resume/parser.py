# StealthInterview - Resume Parser
# Copyright (C) 2026 StealthInterview Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Resume parser for extracting skills, experience, and education."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ResumeData:
    """Parsed resume data."""

    raw_text: str = ""
    skills: list[str] = field(default_factory=list)
    experience: list[dict] = field(default_factory=list)
    education: list[dict] = field(default_factory=list)
    projects: list[dict] = field(default_factory=list)
    contact: dict[str, str] = field(default_factory=dict)


class ResumeParser:
    """
    Parses resume files (PDF, DOCX, TXT) to extract structured data
    for interview personalization.
    """

    def __init__(self) -> None:
        """Initialize the resume parser."""
        self._nlp = None

    def parse(self, file_path: str | Path) -> ResumeData:
        """
        Parse a resume file and extract structured data.

        Args:
            file_path: Path to the resume file (PDF, DOCX, or TXT).

        Returns:
            ResumeData with extracted skills, experience, education, etc.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")

        suffix = path.suffix.lower()
        logger.info("Parsing resume: %s (format: %s)", path.name, suffix)

        if suffix == ".pdf":
            raw_text = self._parse_pdf(path)
        elif suffix == ".docx":
            raw_text = self._parse_docx(path)
        elif suffix in (".txt", ".md"):
            raw_text = self._parse_txt(path)
        else:
            raise ValueError(f"Unsupported resume format: {suffix}")

        return self._extract_structured_data(raw_text)

    def _parse_pdf(self, path: Path) -> str:
        """Extract text from a PDF resume."""
        try:
            import pdfminer.high_level

            text = pdfminer.high_level.extract_text(str(path))
            logger.debug("Extracted %d characters from PDF", len(text))
            return text
        except ImportError:
            logger.error("pdfminer.six not installed. Install with: pip install pdfminer.six")
            raise

    def _parse_docx(self, path: Path) -> str:
        """Extract text from a DOCX resume."""
        try:
            import docx

            doc = docx.Document(str(path))
            text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            logger.debug("Extracted %d characters from DOCX", len(text))
            return text
        except ImportError:
            logger.error("python-docx not installed. Install with: pip install python-docx")
            raise

    def _parse_txt(self, path: Path) -> str:
        """Extract text from a TXT/MD resume."""
        text = path.read_text(encoding="utf-8")
        logger.debug("Read %d characters from TXT", len(text))
        return text

    def _extract_structured_data(self, raw_text: str) -> ResumeData:
        """Extract structured fields from raw resume text."""
        data = ResumeData(raw_text=raw_text)

        # Extract skills (simple keyword matching - can be enhanced with spaCy)
        skills_keywords = [
            "python", "javascript", "typescript", "java", "c++", "rust", "go",
            "react", "angular", "vue", "django", "flask", "fastapi", "spring",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "sql", "postgresql", "mongodb", "redis", "elasticsearch",
            "git", "linux", "ci/cd", "jenkins", "github actions",
        ]
        text_lower = raw_text.lower()
        data.skills = [s for s in skills_keywords if s in text_lower]

        # Extract experience section (basic)
        data.experience = self._extract_section(raw_text, "experience")
        data.education = self._extract_section(raw_text, "education")
        data.projects = self._extract_section(raw_text, "projects")

        # Extract contact info (basic email/phone)
        import re

        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text)
        if email_match:
            data.contact["email"] = email_match.group()

        phone_match = re.search(r"(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", raw_text)
        if phone_match:
            data.contact["phone"] = phone_match.group()

        logger.info(
            "Parsed resume: %d skills, %d experience entries, %d education entries",
            len(data.skills),
            len(data.experience),
            len(data.education),
        )

        return data

    def _extract_section(self, text: str, section_name: str) -> list[dict]:
        """Extract a section from resume text (basic implementation)."""
        entries: list[dict] = []
        lines = text.split("\n")
        in_section = False
        current_entry: dict = {}

        section_keywords = {
            "experience": ["experience", "work experience", "employment", "professional experience"],
            "education": ["education", "academic background", "qualifications"],
            "projects": ["projects", "personal projects", "key projects"],
        }

        keywords = section_keywords.get(section_name, [section_name])

        for line in lines:
            line_lower = line.lower().strip()

            # Detect section header
            if any(kw in line_lower for kw in keywords) and len(line) < 50:
                in_section = True
                continue

            # Detect next section (stop current section)
            if in_section and line.strip() and not line.startswith(" "):
                if current_entry:
                    entries.append(current_entry)
                    current_entry = {}
                # Check if this line starts a new known section
                all_keywords = []
                for kws in section_keywords.values():
                    all_keywords.extend(kws)
                if any(kw in line_lower for kw in all_keywords):
                    in_section = False
                    continue

            if in_section and line.strip():
                if not current_entry:
                    current_entry = {"title": line.strip(), "details": []}
                else:
                    current_entry.setdefault("details", []).append(line.strip())

        if current_entry:
            entries.append(current_entry)

        return entries
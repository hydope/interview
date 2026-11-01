# StealthInterview - Mock Interview Simulator
# Copyright (C) 2026 StealthInterview Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Mock interview simulator with real-world question databases."""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

# Sentinel to distinguish "not provided" from "explicitly None"
_SENTINEL = object()


@dataclass
class MockQuestion:
    """A mock interview question."""

    id: str
    question: str
    category: str  # behavioral, coding, system_design
    difficulty: str  # easy, medium, hard
    tags: list[str] = field(default_factory=list)
    sample_answer: Optional[str] = None


@dataclass
class MockSession:
    """A mock interview session."""

    id: str
    format: str
    difficulty: str
    questions: list[MockQuestion] = field(default_factory=list)
    current_index: int = 0
    answers: dict[str, str] = field(default_factory=dict)
    feedback: dict[str, str] = field(default_factory=dict)


# Built-in question banks
BEHAVIORAL_QUESTIONS: list[MockQuestion] = [
    MockQuestion(
        id="beh_001",
        question="Tell me about yourself.",
        category="behavioral",
        difficulty="easy",
        tags=["introduction", "background"],
    ),
    MockQuestion(
        id="beh_002",
        question="Describe a time you faced a challenging situation at work and how you handled it.",
        category="behavioral",
        difficulty="medium",
        tags=["conflict", "problem-solving"],
    ),
    MockQuestion(
        id="beh_003",
        question="Tell me about a time you disagreed with a teammate. How did you resolve it?",
        category="behavioral",
        difficulty="medium",
        tags=["teamwork", "conflict"],
    ),
    MockQuestion(
        id="beh_004",
        question="What is your greatest strength?",
        category="behavioral",
        difficulty="easy",
        tags=["self-awareness"],
    ),
    MockQuestion(
        id="beh_005",
        question="Describe a project you're most proud of.",
        category="behavioral",
        difficulty="medium",
        tags=["achievement"],
    ),
]

CODING_QUESTIONS: list[MockQuestion] = [
    MockQuestion(
        id="code_001",
        question="Reverse a linked list.",
        category="coding",
        difficulty="easy",
        tags=["linked-list", "pointers"],
    ),
    MockQuestion(
        id="code_002",
        question="Implement a function to check if a string is a palindrome.",
        category="coding",
        difficulty="easy",
        tags=["string", "palindrome"],
    ),
    MockQuestion(
        id="code_003",
        question="Find the maximum subarray sum (Kadane's algorithm).",
        category="coding",
        difficulty="medium",
        tags=["array", "dynamic-programming"],
    ),
    MockQuestion(
        id="code_004",
        question="Implement a binary search algorithm.",
        category="coding",
        difficulty="easy",
        tags=["search", "binary-search"],
    ),
    MockQuestion(
        id="code_005",
        question="Merge two sorted linked lists.",
        category="coding",
        difficulty="easy",
        tags=["linked-list", "merge"],
    ),
]

SYSTEM_DESIGN_QUESTIONS: list[MockQuestion] = [
    MockQuestion(
        id="sd_001",
        question="Design a URL shortening service like bit.ly.",
        category="system_design",
        difficulty="medium",
        tags=["scalability", "database", "caching"],
    ),
    MockQuestion(
        id="sd_002",
        question="Design a chat system like WhatsApp.",
        category="system_design",
        difficulty="hard",
        tags=["real-time", "websockets", "scalability"],
    ),
    MockQuestion(
        id="sd_003",
        question="Design a video streaming platform like YouTube.",
        category="system_design",
        difficulty="hard",
        tags=["streaming", "cdn", "storage"],
    ),
]


class MockSimulator:
    """
    Mock interview simulator with question banks for behavioral,
    coding, and system design interviews.
    """

    def __init__(
        self,
        question_bank: str = "default",
        difficulty: str = "medium",
    ) -> None:
        """
        Initialize the mock simulator.

        Args:
            question_bank: Source of questions (default, leetcode, glassdoor, custom).
            difficulty: Default difficulty (easy, medium, hard).
        """
        self.question_bank = question_bank
        self.difficulty = difficulty
        self._question_banks = {
            "behavioral": BEHAVIORAL_QUESTIONS,
            "coding": CODING_QUESTIONS,
            "system_design": SYSTEM_DESIGN_QUESTIONS,
        }

    def get_questions(
        self,
        format: str = "behavioral",
        difficulty: Optional[str] = _SENTINEL,
        count: int = 5,
    ) -> list[MockQuestion]:
        """
        Get mock questions for a given format and difficulty.

        Args:
            format: Interview format (behavioral, coding, system_design).
            difficulty: Question difficulty (easy, medium, hard, all).
                        Use None to disable difficulty filtering.
            count: Number of questions to return.

        Returns:
            List of MockQuestion objects.
        """
        questions = self._question_banks.get(format, [])

        # Use instance default if difficulty not explicitly provided
        if difficulty is _SENTINEL:
            diff = self.difficulty
        else:
            diff = difficulty

        if diff and diff != "all":
            questions = [q for q in questions if q.difficulty == diff]

        random.shuffle(questions)
        return questions[:count]

    def start_session(
        self,
        format: str = "behavioral",
        difficulty: Optional[str] = None,
        num_questions: int = 5,
    ) -> MockSession:
        """
        Start a new mock interview session.

        Args:
            format: Interview format.
            difficulty: Question difficulty.
            num_questions: Number of questions in the session.

        Returns:
            MockSession with selected questions.
        """
        import uuid

        session = MockSession(
            id=str(uuid.uuid4()),
            format=format,
            difficulty=difficulty or self.difficulty,
            questions=self.get_questions(format, difficulty, num_questions),
        )

        logger.info(
            "Started mock session %s: %s format, %d questions",
            session.id,
            format,
            len(session.questions),
        )

        return session

    def submit_answer(
        self,
        session: MockSession,
        question_id: str,
        answer: str,
    ) -> None:
        """
        Submit an answer for a question in the session.

        Args:
            session: The mock session.
            question_id: ID of the question being answered.
            answer: The candidate's answer.
        """
        session.answers[question_id] = answer
        logger.info("Answer submitted for question %s in session %s", question_id, session.id)

    def evaluate(
        self,
        answer: str,
        question: MockQuestion,
    ) -> str:
        """
        Evaluate an answer and provide feedback.

        Args:
            answer: The candidate's answer.
            question: The question being answered.

        Returns:
            Feedback string.
        """
        word_count = len(answer.split())

        feedback_parts: list[str] = []

        if word_count < 30:
            feedback_parts.append("Your answer is quite brief. Consider expanding with more detail.")
        elif word_count > 300:
            feedback_parts.append("Your answer is quite long. Try to be more concise.")
        else:
            feedback_parts.append("Good answer length.")

        if question.category == "behavioral":
            star_keywords = ["situation", "task", "action", "result"]
            found = [k for k in star_keywords if k in answer.lower()]
            if len(found) >= 3:
                feedback_parts.append("Good use of the STAR method.")
            else:
                feedback_parts.append("Consider using the STAR method (Situation, Task, Action, Result).")

        feedback = " ".join(feedback_parts)
        logger.info("Evaluated answer for question %s: %s", question.id, feedback[:80])

        return feedback
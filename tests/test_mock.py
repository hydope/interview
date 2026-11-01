"""Tests for mock interview simulator."""

from __future__ import annotations

from src.mock.simulator import MockSimulator


def test_simulator_init() -> None:
    """Test MockSimulator initialization."""
    sim = MockSimulator()
    assert sim.question_bank == "default"
    assert sim.difficulty == "medium"


def test_get_behavioral_questions() -> None:
    """Test getting behavioral questions."""
    sim = MockSimulator()
    questions = sim.get_questions(format="behavioral", count=3)

    assert len(questions) == 3
    for q in questions:
        assert q.category == "behavioral"


def test_get_coding_questions() -> None:
    """Test getting coding questions."""
    sim = MockSimulator()
    questions = sim.get_questions(format="coding", difficulty=None, count=2)

    assert len(questions) == 2
    for q in questions:
        assert q.category == "coding"


def test_get_system_design_questions() -> None:
    """Test getting system design questions."""
    sim = MockSimulator()
    questions = sim.get_questions(format="system_design", difficulty=None, count=2)

    assert len(questions) == 2
    for q in questions:
        assert q.category == "system_design"


def test_start_session() -> None:
    """Test starting a mock session."""
    sim = MockSimulator()
    session = sim.start_session(format="behavioral", num_questions=3)

    assert session.format == "behavioral"
    assert len(session.questions) == 3
    assert session.id is not None


def test_evaluate_answer() -> None:
    """Test answer evaluation."""
    sim = MockSimulator()

    from src.mock.simulator import MockQuestion

    question = MockQuestion(
        id="test_001",
        question="Tell me about yourself",
        category="behavioral",
        difficulty="easy",
    )

    # Short answer
    feedback = sim.evaluate("I am a developer.", question)
    assert "brief" in feedback.lower() or "length" in feedback.lower()

    # STAR-method answer
    star_answer = (
        "Situation: We had a bug. Task: Fix it. Action: I debugged. "
        "Result: It was fixed."
    )
    feedback = sim.evaluate(star_answer, question)
    assert "STAR" in feedback or "star" in feedback.lower()
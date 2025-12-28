"""LangGraph state definitions."""

from operator import add
from typing import Annotated

from typing_extensions import TypedDict


class SessionState(TypedDict):
    """State for session processing workflow."""

    # Inputs
    transcript: str
    chat_log: str
    slides: str | None
    course_name: str
    session_number: int

    # Task outputs (populated as chains complete)
    session_summary: str | None
    concept_timeline: str | None
    friction_analysis: str | None
    coverage_gaps: str | None
    learning_resources: str | None
    action_items: str | None
    concept_chunks: str | None

    # Metadata
    completed_tasks: Annotated[list[str], add]
    errors: Annotated[list[str], add]

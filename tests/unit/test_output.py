"""Tests for output generation."""

import tempfile
from pathlib import Path

import pytest

from rewindlearn.output.builder import OutputBuilder
from rewindlearn.templates.loader import TemplateLoader


@pytest.fixture
def template(templates_dir):
    """Load the test template."""
    loader = TemplateLoader(templates_dir)
    return loader.load("online-course-v1")


def test_make_filename(template):
    """Test filename generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder = OutputBuilder(template, Path(tmpdir))
        filename = builder._make_filename("session_summary", "md", "AI Engineering", 5)
        assert filename == "ai-engineering-S05-session_summary.md"


def test_make_filename_cleans_course_name(template):
    """Test that course name is cleaned for filename."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder = OutputBuilder(template, Path(tmpdir))
        filename = builder._make_filename("summary", "md", "Python for Data Science!", 1)
        assert "!" not in filename
        assert " " not in filename


def test_add_frontmatter(template):
    """Test frontmatter generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder = OutputBuilder(template, Path(tmpdir))
        content = "# Summary\n\nThis is a summary."
        result = builder._add_frontmatter(content, "session_summary", "AI", 1)

        assert result.startswith("---")
        assert "course: \"AI\"" in result
        assert "session: 1" in result
        assert "deliverable: session_summary" in result
        assert content in result


def test_generate_creates_output_dir(template):
    """Test that generate creates output directory if needed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "nested" / "output"
        builder = OutputBuilder(template, output_dir)
        assert output_dir.exists()


def test_generate_writes_files(template):
    """Test that generate writes output files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder = OutputBuilder(template, Path(tmpdir))
        state = {
            "session_summary": "# Summary\n\nTest summary content.",
            "concept_timeline": "# Timeline\n\n| Timestamp | Concept |",
            "concept_chunks": "concept,description,start_time,end_time\n01_test,desc,00:00:00,00:05:00",
        }

        files = builder.generate(state, "Test Course", 1)

        assert len(files) == 3
        for f in files:
            assert f.exists()
            assert f.stat().st_size > 0

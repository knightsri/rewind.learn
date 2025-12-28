"""Tests for template loader module."""

from pathlib import Path

import pytest

from rewindlearn.core.exceptions import TemplateError
from rewindlearn.templates.loader import TemplateLoader


def test_list_templates(templates_dir):
    """Test listing available templates."""
    loader = TemplateLoader(templates_dir)
    templates = loader.list_templates()
    assert "online-course-v1" in templates


def test_load_valid_template(templates_dir):
    """Test loading a valid template."""
    loader = TemplateLoader(templates_dir)
    template = loader.load("online-course-v1")

    assert template.template_id == "online-course"
    assert template.name == "Online Course Session"
    assert template.version == "1.0"
    assert "transcript" in template.inputs.required


def test_load_template_not_found():
    """Test that loading non-existent template raises error."""
    loader = TemplateLoader(Path("/nonexistent"))
    with pytest.raises(TemplateError, match="Template not found"):
        loader.load("nonexistent-template")


def test_template_get_tasks(templates_dir):
    """Test getting tasks from a template."""
    loader = TemplateLoader(templates_dir)
    template = loader.load("online-course-v1")
    tasks = template.get_tasks()

    assert len(tasks) >= 3
    task_names = [t.name for t in tasks]
    assert "session_summary" in task_names
    assert "concept_timeline" in task_names


def test_template_build_dependency_graph(templates_dir):
    """Test building dependency graph from template."""
    loader = TemplateLoader(templates_dir)
    template = loader.load("online-course-v1")
    graph = template.build_dependency_graph()

    # session_summary has no dependencies
    assert graph["session_summary"] == []
    # friction_analysis depends on session_summary
    assert "session_summary" in graph["friction_analysis"]


def test_validate_template(fixtures_dir):
    """Test template validation."""
    loader = TemplateLoader(fixtures_dir / "templates")
    valid, errors = loader.validate(fixtures_dir / "templates" / "valid-template.yaml")
    assert valid
    assert len(errors) == 0


def test_validate_invalid_template(fixtures_dir):
    """Test validation of invalid template."""
    loader = TemplateLoader(fixtures_dir / "templates")
    valid, errors = loader.validate(fixtures_dir / "templates" / "invalid-template.yaml")
    assert not valid
    assert len(errors) > 0

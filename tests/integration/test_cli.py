"""Integration tests for CLI."""

import pytest
from typer.testing import CliRunner

from rewindlearn.cli.main import app


runner = CliRunner()


def test_cli_version():
    """Test that --version shows version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "rewindlearn" in result.stdout


def test_cli_help():
    """Test that --help shows help."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Transform session artifacts" in result.stdout


def test_cli_config_show():
    """Test config show command."""
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "Default Provider" in result.stdout


def test_cli_template_list(templates_dir, monkeypatch):
    """Test template list command."""
    monkeypatch.setenv("REWINDLEARN_TEMPLATES_DIR", str(templates_dir))
    result = runner.invoke(app, ["template", "list"])
    # May show templates or "No templates found"
    assert result.exit_code == 0


def test_cli_process_missing_transcript():
    """Test that process run fails without transcript."""
    result = runner.invoke(app, ["process", "run", "--template", "online-course"])
    assert result.exit_code != 0  # Should fail due to missing required option

"""Rewind.Learn - Transform session artifacts into structured knowledge."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("rewindlearn")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

# Public API exports
from rewindlearn.core.config import Settings
from rewindlearn.templates.loader import TemplateLoader
from rewindlearn.workflow.executor import process_session

__all__ = [
    "__version__",
    "process_session",
    "TemplateLoader",
    "Settings",
]

# Rewind.Learn - Master Implementation Specification

> **Purpose:** This is the single source of truth for building the Rewind.Learn Python library.
> Hand this document to Claude Code with: "Build this project following this specification."

---

## 🎯 Project Overview

**Name:** Rewind.Learn  
**Goal:** A Python library that transforms session artifacts (transcripts, chat logs) into structured learning materials.

**Primary Deliverable:** `pip install rewindlearn` - a PyPI-published package  
**Secondary Deliverable:** Docker container for containerized deployments

**What It Does:**
```
Input:  Session artifacts (transcript.vtt, chat.txt, slides.pdf)
        + Template (online-course.yaml)
        ↓
Process: LangGraph workflow with parallel LLM chains
        ↓
Output: Study guide, concept timeline, friction analysis, 
        video clip markers (CSV), action items
```

---

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Rewind.Learn Architecture                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │   CLI       │    │  Python API │    │   Docker    │                     │
│  │  (Typer)    │    │  (Import)   │    │  Container  │                     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                     │
│         │                  │                  │                             │
│         └──────────────────┼──────────────────┘                             │
│                            ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        TEMPLATE ENGINE                               │   │
│  │   • YAML template loading & validation                               │   │
│  │   • Task dependency resolution                                       │   │
│  │   • Prompt template management                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                            │                                                │
│         ┌──────────────────┼──────────────────┐                            │
│         ▼                  ▼                  ▼                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │ Processors  │    │   Chains    │    │   Output    │                     │
│  │ • Transcript│    │ • Summary   │    │ • Markdown  │                     │
│  │ • Chat      │    │ • Timeline  │    │ • CSV       │                     │
│  │ • (Slides)  │    │ • Friction  │    │ • (PDF)     │                     │
│  └─────────────┘    │ • Coverage  │    └─────────────┘                     │
│                     │ • Resources │                                        │
│                     │ • Actions   │                                        │
│                     │ • Chunks    │                                        │
│                     └──────┬──────┘                                        │
│                            │                                                │
│  ┌─────────────────────────┴───────────────────────────────────────────┐   │
│  │                      LANGGRAPH WORKFLOW                              │   │
│  │   • Parallel execution of independent tasks                          │   │
│  │   • Dependency-based task ordering                                   │   │
│  │   • Progress tracking & error handling                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                            │                                                │
│                            ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        LLM ROUTER                                    │   │
│  │   • Anthropic (Claude) - Primary                                     │   │
│  │   • OpenAI (GPT) - Fallback                                          │   │
│  │   • LangSmith tracing                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
rewind.learn/
├── src/
│   └── rewindlearn/
│       ├── __init__.py              # Package exports + version
│       ├── __main__.py              # python -m rewindlearn
│       ├── py.typed                 # PEP 561 type hint marker
│       │
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── main.py              # Typer CLI app
│       │   └── commands/
│       │       ├── __init__.py
│       │       ├── process.py       # rewindlearn process
│       │       ├── config.py        # rewindlearn config
│       │       └── template.py      # rewindlearn template
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py            # Pydantic Settings
│       │   ├── exceptions.py        # Custom exceptions
│       │   └── logging.py           # Rich logging setup
│       │
│       ├── templates/
│       │   ├── __init__.py
│       │   ├── loader.py            # YAML template loader
│       │   ├── validator.py         # Schema validation
│       │   └── models.py            # Pydantic models
│       │
│       ├── processors/
│       │   ├── __init__.py          # Processor registry
│       │   ├── base.py              # Abstract base class
│       │   ├── transcript.py        # .txt, .vtt, .srt handlers
│       │   └── chat.py              # Zoom/Teams chat handlers
│       │
│       ├── chains/
│       │   ├── __init__.py          # Chain factory
│       │   ├── base.py              # Base chain class
│       │   ├── summary.py           # Session summary
│       │   ├── timeline.py          # Concept timeline
│       │   ├── friction.py          # Friction analysis
│       │   ├── coverage.py          # Coverage gaps
│       │   ├── resources.py         # Learning resources
│       │   ├── actions.py           # Action items
│       │   └── chunks.py            # Concept chunks (CSV)
│       │
│       ├── workflow/
│       │   ├── __init__.py
│       │   ├── state.py             # LangGraph state
│       │   ├── graph.py             # Workflow builder
│       │   └── executor.py          # Execution engine
│       │
│       ├── output/
│       │   ├── __init__.py
│       │   ├── builder.py           # Output orchestrator
│       │   ├── markdown.py          # Markdown generation
│       │   └── csv.py               # CSV generation
│       │
│       └── llm/
│           ├── __init__.py
│           ├── providers.py         # Anthropic/OpenAI clients
│           └── router.py            # Model routing + fallback
│
├── templates/                        # Built-in YAML templates
│   └── online-course-v1.yaml
│
├── examples/                         # Reference implementations (DEFERRED)
│   ├── README.md                    # Explains deferred features
│   ├── video_chunker.py             # FFmpeg video splitting example
│   └── pdf_converter.py             # WeasyPrint PDF example
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── fixtures/
│   │   ├── transcripts/
│   │   │   ├── simple.txt
│   │   │   └── with-timestamps.vtt
│   │   ├── chats/
│   │   │   └── zoom-chat.txt
│   │   └── templates/
│   │       ├── valid-template.yaml
│   │       └── invalid-template.yaml
│   ├── unit/
│   │   ├── test_config.py
│   │   ├── test_template_loader.py
│   │   ├── test_processors.py
│   │   └── test_output.py
│   └── integration/
│       ├── test_workflow.py
│       └── test_cli.py
│
├── docs/
│   ├── index.md
│   ├── quickstart.md
│   ├── templates.md
│   └── api.md
│
├── .github/
│   └── workflows/
│       ├── test.yml                 # CI on PR
│       └── publish.yml              # PyPI on release
│
├── scripts/
│   ├── docker-run.sh               # Docker helper
│   └── docker-process.sh           # Quick process script
│
├── pyproject.toml                   # Package metadata
├── Dockerfile                       # Production container
├── Dockerfile.dev                   # Development container
├── docker-compose.yaml              # Container orchestration
├── .env.example                     # Environment template
├── .gitignore
├── README.md
├── LICENSE                          # Apache-2.0
└── CHANGELOG.md
```

---

## 🚀 Implementation Phases

### Phase 1: Project Foundation & Docker

**Goal:** Scaffolding that allows `pip install -e .` and `docker compose build` immediately.

#### 1.1 Create pyproject.toml

**File: `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "rewindlearn"
version = "0.1.0"
description = "Transform session artifacts into structured knowledge"
readme = "README.md"
license = "Apache-2.0"
requires-python = ">=3.10"
authors = [
    { name = "Sri Bolisetty", email = "sri@example.com" }
]
keywords = ["langchain", "llm", "education", "transcription", "ai", "learning"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Education",
    "Topic :: Text Processing :: Linguistic",
    "Typing :: Typed",
]

dependencies = [
    # LLM Framework
    "langchain>=0.3",
    "langchain-anthropic>=0.3",
    "langchain-openai>=0.2",
    "langgraph>=0.2",
    "langsmith>=0.1",
    
    # CLI
    "typer[all]>=0.12",
    "rich>=13.0",
    
    # Data Validation
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    
    # File Processing
    "pyyaml>=6.0",
    "python-dotenv>=1.0",
    "webvtt-py>=0.5",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-cov>=5.0",
    "black>=24.0",
    "ruff>=0.4",
    "mypy>=1.10",
    "pre-commit>=3.0",
]
docs = [
    "mkdocs>=1.6",
    "mkdocs-material>=9.5",
    "mkdocstrings[python]>=0.25",
]
# Optional heavy dependencies for examples
examples = [
    "weasyprint>=62",
    "ffmpeg-python>=0.2",
    "pymupdf>=1.24",
]

[project.scripts]
rewindlearn = "rewindlearn.cli.main:app"

[project.urls]
Homepage = "https://github.com/knightsri/rewind.learn"
Documentation = "https://rewindlearn.readthedocs.io"
Repository = "https://github.com/knightsri/rewind.learn"
Issues = "https://github.com/knightsri/rewind.learn/issues"
Changelog = "https://github.com/knightsri/rewind.learn/blob/main/CHANGELOG.md"

[tool.hatch.build.targets.wheel]
packages = ["src/rewindlearn"]

[tool.hatch.build.targets.sdist]
include = [
    "/src",
    "/templates",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "slow: marks tests as slow",
    "integration: integration tests requiring API keys",
]

[tool.coverage.run]
source = ["src/rewindlearn"]
omit = ["*/tests/*", "*/__main__.py"]

[tool.black]
line-length = 100
target-version = ["py310", "py311", "py312"]

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
```

#### 1.2 Create Package Entry Points

**File: `src/rewindlearn/__init__.py`**

```python
"""Rewind.Learn - Transform session artifacts into structured knowledge."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("rewindlearn")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

# Public API exports
from rewindlearn.workflow.executor import process_session
from rewindlearn.templates.loader import TemplateLoader
from rewindlearn.core.config import Settings

__all__ = [
    "__version__",
    "process_session",
    "TemplateLoader",
    "Settings",
]
```

**File: `src/rewindlearn/__main__.py`**

```python
"""Entry point for python -m rewindlearn."""

from rewindlearn.cli.main import app

if __name__ == "__main__":
    app()
```

**File: `src/rewindlearn/py.typed`**

```
# PEP 561 marker file - indicates this package supports type hints
```

#### 1.3 Docker Configuration

**File: `Dockerfile`**

```dockerfile
# =============================================================================
# Rewind.Learn Production Dockerfile
# Multi-stage build for minimal image size
# =============================================================================

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN pip install --no-cache-dir build

# Copy source files needed for build
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/
COPY templates/ templates/

# Build wheel
RUN python -m build --wheel

# =============================================================================
# Runtime stage
# =============================================================================
FROM python:3.11-slim

LABEL maintainer="Sri Bolisetty"
LABEL description="Rewind.Learn - Transform session artifacts into structured knowledge"
LABEL version="0.1.0"

WORKDIR /app

# Install the wheel from build stage
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

# Copy built-in templates
COPY templates/ /app/templates/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash rewindlearn && \
    mkdir -p /data/input /data/output && \
    chown -R rewindlearn:rewindlearn /data

USER rewindlearn

# Environment defaults
ENV REWINDLEARN_TEMPLATES_DIR=/app/templates
ENV REWINDLEARN_OUTPUT_DIR=/data/output

# Working directory for data
WORKDIR /data

ENTRYPOINT ["rewindlearn"]
CMD ["--help"]
```

**File: `Dockerfile.dev`**

```dockerfile
# =============================================================================
# Rewind.Learn Development Dockerfile
# Includes dev dependencies and source mounting
# =============================================================================

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md LICENSE ./

# Install package in editable mode with dev dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Copy source (will be overwritten by volume mount in dev)
COPY . .

# Create data directories
RUN mkdir -p /data/input /data/output

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["bash"]
```

**File: `docker-compose.yaml`**

```yaml
version: "3.9"

services:
  # Production container
  rewindlearn:
    build:
      context: .
      dockerfile: Dockerfile
    image: rewindlearn:latest
    container_name: rewindlearn
    environment:
      - REWINDLEARN_ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REWINDLEARN_OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - REWINDLEARN_LANGSMITH_API_KEY=${LANGSMITH_API_KEY:-}
      - REWINDLEARN_LANGSMITH_TRACING=${LANGSMITH_TRACING:-false}
    volumes:
      - ./data/input:/data/input:ro
      - ./data/output:/data/output
      - ./templates:/app/templates:ro
    working_dir: /data

  # Development container with source mounted
  dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    image: rewindlearn:dev
    container_name: rewindlearn-dev
    environment:
      - REWINDLEARN_ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REWINDLEARN_OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - REWINDLEARN_LANGSMITH_API_KEY=${LANGSMITH_API_KEY:-}
      - REWINDLEARN_LANGSMITH_TRACING=${LANGSMITH_TRACING:-true}
    volumes:
      - .:/app
      - ./data:/data
    working_dir: /app
    command: bash
    stdin_open: true
    tty: true

  # Test runner
  test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    image: rewindlearn:dev
    environment:
      - PYTHONPATH=/app/src
    volumes:
      - .:/app
    working_dir: /app
    command: pytest -v --cov=src/rewindlearn --cov-report=term-missing
```

#### 1.4 Environment Template

**File: `.env.example`**

```bash
# =============================================================================
# Rewind.Learn Configuration
# Copy this file to .env and fill in your values
# =============================================================================

# LLM Provider API Keys (at least one required)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# LangSmith Observability (optional but recommended)
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_TRACING=true

# Rewind.Learn Settings
REWINDLEARN_DEFAULT_PROVIDER=anthropic
REWINDLEARN_DEFAULT_MODEL=claude-sonnet-4-20250514
REWINDLEARN_TEMPLATES_DIR=./templates
REWINDLEARN_OUTPUT_DIR=./output
```

#### 1.5 Core Files

**File: `README.md`**

```markdown
# Rewind.Learn

Transform session artifacts into structured knowledge.

[![PyPI version](https://badge.fury.io/py/rewindlearn.svg)](https://badge.fury.io/py/rewindlearn)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Installation

```bash
pip install rewindlearn
```

## Quick Start

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-key"

# Process a session
rewindlearn process \
    --template online-course \
    --transcript lecture.vtt \
    --chat chat.txt \
    --course "AI Engineering" \
    --session 5 \
    --output study-guides/
```

## Docker

```bash
docker run -v $(pwd)/data:/data \
    -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    rewindlearn process \
    --template online-course \
    --transcript /data/lecture.vtt \
    --output /data/output
```

## Python API

```python
import asyncio
from rewindlearn import process_session

async def main():
    results = await process_session(
        template="online-course",
        transcript_path="lecture.vtt",
        chat_path="chat.txt",
        course_name="AI Engineering",
        session_number=5
    )
    results.save_all("study-guides/")

asyncio.run(main())
```

## License

Apache 2.0
```

**File: `LICENSE`**

```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
   ... (full Apache 2.0 license text)
```

**File: `.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.tox/
.coverage
.coverage.*
htmlcov/
.pytest_cache/
.mypy_cache/

# Environment
.env
.env.local

# Output
output/
data/output/

# OS
.DS_Store
Thumbs.db
```

#### Phase 1 Tasks Checklist

```
[ ] Create directory structure as specified above
[ ] Create pyproject.toml
[ ] Create src/rewindlearn/__init__.py
[ ] Create src/rewindlearn/__main__.py
[ ] Create src/rewindlearn/py.typed
[ ] Create Dockerfile (production)
[ ] Create Dockerfile.dev (development)
[ ] Create docker-compose.yaml
[ ] Create .env.example
[ ] Create README.md
[ ] Create LICENSE (Apache 2.0)
[ ] Create .gitignore
[ ] Create empty __init__.py in all package directories
[ ] Verify: pip install -e . works
[ ] Verify: docker compose build works
[ ] Verify: rewindlearn --help shows usage (will fail until CLI implemented)
```

---

### Phase 2: Configuration System

**Goal:** Centralized configuration with environment variable support.

#### 2.1 Settings Class

**File: `src/rewindlearn/core/__init__.py`**

```python
"""Core configuration and utilities."""

from rewindlearn.core.config import Settings
from rewindlearn.core.exceptions import RewindLearnError

__all__ = ["Settings", "RewindLearnError"]
```

**File: `src/rewindlearn/core/config.py`**

```python
"""Application configuration using Pydantic Settings."""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="REWINDLEARN_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM Providers
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    default_provider: str = Field(default="anthropic", description="Default LLM provider")
    default_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Default model to use"
    )

    # LangSmith Observability
    langsmith_api_key: Optional[str] = Field(default=None, description="LangSmith API key")
    langsmith_project: str = Field(default="rewindlearn", description="LangSmith project name")
    langsmith_tracing: bool = Field(default=False, description="Enable LangSmith tracing")

    # Processing Settings
    max_retries: int = Field(default=3, ge=1, le=10, description="Max LLM retry attempts")
    temperature_default: float = Field(default=0.3, ge=0.0, le=1.0)
    max_tokens_default: int = Field(default=4000, gt=0)

    # Paths
    templates_dir: Path = Field(default=Path("templates"), description="Templates directory")
    output_dir: Path = Field(default=Path("output"), description="Output directory")

    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for the specified provider."""
        if provider == "anthropic":
            return self.anthropic_api_key
        elif provider == "openai":
            return self.openai_api_key
        return None

    def validate_api_keys(self) -> None:
        """Raise error if no API keys are configured."""
        if not self.anthropic_api_key and not self.openai_api_key:
            raise ValueError(
                "No LLM API keys configured. "
                "Set REWINDLEARN_ANTHROPIC_API_KEY or REWINDLEARN_OPENAI_API_KEY"
            )


# Global settings instance (lazy loaded)
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
```

#### 2.2 Custom Exceptions

**File: `src/rewindlearn/core/exceptions.py`**

```python
"""Custom exceptions for Rewind.Learn."""


class RewindLearnError(Exception):
    """Base exception for Rewind.Learn."""

    pass


class ConfigurationError(RewindLearnError):
    """Configuration-related errors."""

    pass


class TemplateError(RewindLearnError):
    """Template loading or validation errors."""

    pass


class ProcessorError(RewindLearnError):
    """File processing errors."""

    pass


class WorkflowError(RewindLearnError):
    """Workflow execution errors."""

    pass


class LLMError(RewindLearnError):
    """LLM invocation errors."""

    pass
```

#### 2.3 Logging Setup

**File: `src/rewindlearn/core/logging.py`**

```python
"""Structured logging with Rich."""

import logging
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

# Global console for CLI output
console = Console()


def setup_logging(level: str = "INFO", verbose: bool = False) -> None:
    """Configure logging with Rich handler."""
    log_level = logging.DEBUG if verbose else getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                show_time=verbose,
                show_path=verbose,
            )
        ],
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name or "rewindlearn")
```

#### Phase 2 Tasks Checklist

```
[ ] Create src/rewindlearn/core/__init__.py
[ ] Create src/rewindlearn/core/config.py
[ ] Create src/rewindlearn/core/exceptions.py
[ ] Create src/rewindlearn/core/logging.py
[ ] Verify: Settings loads from .env
[ ] Verify: Settings loads from environment variables
[ ] Test: Missing API keys raises appropriate error
```

---

### Phase 3: Template Engine

**Goal:** Load and validate YAML templates that define processing workflows.

#### 3.1 Template Models

**File: `src/rewindlearn/templates/__init__.py`**

```python
"""Template engine for processing workflows."""

from rewindlearn.templates.loader import TemplateLoader
from rewindlearn.templates.models import Template, TaskDefinition

__all__ = ["TemplateLoader", "Template", "TaskDefinition"]
```

**File: `src/rewindlearn/templates/models.py`**

```python
"""Pydantic models for template definitions."""

from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class LLMConfig(BaseModel):
    """LLM configuration for a task."""

    model: str = "claude-sonnet-4-20250514"
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4000, gt=0)
    fallback_model: Optional[str] = None


class TaskDefinition(BaseModel):
    """Definition of a single processing task."""

    name: str = Field(description="Unique task identifier")
    prompt_template: str = Field(description="Prompt template with {placeholders}")
    llm_config: LLMConfig = Field(default_factory=LLMConfig)
    dependencies: list[str] = Field(default_factory=list)
    output_format: Literal["markdown", "csv", "json"] = "markdown"


class InputSchema(BaseModel):
    """Schema for template inputs."""

    required: list[str] = Field(description="Required input fields")
    optional: list[str] = Field(default_factory=list)


class OutputSchema(BaseModel):
    """Schema for template outputs."""

    deliverables: list[str] = Field(description="List of output deliverables")
    formats: list[Literal["markdown", "pdf", "html", "csv"]] = Field(default=["markdown"])
    languages: list[str] = Field(default=["en"])
    naming_pattern: str = Field(default="{template_id}-{deliverable}.{format}")


class Template(BaseModel):
    """Complete template definition."""

    template_id: str = Field(description="Unique template identifier")
    name: str = Field(description="Human-readable name")
    version: str = Field(description="Template version")
    description: Optional[str] = None
    inputs: InputSchema
    processing: dict = Field(description="Contains 'tasks' list")
    outputs: OutputSchema

    @field_validator("processing")
    @classmethod
    def validate_processing(cls, v: dict) -> dict:
        """Ensure processing contains tasks."""
        if "tasks" not in v:
            raise ValueError("processing must contain 'tasks' list")
        if not isinstance(v["tasks"], list):
            raise ValueError("processing.tasks must be a list")
        return v

    def get_tasks(self) -> list[TaskDefinition]:
        """Get task definitions from processing config."""
        return [TaskDefinition(**t) for t in self.processing["tasks"]]

    def build_dependency_graph(self) -> dict[str, list[str]]:
        """Build task dependency graph for execution ordering."""
        tasks = self.get_tasks()
        return {t.name: t.dependencies for t in tasks}

    def validate_dependencies(self) -> list[str]:
        """Validate all dependencies exist and no cycles."""
        errors = []
        tasks = self.get_tasks()
        task_names = {t.name for t in tasks}

        for task in tasks:
            for dep in task.dependencies:
                if dep not in task_names:
                    errors.append(f"Task '{task.name}' depends on unknown task '{dep}'")

        # Check for cycles using DFS
        if self._has_circular_deps():
            errors.append("Circular dependencies detected in task graph")

        return errors

    def _has_circular_deps(self) -> bool:
        """Detect circular dependencies using DFS."""
        graph = self.build_dependency_graph()
        visited: set[str] = set()
        rec_stack: set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for dep in graph.get(node, []):
                if dep not in visited:
                    if dfs(dep):
                        return True
                elif dep in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if dfs(node):
                    return True
        return False
```

#### 3.2 Template Loader

**File: `src/rewindlearn/templates/loader.py`**

```python
"""YAML template loading and validation."""

from pathlib import Path
from typing import Optional

import yaml

from rewindlearn.core.exceptions import TemplateError
from rewindlearn.templates.models import Template


class TemplateLoader:
    """Load and validate YAML templates."""

    def __init__(self, templates_dir: Path):
        self.templates_dir = Path(templates_dir)
        self._cache: dict[str, Template] = {}

    def load(self, template_id: str) -> Template:
        """Load a template by ID or path."""
        # Return cached if available
        if template_id in self._cache:
            return self._cache[template_id]

        # Find template file
        path = self._find_template(template_id)
        if path is None:
            raise TemplateError(f"Template not found: {template_id}")

        # Load and parse
        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            template = Template(**data)
        except yaml.YAMLError as e:
            raise TemplateError(f"Invalid YAML in template {template_id}: {e}")
        except Exception as e:
            raise TemplateError(f"Error loading template {template_id}: {e}")

        # Validate dependencies
        errors = template.validate_dependencies()
        if errors:
            raise TemplateError(f"Template validation failed: {'; '.join(errors)}")

        # Cache and return
        self._cache[template_id] = template
        return template

    def _find_template(self, template_id: str) -> Optional[Path]:
        """Find template file by ID."""
        # Direct path
        if Path(template_id).exists():
            return Path(template_id)

        # In templates directory
        direct = self.templates_dir / f"{template_id}.yaml"
        if direct.exists():
            return direct

        # With version suffix
        matches = list(self.templates_dir.glob(f"{template_id}*.yaml"))
        if matches:
            # Return most recent version (alphabetically last)
            return sorted(matches)[-1]

        return None

    def validate(self, path: Path) -> tuple[bool, list[str]]:
        """Validate a template file without caching."""
        errors: list[str] = []

        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            template = Template(**data)
            errors.extend(template.validate_dependencies())
        except Exception as e:
            errors.append(str(e))

        return len(errors) == 0, errors

    def list_templates(self) -> list[str]:
        """List available template IDs."""
        templates = []
        if self.templates_dir.exists():
            for f in self.templates_dir.glob("*.yaml"):
                templates.append(f.stem)
        return sorted(templates)
```

#### 3.3 Built-in Template

**File: `templates/online-course-v1.yaml`**

```yaml
template_id: online-course
name: Online Course Session
version: "1.0"
description: |
  Process online course recordings into comprehensive study materials.
  Generates summary, timeline, friction points, coverage gaps, 
  learning resources, action items, and video clip markers.

inputs:
  required:
    - transcript
  optional:
    - chat_log
    - slides

processing:
  tasks:
    # Independent tasks (run in parallel)
    - name: session_summary
      prompt_template: |
        Analyze this course session transcript and create a comprehensive summary.
        
        **Course:** {course_name}
        **Session:** {session_number}
        
        **Transcript:**
        {transcript}
        
        **Chat Log (if available):**
        {chat_log}
        
        Create a structured summary with:
        1. **Session Overview** (2-3 sentences capturing the main focus)
        2. **Key Topics Covered** (bullet points with brief explanations)
        3. **Main Takeaways** (3-5 actionable insights)
        4. **Prerequisites Mentioned** (what students should know beforehand)
        5. **Next Steps/Homework** (assignments or preparation for next session)
        
        Use markdown formatting. Be concise but comprehensive.
      llm_config:
        model: claude-sonnet-4-20250514
        temperature: 0.3
        max_tokens: 2500
      dependencies: []
      output_format: markdown

    - name: concept_timeline
      prompt_template: |
        Create a chronological timeline of concepts taught in this session.
        
        **Transcript:**
        {transcript}
        
        For each major concept, provide:
        - **Timestamp** (from transcript, format: HH:MM:SS)
        - **Concept Name** (clear, searchable title)
        - **Description** (1-2 sentences explaining the concept)
        - **Difficulty** (Beginner / Intermediate / Advanced)
        
        Format as a markdown table:
        | Timestamp | Concept | Description | Difficulty |
        |-----------|---------|-------------|------------|
        
        Include ALL substantive teaching moments. Skip breaks and off-topic chat.
      llm_config:
        model: claude-sonnet-4-20250514
        temperature: 0.2
        max_tokens: 2500
      dependencies: []
      output_format: markdown

    - name: concept_chunks
      prompt_template: |
        Extract video clip boundaries for each teachable concept.
        
        **Transcript:**
        {transcript}
        
        Output ONLY CSV format with these columns:
        concept,description,start_time,end_time
        
        Rules:
        - Each clip should be 3-7 minutes long
        - Use exact timestamps from transcript (HH:MM:SS format)
        - Concept names should be search-friendly (use underscores, no spaces)
        - Description explains what the student will learn
        - Skip breaks, introductions, and off-topic discussions
        - Number concepts with 2-digit prefix: 01_, 02_, etc.
        
        Example:
        concept,description,start_time,end_time
        01_HTTP_Request_Basics,Learn how to construct HTTP requests with headers,00:05:30,00:10:45
        02_API_Authentication,Understand OAuth2 flow and token management,00:10:45,00:17:20
      llm_config:
        model: claude-sonnet-4-20250514
        temperature: 0.1
        max_tokens: 2000
      dependencies: []
      output_format: csv

    # Dependent tasks (run after dependencies complete)
    - name: friction_analysis
      prompt_template: |
        Based on the session content, identify potential student friction points.
        
        **Session Summary:**
        {session_summary}
        
        **Chat Log:**
        {chat_log}
        
        Analyze and provide:
        
        ## Potential Confusion Points
        - Concepts that may need more explanation
        - Technical terms that weren't clearly defined
        - Steps that were glossed over too quickly
        
        ## Questions from Chat
        - Extract actual questions from the chat log
        - Note which were answered vs. unanswered
        
        ## Pace Issues
        - Sections that moved too fast
        - Areas with unnecessary repetition
        
        ## Missing Prerequisites
        - Knowledge assumed but not covered
        - Links to prerequisite materials needed
        
        ## Recommendations for Instructor
        - Specific improvements for next session
        - Additional examples that would help
      llm_config:
        model: claude-sonnet-4-20250514
        temperature: 0.4
        max_tokens: 2000
      dependencies:
        - session_summary
      output_format: markdown

    - name: coverage_gaps
      prompt_template: |
        Analyze what topics were NOT covered that students might expect.
        
        **Session Summary:**
        {session_summary}
        
        **Concept Timeline:**
        {concept_timeline}
        
        Identify:
        
        ## Related Topics Not Covered
        - Topics closely related to what was taught
        - Why they might be important
        - Suggested resources to learn them
        
        ## Depth Gaps
        - Areas where the session went broad but not deep
        - Advanced aspects left unexplored
        
        ## Practical Applications Missing
        - Real-world use cases not demonstrated
        - Industry practices not mentioned
        
        ## Suggested Follow-up Topics
        - Natural next steps for learning
        - Topics for future sessions
      llm_config:
        model: claude-sonnet-4-20250514
        temperature: 0.4
        max_tokens: 1500
      dependencies:
        - session_summary
        - concept_timeline
      output_format: markdown

    - name: learning_resources
      prompt_template: |
        Curate learning resources for students based on the session content.
        
        **Concept Timeline:**
        {concept_timeline}
        
        **Coverage Gaps:**
        {coverage_gaps}
        
        For each major concept and gap, provide:
        
        ## Official Documentation
        - Links to official docs for tools/frameworks mentioned
        - Specific relevant sections
        
        ## Tutorials & Guides
        - Video tutorials (YouTube, courses)
        - Written tutorials (blogs, guides)
        - Interactive tutorials (playgrounds, sandboxes)
        
        ## Books & Papers
        - Relevant chapters from recommended books
        - Academic papers for deep understanding
        
        ## Practice Resources
        - Coding exercises
        - Project ideas
        - Challenges and competitions
        
        ## Community Resources
        - Forums and discussion groups
        - Discord/Slack communities
        - Stack Overflow tags
        
        Format with clear categories and working URLs where possible.
      llm_config:
        model: claude-sonnet-4-20250514
        temperature: 0.5
        max_tokens: 2000
      dependencies:
        - concept_timeline
        - coverage_gaps
      output_format: markdown

    - name: action_items
      prompt_template: |
        Extract actionable items for students from this session.
        
        **Session Summary:**
        {session_summary}
        
        **Friction Analysis:**
        {friction_analysis}
        
        Create a prioritized action list:
        
        ## Immediate (Before Next Session)
        - [ ] Tasks to complete right away
        - [ ] Homework assignments mentioned
        - [ ] Setup or installation needed
        
        ## Short-term (This Week)
        - [ ] Practice exercises
        - [ ] Reading materials
        - [ ] Projects to start
        
        ## Long-term (This Month)
        - [ ] Deeper learning goals
        - [ ] Portfolio projects
        - [ ] Skills to develop
        
        ## Questions to Research
        - Unanswered questions from the session
        - Topics to explore independently
        
        Include time estimates where helpful.
      llm_config:
        model: claude-sonnet-4-20250514
        temperature: 0.3
        max_tokens: 1500
      dependencies:
        - session_summary
        - friction_analysis
      output_format: markdown

outputs:
  deliverables:
    - session_summary
    - concept_timeline
    - concept_chunks
    - friction_analysis
    - coverage_gaps
    - learning_resources
    - action_items
  formats:
    - markdown
    - csv
  naming_pattern: "{course_name}-S{session_number:02d}-{deliverable}"
```

#### Phase 3 Tasks Checklist

```
[ ] Create src/rewindlearn/templates/__init__.py
[ ] Create src/rewindlearn/templates/models.py
[ ] Create src/rewindlearn/templates/loader.py
[ ] Create templates/online-course-v1.yaml
[ ] Test: Load template successfully
[ ] Test: Validate template with circular deps fails
[ ] Test: List templates returns correct list
```

---

### Phase 4: File Processors

**Goal:** Parse transcript and chat files into structured content.

#### 4.1 Base Processor

**File: `src/rewindlearn/processors/__init__.py`**

```python
"""File processors for session artifacts."""

from pathlib import Path
from typing import Optional

from rewindlearn.processors.base import BaseProcessor, ProcessedContent
from rewindlearn.processors.transcript import TranscriptProcessor
from rewindlearn.processors.chat import ChatProcessor

# Processor registry
PROCESSORS: dict[str, BaseProcessor] = {
    "transcript": TranscriptProcessor(),
    "chat_log": ChatProcessor(),
}


def process_input(input_type: str, path: Path) -> ProcessedContent:
    """Process an input file using the appropriate processor."""
    processor = PROCESSORS.get(input_type)
    if not processor:
        raise ValueError(f"Unknown input type: {input_type}")
    return processor.process(path)


def get_processor_for_file(path: Path) -> Optional[BaseProcessor]:
    """Get the appropriate processor for a file based on extension."""
    for processor in PROCESSORS.values():
        if processor.can_handle(path):
            return processor
    return None


__all__ = [
    "BaseProcessor",
    "ProcessedContent",
    "TranscriptProcessor",
    "ChatProcessor",
    "process_input",
    "get_processor_for_file",
]
```

**File: `src/rewindlearn/processors/base.py`**

```python
"""Base processor class for file processing."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ProcessedContent(BaseModel):
    """Result of processing a file."""

    raw_text: str = Field(description="Full text content")
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamps: list[dict[str, str]] = Field(
        default_factory=list,
        description="List of {text, start, end} timestamp entries"
    )


class BaseProcessor(ABC):
    """Abstract base class for file processors."""

    supported_extensions: list[str] = []

    @abstractmethod
    def process(self, path: Path) -> ProcessedContent:
        """Process a file and return structured content."""
        pass

    @classmethod
    def can_handle(cls, path: Path) -> bool:
        """Check if this processor can handle the given file."""
        return path.suffix.lower() in cls.supported_extensions
```

#### 4.2 Transcript Processor

**File: `src/rewindlearn/processors/transcript.py`**

```python
"""Transcript file processor for .txt, .vtt, .srt files."""

import re
from pathlib import Path

import webvtt

from rewindlearn.processors.base import BaseProcessor, ProcessedContent


class TranscriptProcessor(BaseProcessor):
    """Process transcript files with optional timestamp extraction."""

    supported_extensions = [".txt", ".vtt", ".srt"]

    def process(self, path: Path) -> ProcessedContent:
        """Process a transcript file."""
        ext = path.suffix.lower()

        if ext == ".txt":
            return self._process_txt(path)
        elif ext in [".vtt", ".srt"]:
            return self._process_vtt(path)
        else:
            raise ValueError(f"Unsupported transcript format: {ext}")

    def _process_txt(self, path: Path) -> ProcessedContent:
        """Process plain text transcript."""
        text = path.read_text(encoding="utf-8")
        timestamps = self._extract_inline_timestamps(text)

        return ProcessedContent(
            raw_text=text,
            timestamps=timestamps,
            metadata={
                "format": "txt",
                "has_timestamps": len(timestamps) > 0,
                "char_count": len(text),
            }
        )

    def _process_vtt(self, path: Path) -> ProcessedContent:
        """Process VTT/SRT subtitle file."""
        try:
            captions = webvtt.read(str(path))
        except Exception as e:
            raise ValueError(f"Error parsing VTT/SRT file: {e}")

        timestamps = []
        full_text_parts = []

        for caption in captions:
            timestamps.append({
                "text": caption.text,
                "start": caption.start,
                "end": caption.end
            })
            full_text_parts.append(f"[{caption.start}] {caption.text}")

        return ProcessedContent(
            raw_text="\n".join(full_text_parts),
            timestamps=timestamps,
            metadata={
                "format": path.suffix.lower(),
                "caption_count": len(captions),
                "has_timestamps": True,
            }
        )

    def _extract_inline_timestamps(self, text: str) -> list[dict[str, str]]:
        """Extract timestamps from inline format like [00:01:23] or (00:01:23)."""
        timestamps = []

        # Pattern: [HH:MM:SS] or (HH:MM:SS) followed by text
        pattern = r'[\[\(](\d{1,2}:\d{2}:\d{2})[\]\)]\s*(.+?)(?=[\[\(]\d{1,2}:\d{2}:\d{2}[\]\)]|$)'
        matches = re.findall(pattern, text, re.DOTALL)

        for i, (timestamp, content) in enumerate(matches):
            # Calculate end time (use next timestamp or add 30s)
            if i + 1 < len(matches):
                end_time = matches[i + 1][0]
            else:
                end_time = self._add_seconds(timestamp, 30)

            timestamps.append({
                "text": content.strip(),
                "start": timestamp,
                "end": end_time
            })

        return timestamps

    def _add_seconds(self, timestamp: str, seconds: int) -> str:
        """Add seconds to a timestamp string."""
        parts = timestamp.split(":")
        h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
        total_seconds = h * 3600 + m * 60 + s + seconds
        return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"
```

#### 4.3 Chat Processor

**File: `src/rewindlearn/processors/chat.py`**

```python
"""Chat log processor for Zoom, Teams, and generic formats."""

import json
import re
from pathlib import Path
from typing import Any

from rewindlearn.processors.base import BaseProcessor, ProcessedContent


class ChatProcessor(BaseProcessor):
    """Process chat log files."""

    supported_extensions = [".txt", ".json"]

    def process(self, path: Path) -> ProcessedContent:
        """Process a chat log file."""
        ext = path.suffix.lower()

        if ext == ".json":
            return self._process_json(path)
        elif ext == ".txt":
            return self._process_txt(path)
        else:
            raise ValueError(f"Unsupported chat format: {ext}")

    def _process_txt(self, path: Path) -> ProcessedContent:
        """Process plain text chat (Zoom format)."""
        text = path.read_text(encoding="utf-8")
        messages = self._parse_zoom_chat(text)

        return ProcessedContent(
            raw_text=text,
            timestamps=[
                {"text": m["text"], "start": m["timestamp"], "end": m["timestamp"]}
                for m in messages if "timestamp" in m
            ],
            metadata={
                "format": "zoom_txt",
                "message_count": len(messages),
                "participants": list({m.get("sender", "Unknown") for m in messages}),
            }
        )

    def _process_json(self, path: Path) -> ProcessedContent:
        """Process JSON chat export."""
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        # Handle different JSON structures
        if isinstance(data, list):
            messages = data
        elif isinstance(data, dict) and "messages" in data:
            messages = data["messages"]
        else:
            messages = [data]

        # Build text representation
        text_parts = []
        timestamps = []

        for msg in messages:
            sender = msg.get("sender", msg.get("from", msg.get("author", "Unknown")))
            content = msg.get("text", msg.get("content", msg.get("message", "")))
            timestamp = msg.get("timestamp", msg.get("time", ""))

            text_parts.append(f"[{timestamp}] {sender}: {content}")
            if timestamp:
                timestamps.append({
                    "text": f"{sender}: {content}",
                    "start": str(timestamp),
                    "end": str(timestamp)
                })

        return ProcessedContent(
            raw_text="\n".join(text_parts),
            timestamps=timestamps,
            metadata={
                "format": "json",
                "message_count": len(messages),
            }
        )

    def _parse_zoom_chat(self, text: str) -> list[dict[str, Any]]:
        """Parse Zoom chat format: HH:MM:SS From Name to Everyone: message"""
        messages = []

        # Zoom format pattern
        pattern = r'(\d{2}:\d{2}:\d{2})\s+From\s+(.+?)\s+to\s+(.+?):\s*(.+?)(?=\d{2}:\d{2}:\d{2}\s+From|$)'
        matches = re.findall(pattern, text, re.DOTALL)

        for timestamp, sender, recipient, content in matches:
            messages.append({
                "timestamp": timestamp,
                "sender": sender.strip(),
                "recipient": recipient.strip(),
                "text": content.strip()
            })

        # If no Zoom format found, try generic line-by-line
        if not messages:
            for line in text.strip().split("\n"):
                if line.strip():
                    messages.append({"text": line.strip()})

        return messages
```

#### Phase 4 Tasks Checklist

```
[ ] Create src/rewindlearn/processors/__init__.py
[ ] Create src/rewindlearn/processors/base.py
[ ] Create src/rewindlearn/processors/transcript.py
[ ] Create src/rewindlearn/processors/chat.py
[ ] Create tests/fixtures/transcripts/simple.txt
[ ] Create tests/fixtures/transcripts/with-timestamps.vtt
[ ] Create tests/fixtures/chats/zoom-chat.txt
[ ] Test: Process .txt transcript
[ ] Test: Process .vtt transcript with timestamps
[ ] Test: Process Zoom chat format
[ ] Test: Process JSON chat format
```

---

### Phase 5: LLM Integration

**Goal:** Abstract LLM providers with fallback support.

#### 5.1 LLM Providers

**File: `src/rewindlearn/llm/__init__.py`**

```python
"""LLM provider abstraction."""

from rewindlearn.llm.providers import LLMProvider
from rewindlearn.llm.router import LLMRouter

__all__ = ["LLMProvider", "LLMRouter"]
```

**File: `src/rewindlearn/llm/providers.py`**

```python
"""LLM provider clients."""

from typing import Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from rewindlearn.core.config import Settings
from rewindlearn.core.exceptions import LLMError


class LLMProvider:
    """Factory for LLM clients."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._clients: dict[str, BaseChatModel] = {}

    def get_client(self, model: str) -> BaseChatModel:
        """Get or create an LLM client for the specified model."""
        if model in self._clients:
            return self._clients[model]

        client = self._create_client(model)
        self._clients[model] = client
        return client

    def _create_client(self, model: str) -> BaseChatModel:
        """Create a new LLM client."""
        if model.startswith("claude"):
            api_key = self.settings.anthropic_api_key
            if not api_key:
                raise LLMError("Anthropic API key not configured")
            return ChatAnthropic(
                model=model,
                api_key=api_key,
                max_retries=self.settings.max_retries,
            )
        elif model.startswith("gpt"):
            api_key = self.settings.openai_api_key
            if not api_key:
                raise LLMError("OpenAI API key not configured")
            return ChatOpenAI(
                model=model,
                api_key=api_key,
                max_retries=self.settings.max_retries,
            )
        else:
            raise LLMError(f"Unknown model: {model}")
```

#### 5.2 LLM Router

**File: `src/rewindlearn/llm/router.py`**

```python
"""LLM routing with fallback support."""

from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable

from rewindlearn.core.exceptions import LLMError
from rewindlearn.core.logging import get_logger
from rewindlearn.llm.providers import LLMProvider
from rewindlearn.templates.models import LLMConfig

logger = get_logger(__name__)


class LLMRouter:
    """Route LLM requests with fallback support."""

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    @traceable(name="llm_invoke")
    async def invoke(
        self,
        prompt: str,
        config: LLMConfig,
        task_name: str = "unknown",
        system_prompt: Optional[str] = None,
    ) -> str:
        """Invoke LLM with the given prompt and config."""
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        try:
            client = self.provider.get_client(config.model)
            response = await client.ainvoke(
                messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
            return str(response.content)

        except Exception as e:
            logger.warning(f"Primary model failed for {task_name}: {e}")

            # Try fallback if configured
            if config.fallback_model:
                try:
                    logger.info(f"Trying fallback model: {config.fallback_model}")
                    fallback_client = self.provider.get_client(config.fallback_model)
                    response = await fallback_client.ainvoke(
                        messages,
                        temperature=config.temperature,
                        max_tokens=config.max_tokens,
                    )
                    return str(response.content)
                except Exception as fallback_error:
                    raise LLMError(
                        f"Both primary ({config.model}) and fallback ({config.fallback_model}) "
                        f"failed for {task_name}: {fallback_error}"
                    )

            raise LLMError(f"LLM invocation failed for {task_name}: {e}")
```

#### Phase 5 Tasks Checklist

```
[ ] Create src/rewindlearn/llm/__init__.py
[ ] Create src/rewindlearn/llm/providers.py
[ ] Create src/rewindlearn/llm/router.py
[ ] Test: Create Anthropic client
[ ] Test: Create OpenAI client
[ ] Test: Fallback works when primary fails
```

---

### Phase 6: LangChain Chains

**Goal:** Implement processing chains for each deliverable.

#### 6.1 Base Chain

**File: `src/rewindlearn/chains/__init__.py`**

```python
"""Processing chains for session analysis."""

from rewindlearn.chains.base import BaseChain
from rewindlearn.chains.summary import SummaryChain
from rewindlearn.chains.timeline import TimelineChain
from rewindlearn.chains.friction import FrictionChain
from rewindlearn.chains.coverage import CoverageChain
from rewindlearn.chains.resources import ResourcesChain
from rewindlearn.chains.actions import ActionsChain
from rewindlearn.chains.chunks import ChunksChain

from rewindlearn.llm.router import LLMRouter
from rewindlearn.templates.models import TaskDefinition


# Chain registry
CHAIN_CLASSES: dict[str, type[BaseChain]] = {
    "session_summary": SummaryChain,
    "concept_timeline": TimelineChain,
    "friction_analysis": FrictionChain,
    "coverage_gaps": CoverageChain,
    "learning_resources": ResourcesChain,
    "action_items": ActionsChain,
    "concept_chunks": ChunksChain,
}


def create_chain(task: TaskDefinition, router: LLMRouter) -> BaseChain:
    """Create a chain instance for the given task."""
    chain_class = CHAIN_CLASSES.get(task.name, BaseChain)
    return chain_class(task, router)


__all__ = [
    "BaseChain",
    "create_chain",
    "SummaryChain",
    "TimelineChain",
    "FrictionChain",
    "CoverageChain",
    "ResourcesChain",
    "ActionsChain",
    "ChunksChain",
]
```

**File: `src/rewindlearn/chains/base.py`**

```python
"""Base chain class for LLM processing tasks."""

from typing import Any

from langchain.prompts import PromptTemplate
from langsmith import traceable

from rewindlearn.llm.router import LLMRouter
from rewindlearn.templates.models import TaskDefinition


class BaseChain:
    """Base class for processing chains."""

    def __init__(self, task: TaskDefinition, router: LLMRouter):
        self.task = task
        self.router = router
        self.prompt = PromptTemplate.from_template(task.prompt_template)

    @traceable
    async def run(self, inputs: dict[str, Any]) -> str:
        """Execute the chain with given inputs."""
        # Fill in missing optional inputs with empty strings
        template_vars = self.prompt.input_variables
        safe_inputs = {k: inputs.get(k, "") for k in template_vars}

        formatted_prompt = self.prompt.format(**safe_inputs)

        result = await self.router.invoke(
            formatted_prompt,
            self.task.llm_config,
            task_name=self.task.name
        )

        return self.post_process(result)

    def post_process(self, result: str) -> str:
        """Override for custom post-processing."""
        return result.strip()
```

#### 6.2 Specific Chains

**File: `src/rewindlearn/chains/summary.py`**

```python
"""Session summary chain."""

from rewindlearn.chains.base import BaseChain


class SummaryChain(BaseChain):
    """Generate session summary."""

    def post_process(self, result: str) -> str:
        """Ensure proper markdown formatting."""
        result = super().post_process(result)
        # Ensure it starts with a heading if not present
        if not result.startswith("#"):
            result = "# Session Summary\n\n" + result
        return result
```

**File: `src/rewindlearn/chains/timeline.py`**

```python
"""Concept timeline chain."""

from rewindlearn.chains.base import BaseChain


class TimelineChain(BaseChain):
    """Generate concept timeline."""

    def post_process(self, result: str) -> str:
        """Ensure proper table formatting."""
        result = super().post_process(result)
        if not result.startswith("#"):
            result = "# Concept Timeline\n\n" + result
        return result
```

**File: `src/rewindlearn/chains/friction.py`**

```python
"""Friction analysis chain."""

from rewindlearn.chains.base import BaseChain


class FrictionChain(BaseChain):
    """Analyze student friction points."""

    def post_process(self, result: str) -> str:
        result = super().post_process(result)
        if not result.startswith("#"):
            result = "# Friction Analysis\n\n" + result
        return result
```

**File: `src/rewindlearn/chains/coverage.py`**

```python
"""Coverage gaps chain."""

from rewindlearn.chains.base import BaseChain


class CoverageChain(BaseChain):
    """Analyze coverage gaps."""

    def post_process(self, result: str) -> str:
        result = super().post_process(result)
        if not result.startswith("#"):
            result = "# Coverage Gaps\n\n" + result
        return result
```

**File: `src/rewindlearn/chains/resources.py`**

```python
"""Learning resources chain."""

from rewindlearn.chains.base import BaseChain


class ResourcesChain(BaseChain):
    """Curate learning resources."""

    def post_process(self, result: str) -> str:
        result = super().post_process(result)
        if not result.startswith("#"):
            result = "# Learning Resources\n\n" + result
        return result
```

**File: `src/rewindlearn/chains/actions.py`**

```python
"""Action items chain."""

from rewindlearn.chains.base import BaseChain


class ActionsChain(BaseChain):
    """Extract action items."""

    def post_process(self, result: str) -> str:
        result = super().post_process(result)
        if not result.startswith("#"):
            result = "# Action Items\n\n" + result
        return result
```

**File: `src/rewindlearn/chains/chunks.py`**

```python
"""Concept chunks chain for CSV output."""

import csv
import io

from rewindlearn.chains.base import BaseChain


class ChunksChain(BaseChain):
    """Extract concept chunks for video splitting."""

    def post_process(self, result: str) -> str:
        """Validate and clean CSV output."""
        result = super().post_process(result)

        # Remove markdown code fences if present
        if result.startswith("```"):
            lines = result.split("\n")
            result = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

        # Parse and re-format as clean CSV
        lines = result.strip().split("\n")
        output = io.StringIO()
        writer = csv.writer(output)

        # Ensure header row
        header_written = False
        expected_header = ["concept", "description", "start_time", "end_time"]

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            try:
                reader = csv.reader([line])
                row = next(reader)

                # Check if this is a header row
                if not header_written:
                    if row[0].lower() == "concept":
                        writer.writerow(expected_header)
                        header_written = True
                        continue
                    else:
                        writer.writerow(expected_header)
                        header_written = True

                # Write data row if it has enough columns
                if len(row) >= 4:
                    writer.writerow(row[:4])
            except Exception:
                continue

        return output.getvalue()
```

#### Phase 6 Tasks Checklist

```
[ ] Create src/rewindlearn/chains/__init__.py
[ ] Create src/rewindlearn/chains/base.py
[ ] Create src/rewindlearn/chains/summary.py
[ ] Create src/rewindlearn/chains/timeline.py
[ ] Create src/rewindlearn/chains/friction.py
[ ] Create src/rewindlearn/chains/coverage.py
[ ] Create src/rewindlearn/chains/resources.py
[ ] Create src/rewindlearn/chains/actions.py
[ ] Create src/rewindlearn/chains/chunks.py
[ ] Test: Chain factory creates correct chain types
[ ] Test: CSV post-processing cleans output correctly
```

---

### Phase 7: LangGraph Workflow

**Goal:** Orchestrate chains with parallel execution and dependency management.

#### 7.1 State Definition

**File: `src/rewindlearn/workflow/__init__.py`**

```python
"""Workflow orchestration with LangGraph."""

from rewindlearn.workflow.executor import WorkflowExecutor, process_session
from rewindlearn.workflow.state import SessionState

__all__ = ["WorkflowExecutor", "process_session", "SessionState"]
```

**File: `src/rewindlearn/workflow/state.py`**

```python
"""LangGraph state definitions."""

from typing import Annotated, Any, Optional
from operator import add

from typing_extensions import TypedDict


class SessionState(TypedDict):
    """State for session processing workflow."""

    # Inputs
    transcript: str
    chat_log: str
    slides: Optional[str]
    course_name: str
    session_number: int

    # Task outputs (populated as chains complete)
    session_summary: Optional[str]
    concept_timeline: Optional[str]
    friction_analysis: Optional[str]
    coverage_gaps: Optional[str]
    learning_resources: Optional[str]
    action_items: Optional[str]
    concept_chunks: Optional[str]

    # Metadata
    completed_tasks: Annotated[list[str], add]
    errors: Annotated[list[str], add]
```

#### 7.2 Graph Builder

**File: `src/rewindlearn/workflow/graph.py`**

```python
"""LangGraph workflow construction."""

from typing import Any, Callable

from langgraph.graph import END, StateGraph

from rewindlearn.chains import create_chain
from rewindlearn.llm.router import LLMRouter
from rewindlearn.templates.models import Template
from rewindlearn.workflow.state import SessionState


class WorkflowBuilder:
    """Build LangGraph workflows from templates."""

    def __init__(self, template: Template, router: LLMRouter):
        self.template = template
        self.router = router

    def build(self) -> StateGraph:
        """Build and compile the workflow graph."""
        graph = StateGraph(SessionState)
        tasks = self.template.get_tasks()
        dep_graph = self.template.build_dependency_graph()

        # Add nodes for each task
        for task in tasks:
            chain = create_chain(task, self.router)
            graph.add_node(task.name, self._make_node(chain, task.name))

        # Add edges based on dependencies
        for task in tasks:
            if not dep_graph[task.name]:
                # No dependencies - start from __start__
                graph.add_edge("__start__", task.name)
            else:
                # Add edge from each dependency
                for dep in dep_graph[task.name]:
                    graph.add_edge(dep, task.name)

        # All leaf nodes go to END
        leaf_tasks = self._find_leaf_tasks(tasks, dep_graph)
        for leaf in leaf_tasks:
            graph.add_edge(leaf, END)

        return graph.compile()

    def _make_node(self, chain: Any, task_name: str) -> Callable:
        """Create a node function for the graph."""

        async def node(state: SessionState) -> dict[str, Any]:
            try:
                result = await chain.run(dict(state))
                return {
                    task_name: result,
                    "completed_tasks": [task_name]
                }
            except Exception as e:
                return {
                    "errors": [f"{task_name}: {str(e)}"]
                }

        return node

    def _find_leaf_tasks(
        self,
        tasks: list,
        dep_graph: dict[str, list[str]]
    ) -> list[str]:
        """Find tasks that no other task depends on."""
        all_deps: set[str] = set()
        for deps in dep_graph.values():
            all_deps.update(deps)

        return [t.name for t in tasks if t.name not in all_deps]
```

#### 7.3 Workflow Executor

**File: `src/rewindlearn/workflow/executor.py`**

```python
"""Workflow execution engine."""

from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from rewindlearn.core.config import Settings, get_settings
from rewindlearn.core.logging import console
from rewindlearn.llm.providers import LLMProvider
from rewindlearn.llm.router import LLMRouter
from rewindlearn.processors import process_input
from rewindlearn.templates.loader import TemplateLoader
from rewindlearn.workflow.graph import WorkflowBuilder
from rewindlearn.workflow.state import SessionState


class WorkflowExecutor:
    """Execute processing workflows."""

    def __init__(
        self,
        template_id: str,
        settings: Optional[Settings] = None,
        console: Optional[Console] = None
    ):
        self.settings = settings or get_settings()
        self.console = console or Console()

        # Load template
        loader = TemplateLoader(self.settings.templates_dir)
        self.template = loader.load(template_id)

        # Set up LLM
        provider = LLMProvider(self.settings)
        self.router = LLMRouter(provider)

    async def execute(
        self,
        transcript_path: Path,
        chat_path: Optional[Path] = None,
        slides_path: Optional[Path] = None,
        course_name: str = "Unknown Course",
        session_number: int = 1,
    ) -> SessionState:
        """Execute the workflow with the given inputs."""

        # Process input files
        transcript = process_input("transcript", transcript_path)
        chat_log = ""
        if chat_path and chat_path.exists():
            chat_log = process_input("chat_log", chat_path).raw_text

        # Build initial state
        initial_state: SessionState = {
            "transcript": transcript.raw_text,
            "chat_log": chat_log,
            "slides": None,
            "course_name": course_name,
            "session_number": session_number,
            "session_summary": None,
            "concept_timeline": None,
            "friction_analysis": None,
            "coverage_gaps": None,
            "learning_resources": None,
            "action_items": None,
            "concept_chunks": None,
            "completed_tasks": [],
            "errors": [],
        }

        # Build and run workflow
        builder = WorkflowBuilder(self.template, self.router)
        graph = builder.build()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Processing session...", total=None)

            final_state = await graph.ainvoke(initial_state)

            progress.update(task, description="Complete!")

        return final_state


async def process_session(
    template: str,
    transcript_path: str | Path,
    chat_path: Optional[str | Path] = None,
    slides_path: Optional[str | Path] = None,
    course_name: str = "Unknown Course",
    session_number: int = 1,
    settings: Optional[Settings] = None,
) -> SessionState:
    """
    High-level API to process a session.

    This is the main public API for programmatic usage.

    Example:
        >>> results = await process_session(
        ...     template="online-course",
        ...     transcript_path="lecture.vtt",
        ...     course_name="AI Engineering",
        ...     session_number=5
        ... )
        >>> print(results["session_summary"])
    """
    executor = WorkflowExecutor(template, settings=settings)
    return await executor.execute(
        transcript_path=Path(transcript_path),
        chat_path=Path(chat_path) if chat_path else None,
        slides_path=Path(slides_path) if slides_path else None,
        course_name=course_name,
        session_number=session_number,
    )
```

#### Phase 7 Tasks Checklist

```
[ ] Create src/rewindlearn/workflow/__init__.py
[ ] Create src/rewindlearn/workflow/state.py
[ ] Create src/rewindlearn/workflow/graph.py
[ ] Create src/rewindlearn/workflow/executor.py
[ ] Test: Workflow builds correct dependency graph
[ ] Test: Parallel tasks execute concurrently
[ ] Test: Dependent tasks wait for dependencies
[ ] Test: Errors are captured in state
```

---

### Phase 8: Output Generation

**Goal:** Generate markdown and CSV output files.

#### 8.1 Output Builder

**File: `src/rewindlearn/output/__init__.py`**

```python
"""Output generation."""

from rewindlearn.output.builder import OutputBuilder

__all__ = ["OutputBuilder"]
```

**File: `src/rewindlearn/output/builder.py`**

```python
"""Output file generation."""

from datetime import datetime
from pathlib import Path
from typing import Any

from rewindlearn.templates.models import Template
from rewindlearn.workflow.state import SessionState


class OutputBuilder:
    """Generate output files from workflow results."""

    def __init__(self, template: Template, output_dir: Path):
        self.template = template
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        state: SessionState,
        course_name: str,
        session_number: int
    ) -> list[Path]:
        """Generate all output files from workflow state."""
        outputs: list[Path] = []

        for deliverable in self.template.outputs.deliverables:
            content = state.get(deliverable)
            if not content:
                continue

            # Determine format
            if deliverable == "concept_chunks":
                ext = "csv"
            else:
                ext = "md"

            # Generate filename
            filename = self._make_filename(
                deliverable, ext, course_name, session_number
            )
            path = self.output_dir / filename

            # Write file
            if ext == "csv":
                path.write_text(content, encoding="utf-8")
            else:
                # Add frontmatter to markdown
                full_content = self._add_frontmatter(
                    content, deliverable, course_name, session_number
                )
                path.write_text(full_content, encoding="utf-8")

            outputs.append(path)

        return outputs

    def _make_filename(
        self,
        deliverable: str,
        ext: str,
        course_name: str,
        session_number: int
    ) -> str:
        """Generate output filename."""
        # Clean course name for filename
        safe_name = course_name.replace(" ", "-").lower()
        safe_name = "".join(c for c in safe_name if c.isalnum() or c == "-")

        return f"{safe_name}-S{session_number:02d}-{deliverable}.{ext}"

    def _add_frontmatter(
        self,
        content: str,
        deliverable: str,
        course_name: str,
        session_number: int
    ) -> str:
        """Add YAML frontmatter to markdown content."""
        frontmatter = f"""---
course: "{course_name}"
session: {session_number}
deliverable: {deliverable}
template: {self.template.template_id}
generated: {datetime.now().isoformat()}
---

"""
        return frontmatter + content
```

#### Phase 8 Tasks Checklist

```
[ ] Create src/rewindlearn/output/__init__.py
[ ] Create src/rewindlearn/output/builder.py
[ ] Test: Markdown files have correct frontmatter
[ ] Test: CSV files are valid
[ ] Test: Filenames follow pattern
```

---

### Phase 9: CLI Implementation

**Goal:** Typer CLI with rich output.

#### 9.1 Main CLI App

**File: `src/rewindlearn/cli/__init__.py`**

```python
"""CLI package."""
```

**File: `src/rewindlearn/cli/main.py`**

```python
"""Main CLI application."""

import typer
from rich.console import Console

from rewindlearn import __version__
from rewindlearn.cli.commands import config, process, template

app = typer.Typer(
    name="rewindlearn",
    help="Transform session artifacts into structured knowledge.",
    no_args_is_help=True,
)

console = Console()

# Register command groups
app.add_typer(process.app, name="process")
app.add_typer(template.app, name="template")
app.add_typer(config.app, name="config")


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show version")
):
    """Rewind.Learn - Session Processing Framework"""
    if version:
        console.print(f"rewindlearn {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
```

#### 9.2 Process Command

**File: `src/rewindlearn/cli/commands/__init__.py`**

```python
"""CLI commands."""
```

**File: `src/rewindlearn/cli/commands/process.py`**

```python
"""Process command for session processing."""

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rewindlearn.core.config import get_settings
from rewindlearn.core.logging import setup_logging
from rewindlearn.output.builder import OutputBuilder
from rewindlearn.templates.loader import TemplateLoader
from rewindlearn.workflow.executor import WorkflowExecutor

app = typer.Typer(help="Process session files")
console = Console()


@app.command("run")
def run(
    template: str = typer.Option(
        ..., "--template", "-t",
        help="Template ID or path to template YAML"
    ),
    transcript: Path = typer.Option(
        ..., "--transcript",
        help="Path to transcript file (.txt, .vtt, .srt)",
        exists=True
    ),
    chat: Path = typer.Option(
        None, "--chat",
        help="Path to chat log file",
        exists=True
    ),
    output: Path = typer.Option(
        Path("output"), "--output", "-o",
        help="Output directory"
    ),
    course: str = typer.Option(
        "Unknown Course", "--course", "-c",
        help="Course name"
    ),
    session: int = typer.Option(
        1, "--session", "-s",
        help="Session number"
    ),
    verbose: bool = typer.Option(
        False, "--verbose",
        help="Enable verbose output"
    ),
):
    """Process a session with the specified template."""
    setup_logging(verbose=verbose)
    settings = get_settings()

    # Validate API keys
    try:
        settings.validate_api_keys()
    except ValueError as e:
        console.print(f"[red]Configuration error:[/red] {e}")
        raise typer.Exit(1)

    console.print(Panel.fit(
        f"[bold blue]Rewind.Learn[/bold blue]\n"
        f"Template: {template}\n"
        f"Transcript: {transcript.name}\n"
        f"Output: {output}"
    ))

    # Load template for output building
    loader = TemplateLoader(settings.templates_dir)
    try:
        tmpl = loader.load(template)
    except Exception as e:
        console.print(f"[red]Template error:[/red] {e}")
        raise typer.Exit(1)

    # Execute workflow
    try:
        executor = WorkflowExecutor(template, settings=settings, console=console)
        state = asyncio.run(executor.execute(
            transcript_path=transcript,
            chat_path=chat,
            course_name=course,
            session_number=session,
        ))
    except Exception as e:
        console.print(f"[red]Processing error:[/red] {e}")
        raise typer.Exit(1)

    # Generate outputs
    builder = OutputBuilder(tmpl, output)
    files = builder.generate(state, course, session)

    # Summary
    table = Table(title="Generated Files")
    table.add_column("File", style="green")
    table.add_column("Size")

    for f in files:
        table.add_row(f.name, f"{f.stat().st_size:,} bytes")

    console.print(table)

    # Show errors if any
    if state.get("errors"):
        console.print("\n[yellow]Warnings:[/yellow]")
        for err in state["errors"]:
            console.print(f"  ⚠ {err}")

    # Show completed tasks
    completed = state.get("completed_tasks", [])
    console.print(f"\n[green]✓[/green] Completed {len(completed)} tasks")
```

#### 9.3 Template Command

**File: `src/rewindlearn/cli/commands/template.py`**

```python
"""Template management commands."""

from pathlib import Path

import typer
from rich.console import Console

from rewindlearn.core.config import get_settings
from rewindlearn.templates.loader import TemplateLoader

app = typer.Typer(help="Template management")
console = Console()


@app.command("list")
def list_templates():
    """List available templates."""
    settings = get_settings()
    loader = TemplateLoader(settings.templates_dir)
    templates = loader.list_templates()

    if not templates:
        console.print("[yellow]No templates found[/yellow]")
        console.print(f"Templates directory: {settings.templates_dir}")
        return

    console.print("[bold]Available Templates:[/bold]")
    for t in templates:
        console.print(f"  • {t}")


@app.command("validate")
def validate(
    path: Path = typer.Argument(..., help="Template YAML file to validate", exists=True)
):
    """Validate a template file."""
    settings = get_settings()
    loader = TemplateLoader(settings.templates_dir)

    valid, errors = loader.validate(path)

    if valid:
        console.print(f"[green]✓ Template is valid:[/green] {path}")
    else:
        console.print(f"[red]✗ Template has errors:[/red]")
        for err in errors:
            console.print(f"  • {err}")
        raise typer.Exit(1)


@app.command("show")
def show(
    template_id: str = typer.Argument(..., help="Template ID to show")
):
    """Show template details."""
    settings = get_settings()
    loader = TemplateLoader(settings.templates_dir)

    try:
        tmpl = loader.load(template_id)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    console.print(f"[bold]{tmpl.name}[/bold] (v{tmpl.version})")
    console.print(f"ID: {tmpl.template_id}")
    if tmpl.description:
        console.print(f"\n{tmpl.description}")

    console.print("\n[bold]Inputs:[/bold]")
    console.print(f"  Required: {', '.join(tmpl.inputs.required)}")
    console.print(f"  Optional: {', '.join(tmpl.inputs.optional) or 'none'}")

    console.print("\n[bold]Tasks:[/bold]")
    for task in tmpl.get_tasks():
        deps = f" (depends on: {', '.join(task.dependencies)})" if task.dependencies else ""
        console.print(f"  • {task.name}{deps}")

    console.print("\n[bold]Outputs:[/bold]")
    console.print(f"  Deliverables: {', '.join(tmpl.outputs.deliverables)}")
    console.print(f"  Formats: {', '.join(tmpl.outputs.formats)}")
```

#### 9.4 Config Command

**File: `src/rewindlearn/cli/commands/config.py`**

```python
"""Configuration commands."""

import typer
from rich.console import Console

from rewindlearn.core.config import get_settings

app = typer.Typer(help="Configuration management")
console = Console()


@app.command("show")
def show():
    """Show current configuration."""
    settings = get_settings()

    console.print("[bold]Current Configuration:[/bold]")
    console.print(f"  Default Provider: {settings.default_provider}")
    console.print(f"  Default Model: {settings.default_model}")
    console.print(f"  Templates Dir: {settings.templates_dir}")
    console.print(f"  Output Dir: {settings.output_dir}")
    console.print(f"  LangSmith Tracing: {settings.langsmith_tracing}")

    console.print("\n[bold]API Keys:[/bold]")
    console.print(
        f"  Anthropic: {'✓ Set' if settings.anthropic_api_key else '✗ Not set'}"
    )
    console.print(
        f"  OpenAI: {'✓ Set' if settings.openai_api_key else '✗ Not set'}"
    )
    console.print(
        f"  LangSmith: {'✓ Set' if settings.langsmith_api_key else '✗ Not set'}"
    )


@app.command("check")
def check():
    """Check configuration validity."""
    settings = get_settings()

    issues = []

    if not settings.anthropic_api_key and not settings.openai_api_key:
        issues.append("No LLM API key configured")

    if not settings.templates_dir.exists():
        issues.append(f"Templates directory not found: {settings.templates_dir}")

    if issues:
        console.print("[red]Configuration issues found:[/red]")
        for issue in issues:
            console.print(f"  ✗ {issue}")
        raise typer.Exit(1)
    else:
        console.print("[green]✓ Configuration is valid[/green]")
```

#### Phase 9 Tasks Checklist

```
[ ] Create src/rewindlearn/cli/__init__.py
[ ] Create src/rewindlearn/cli/main.py
[ ] Create src/rewindlearn/cli/commands/__init__.py
[ ] Create src/rewindlearn/cli/commands/process.py
[ ] Create src/rewindlearn/cli/commands/template.py
[ ] Create src/rewindlearn/cli/commands/config.py
[ ] Test: rewindlearn --help works
[ ] Test: rewindlearn --version shows version
[ ] Test: rewindlearn process run --help shows options
[ ] Test: rewindlearn template list shows templates
[ ] Test: rewindlearn config show displays config
```

---

### Phase 10: GitHub Actions & PyPI Publishing

**Goal:** Automated testing and publishing.

#### 10.1 Test Workflow

**File: `.github/workflows/test.yml`**

```yaml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint with ruff
        run: ruff check src/

      - name: Type check with mypy
        run: mypy src/

      - name: Test with pytest
        run: pytest -v --cov=src/rewindlearn --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```

#### 10.2 Publish Workflow

**File: `.github/workflows/publish.yml`**

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

permissions:
  contents: read
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build tools
        run: pip install build

      - name: Build package
        run: python -m build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish-testpypi:
    needs: build
    runs-on: ubuntu-latest
    environment: testpypi
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to TestPyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/

  publish-pypi:
    needs: publish-testpypi
    runs-on: ubuntu-latest
    environment: pypi
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

#### 10.3 Manual Publishing Steps

```bash
# 1. Install build tools
pip install build twine

# 2. Build package
python -m build

# 3. Check package
twine check dist/*

# 4. Test on TestPyPI first
twine upload --repository testpypi dist/*

# 5. Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    rewindlearn

# 6. Verify it works
rewindlearn --version
rewindlearn --help

# 7. Publish to production PyPI
twine upload dist/*
```

#### Phase 10 Tasks Checklist

```
[ ] Create .github/workflows/test.yml
[ ] Create .github/workflows/publish.yml
[ ] Create PyPI account at https://pypi.org
[ ] Create TestPyPI account at https://test.pypi.org
[ ] Set up GitHub environments (testpypi, pypi) with trusted publishing
[ ] Test: GitHub Actions runs on PR
[ ] Test: Manual publish to TestPyPI works
[ ] Test: Install from TestPyPI works
[ ] Publish v0.1.0 to PyPI
```

---

### Phase 11: Examples (Deferred Features)

**Goal:** Provide reference implementations for deferred features.

**File: `examples/README.md`**

```markdown
# Examples

This directory contains reference implementations for features not included
in the core library to keep dependencies minimal.

## Video Chunker

`video_chunker.py` - Split videos into concept clips using FFmpeg.

**Requirements:**
- FFmpeg installed on system
- `pip install ffmpeg-python`

**Usage:**
```bash
python examples/video_chunker.py \
    --input lecture.mp4 \
    --chunks output/concept_chunks.csv \
    --output clips/
```

## PDF Converter

`pdf_converter.py` - Convert markdown to PDF using WeasyPrint.

**Requirements:**
- `pip install weasyprint markdown`
- System dependencies for WeasyPrint (see their docs)

**Usage:**
```bash
python examples/pdf_converter.py \
    --input output/session_summary.md \
    --output output/session_summary.pdf
```
```

**File: `examples/video_chunker.py`**

```python
#!/usr/bin/env python3
"""
Video chunker example - split videos into concept clips.

Requirements:
    pip install ffmpeg-python
    FFmpeg must be installed on the system

Usage:
    python video_chunker.py --input video.mp4 --chunks concepts.csv --output clips/
"""

import argparse
import csv
import subprocess
from pathlib import Path


def load_chunks(csv_path: Path) -> list[dict]:
    """Load concept chunks from CSV."""
    chunks = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            chunks.append({
                "concept": row["concept"],
                "description": row.get("description", ""),
                "start_time": row["start_time"],
                "end_time": row["end_time"],
            })
    return chunks


def sanitize_filename(name: str) -> str:
    """Make a string safe for use as filename."""
    invalid = '<>:"/\\|?*'
    for char in invalid:
        name = name.replace(char, "")
    return name.lower().replace(" ", "-")[:50]


def split_video(
    video_path: Path,
    chunks: list[dict],
    output_dir: Path,
    ffmpeg_path: str = "ffmpeg"
) -> list[Path]:
    """Split video into clips based on chunk timestamps."""
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []

    for i, chunk in enumerate(chunks, 1):
        safe_name = sanitize_filename(chunk["concept"])
        output_file = output_dir / f"{i:02d}-{safe_name}.mp4"

        cmd = [
            ffmpeg_path,
            "-i", str(video_path),
            "-ss", chunk["start_time"],
            "-to", chunk["end_time"],
            "-c", "copy",  # Fast copy without re-encoding
            "-y",  # Overwrite existing
            str(output_file)
        ]

        print(f"Creating: {output_file.name}")
        subprocess.run(cmd, check=True, capture_output=True)
        outputs.append(output_file)

    return outputs


def main():
    parser = argparse.ArgumentParser(description="Split video into concept clips")
    parser.add_argument("--input", "-i", required=True, help="Input video file")
    parser.add_argument("--chunks", "-c", required=True, help="Concept chunks CSV")
    parser.add_argument("--output", "-o", default="clips", help="Output directory")
    args = parser.parse_args()

    video_path = Path(args.input)
    csv_path = Path(args.chunks)
    output_dir = Path(args.output)

    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}")
        return 1

    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        return 1

    chunks = load_chunks(csv_path)
    print(f"Loaded {len(chunks)} concept chunks")

    outputs = split_video(video_path, chunks, output_dir)
    print(f"\nCreated {len(outputs)} video clips in {output_dir}/")

    return 0


if __name__ == "__main__":
    exit(main())
```

#### Phase 11 Tasks Checklist

```
[ ] Create examples/README.md
[ ] Create examples/video_chunker.py
[ ] Create examples/pdf_converter.py
[ ] Test: Video chunker works with sample CSV
```

---

## ✅ Final Verification Checklist

Before declaring the project complete:

```
Package Distribution:
[ ] pip install rewindlearn works from PyPI
[ ] CLI available as rewindlearn command after install
[ ] Works on Python 3.10, 3.11, 3.12
[ ] All dependencies install cleanly

Core Functionality:
[ ] rewindlearn --version shows correct version
[ ] rewindlearn process run generates all 7 deliverables
[ ] rewindlearn template list shows built-in templates
[ ] rewindlearn config show displays configuration
[ ] Programmatic API works: from rewindlearn import process_session

Docker:
[ ] docker compose build succeeds
[ ] docker compose run rewindlearn --help works
[ ] Container can process files from mounted volumes

Quality:
[ ] All tests pass: pytest
[ ] Type checks pass: mypy src/
[ ] Linting clean: ruff check src/
[ ] 80%+ code coverage
```

---

## 🚀 Quick Start After Implementation

```bash
# Install from PyPI
pip install rewindlearn

# Set API key
export ANTHROPIC_API_KEY="your-key"

# Process a session
rewindlearn process run \
    --template online-course \
    --transcript lecture.vtt \
    --chat chat.txt \
    --course "AI Engineering" \
    --session 5 \
    --output study-guides/

# Or use Docker
docker compose run rewindlearn process run \
    --template online-course \
    --transcript /data/input/lecture.vtt \
    --output /data/output
```

---

## 📝 Notes for Claude Code

1. **Build incrementally** - Complete each phase before moving to the next
2. **Test as you go** - Don't wait until the end to test
3. **Use the checklist** - Check off tasks as you complete them
4. **Docker early** - Verify Docker builds work after Phase 1
5. **Real data** - Test with actual transcript files when available
6. **Error messages** - Make error messages helpful and actionable

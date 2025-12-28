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
# Set your API key (at least one required)
export REWINDLEARN_OPENROUTER_API_KEY="sk-or-..."   # Recommended
# OR
export REWINDLEARN_ANTHROPIC_API_KEY="sk-ant-..."
# OR
export REWINDLEARN_OPENAI_API_KEY="sk-..."

# Process a session
rewindlearn process run \
    --template online-course-v1 \
    --transcript lecture.vtt \
    --chat chat.txt \
    --course "AI Engineering" \
    --session 5 \
    --output study-guides/
```

## Python API

```python
import asyncio
from rewindlearn import process_session

async def main():
    results = await process_session(
        template="online-course-v1",
        transcript_path="lecture.vtt",
        chat_path="chat.txt",
        course_name="AI Engineering",
        session_number=5
    )
    print(results["session_summary"])

asyncio.run(main())
```

## Features

- **Session Summary**: Comprehensive overview of the session content
- **Concept Timeline**: Chronological breakdown of concepts with timestamps
- **Friction Analysis**: Identifies potential confusion points and questions
- **Coverage Gaps**: Topics that could use more coverage
- **Learning Resources**: Curated resources for each topic
- **Action Items**: Prioritized tasks for students
- **Concept Chunks**: CSV with video clip markers for splitting

## LLM Providers

Rewind.Learn supports multiple LLM providers with automatic fallback:

| Priority | Provider | API Key | Models |
|----------|----------|---------|--------|
| 1 | OpenRouter | `REWINDLEARN_OPENROUTER_API_KEY` | Any model (e.g., `anthropic/claude-sonnet-4`) |
| 2 | Anthropic | `REWINDLEARN_ANTHROPIC_API_KEY` | Claude models (e.g., `claude-sonnet-4-20250514`) |
| 3 | OpenAI | `REWINDLEARN_OPENAI_API_KEY` | GPT models (e.g., `gpt-4o`) |

**Fallback chain**: If OpenRouter is unavailable, falls back to Anthropic, then OpenAI.

## CLI Commands

```bash
# Show help
rewindlearn --help

# Show version
rewindlearn --version

# Process a session
rewindlearn process run --template online-course-v1 --transcript lecture.vtt --output ./output

# List available templates
rewindlearn template list

# Show template details
rewindlearn template show online-course-v1

# Validate a template
rewindlearn template validate custom-template.yaml

# Show current configuration
rewindlearn config show

# Check configuration validity
rewindlearn config check
```

## Configuration

Create a `.env` file or set environment variables:

```bash
# =============================================================================
# Rewind.Learn Configuration
# Copy this file to .env and fill in your values
# =============================================================================

# LLM Provider API Keys (at least one required)
# Fallback chain: OpenRouter -> Anthropic -> OpenAI
REWINDLEARN_OPENROUTER_API_KEY=sk-or-...   # Recommended - access any model
REWINDLEARN_ANTHROPIC_API_KEY=sk-ant-...   # Direct Anthropic access
REWINDLEARN_OPENAI_API_KEY=sk-...          # Direct OpenAI access

# LangSmith Observability (optional but recommended)
REWINDLEARN_LANGSMITH_API_KEY=lsv2_...
REWINDLEARN_LANGSMITH_TRACING=true

# Rewind.Learn Settings
REWINDLEARN_DEFAULT_PROVIDER=openrouter
REWINDLEARN_DEFAULT_MODEL=anthropic/claude-sonnet-4
REWINDLEARN_TEMPLATES_DIR=./templates
REWINDLEARN_OUTPUT_DIR=./output

# Fallback Models (used when primary provider is unavailable)
REWINDLEARN_ANTHROPIC_FALLBACK_MODEL=claude-sonnet-4-20250514
REWINDLEARN_OPENAI_FALLBACK_MODEL=gpt-4o
```

## Development

```bash
# Clone the repository
git clone https://github.com/knightsri/rewind.learn.git
cd rewind.learn

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest -v

# Type checking
mypy src/

# Linting
ruff check src/
```

## License

Apache 2.0

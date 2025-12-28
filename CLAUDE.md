# Rewind.Learn - Claude Code Instructions

> **Single Source of Truth:** `rewindlearn-master-spec.md`

## Project Goal

Build a Python library published to PyPI: `pip install rewindlearn`

## Instructions for Claude Code

1. **Read `rewindlearn-master-spec.md` completely** before starting
2. **Follow the phases in order** (Phase 1 → Phase 11)
3. **Complete each phase's checklist** before moving to the next
4. **Test as you go** - don't wait until the end

## Quick Reference

```bash
# Development setup (after Phase 1)
pip install -e ".[dev]"

# Run tests
pytest -v

# Type checking
mypy src/

# Linting
ruff check src/

# Build package
python -m build

# Docker
docker compose build
docker compose run rewindlearn --help
```

## Key Files to Create First (Phase 1)

```
├── pyproject.toml          # Package definition
├── src/rewindlearn/        # Source code
├── templates/              # Built-in YAML templates
├── Dockerfile              # Production container
├── docker-compose.yaml     # Container orchestration
└── .env.example            # Environment template
```

## What NOT to Do

- Don't skip phases
- Don't implement deferred features (video chunker, PDF) in core - put in `/examples`
- Don't add dependencies not in the spec without asking
- Don't forget Docker - it's Phase 1, not an afterthought

## Success Criteria

When complete, these must work:

```bash
# From PyPI
pip install rewindlearn
rewindlearn --version
rewindlearn --help

# CLI processing
rewindlearn process run --template online-course --transcript lecture.vtt --output ./

# Docker
docker compose run rewindlearn --help

# Python API
python -c "from rewindlearn import process_session; print('OK')"
```

## Archive

Historical documents preserved in `docs/archive/` for reference only.
The master spec supersedes all previous documentation.

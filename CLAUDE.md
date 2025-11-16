# CLAUDE.md - AI Assistant Context for Rewind.Learn

**Last Updated:** November 2025
**Purpose:** Guide AI assistants to make decisions aligned with project goals, constraints, and architecture

---

## Project Mission

**Rewind.Learn** is an open-source, template-driven framework that transforms online session artifacts (transcripts, chat logs, recordings) into structured, actionable deliverables using AI-powered analysis.

**Core Problem:** 80-90% of knowledge from online sessions (courses, meetings, workshops) remains trapped in unwatched recordings and unread transcripts.

**Solution:** Automate the extraction and structuring of this knowledge through configurable templates powered by LangChain/LangGraph workflows.

---

## Project Goals

### Primary Goals (MVP - 8 weeks)
1. **Template Engine:** YAML-based system that defines how to process different session types
2. **Online Course Template:** First working template that processes educational sessions into 6 deliverables
3. **LangChain/LangGraph Integration:** Production-grade LLM orchestration with proper state management
4. **CLI Tool:** Command-line interface for processing sessions
5. **Quality Output:** User ratings ≥8/10, processing time <3 min, cost <$2 per session

### Secondary Goals (Post-MVP)
1. **Template Marketplace:** Community-contributed templates for different meeting types
2. **Knowledge Graph:** Cross-session intelligence using vector embeddings
3. **Multiple Templates:** Agile retrospective, medical reviews, legal depositions, etc.
4. **Web UI:** Browser-based interface
5. **Managed Hosting:** Optional cloud service

---

## Critical Constraints

### Technical Constraints
- **Python 3.10+** required
- **LangChain/LangGraph/LangSmith stack** (non-negotiable - this is the foundation)
- **Self-hostable:** Must run on user's infrastructure, no cloud dependencies
- **Privacy-first:** User data never leaves their environment
- **LLM Provider Agnostic:** Support Claude, OpenAI, and local models (Ollama)
- **Template-driven:** New session types should NOT require code changes

### Time Constraints
- **8-week MVP timeline** (currently Week 1)
- **Week 7 buffer** for testing and documentation
- **Knowledge graph is optional** if behind schedule
- **Must have at least 3 of 6 chains working** (can finish remaining post-MVP)

### Cost Constraints
- **Processing cost target:** <$2.00 per session
- **Track every API call** via LangSmith
- **Use appropriate models:** Claude Sonnet 4 for complex tasks, Haiku/GPT-4o-mini for simple extraction

### Quality Constraints
- **User satisfaction:** ≥8/10 ratings
- **Processing time:** <3 minutes per session
- **Output quality:** Consistent, actionable deliverables
- **Error handling:** Graceful degradation, no silent failures

---

## Technology Stack

### Core Framework (Non-Negotiable)
```python
# LLM Orchestration
langchain>=0.1.0          # Chain management, prompts
langgraph>=0.0.20         # Workflow state machine
langsmith>=0.0.60         # Observability, tracing

# Data Validation
pydantic>=2.0.0           # Schema validation

# CLI & UX
typer>=0.9.0              # CLI framework
rich>=13.0.0              # Terminal UI

# File Processing
pyyaml>=6.0               # Template parsing
```

### LLM Providers
- **Primary:** Anthropic Claude (Sonnet 4 for complex, Haiku for simple)
- **Secondary:** OpenAI (GPT-4o for sentiment analysis, GPT-4o-mini for extraction)
- **Local:** Ollama (for privacy-sensitive deployments)

### Optional Components
```python
# Knowledge Graph (Phase 4 - Optional)
supabase>=2.0.0           # pgvector for embeddings
chromadb>=0.4.0           # Alternative vector store

# Output Generation
python-markdown>=3.4.0    # Markdown processing
weasyprint>=60.0          # PDF generation
jinja2>=3.1.0             # HTML templates

# Automation (Future)
redis>=5.0.0              # Caching
celery>=5.3.0             # Task queue (managed hosting)
```

---

## Architecture Principles

### 1. Template-First Design
**Principle:** The framework should handle ANY session type through configuration, not code changes.

**What this means:**
- New templates are YAML files, not Python code
- Template validation ensures correctness before processing
- Processing logic is generic and driven by template specifications
- Users should be able to create custom templates without knowing Python

**Decision Guidance:**
- If adding a new feature requires code changes for each template → **rethink the approach**
- If a feature can be configured in YAML → **do that instead**

### 2. Privacy-First, Self-Hostable
**Principle:** Users must be able to run everything on their own infrastructure.

**What this means:**
- No required cloud services or SaaS dependencies
- Support local LLM models (Ollama)
- Knowledge graph is optional (can use local ChromaDB or skip entirely)
- All data processing happens where the user controls it

**Decision Guidance:**
- If a feature requires a cloud service → **make it optional with local alternative**
- If API keys are required → **support self-hosted alternatives**

### 3. Observable and Cost-Conscious
**Principle:** Every LLM call must be tracked, traceable, and optimizable.

**What this means:**
- LangSmith integration from day 1
- Track token usage, cost, latency for every task
- Support A/B testing of prompts
- Users should see exactly what each session costs

**Decision Guidance:**
- If adding a new LLM call → **wrap it with @traceable decorator**
- If a task can use a cheaper model → **use it (e.g., Haiku vs Sonnet)**
- If processing cost exceeds $2/session → **optimize or warn user**

### 4. Production-Grade AI Stack
**Principle:** Use proven, maintained frameworks (LangChain/LangGraph), not custom solutions.

**What this means:**
- LangGraph for ALL workflow orchestration (not custom state machines)
- LangChain for ALL LLM interactions (not direct API calls)
- Pydantic for ALL data validation (not ad-hoc checking)
- Follow LangChain best practices for prompt management

**Decision Guidance:**
- If considering direct LLM API calls → **use LangChain instead**
- If building custom state management → **use LangGraph instead**
- If creating custom validation → **use Pydantic models instead**

### 5. Fail Gracefully, Retry Intelligently
**Principle:** LLM calls can fail; handle it without losing all work.

**What this means:**
- Tasks with no dependencies can run in parallel
- If one task fails, others continue (collect partial results)
- Implement retries with exponential backoff for transient failures
- Save intermediate state so failures can be resumed

**Decision Guidance:**
- If a task failure stops everything → **allow partial results**
- If network errors aren't retried → **add retry logic**
- If state is lost on failure → **persist intermediate results**

---

## Project Structure

### Current Structure
```
rewind.learn/
├── docs/                    # Documentation
│   ├── CONCEPT.md          # Project vision
│   ├── ARCHITECTURE.md     # Technical design
│   ├── TEMPLATES.md        # Template specifications
│   ├── QUICK-REFERENCE.md  # Quick reference
│   └── ...
├── README.md               # Public-facing overview
└── CLAUDE.md              # This file
```

### Target Structure (MVP)
```
rewind.learn/
├── src/rewindlearn/
│   ├── __init__.py
│   ├── core/               # Template engine, models
│   │   ├── template.py    # Template loading & validation
│   │   ├── models.py      # Pydantic schemas
│   │   └── config.py      # Configuration management
│   ├── processors/         # File parsers
│   │   ├── transcript.py  # Transcript processing
│   │   ├── chat.py        # Chat log processing
│   │   └── slides.py      # Slide processing (optional)
│   ├── workflow/           # LangGraph state machine
│   │   ├── graph.py       # Workflow builder
│   │   └── state.py       # State schema
│   ├── chains/             # Individual LangChain chains
│   │   ├── summary.py     # Session summary
│   │   ├── timeline.py    # Concept timeline
│   │   ├── friction.py    # Friction analysis
│   │   └── ...
│   ├── output/             # Output generation
│   │   ├── markdown.py    # Markdown generation
│   │   └── pdf.py         # PDF conversion (optional)
│   ├── cli/                # CLI commands
│   │   └── main.py        # Typer CLI app
│   └── utils/              # Helpers
├── templates/              # Built-in templates
│   ├── online-course-v1.yaml
│   └── agile-retro-v1.yaml (future)
├── tests/                  # Test suite
├── examples/               # Sample data
│   └── sample-session/
│       ├── transcript.txt
│       ├── chat.json
│       └── context.yaml
└── docs/                   # Documentation
```

---

## Key Design Decisions

### Why LangGraph Instead of Direct Chains?
**Reason:** Complex workflows with task dependencies, parallel execution, error recovery, and state persistence require a state machine. LangGraph provides this out-of-the-box with observability.

**Alternative Considered:** Custom orchestration with asyncio
**Rejected Because:** Would be reinventing LangGraph; less maintainable

### Why YAML for Templates Instead of Python?
**Reason:** Lower barrier to entry. Educators, product managers, and domain experts can create templates without coding.

**Alternative Considered:** Python-based template classes
**Rejected Because:** Requires programming knowledge; harder to share and validate

### Why Support Multiple LLM Providers?
**Reason:**
1. Users may have existing contracts/preferences
2. Some models better for specific tasks (GPT-4o for sentiment, Claude for structured output)
3. Privacy-sensitive orgs need local models (Ollama)
4. Cost optimization (mix expensive and cheap models)

**Alternative Considered:** Lock to Claude only
**Rejected Because:** Limits adoption, vendor lock-in violates privacy-first principle

### Why Make Knowledge Graph Optional?
**Reason:** Adds significant complexity; not essential for MVP value proposition. Cross-session analysis is a "nice to have" that can come later.

**Alternative Considered:** Make it mandatory
**Rejected Because:** Time constraint; risk to MVP delivery

### Why CLI Before Web UI?
**Reason:**
1. Faster to implement (8-week constraint)
2. Easier to test and debug
3. Targets power users and developers first (early adopters)
4. Web UI can wrap CLI later

**Alternative Considered:** Web UI first
**Rejected Because:** More complex; slower feedback loop

---

## What to Prioritize (Decision Framework)

### HIGH Priority (Must Have for MVP)
1. **Template engine with validation** - everything depends on this
2. **File processors (transcript + chat)** - core inputs
3. **LangGraph workflow builder** - orchestration layer
4. **At least 3 working chains** - proof of value (summary, timeline, friction)
5. **Markdown output generation** - deliverables
6. **Basic CLI** - user interface
7. **LangSmith integration** - observability

### MEDIUM Priority (Should Have)
1. **All 6 chains working** - complete experience (can finish 3-4 post-MVP)
2. **Error handling & retries** - production readiness
3. **Cost tracking** - user transparency
4. **Template validation CLI command** - developer experience

### LOW Priority (Nice to Have)
1. **PDF conversion** - Markdown is sufficient for MVP
2. **Slide processing** - optional input
3. **Video timestamp indexing** - enhancement
4. **Knowledge graph** - skip if behind schedule
5. **Advanced CLI features** - polish for later

---

## What to Avoid

### Anti-Patterns
1. **Hardcoding session types** - Use templates, not if/else logic
2. **Direct LLM API calls** - Always use LangChain for observability
3. **Synchronous processing** - Use LangGraph for parallelization
4. **Ignoring errors** - Fail gracefully, log everything
5. **Premature optimization** - Get it working first, optimize later

### Technical Debt to Avoid
1. **Skipping Pydantic validation** - Validate inputs early
2. **Not using type hints** - Python 3.10+ requires them
3. **Bypassing LangSmith tracing** - Every chain must be traceable
4. **Mixing async and sync code** - Stick to async throughout
5. **Hardcoded paths** - Use pathlib.Path, respect user's config

### Scope Creep Traps
1. **Adding real-time processing** - Post-MVP feature
2. **Building template marketplace** - V1.0 feature
3. **User authentication** - Only needed for managed hosting (V2.0)
4. **Multiple output languages** - Start with English, add later
5. **Advanced RAG features** - Knowledge graph is already optional

---

## Development Phases & Status

### Phase 1: Core Engine (Weeks 1-2)
**Status:** Starting
**Goals:**
- Template loader and YAML validator
- File processors (transcript, chat)
- Pydantic models for all data structures
- Basic configuration management

**Success Criteria:**
- [ ] Load and validate online-course template
- [ ] Parse sample transcript into structured format
- [ ] Parse sample chat log into structured format
- [ ] Configuration system for API keys

### Phase 2: LangChain Integration (Weeks 3-4)
**Status:** Not started
**Goals:**
- Build LangGraph workflow from template
- Implement 3+ LangChain chains (summary, timeline, friction)
- LangSmith tracing for all chains
- Parallel task execution for independent chains

**Success Criteria:**
- [ ] Generate session summary from transcript
- [ ] Generate concept timeline with timestamps
- [ ] Analyze student friction from chat
- [ ] All chains traceable in LangSmith
- [ ] Processing completes in <3 minutes

### Phase 3: CLI & Output (Weeks 5-6)
**Status:** Not started
**Goals:**
- Typer CLI with Rich terminal UI
- Markdown output generation
- Cost tracking and reporting
- End-to-end processing workflow

**Success Criteria:**
- [ ] `rewindlearn process` command works
- [ ] Generates 3+ Markdown files
- [ ] Shows progress with Rich UI
- [ ] Reports processing cost

### Phase 4: Polish & Testing (Week 7)
**Status:** Not started
**Goals:**
- Error handling and retries
- Test suite for critical paths
- Documentation
- Demo preparation

**Success Criteria:**
- [ ] Handles missing inputs gracefully
- [ ] Retries transient LLM failures
- [ ] Test coverage >60%
- [ ] README with quickstart

### Phase 5: Pilot (Week 8)
**Status:** Not started
**Goals:**
- Process real course sessions
- Gather user feedback
- Measure quality and cost
- Iterate on prompts

**Success Criteria:**
- [ ] 5-7 users process their sessions
- [ ] User ratings ≥8/10
- [ ] Cost <$2 per session
- [ ] Processing time <3 minutes

---

## Common Scenarios & Guidance

### Scenario: User wants to add a new template
**Guidance:**
1. Help them create a YAML file based on existing template structure
2. Validate the template using Pydantic models
3. Test with sample data before production use
4. NO code changes should be needed (if they are, the engine is incomplete)

### Scenario: Processing is too expensive
**Guidance:**
1. Check which tasks use Sonnet vs Haiku
2. Review prompt lengths (can they be shorter?)
3. Consider if some tasks can use GPT-4o-mini instead
4. Check if temperature is unnecessarily high (wastes tokens)
5. Use LangSmith to identify expensive chains

### Scenario: LLM call fails
**Guidance:**
1. Retry with exponential backoff (2s, 4s, 8s delays)
2. If retry limit reached, mark task as failed
3. Continue processing other independent tasks
4. Return partial results with warnings
5. Log failure details for debugging

### Scenario: User wants faster processing
**Guidance:**
1. Check if tasks are running in parallel (LangGraph should handle this)
2. Review task dependencies (can more run in parallel?)
3. Consider using streaming responses for long tasks
4. Profile with LangSmith to find bottlenecks
5. Consider caching repeated analyses (e.g., transcript summary)

### Scenario: Output quality is poor
**Guidance:**
1. Review prompt templates (are they specific enough?)
2. Check temperature settings (too high = inconsistent)
3. Use LangSmith to A/B test prompt variations
4. Consider if wrong model is being used (Sonnet vs GPT-4o)
5. Validate that input files are high quality

### Scenario: User wants to skip knowledge graph
**Guidance:**
1. This is COMPLETELY FINE - it's optional by design
2. Comment out knowledge graph imports in requirements
3. Skip vector embedding steps in processing
4. Template validation should still work
5. All core functionality remains intact

---

## Prompt Engineering Guidelines

### For Structured Extraction (Summary, Timeline, Actions)
```yaml
llm_config:
  model: "claude-sonnet-4"
  temperature: 0.2-0.3        # Low for consistency
  max_tokens: 2000-4000       # Depends on expected output length

prompt_template: |
  You are analyzing a {session_type} session.

  INPUT:
  {input_data}

  OUTPUT REQUIREMENTS:
  1. Specific structure (use headers, bullets)
  2. Include examples of good output
  3. Specify exact format (timestamps, etc.)

  Example good output:
  ## [00:15:30 - 00:23:45] Topic Name
  - Sub-point 1
  - Sub-point 2
```

### For Creative Tasks (Resource Curation)
```yaml
llm_config:
  model: "claude-sonnet-4"
  temperature: 0.6-0.7        # Higher for variety
  max_tokens: 4000            # Allow more exploration

prompt_template: |
  Curate diverse learning resources for these topics.

  Focus on:
  - High-quality sources
  - Multiple formats (video, text, interactive)
  - Range of difficulty levels

  Be creative but maintain quality standards.
```

### For Sentiment Analysis (Friction Detection)
```yaml
llm_config:
  model: "gpt-4o"             # Good at sentiment
  temperature: 0.4            # Balanced
  max_tokens: 3000

prompt_template: |
  Analyze chat messages for signs of confusion.

  Look for:
  - Questions indicating misunderstanding
  - Repeated questions on same topic
  - Requests for clarification

  Provide specific examples from chat.
```

---

## Testing Strategy

### Unit Tests (Core Components)
- Template validation logic
- File parsers (transcript, chat)
- Pydantic model validation
- Configuration loading

### Integration Tests (LangChain/LangGraph)
- Individual chains with mocked LLM responses
- LangGraph workflow state transitions
- Error handling and retries
- Parallel task execution

### End-to-End Tests (Full Pipeline)
- Process sample session with real LLM calls
- Verify all deliverables generated
- Check output quality against criteria
- Measure processing time and cost

### Template Tests
- Validate all built-in templates
- Test with various input combinations
- Check for circular dependencies
- Ensure all referenced tasks exist

---

## File Format Expectations

### Transcript Format
- **Preferred:** .txt with timestamps `[HH:MM:SS] Speaker: Text`
- **Supported:** .vtt, .srt (subtitle formats)
- **Encoding:** UTF-8
- **Size limit:** ~1M tokens (~750K words) - split larger sessions

### Chat Log Format
- **Preferred:** JSON array of messages
```json
[
  {
    "timestamp": "2024-11-16T14:30:00Z",
    "sender": "John Doe",
    "message": "What is backpropagation?"
  }
]
```
- **Alternative:** .txt with format `[HH:MM:SS] User: Message`

### Course Context Format
- **Format:** YAML
```yaml
course_name: "AI Engineering Bootcamp"
session_number: 5
instructor_name: "Sri"
session_date: "2024-11-16"
planned_topics:
  - "Neural networks basics"
  - "Backpropagation"
  - "Training strategies"
```

---

## API Usage Patterns

### Anthropic Claude
- **Sonnet 4:** Complex reasoning, structured output, multi-step analysis
- **Haiku:** Simple extraction, formatting, quick tasks
- **Cost:** Sonnet ~$3/M input tokens, $15/M output tokens
- **Best for:** Primary processing tasks

### OpenAI
- **GPT-4o:** Sentiment analysis, creative tasks, cross-validation
- **GPT-4o-mini:** Cheap extraction, formatting, high-volume tasks
- **Cost:** GPT-4o ~$2.50/M input, $10/M output
- **Best for:** Specific tasks where it excels (sentiment, function calling)

### Ollama (Local)
- **Models:** Llama 3, Mistral, Phi-3
- **Cost:** $0 (compute only)
- **Best for:** Privacy-sensitive deployments, development, testing
- **Trade-off:** Lower quality than Sonnet/GPT-4o, slower

---

## Success Metrics

### During Development
- Template validation pass rate: 100%
- Chain success rate: >95%
- Test coverage: >60%
- Processing time: <3 minutes
- Cost per session: <$2.00

### At MVP Demo
- User can process session in <5 minutes (setup + processing)
- Output quality rated ≥8/10 by pilot users
- Can create new template in <4 hours
- Documentation complete for quickstart

### Post-MVP
- 60%+ user retention after 10 sessions
- <1 hour support time per user
- <2 bugs per 100 sessions processed
- Community template contributions: 2+ in first 3 months

---

## Quick Reference

### When to Use Which LLM Model
| Task Type | Model | Temperature | Reasoning |
|-----------|-------|-------------|-----------|
| Session Summary | Claude Sonnet 4 | 0.3 | Structured, comprehensive |
| Concept Timeline | Claude Sonnet 4 | 0.2 | Precise timestamps |
| Friction Analysis | GPT-4o | 0.4 | Good at sentiment |
| Coverage Gaps | Claude Sonnet 4 | 0.3 | Comparison reasoning |
| Resource Curation | Claude Sonnet 4 | 0.7 | Creative, diverse |
| Action Items | Claude Haiku | 0.2 | Simple extraction |

### Critical Path (Must Complete)
1. Week 1-2: Template engine + file processors
2. Week 3-4: LangGraph + 3 chains working
3. Week 5-6: CLI + Markdown output
4. Week 7: Testing + documentation
5. Week 8: Pilot with real users

### Emergency Descope Plan (If Behind Schedule)
1. Drop to 3 chains only (summary, timeline, friction)
2. Skip PDF generation (Markdown only)
3. Skip knowledge graph
4. Reduce CLI features (process command only)
5. Simplify error handling (fail fast)

---

## Contact & Resources

### Documentation
- **Concept:** docs/CONCEPT.md
- **Architecture:** docs/ARCHITECTURE.md
- **Templates:** docs/TEMPLATES.md
- **Quick Ref:** docs/QUICK-REFERENCE.md

### AI Viability Analyses
- [Gemini 2.5 Pro Analysis](https://mvp.shalusri.com/rewind.learn/rewind.learn-analysis-gemini-2-5-pro-20251022/)
- [Sonnet 4.5 Analysis](https://mvp.shalusri.com/rewind.learn/rewind.learn-analysis-claude-sonnet-4-5-20251022/)

### External Tools
- LangChain: https://langchain.com
- LangGraph: https://langchain-ai.github.io/langgraph/
- LangSmith: https://smith.langchain.com
- Supabase: https://supabase.com

---

## Key Principles for AI Assistants

When working on this project:

1. **Template-driven first** - Don't hardcode session types
2. **Use LangChain/LangGraph** - Don't reinvent orchestration
3. **Privacy matters** - Keep everything self-hostable
4. **Track everything** - LangSmith integration is non-negotiable
5. **Fail gracefully** - Partial results better than total failure
6. **8-week timeline** - Descope features, not quality
7. **Open source spirit** - Write code others can extend

**Remember:** The template engine IS the product. The online course template is just proof it works. Success = anyone can create a new template for their meeting type in YAML.

---

**Last Updated:** November 2025
**Status:** Week 1 - Core Engine Development
**Next Milestone:** Template validation + file processors (Week 2)

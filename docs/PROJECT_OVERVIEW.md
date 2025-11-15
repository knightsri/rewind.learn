# Rewind.Learn - Project Overview

**Version:** 1.0 (MVP)  
**Author:** Sri Bolisetty (@KnightSri)  
**Last Updated:** November 2025  
**Timeline:** 8 weeks  
**Target Completion:** January 2026  
**Demo Day:** January 17, 2026

---

## What is Rewind.Learn?

Rewind.Learn is an **open-source, template-driven framework** that transforms online session artifacts (transcripts, chat logs, recordings) into structured, actionable deliverables through AI-powered workflows.

**The Core Innovation:**

One framework processes ANY meeting type through configuration, not code:
- **Online courses** → Study guides, concept timelines, confusion analysis
- **Sprint retrospectives** → Action items, sentiment analysis, blocker patterns
- **Sales calls** → Decision summaries, objections, next steps
- **Medical rounds** → Case summaries, teaching points, diagnostic pathways
- **Legal depositions** → Testimony timelines, key arguments, evidence catalogs

**The template system IS the product.** The online course template is the MVP proof-of-concept.

---

## The Problem

Every online session—courses, team meetings, training workshops, retrospectives—generates valuable content: transcripts, chat logs, recordings, slides. Yet **80-90% of this knowledge remains trapped** in unwatched recordings and unread transcripts.

**The Pain Points:**

**Educators** spend 3-5 hours per session manually creating study guides  
**Agile teams** lose 15-20% of retrospective insights to poor documentation  
**Students** struggle to find specific concepts in 90-minute recordings  
**Organizations** cannot extract value from thousands of recorded meetings

**The Gap:**

No vendor-neutral framework exists for transforming meeting artifacts into structured deliverables. Organizations must either:
- Build custom solutions for each meeting type (expensive, non-reusable)
- Use proprietary SaaS tools (vendor lock-in, privacy concerns, inflexible)
- Continue manual documentation (unsustainable)

**Why Platforms Haven't Solved This:**

Zoom, Microsoft Teams, and Google Meet *should* build this natively—they have the data, users, and infrastructure. They haven't. This creates an opportunity for an open-source, extensible solution that works across platforms and meeting types.

---

## The Solution

**Template-Driven Processing Framework**

Each **template** defines:
- **Input schema** (what artifacts are required/optional)
- **Processing workflow** (LLM analysis tasks with dependencies)
- **Output deliverables** (what gets generated)

Templates are configurable (YAML) and extensible—community can build new ones for different session types **without writing code**.

**Example: Online Course Session**

```bash
# Process a 2-hour lecture
rewindlearn process \
  --template online-course \
  --transcript session-01.txt \
  --chat chat-01.json \
  --output study-guides/

# Outputs (generated in ~3 minutes, cost ~$1.50):
# - session-summary.md
# - concept-timeline.md  
# - student-friction-analysis.md
# - coverage-gaps.md
# - learning-resources.md
# - action-items.md
```

---

## Key Features

### 🎨 Template-Driven Architecture
Define custom processing workflows for any session type. Templates specify inputs, LLM tasks, and output formats—no code required for new use cases.

### 🔒 Privacy-First, Self-Hostable
Run entirely on your infrastructure. Your data never leaves your environment. Choose your LLM provider (Claude, GPT-4, local models).

### 🧠 Cross-Session Intelligence
Knowledge graphs connect concepts across sessions. Identify prerequisite gaps, recurring confusion, and learning patterns over time.

### 🔧 Built on Modern AI Stack
- **LangChain** for LLM orchestration
- **LangGraph** for workflow state management
- **LangSmith** for observability and prompt optimization
- **Supabase** for knowledge graph storage

### 📊 Observable & Cost-Conscious
Track quality metrics, token usage, and processing costs per session. A/B test prompts. Optimize for your budget.

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Rewind.Learn System                  │
│                                                       │
│  User (CLI) → Template Loader → LangGraph Workflow  │
│                                      ↓                │
│                         File Processors               │
│                    (Transcript, Chat, Slides)         │
│                                      ↓                │
│                      LangChain Chains                 │
│                   (Multi-stage LLM tasks)             │
│                                      ↓                │
│                    Output Generation                  │
│                  (Markdown → PDF/HTML)                │
│                                      ↓                │
│                  Knowledge Graph (Optional)           │
│                 (Cross-session intelligence)          │
└─────────────────────────────────────────────────────┘
```

**Core Components:**

1. **Template Engine** - Parse & validate YAML templates
2. **File Processors** - Handle transcripts, chat logs, slides, videos
3. **LangGraph Workflow** - State machine managing task dependencies
4. **LangChain Chains** - Individual LLM analysis tasks
5. **Output Builder** - Generate Markdown, PDF, HTML deliverables
6. **Knowledge Graph** - Vector storage for cross-session analysis (optional)

---

## Technology Stack

**Core Framework:**
- Python 3.10+
- LangChain (LLM orchestration)
- LangGraph (workflow state management)
- LangSmith (observability & prompt optimization)

**LLM Providers:**
- Anthropic Claude (Sonnet 4 primary)
- OpenAI GPT-4o (alternative)
- Ollama (local models for privacy)

**Data & Storage:**
- Supabase (PostgreSQL + pgvector for knowledge graph)
- Redis (optional caching)
- Local filesystem / S3

**CLI & Output:**
- Typer (CLI framework)
- Rich (beautiful terminal UI)
- Pydantic (data validation)
- WeasyPrint/Pandoc (PDF generation)

---

## MVP Scope: Online Course Template

**Primary Use Case:** Transform lecture sessions into comprehensive study materials

**Input Requirements:**

Required:
- Session transcript (any format: .txt, .vtt, .srt)
- Chat log export (.json or .txt)
- Course context (course name, session number)

Optional:
- Previous session summaries (for prerequisite detection)
- Session agenda/outline
- Slide deck (PDF)
- Video recording (for timestamp indexing)

**Processing Tasks (6 LangChain chains):**

1. **Session Summary** - Executive overview, key concepts, learning objectives
2. **Concept Timeline** - Chronological outline (5-10 min segments with video timestamps)
3. **Student Friction Analysis** - Confusion indicators from chat, topics needing review
4. **Coverage Gap Report** - Planned topics vs. actual coverage
5. **Learning Resources** - Curated external resources (papers, videos, tutorials)
6. **Action Items** - Homework, assignments, deadlines

**Output Deliverables:**

All outputs generated in Markdown, convertible to PDF/HTML:
- `session-summary.md`
- `concept-timeline.md`
- `student-friction-analysis.md`
- `coverage-gaps.md`
- `learning-resources.md`
- `action-items.md`

**Performance Targets:**
- Processing time: <3 minutes per session
- Cost: <$2.00 per session
- Quality: ≥8/10 user ratings

---

## Example Template Structure

**Template YAML (online-course-v1.yaml):**

```yaml
template_id: "online-course-v1"
name: "Online Course Session"
version: "1.0"

inputs:
  required:
    - transcript
    - chat_log
    - course_context
  optional:
    - slides
    - previous_session_summary
    - agenda

processing:
  tasks:
    - name: "session_summary"
      prompt_template: |
        Analyze this course session...
      llm_config:
        model: "claude-sonnet-4"
        temperature: 0.3
      dependencies: []
    
    - name: "concept_timeline"
      llm_config:
        model: "claude-sonnet-4"
        temperature: 0.2
      dependencies: ["session_summary"]
    
    # ... 4 more tasks

outputs:
  deliverables:
    - session_summary
    - concept_timeline
    - friction_analysis
    - coverage_gaps
    - learning_resources
    - action_items
  formats:
    - markdown
    - pdf
  languages:
    - en
```

**See TEMPLATES.md for complete specifications.**

---

## Project Status

**Current Phase:** MVP Development (Weeks 1-8)

**Timeline:**

| Phase | Dates | Deliverable |
|-------|-------|-------------|
| **Phase 1** | Weeks 1-2 | Template engine & file processors |
| **Phase 2** | Weeks 3-4 | LangChain/LangGraph integration |
| **Phase 3** | Weeks 5-6 | CLI & output generation |
| **Phase 4** | Week 7 | Knowledge graph (optional) |
| **Phase 5** | Week 8 | Testing, docs, demo prep |

**Completed:**
- ✅ Project concept and architecture
- ✅ Template specification design
- ✅ AI viability validation (7-9/10 scores from Gemini 2.5 Pro & Claude Sonnet 4.5)
- ✅ Repository setup
- ✅ Documentation complete

**In Progress:**
- 🚧 Template engine implementation (Week 1-2)
- 🚧 File processors (transcript, chat, slides)
- 🚧 LangChain chain development

**Next Steps:**
- 📋 LangGraph workflow orchestration
- 📋 CLI implementation
- 📋 Output generation (Markdown → PDF)
- 📋 Pilot with 5-7 users

---

## Success Metrics

**MVP Requirements:**

| Category | Metric | Target |
|----------|--------|--------|
| **Framework Viability** | Template system works | New templates via YAML only |
| **MVP Quality** | User ratings | ≥8/10 from 5-7 pilot users |
| **Processing Speed** | Complete workflow | <3 minutes per session |
| **Cost Efficiency** | Processing cost | <$2.00 per session |
| **Extensibility Proof** | Second template | Implementable in <1 week |

**Success Criteria:**
1. ✅ Template engine enables new meeting types without code
2. ✅ Online course template generates high-quality study materials
3. ✅ Processing is fast and cost-effective
4. ✅ Can implement agile retrospective template quickly (proves extensibility)

---

## Use Cases

### Education
- **Bootcamps & Online Courses**: Auto-generate study guides after each lecture
- **University Courses**: Create searchable knowledge base across semester
- **Corporate Training**: Document training sessions for compliance

### Agile Teams
- **Sprint Retrospectives**: Track action items, sentiment, recurring blockers
- **Planning Meetings**: Extract decisions, dependencies, risks
- **Standups**: Aggregate daily updates into sprint summaries

### Professional Services
- **Consulting**: Document client meetings, decisions, action items
- **Legal**: Deposition summaries, testimony analysis
- **Medical**: Case reviews, teaching rounds, clinical discussions

---

## The Framework Vision

**Core Insight:** The same framework processes ANY meeting type through templates.

**Potential Meeting Types:**
- Education: Lectures, bootcamps, training, certifications
- Agile Teams: Retrospectives, planning, standups, demos
- Sales: Client calls, discovery meetings, demos, objections
- Medical: Case reviews, teaching rounds, tumor boards
- Legal: Depositions, case strategy, client interviews
- Consulting: Client meetings, deliverable reviews
- Design: Critiques, stakeholder reviews, user testing
- Executive: Town halls, board meetings, strategy sessions

**Why This Matters:**

A hospital can process medical rounds.  
A law firm can process depositions.  
A software team can process retrospectives.  
**All using the same framework, different templates.**

**The framework is the product.** The lecture template proves it works.

---

## Example Usage (When Complete)

```bash
# Install
pip install rewindlearn

# Configure LLM provider
rewindlearn config set-provider claude --api-key $ANTHROPIC_API_KEY

# Process a course session
rewindlearn process \
  --template online-course \
  --transcript lecture-01.txt \
  --chat chat-01.json \
  --output study-guides/

# Results:
Processing session... ✓
├─ Session summary generated (982 tokens, $0.25)
├─ Concept timeline created (1,245 tokens, $0.31)
├─ Friction analysis complete (734 tokens, $0.18)
├─ Coverage gaps identified (456 tokens, $0.11)
├─ Learning resources curated (1,123 tokens, $0.28)
└─ Action items extracted (389 tokens, $0.10)

Total: 4,929 tokens, $1.23, 2m 14s

Outputs saved to: study-guides/
├─ session-summary.md
├─ concept-timeline.md
├─ student-friction-analysis.md
├─ coverage-gaps.md
├─ learning-resources.md
└─ action-items.md
```

---

## Development Timeline

**8-Week MVP Schedule:**

**Weeks 1-2: Core Engine**
- Template loader and validator
- File processors (transcript, chat, slides)
- Basic LangChain for one task (summary)
- CLI skeleton

**Weeks 3-4: Full Workflow**
- LangGraph state machine
- All 6 processing tasks working
- Parallel task execution
- Error handling and retries

**Weeks 5-6: Output & Integration**
- Output generation (Markdown → PDF/HTML)
- LangSmith integration
- Cost tracking
- CLI polish

**Week 7: Knowledge Graph (Optional)**
- Supabase setup with pgvector
- Session embedding and storage
- Cross-session concept linking
- **Can skip if behind schedule**

**Week 8: Polish & Demo**
- Comprehensive testing
- Documentation
- Demo preparation
- Pilot user testing

---

## Comparison with Alternatives

| Feature | Rewind.Learn | Zoom AI Companion | Fireflies.ai | Manual Process |
|---------|--------------|-------------------|--------------|----------------|
| **Privacy** | ✅ Self-hosted | ❌ Cloud only | ❌ Cloud only | ✅ Full control |
| **Extensible** | ✅ Templates | ❌ Fixed features | ❌ Fixed features | ✅ Manual work |
| **Cross-platform** | ✅ Any transcript | ❌ Zoom only | ⚠️ Limited | ✅ Any source |
| **Cost** | ~$1.50/session | $12/user/month | $10-40/user/month | Time expensive |
| **Customizable** | ✅ YAML config | ❌ No | ⚠️ Limited | ✅ Full control |
| **Open Source** | ✅ Yes | ❌ No | ❌ No | N/A |

**Why Rewind.Learn:**
- Works across platforms (not locked to Zoom/Teams)
- Fully customizable for your workflows
- Privacy-respecting (self-hostable)
- Open-source and extensible
- Community can contribute templates

---

## Roadmap

### MVP (Q4 2025)
- ✅ Core template engine
- ✅ Online course template (fully implemented)
- ✅ CLI tool
- ✅ LangSmith integration
- ✅ Pilot with 5-7 users
- ✅ Documentation

### V1.0 (Q1 2026)
- Agile retrospective template
- Knowledge graph for cross-session analysis
- Docker deployment
- Template marketplace (browse community templates)
- Web UI (basic)

### V2.0 (Q2 2026)
- Managed cloud hosting option
- Real-time processing during sessions
- Video timestamp indexing
- 5+ community templates
- Enterprise features (SSO, audit logs)

---

## Resources

**Project Documentation:**
- Architecture: `ARCHITECTURE.md`
- Template Specs: `rewind-learn-TEMPLATES.md`
- Implementation Guide: `rewind-learn-claude-code-task-list.md`
- Quick Reference: `rewind-learn-QUICK-REFERENCE.md`

**AI Viability Analyses:**
- [Gemini 2.5 Pro Analysis](https://mvp.shalusri.com/rewind.learn/rewind.learn-analysis-gemini-2-5-pro-20251022/) (Score: 7-9/10)
- [Sonnet 4.5 Analysis](https://mvp.shalusri.com/rewind.learn/rewind.learn-analysis-claude-sonnet-4-5-20251022/) (Score: 7-9/10)

**External Tools:**
- LangChain: <https://langchain.com>
- LangSmith: <https://smith.langchain.com>
- Supabase: <https://supabase.com>
- Anthropic: <https://anthropic.com>

---

## Contributing (Post-MVP)

We welcome contributions:
- 👨‍💻 **Developers** - Build templates, integrations
- 👨‍🏫 **Educators** - Test templates, provide feedback
- 📝 **Technical Writers** - Improve docs
- 🎨 **Designers** - Create UI/UX
- 🧪 **Testers** - Try templates, report issues

---

## License

Apache 2.0 - Open-source, forever. Use commercially, modify, distribute freely.

---

## Contact

**Sri Bolisetty**
- GitHub: [@KnightSri](https://github.com/KnightSri)
- Email: sri@rewindlearn.com
- Project: AI Generalist Capstone

---

**Built with ❤️ by educators and developers who believe knowledge should be accessible and actionable.**
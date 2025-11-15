# Rewind.Learn - Quick Reference Guide

**Last Updated:** November 2025

---

## 🎯 Project at a Glance

**What:** Template-driven framework for transforming session artifacts into structured deliverables  
**Why:** 80-90% of meeting knowledge trapped in recordings/transcripts  
**How:** YAML templates + LangChain/LangGraph + LLM processing  
**Timeline:** 8 weeks (MVP)  
**Status:** Week 1 starting 🔜

---

## 📝 Core Concepts

### Template-Driven Architecture
Templates define WHAT to process and HOW, not code. One framework, unlimited meeting types.

### LangGraph Workflow
State machine managing multi-stage LLM tasks with dependencies. Handles errors, retries, parallel execution.

### Cross-Session Intelligence (Optional)
Knowledge graph links concepts across sessions. Finds prerequisites, patterns, recurring issues.

---

## 🏗️ Key Components

| Component | Purpose | File |
|-----------|---------|------|
| **Template Engine** | Load & validate YAML | `src/rewindlearn/core/template.py` |
| **File Processors** | Parse transcripts/chat/slides | `src/rewindlearn/processors/` |
| **LangGraph Workflow** | Orchestrate LLM tasks | `src/rewindlearn/workflow/graph.py` |
| **LangChain Chains** | Individual LLM tasks | `src/rewindlearn/chains/` |
| **Output Builder** | Generate Markdown/PDF | `src/rewindlearn/output/` |
| **CLI** | Command-line interface | `src/rewindlearn/cli/main.py` |

---

## 🎬 Quick Start (When Complete)

```bash
# Install
pip install rewindlearn

# Configure
rewindlearn config set-provider claude --api-key $ANTHROPIC_API_KEY

# Process session
rewindlearn process \
  --template online-course \
  --transcript session-01.txt \
  --chat chat-01.json \
  --output study-guides/

# View results
ls study-guides/
```

---

## 📚 Primary Use Case: Online Course

**Input:**
- Transcript (3-hour lecture)
- Chat log (200 messages)
- Course context (name, session #)

**Processing:** 6 LangChain chains
1. Session summary
2. Concept timeline
3. Friction analysis
4. Coverage gaps
5. Learning resources
6. Action items

**Output:** 6 Markdown files  
**Time:** <3 minutes  
**Cost:** <$2.00

---

## 🏆 Success Criteria

**Functional:**
- ✅ Template system works (new types via YAML)
- ✅ Online course template generates quality output
- ✅ Processing <3 min per session
- ✅ Cost <$2.00 per session
- ✅ User ratings ≥8/10

**Technical:**
- ✅ LangGraph state management works
- ✅ Error handling & retries robust
- ✅ LangSmith tracking accurate
- ✅ Output quality consistent

---

## 📅 Timeline Milestones

| Phase | Dates | Deliverable |
|-------|-------|-------------|
| **Phase 1** | Weeks 1-2 | Template engine + file processors |
| **Phase 2** | Weeks 3-4 | LangChain/LangGraph integration |
| **Phase 3** | Weeks 5-6 | CLI + output generation |
| **Phase 4** | Week 7 | Knowledge graph (optional) |
| **Phase 5** | Week 8 | Testing, docs, demo |

---

## ⚡ Critical Path

**Must Complete:**
1. Template engine (Week 1-2)
2. File processors (Week 1-2)
3. LangGraph workflow (Week 3-4)
4. At least 3 of 6 chains working (Week 3-4)
5. Output generation (Week 5-6)
6. CLI basics (Week 5-6)

**Can Compress:**
- Knowledge graph (skip if behind)
- All 6 chains (minimum 3)
- PDF conversion (Markdown is enough)
- Advanced CLI features

**Cannot Drop:**
- Template engine
- File processors
- LangGraph orchestration
- Output generation
- Basic CLI

---

## 🔧 Tech Stack Quick Ref

```python
# Core framework
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langgraph.graph import StateGraph
from langsmith import traceable

# LLM providers
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

# Data validation
from pydantic import BaseModel, Field

# CLI
import typer
from rich.console import Console

# File processing
import yaml
from pathlib import Path
```

**Key Dependencies:**
- `langchain>=0.1.0` - LLM orchestration
- `langgraph>=0.0.20` - Workflow state
- `langsmith>=0.0.60` - Observability
- `pydantic>=2.0.0` - Data validation
- `typer>=0.9.0` - CLI framework
- `rich>=13.0.0` - Terminal UI
- `pyyaml>=6.0` - YAML parsing

---

## 📋 Must-Have vs Nice-to-Have

### Must Have (MVP)
- [x] Template engine
- [ ] File processors (transcript, chat)
- [ ] LangGraph workflow
- [ ] 3+ LangChain chains working
- [ ] Markdown output generation
- [ ] Basic CLI
- [ ] LangSmith integration
- [ ] Online course template complete

### Nice to Have (Post-MVP)
- [ ] All 6 chains
- [ ] PDF conversion
- [ ] Slide processing
- [ ] Video timestamp indexing
- [ ] Knowledge graph
- [ ] Second template (retrospective)
- [ ] Web UI
- [ ] Advanced CLI features

---

## 🚨 Risk Management

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| LangGraph complexity | Medium | Start simple, add features incrementally |
| LangChain API changes | Low | Pin versions, follow LTS releases |
| Prompt inconsistency | Medium | Use LangSmith for A/B testing |
| Processing cost overruns | Low | Track costs per task, optimize |
| Time overrun | Medium | Week 7 buffer, knowledge graph optional |

---

## 📦 Project Structure

```
rewindlearn/
├── src/rewindlearn/
│   ├── core/               # Template engine, models
│   ├── processors/         # File parsers
│   ├── workflow/           # LangGraph state machine
│   ├── chains/             # Individual LangChain chains
│   ├── output/             # Markdown → PDF/HTML
│   ├── cli/                # CLI commands
│   └── utils/              # Helpers
├── templates/              # Built-in templates
├── tests/                  # Test suite
├── examples/               # Sample data
└── docs/                   # Documentation
```

---

## 🎯 Demo Script (10 minutes)

**1. The Problem (2 min)**
- 80-90% of meeting knowledge unused
- Manual documentation unsustainable
- No vendor-neutral solution exists

**2. The Framework (3 min)**
- Show template YAML
- Explain: Same engine, different templates
- Framework is the product (lecture is proof)

**3. Live Demo (4 min)**
- Process lecture transcript
- Show generated deliverables
- Display cost tracking

**4. Vision (1 min)**
- Second template architecture (retrospective)
- Community template marketplace
- Open-source extensibility

---

## 🔍 Key Metrics to Track

**During Development:**
- Template validation pass rate
- LangChain chain success rate
- LangGraph task completion time
- Cost per session (target: <$2.00)
- Output quality scores

**At Demo:**
- Processing time (target: <3 min)
- User satisfaction (target: ≥8/10)
- Template extensibility (can create retro template in <1 week)
- Cost accuracy (vs actual API charges)

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `rewind-learn-PROJECT-OVERVIEW.md` | High-level summary |
| `rewind-learn-claude-code-task-list.md` | Implementation tasks |
| `rewind-learn-ARCHITECTURE.md` | Technical design |
| `rewind-learn-TEMPLATES.md` | Template specifications |
| `rewind-learn-QUICK-REFERENCE.md` | This file |

---

## 🤝 Comparison with LLM TaskBench

| Aspect | LLM TaskBench | Rewind.Learn |
|--------|---------------|--------------|
| **Core Concept** | Single evaluation workflow | Template-driven multi-workflow |
| **Complexity** | Medium | High |
| **Architecture** | Direct API calls | LangChain/LangGraph |
| **Primary Output** | Tables, CSV, JSON | Markdown → PDF/HTML |
| **Unique Feature** | LLM-as-judge | Template engine + Knowledge graph |
| **Extensibility** | Fixed workflow | Infinite via templates |

---

## 💡 Design Principles

1. **Template-First:** Framework works for ANY meeting type via config
2. **Privacy-First:** Self-hostable, no vendor lock-in
3. **Quality-Aware:** LangSmith tracking, prompt optimization
4. **Cost-Conscious:** Track every token, optimize per task
5. **User-Friendly:** YAML config, no coding required
6. **Open-Source:** Community can extend and contribute

---

## ⚙️ Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional (for alternative providers)
OPENAI_API_KEY=sk-...

# Optional (for knowledge graph)
SUPABASE_URL=https://...
SUPABASE_KEY=...

# Optional (for observability)
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=rewindlearn
```

---

## 🔗 Quick Links

**Project Resources:**
- Overview: `rewind-learn-PROJECT-OVERVIEW.md`
- Architecture: `ARCHITECTURE.md`
- Templates: `rewind-learn-TEMPLATES.md`
- Task List: `rewind-learn-claude-code-task-list.md`

**AI Viability:**
- Gemini Analysis: [Link](https://mvp.shalusri.com/rewind.learn/rewind.learn-analysis-gemini-2-5-pro-20251022/)
- Claude Analysis: [Link](https://mvp.shalusri.com/rewind.learn/rewind.learn-analysis-claude-sonnet-4-5-20251022/)

**External Tools:**
- LangChain: <https://langchain.com>
- LangGraph: <https://langchain-ai.github.io/langgraph/>
- LangSmith: <https://smith.langchain.com>
- Supabase: <https://supabase.com>

---

## 🎯 CLI Commands (When Complete)

```bash
# Configuration
rewindlearn config set-provider claude --api-key $KEY
rewindlearn config show

# Template management
rewindlearn template list
rewindlearn template validate online-course.yaml
rewindlearn template test online-course.yaml --sample data/

# Processing
rewindlearn process \
  --template online-course \
  --transcript session.txt \
  --chat chat.json \
  --output results/

# With options
rewindlearn process session/ \
  --template online-course \
  --watch \
  --format pdf \
  --language en

# History
rewindlearn history --last 10 --show-costs
```

---

## 🐛 Common Issues & Solutions

**Issue:** "Template validation failed"
- Check YAML syntax
- Verify all required fields present
- Check task dependencies aren't circular

**Issue:** "LangGraph task timeout"
- Increase timeout in config
- Check LLM API is responding
- Verify prompt isn't too long

**Issue:** "Output generation failed"
- Check Markdown is valid
- Verify WeasyPrint installed for PDF
- Check file permissions

**Issue:** "Cost higher than expected"
- Check temperature settings (higher = more tokens)
- Review prompt lengths
- Consider using cheaper models for simple tasks

---

## 📊 Template Quick Ref

**Online Course Template:**
- Inputs: transcript, chat, context
- Tasks: 6 chains (summary, timeline, friction, gaps, resources, actions)
- Outputs: 6 Markdown files
- Time: ~2-3 minutes
- Cost: ~$1.50

**Agile Retrospective Template (Future):**
- Inputs: transcript, chat, sprint context
- Tasks: 8 chains
- Outputs: 8 Markdown files + Jira import
- Time: ~3-4 minutes
- Cost: ~$2.00

---

## 🎯 Remember

**What Makes This Project Special:**
1. Template system enables infinite meeting types
2. Privacy-first, self-hostable architecture
3. Built on production-grade AI stack (LangChain/LangGraph)
4. Open-source and community-extensible
5. Solves real problem (80-90% knowledge waste)

**Keys to Success:**
- Template engine FIRST (everything depends on it)
- Start simple with LangGraph, add complexity
- Test each chain independently before orchestration
- Use LangSmith from day 1 (debugging is easier)
- Have backup plan (skip knowledge graph if behind)

---

**Ready to build! 🚀**

See `rewind-learn-claude-code-task-list.md` for detailed implementation tasks.
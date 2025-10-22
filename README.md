# Rewind.Learn

**Open-source, template-driven framework for transforming online session artifacts into structured knowledge.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Powered-green)](https://langchain.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 🎯 The Problem

Every online session—courses, team meetings, training workshops—generates valuable content: transcripts, chat logs, recordings, slides. Yet **80-90% of this knowledge remains trapped** in unwatched recordings and unread transcripts.

**Educators** spend 3-5 hours per session manually creating study guides.  
**Agile teams** lose 15-20% of retrospective insights to poor documentation.  
**Students** struggle to find specific concepts in 90-minute recordings.

---

## 💡 The Solution

**Rewind.Learn** automates the transformation of raw session data into structured, actionable deliverables using AI-powered templates:

- 📚 **Online courses** → Comprehensive study guides with concept timelines, confusion analysis, and curated resources
- 🔄 **Sprint retrospectives** → Action item registers, sentiment analysis, and pattern detection across sprints
- 🏥 **Medical reviews** → Case summaries, diagnostic pathways, and teaching points
- ⚖️ **Legal depositions** → Testimony timelines, key arguments, and evidence cataloging

**One framework. Infinite use cases.**

---

## ✨ Key Features

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

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (coming soon)
pip install rewindlearn

# Or install from source
git clone https://github.com/knightsri/rewind.learn.git
cd rewind.learn
pip install -e .
```

### Basic Usage

```bash
# Configure your LLM provider
rewindlearn config set-provider claude --api-key $ANTHROPIC_API_KEY

# Process a session with the online course template
rewindlearn process \
  --template online-course \
  --transcript session-transcript.txt \
  --chat chat-log.json \
  --output study-guides/

# View generated materials
ls study-guides/
# session-summary.md
# concept-timeline.md
# student-friction-analysis.md
# coverage-gaps.md
# learning-resources.md
# action-items.md
```

### Example Output

From a 2-hour AI Engineering course session:

**Input:**
- Transcript (15,000 words)
- Chat log (200 messages)
- Slide deck (optional)

**Output (generated in ~3 minutes):**
- 📄 Executive summary (key concepts, learning objectives)
- 📅 Concept timeline (5-10 min segments with video timestamps)
- ❓ Student confusion analysis (topics needing review)
- ✅ Coverage gap report (planned vs. actual topics)
- 🔗 Curated learning resources (papers, videos, tutorials)
- ✏️ Action items (homework, deadlines, exercises)

**Cost:** ~$1.50 per session  
**Time saved:** 3-5 hours of manual work

---

## 📚 Documentation

- **[Concept Document](docs/CONCEPT.md)** - Project vision and template system overview
- **[Architecture](docs/ARCHITECTURE.md)** - Technical design and LangChain integration
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute templates and code
- **[Template Specification](docs/TEMPLATES.md)** - How to create custom templates

### AI Viability Analyses
Independent AI assessments of project viability (both scored 7-9/10):
- [Gemini 2.5 Pro Analysis](https://mvp.shalusri.com/rewind.learn/rewind.learn-analysis-gemini-2-5-pro-20251022/)
- [Sonnet 4.5 Analysis](https://mvp.shalusri.com/rewind.learn/rewind.learn-analysis-claude-sonnet-4-5-20251022/)
- [Comparative Analysis](https://mvp.shalusri.com/rewind.learn/analysis_comparison.html)

---

## 🎨 Template System

Templates define how sessions are processed. Example structure:

```yaml
template_id: "online-course-v1"
name: "Online Course Session"
version: "1.0"

inputs:
  required:
    - transcript
    - chat_log
  optional:
    - slides
    - previous_session_summary

processing:
  tasks:
    - name: "session_summary"
      prompt_template: |
        Analyze this course session and create a comprehensive summary...
      llm_config:
        model: "claude-sonnet-4"
        temperature: 0.3
      dependencies: []
    
    - name: "concept_timeline"
      prompt_template: |
        Create a chronological timeline of concepts covered...
      llm_config:
        model: "claude-sonnet-4"
        temperature: 0.2
      dependencies: ["session_summary"]

outputs:
  deliverables:
    - session_summary
    - concept_timeline
    - friction_analysis
  formats:
    - markdown
    - pdf
```

**Current Templates:**
- ✅ Online Course Session
- 🚧 Agile Sprint Retrospective (in development)

**Community Templates (coming soon):**
- Medical Case Discussions
- Sales Training Sessions
- Design Critiques
- Legal Depositions

---

## 🏗️ Project Status

**Current Phase:** MVP Development (Weeks 1-8)

**Completed:**
- ✅ Project concept and architecture
- ✅ Template specification design
- ✅ AI viability validation (7-9/10 scores)
- ✅ Repository setup

**In Progress:**
- 🚧 Core template engine (Week 1-3)
- 🚧 LangChain/LangGraph integration
- 🚧 CLI implementation
- 🚧 Online course template (first working version)

**Next Steps:**
- 📋 Pilot with 5-7 real users (Weeks 8-12)
- 📋 Add Agile Retrospective template
- 📋 Knowledge graph for cross-session analysis
- 📋 Web UI and managed hosting option

---

## 🤝 Contributing

We welcome contributions! Whether you're:

- 👨‍💻 **Developers** - Help build the core engine, templates, or integrations
- 👨‍🏫 **Educators** - Share prompts, test templates, provide feedback
- 📝 **Technical Writers** - Improve documentation and guides
- 🎨 **Designers** - Create UI/UX for web interface
- 🧪 **Testers** - Try templates with your sessions, report issues

**Getting Started:**
1. Read the [Contributing Guide](CONTRIBUTING.md)
2. Check [open issues](https://github.com/knightsri/rewind.learn/issues)
3. Join discussions in [GitHub Discussions](https://github.com/knightsri/rewind.learn/discussions)

**Good First Issues:**
- Add support for new transcript formats (.vtt, .srt)
- Create templates for specific domains
- Improve error handling and user feedback
- Write tests for template validation

---

## 🛠️ Technology Stack

**Core Framework:**
- Python 3.10+
- LangChain (LLM orchestration)
- LangGraph (workflow management)
- LangSmith (observability)

**LLM Providers:**
- Anthropic Claude (primary)
- OpenAI GPT-4 (secondary)
- Ollama (local models)

**Data & Storage:**
- Supabase (pgvector for knowledge graph)
- Redis (caching)
- Local filesystem / S3

**CLI & Output:**
- Typer (CLI framework)
- Rich (terminal UI)
- WeasyPrint / Pandoc (PDF generation)

---

## 🎯 Use Cases

### Education
- **Bootcamps & Online Courses**: Auto-generate study guides after each lecture
- **University Courses**: Create searchable knowledge base across semester
- **Corporate Training**: Document training sessions for compliance and reference

### Agile Teams
- **Sprint Retrospectives**: Track action items, sentiment, recurring blockers
- **Planning Meetings**: Extract decisions, dependencies, risks
- **Standups**: Aggregate daily updates into sprint summaries

### Professional Services
- **Consulting**: Document client meetings, decisions, action items
- **Legal**: Deposition summaries, testimony analysis
- **Medical**: Case reviews, teaching rounds, clinical discussions

---

## 📊 Metrics & Success Criteria

**Target Outcomes:**
- ⏱️ Save 2-5 hours per session in manual documentation
- ⭐ User quality ratings ≥8/10
- 💰 Processing cost <$0.50 per session
- 📈 60%+ user retention after 10 sessions

**Measured via LangSmith:**
- Token usage and cost per task
- Output quality scores
- Processing latency
- Prompt effectiveness

---

## 🗺️ Roadmap

### MVP (Q4 2025)
- ✅ Core engine with template system
- ✅ CLI tool
- ✅ Online course template
- ✅ LangSmith integration
- 🚧 Pilot with 5-7 users

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

## 💬 Community & Support

- **GitHub Discussions**: [Ask questions, share templates](https://github.com/knightsri/rewind.learn/discussions)
- **Issues**: [Report bugs, request features](https://github.com/knightsri/rewind.learn/issues)
- **Email**: sri@rewindlearn.com (project maintainer)

---

## 📄 License

Apache 2.0 - See [LICENSE](LICENSE) for details.

Open-source, forever. Use commercially, modify, distribute freely.

---

## 🙏 Acknowledgments

Built with:
- [LangChain](https://langchain.com/) - LLM application framework
- [LangSmith](https://smith.langchain.com/) - Observability platform
- [Anthropic Claude](https://anthropic.com/) - Primary LLM provider
- [Supabase](https://supabase.com/) - Backend and vector storage

Inspired by the need to make online learning and collaborative sessions more effective.

---

## 🌟 Star History

If you find this project useful, please star it on GitHub! It helps others discover the project.

[![Star History Chart](https://api.star-history.com/svg?repos=knightsri/rewind.learn&type=Date)](https://star-history.com/#knightsri/rewind.learn&Date)

---

**Built with ❤️ by educators and developers who believe knowledge should be accessible and actionable.**
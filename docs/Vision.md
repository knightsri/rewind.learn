# **GAI: Rewind.Learn \- Project Vision Document**

## **1\. Introduction & Project Vision**

### **1.1. Project Name:**

**Rewind.Learn**

### **1.2. Project Goal:**

Build an open-source, template-driven framework that transforms **any type of online session** into structured, actionable deliverables through AI-powered workflows. The system is extensible—users define custom session types (lectures, retrospectives, sales calls, medical rounds, legal depositions) via configuration, not code. The capstone demonstrates this framework's viability through one fully-implemented use case: online course session processing.

### **1.3. Problem Statement:**

Every online meeting—courses, team retrospectives, client calls, medical reviews, legal depositions—generates valuable artifacts (transcripts, chat logs, recordings). Yet **80-90% of this knowledge is never used** because manual documentation is time-intensive and non-scalable.

**The gap:** No vendor-neutral framework exists for transforming meeting artifacts into structured deliverables. Organizations must either:

* Build custom solutions for each meeting type (expensive, non-reusable)  
* Use proprietary SaaS tools (vendor lock-in, privacy concerns, inflexible)  
* Continue manual documentation (unsustainable)

**Why platforms haven't solved this:** Zoom, Microsoft Teams, and Google Meet *should* build this natively—they have the data, the users, and the infrastructure. They haven't. This creates an opportunity for an open-source, extensible solution that works across platforms and meeting types.

### **1.4. Success Criteria:**

1. **Framework Viability**: Template system enables creation of new meeting types through YAML configuration (no code required)  
2. **MVP Quality**: Online course template generates study materials rated ≥8/10 by 5-7 pilot users  
3. **Processing Efficiency**: Complete workflow execution in \<3 minutes per session, cost \<$2.00  
4. **Extensibility Validation**: Second template (agile retrospective) implementable in \<1 week, proving framework reusability

---

## **2\. Target Audience & Learning Objectives (Covered by Course)**

### **2.1. Target Audience:**

Advanced Developers (as defined by the course).

### **2.2. Key Learning Objectives:**

This project demonstrates mastery of:

* **Agentic Workflow Orchestration**: Multi-stage LLM task coordination with conditional execution  
* **Framework Design**: Building extensible systems through declarative configuration  
* **LangGraph State Machines**: Managing complex workflow states and dependencies  
* **Template System Architecture**: Enabling non-developers to extend functionality  
* **Production AI Engineering**: LangSmith observability, cost tracking, error recovery, privacy-first design  
* **Real-World Problem Solving**: Addressing a genuine market gap with practical impact

---

## **3\. Core Generative AI Functionality**

### **3.1. Core Task:**

**Template-driven transformation of meeting artifacts into structured deliverables.** The framework ingests raw session data (transcript, chat, recordings), executes a user-defined workflow of LLM analysis tasks, and generates customized outputs specific to the meeting type.

**Key Innovation:** The same framework processes:

* **Online courses** → Study guides, timelines, confusion analysis  
* **Sprint retrospectives** → Action items, sentiment analysis, blocker patterns  
* **Sales calls** → Decision summaries, objections, next steps  
* **Medical rounds** → Case summaries, teaching points, diagnostic pathways  
* **Legal depositions** → Testimony timelines, key arguments, evidence catalogs

**MVP Demonstration:** Fully implements the online course template to prove framework viability. This is the "low-hanging fruit" because the project author has direct experience with educational sessions and can validate quality effectively.

### **3.2. Input Requirements:**

**Framework-Level Inputs (universal):**

* Session transcript (any format: VTT, SRT, JSON, plain text)  
* Chat log export (JSON or text)  
* Session metadata (configurable per template)

**Template-Specific Inputs (defined in YAML):**

* **Online course**: Previous session summaries, agenda, slides, Q\&A exports  
* **Retrospective**: Sprint metrics, previous action items, team velocity data  
* **Sales call**: CRM context, account history, product documentation  
* **Medical review**: Patient history, diagnostic imaging notes, prior cases

**Format Flexibility:** Framework supports any text-based input. Templates specify which inputs are required vs. optional.

### **3.3. Output Requirements:**

**Framework generates template-defined deliverables:**

**Example: Online Course Template**

* Session summary, concept timeline with timestamps, confusion analysis, coverage gaps, curated resources, action items, glossary updates

**Example: Agile Retrospective Template**

* Sprint summary, what went well/poorly analysis, action item register, team health indicators, pattern detection across sprints, recommended adjustments

**Example: Sales Call Template**

* Call summary, decision points, objections raised, competitive mentions, next steps, CRM update recommendations

**Output Formats:** Markdown (primary), PDF, HTML, JSON (for downstream integrations)

### **3.4. Key Features:**

* **Template Engine**: YAML-based workflow definitions for unlimited meeting types  
* **LangGraph Orchestration**: State machine managing multi-stage LLM task dependencies  
* **Cross-Session Intelligence**: Knowledge graph linking concepts/patterns across previous sessions  
* **Privacy-First Design**: Self-hostable, all data remains in user's infrastructure  
* **Multi-Provider Support**: Works with Anthropic Claude, OpenAI GPT, local Ollama models  
* **Cost Transparency**: Real-time token tracking and cost monitoring via LangSmith  
* **Extensibility**: New meeting types added through configuration, not code changes

---

## **4\. Model Selection**

### **4.1. Model Type(s):**

**Large Language Models (LLMs)** for text analysis, reasoning, and structured document generation. The framework is model-agnostic—templates specify which models to use per task, enabling cost-quality optimization.

### **4.2. Model Candidates:**

**Primary Generation Models:**

* Claude Sonnet 4 (Anthropic) \- Balanced performance for document generation  
* Claude Haiku 4 (Anthropic) \- Fast extraction tasks  
* GPT-4o (OpenAI) \- Alternative/cross-validation  
* GPT-4o-mini (OpenAI) \- Cost-efficient simple tasks

**Specialized Reasoning:**

* Claude Opus 4.1 \- Complex analysis requiring deep reasoning  
* GPT-4o \- Cross-validation and comparative assessment

**Local Deployment:**

* Ollama (Llama 3.3 70B) \- Privacy-sensitive environments, air-gapped systems

### **4.3. Selection Criteria & Choice:**

**Framework Default: Claude Sonnet 4**

* Strong structured document generation with consistent formatting  
* 200K token context window (handles long meeting transcripts)  
* Reliable API with good error handling  
* $3.00/M input, $15/M output (balanced cost-quality)

**Task-Specific Optimization:** Templates configure different models for different tasks:

* Simple extraction → Haiku 4 (speed, cost)  
* Complex reasoning → Opus 4.1 (quality)  
* Bulk processing → GPT-4o-mini (volume pricing)

**Multi-Provider Strategy:** Users can override model selection globally or per-task via template YAML, enabling cost optimization without code changes.

### **4.4. Fine-tuning/Customization Strategy:**

**No fine-tuning required.** Framework uses:

1. **Prompt Engineering**: Templates include detailed, task-specific prompts with examples  
2. **RAG for Cross-Session Context**: Vector database stores previous session summaries for prerequisite detection, pattern recognition  
3. **Few-Shot Learning**: Templates provide 2-3 examples per task type  
4. **Structured Output Schemas**: JSON constraints guide LLM responses

**Knowledge Graph Strategy:**

* Supabase pgvector stores embeddings of previous sessions  
* Semantic search finds related concepts across meetings  
* Enables: "Has this blocker appeared in previous retrospectives?" or "Did we cover prerequisites in earlier lectures?"

---

## **5\. Agent Design**

### **5.1. Need for Agents:**

**Yes, essential for complex workflow orchestration.** Requirements:

* **Multi-Stage Dependencies**: Some tasks must complete before others (e.g., generate summary before building timeline)  
* **Conditional Execution**: Skip optional tasks if inputs unavailable, adapt to failures  
* **State Persistence**: Track progress through 5-10+ LLM tasks, handle partial failures gracefully  
* **Dynamic Routing**: Different meeting templates require different task sequences  
* **Error Recovery**: Retry API failures, fallback to alternative models if primary unavailable

A simple sequential script cannot handle real-world variability in meeting artifacts and API reliability.

### **5.2. Agent Architecture:**

**LangGraph State Machine with Template-Driven Workflow**

**High-Level Pattern:**

```
INPUT VALIDATION:
- Parse all session artifacts
- Load template configuration
- Validate required inputs present

TASK EXECUTION (defined by template):
- Execute LLM tasks in dependency order
- Parallel execution where no dependencies exist
- Track tokens, costs, latency per task

ERROR RECOVERY:
- Retry failed tasks (3 attempts)
- Fallback to alternative models
- Continue workflow with partial results if critical tasks succeed

OUTPUT GENERATION:
- Assemble deliverables from task outputs
- Convert to requested formats (Markdown → PDF/HTML)
- Write to file system or return via API
```

**State Management:**

* Workflow tracks which tasks completed, which failed, which skipped  
* Stores generated content from each task  
* Accumulates tokens and costs  
* Maintains cross-session context from knowledge graph

**Memory Requirements:**

* Short-term: Current session data and task outputs  
* Long-term: Knowledge graph of previous sessions (vector embeddings)  
* Caching: Repeated analysis of common concepts

**Planning Mechanism:**

* Static workflow defined by template (DAG of tasks)  
* Dynamic routing based on input availability and task success/failure  
* Conditional branching (e.g., skip slide analysis if no slides provided)

### **5.3. Agent Frameworks/Libraries:**

**LangGraph for orchestration \+ LangChain for LLM integration \+ LangSmith for observability**

**Why LangGraph:**

* Purpose-built for stateful AI workflows with complex dependencies  
* Visual debugging via graph visualization  
* Built-in retry logic and conditional routing  
* Streaming support for real-time progress updates

**Why not alternatives:**

* Simple LangChain chains: Too linear, poor error handling  
* Prefect/Airflow: General workflow engines, not LLM-optimized  
* Custom implementation: Reinventing solved problems (state management, retries)

**Integration Benefits:**

* LangSmith provides built-in observability (token tracking, latency, cost)  
* LangChain provides prompt templates and structured output parsing  
* Unified ecosystem reduces integration complexity

---

## **6\. Tooling & Integration**

### **6.1. Required Tools:**

1. **LLM APIs**: Anthropic, OpenAI, Ollama (local)  
2. **Vector Database**: Supabase pgvector (cross-session knowledge graph)  
3. **Document Conversion**: Pandoc (Markdown → PDF/HTML/DOCX)  
4. **Transcript Parsers**: Support VTT, SRT, JSON, plain text  
5. **LangSmith**: Observability, token tracking, prompt optimization  
6. **Redis** (optional): Caching for repeated concept analysis

### **6.2. Tool Integration Mechanism:**

**Unified Interfaces:**

* Single abstraction for all LLM providers (switch via configuration)  
* Template system dynamically loads tools based on YAML specification  
* Error handling with automatic retry and fallback strategies

**Integration Patterns:**

* API wrappers with rate limiting and retry logic  
* Fallback chains (Claude → GPT-4 → Ollama if all else fails)  
* Tool registry enabling runtime discovery

### **6.3. Vector Database (If RAG/Memory):**

**Supabase with pgvector extension**

**Why Supabase:**

* Open-source, self-hostable (no vendor lock-in)  
* PostgreSQL foundation (familiar to developers)  
* pgvector for semantic search  
* REST API for easy Python integration

**Use Cases:**

* Store previous session summaries with embeddings  
* Semantic search: "Which sessions covered this topic?"  
* Pattern detection: "Has this issue appeared before?"  
* Prerequisite analysis: "What foundational concepts are students missing?"

**Alternative:** ChromaDB for simpler local-only deployments (no server required)

---

## **7\. API Strategy**

### **7.1. Consumed APIs:**

**LLM Providers:**

1. Anthropic Claude API \- Primary (various models: Opus, Sonnet, Haiku)  
2. OpenAI API \- Secondary/fallback (GPT-4o, GPT-4o-mini)  
3. Ollama \- Local deployment option (privacy-sensitive environments)

**Infrastructure:**

1. Supabase API \- Vector storage and knowledge graph  
2. LangSmith API \- Observability, token tracking, prompt versioning

**Rate Limit Strategy:** Framework respects API limits, implements queuing and backoff automatically

### **7.2. Exposed APIs (If Applicable):**

**No REST API in MVP** (CLI-only for capstone).

**Future Phase 2:**

* REST API for LMS integration (Canvas, Moodle, Blackboard)  
* Webhook support for automated processing (Zoom recording uploaded → auto-process)  
* Batch API for overnight multi-session processing

---

## **8\. Data Requirements & Handling**

### **8.1. Input/Training Data:**

**MVP Development:**

* 5-7 real lecture transcripts (100-200KB each, anonymized)  
* Corresponding chat logs and session metadata  
* Manual quality validation dataset

**No model training required** \- using pre-trained LLMs via API

**Pilot Phase:**

* 5-7 educators provide real course sessions for validation  
* Feedback collection for prompt refinement

### **8.2. Output Data Management:**

**Local file system storage** (self-hosted deployment):

* Organized by meeting type, session ID, timestamp  
* Generated deliverables in requested formats  
* Processing logs for debugging  
* Knowledge graph updates (vector embeddings)

**User Controls:**

* All data remains on user's infrastructure  
* No automatic deletion  
* Export capabilities (JSON, CSV)

### **8.3. Data Privacy & Security:**

**Privacy-First Architecture:**

* Self-hostable (no cloud dependency)  
* No telemetry sent to external services (except chosen LLM providers)  
* API keys via environment variables (never logged)  
* FERPA/COPPA/HIPAA considerations documented

**Security Measures:**

* Input validation (prevent injection)  
* Secure temporary file handling  
* API key rotation support  
* Audit logging of all LLM API calls

**For Sensitive Use Cases:**

* Local Ollama deployment option (complete air-gapping)  
* Anonymization helpers (Phase 2 feature)  
* Explicit documentation of data flows

---

## **9\. Testing**

### **9.1. Functional Testing:**

**Unit Tests:**

* Template parser (YAML validation)  
* Transcript format parsers  
* LLM API wrappers  
* Document generators  
* State management

**Integration Tests:**

* End-to-end workflow (transcript → deliverables)  
* Multi-provider fallback  
* RAG knowledge graph retrieval  
* Error recovery scenarios

**Target: 70% code coverage** (focusing on critical paths)

### **9.2. Performance Metrics:**

**Quality Validation:**

* User satisfaction: ≥8/10 ratings from pilot users  
* Accuracy: Manual verification of 20% of extracted concepts  
* Completeness: Coverage analysis matches manual review  
* Usefulness: Generated action items are actionable

**System Performance:**

* Speed: \<3 minutes for 2-hour session  
* Cost: \<$2.00 per session  
* Token efficiency: Tracked via LangSmith

### **9.3. Handling Edge Cases:**

**API Failures:**

* Multi-provider fallback (Claude → GPT-4 → Ollama)  
* 3 retries with exponential backoff  
* Partial success: Generate what's possible, flag gaps

**Invalid Inputs:**

* Missing transcript → Clear error message  
* Empty chat log → Skip related tasks, continue workflow  
* Invalid YAML → Fail fast with syntax details

**Unexpected Outputs:**

* Malformed responses → Retry with stricter prompts  
* Incomplete results → Flag for manual review  
* Hallucinated content → Validation where possible (URL checking)

---

## **10\. Deployment & Scalability (Conceptual)**

### **10.1. Deployment Plan:**

**Development:**

* Local Python 3.10+ environment  
* Docker Compose for Supabase  
* Virtual environment management

**Distribution:**

* Phase 1: GitHub repository with setup docs  
* Phase 2: PyPI package (`pip install rewindlearn`)  
* Phase 3: Docker image for one-command deployment

### **10.2. Scalability Thoughts:**

**Current Bottlenecks:**

* Sequential task execution (can be parallelized)  
* Single machine processing  
* API rate limits on free tiers

**Future Optimizations:**

* Parallel task execution (LangGraph supports concurrent nodes)  
* Cloud deployment options (Lambda, Cloud Run)  
* Queue system (Redis) for batch processing  
* Caching layer for repeated concept analysis

**Cost Scaling:**

* Current: \~$1.50 per session  
* Optimized (caching, smaller models): \~$0.80 per session  
* Enterprise (volume pricing): \~$0.30 per session

---

## **11\. Ethical Considerations & Responsible AI**

### **11.1. Potential Issues:**

1. **Content Accuracy**: AI-generated materials may contain errors or misinterpretations  
2. **Data Privacy**: Meeting transcripts may contain sensitive information sent to third-party APIs  
3. **Bias**: LLMs may favor certain perspectives, teaching styles, or sources  
4. **Over-Automation**: Users might skip manual review, trusting AI outputs blindly  
5. **Accessibility**: Generated materials may not be screen-reader friendly  
6. **Environmental Impact**: Processing many sessions has carbon footprint

### **11.2. Mitigation Strategies:**

**Content Quality:**

* Explicit disclaimers: "⚠️ AI-Generated: Review before distribution"  
* Confidence scoring for extracted information  
* Source attribution (timestamps, context)  
* Educator review workflow built into CLI

**Data Privacy:**

* Anonymization helpers (detect and replace PII)  
* Local-only mode (Ollama, no external APIs)  
* Privacy documentation (FERPA/HIPAA checklists)  
* Audit logging for compliance

**Bias Mitigation:**

* Multi-provider cross-validation (optional)  
* Resource diversity (multiple sources, open-access preference)  
* Teaching style neutrality (reflect content, don't prescribe methods)

**Over-Automation Prevention:**

* Built-in reflection prompts for reviewers  
* Transparency about limitations in generated content  
* Requirement for manual verification documented

**Accessibility:**

* Alt-text generation for diagrams (Phase 2\)  
* Semantic HTML with proper structure  
* Open-access resource preference

**Environmental Considerations:**

* Efficient model selection (use smallest sufficient model)  
* Caching to reduce redundant processing  
* Carbon footprint awareness (Phase 2: reporting)

---

## **12\. Technical Stack Summary**

### **12.1. Programming Languages:**

Python 3.10+

### **12.2. Key Libraries/Frameworks:**

LangChain, LangGraph, LangSmith, Typer, Pydantic, Rich, PyYAML, pandas

### **12.3. Models:**

Claude (Opus 4.1, Sonnet 4, Haiku 4), GPT-4o, GPT-4o-mini, Llama 3.3 70B (Ollama)

### **12.4. Databases/Vector Stores:**

Supabase (PostgreSQL \+ pgvector), Redis (optional caching)

### **12.5. Cloud Services:**

Anthropic API, OpenAI API, Supabase, LangSmith

---

## **13\. Assumptions & Constraints**

### **13.1. Assumptions:**

* API availability for Claude/GPT-4 remains stable  
* Transcripts are reasonably accurate (≥85% quality)  
* Users comfortable with CLI tools or willing to learn  
* Budget available for LLM API costs (\~$1-2 per session)  
* Pilot users available for validation

### **13.2. Constraints:**

* 8-week MVP development timeline  
* Single developer (all design/coding/testing)  
* LLM API testing budget: $100-150  
* MVP limited to one fully-implemented template (online course)  
* No production deployment (proof-of-concept only)  
* CLI interface only (no web UI)

---

## **14\. The Framework Vision: Infinite Possibilities**

**Core Insight:** The template system architecture enables processing of **any meeting type** through configuration, not code. While the MVP demonstrates online course processing (chosen because it's a "low-hanging fruit" with direct validation capability), the framework is designed for universal application.

**Potential Meeting Types:**

* Education: Lectures, bootcamps, training, certifications  
* Agile Teams: Retrospectives, planning, standups, demos  
* Sales: Client calls, discovery meetings, demos, objections  
* Medical: Case reviews, teaching rounds, tumor boards  
* Legal: Depositions, case strategy, client interviews  
* Consulting: Client meetings, deliverable reviews  
* Design: Critiques, stakeholder reviews, user testing  
* Executive: Town halls, board meetings, strategy sessions

**Why This Matters:** The same core engine processes radically different meeting types. A hospital can process medical rounds. A law firm can process depositions. A software team can process retrospectives. **All using the same framework, different templates.**

**Why Platforms Haven't Built This:** Zoom, Microsoft Teams, and Google Meet have the data, users, and infrastructure to build native meeting intelligence. They haven't. This gap creates the opportunity for an open-source, vendor-neutral solution that:

* Works across platforms (not locked to Zoom/Teams/Meet)  
* Is customizable (organizations control templates and data)  
* Is privacy-respecting (self-hostable, no vendor access)  
* Is extensible (community can contribute templates)

**The Framework is the Product:** Not the lecture template. The lecture template proves the framework works.

---

## **15\. Success Definition & Demo Readiness**

### **Project Success Criteria:**

1. ✅ **Framework Viability**: Template system enables new meeting types via YAML  
2. ✅ **MVP Quality**: Online course template generates ≥8/10 rated materials  
3. ✅ **Processing Efficiency**: \<3 minutes, \<$2.00 per session  
4. ✅ **Extensibility Proof**: Can implement second template (retrospective) in \<1 week

### **Demo Strategy (10 minutes):**

**Act 1: The Problem (2 min)**

* "80% of meeting knowledge trapped in recordings"  
* "Zoom/Teams should solve this—they haven't"  
* "No open-source framework exists"

**Act 2: The Framework (3 min)**

* Show template YAML defining workflow  
* Explain: Same engine, different templates, infinite meeting types  
* "Lecture is MVP demo—framework supports any meeting"

**Act 3: Live Demo (4 min)**

* Process real lecture transcript through CLI  
* Show generated study guide deliverables  
* Display cost/token tracking

**Act 4: Vision (1 min)**

* Second template (retrospective) architecture shown  
* Community template marketplace concept  
* Open-source extensibility path

**Backup Plan:** Pre-processed results, video walkthrough, static screenshots

---


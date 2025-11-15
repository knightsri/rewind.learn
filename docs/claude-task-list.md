# Rewind.Learn - Claude Code Implementation Task List

**Version:** 1.0  
**Target:** MVP completion by January 2026  
**Current Phase:** Ready for Phase 1 implementation  
**Execution Model:** Sequential implementation with validation at each milestone

---

## ⚡ CRITICAL INSTRUCTIONS FOR CLAUDE CODE

**How to use this task list:**

1. **Work sequentially** - Complete each task in order, as later tasks depend on earlier ones
2. **Validate at each step** - Don't move forward until validation criteria are met
3. **Test as you go** - Write unit tests alongside implementation
4. **Document decisions** - Add docstrings and comments explaining design choices
5. **Check dependencies** - Install required packages as needed via pip

**Success criteria for each task:**
- Code runs without errors
- Tests pass (if testing is specified)
- Validation criteria are met
- Type hints are present
- Docstrings are complete

---

## 📋 Project Context

You are building **Rewind.Learn**, an open-source, template-driven framework that transforms online session artifacts (transcripts, chat logs, recordings, slides) into structured deliverables through AI-powered workflows.

**Key Innovation:** One framework processes ANY meeting type through YAML templates, not code:
- **Online courses** → Study guides, concept timelines, confusion analysis
- **Sprint retrospectives** → Action items, sentiment analysis, blocker patterns
- **Sales calls** → Decision summaries, objections, next steps
- **Medical rounds** → Case summaries, teaching points
- **Legal depositions** → Testimony timelines, evidence catalogs

**MVP Focus:** Build the template engine and fully implement the online course template to prove framework viability.

**Core Difference from LLM TaskBench:** This project uses LangChain/LangGraph for workflow orchestration with state management, not just direct API calls.

---

## 🏗️ Project Structure Setup

**TASK 0: Initialize Project Structure**

Create the following directory structure:

```
rewindlearn/
├── src/
│   └── rewindlearn/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── template.py        # Template loader & validator
│       │   ├── models.py          # Pydantic models
│       │   └── config.py          # Configuration management
│       ├── processors/
│       │   ├── __init__.py
│       │   ├── transcript.py      # Transcript parser
│       │   ├── chat.py            # Chat log parser
│       │   ├── slides.py          # Slide processor (optional)
│       │   └── base.py            # Base processor class
│       ├── chains/
│       │   ├── __init__.py
│       │   ├── summary.py         # Session summary chain
│       │   ├── timeline.py        # Concept timeline chain
│       │   ├── friction.py        # Friction analysis chain
│       │   ├── gaps.py            # Coverage gaps chain
│       │   ├── resources.py       # Learning resources chain
│       │   └── actions.py         # Action items chain
│       ├── workflow/
│       │   ├── __init__.py
│       │   ├── graph.py           # LangGraph state machine
│       │   ├── state.py           # State definitions
│       │   └── nodes.py           # Graph node functions
│       ├── output/
│       │   ├── __init__.py
│       │   ├── markdown.py        # Markdown generator
│       │   ├── pdf.py             # PDF converter (optional)
│       │   └── builder.py         # Output builder
│       ├── knowledge_graph/       # Optional (Phase 4)
│       │   ├── __init__.py
│       │   ├── vector_store.py
│       │   └── search.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── main.py            # Typer CLI commands
│       └── utils/
│           ├── __init__.py
│           ├── logging.py         # Logging configuration
│           └── validation.py      # Input validation
├── templates/
│   ├── online-course-v1.yaml      # Built-in template
│   └── template-schema.yaml       # Template schema reference
├── tests/
│   ├── __init__.py
│   ├── test_template.py
│   ├── test_processors.py
│   ├── test_chains.py
│   ├── test_workflow.py
│   ├── test_output.py
│   └── fixtures/
│       ├── sample-transcript.txt
│       ├── sample-chat.json
│       └── sample-template.yaml
├── examples/
│   ├── sample-session/
│   │   ├── transcript.txt
│   │   └── chat.json
│   └── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── TEMPLATES.md
│   └── USAGE.md
├── .github/
│   └── workflows/
│       └── tests.yml
├── pyproject.toml
├── requirements.txt
├── README.md
├── LICENSE (Apache 2.0)
└── .gitignore
```

**Action Items:**
1. Create all directories and `__init__.py` files
2. Create empty placeholder files for each module
3. Create `.gitignore` with Python standard ignores plus:
   - `.env`
   - `*.yaml` in root (for local testing)
   - `results/` directory
   - `.pytest_cache/`
   - `__pycache__/`
   - `outputs/`

**Validation:**
- All directories exist
- All `__init__.py` files are present
- Can import `rewindlearn` package

---

## 📦 TASK 1: Setup Dependencies

**Goal:** Configure project dependencies and environment

**Action Items:**

1. **Create `requirements.txt`** with these dependencies:

Core Framework:
- `langchain>=0.1.0` - LLM orchestration
- `langgraph>=0.0.20` - Workflow state management
- `langsmith>=0.0.60` - Observability & prompt optimization
- `langchain-anthropic>=0.1.0` - Claude integration
- `langchain-openai>=0.0.5` - OpenAI integration

Data & Validation:
- `pydantic>=2.0.0` - Data validation
- `pyyaml>=6.0` - YAML parsing
- `python-dotenv>=1.0.0` - Environment variables

CLI & Output:
- `typer>=0.9.0` - CLI framework
- `rich>=13.0.0` - Beautiful terminal output

Testing:
- `pytest>=7.4.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support
- `pytest-cov>=4.1.0` - Coverage reporting

Optional (for advanced features):
- `supabase>=1.0.0` - Knowledge graph storage
- `weasyprint>=60.0` - PDF generation
- `pandas>=2.0.0` - Data manipulation

2. **Create `pyproject.toml`** with:
   - Project metadata (name, version, description, author)
   - Python version requirement: >=3.10
   - Entry point: `rewindlearn = rewindlearn.cli.main:app`
   - Build system: `setuptools`

3. **Create `.env.example`** file documenting required environment variables:
   - `ANTHROPIC_API_KEY=your_key_here`
   - `OPENAI_API_KEY=your_key_here` (optional)
   - `LANGSMITH_API_KEY=your_key_here` (optional)
   - `LANGSMITH_PROJECT=rewindlearn` (optional)
   - `SUPABASE_URL=https://...` (optional, for knowledge graph)
   - `SUPABASE_KEY=...` (optional, for knowledge graph)

**Validation:**
- `pip install -r requirements.txt` succeeds
- Can import all required packages
- `pip install -e .` makes `rewindlearn` command available

---

## 🎯 PHASE 1: Template Engine & File Processors (Weeks 1-2)

**Goal:** Load and validate templates, parse session artifacts  
**Target:** Can load templates and parse transcript/chat files

---

### MILESTONE 1.1: Pydantic Data Models (Days 1-2)

**Deliverable:** All core data structures defined with validation

---

#### TASK 1.1.1: Create Core Pydantic Models

**File:** `src/rewindlearn/core/models.py`

**Goal:** Define all core data structures using Pydantic for type safety and validation

**Requirements:**

Create the following Pydantic models with proper validation:

1. **TaskDefinition** - Individual LLM task within a template
   - Fields: name, prompt_template, llm_config, dependencies, output_key
   - llm_config includes: model, temperature, max_tokens, fallback_model
   - dependencies is a list of task names that must complete first

2. **TemplateConfig** - Complete template specification
   - Fields: template_id, name, version, description, inputs, processing, outputs
   - inputs: required (list), optional (list)
   - processing: tasks (list of TaskDefinition)
   - outputs: deliverables (list), formats (list), languages (list)

3. **SessionContext** - Metadata about the session being processed
   - Fields: session_id, session_type, course_name (optional), session_number (optional), date, metadata
   - metadata is a dict for flexible additional info

4. **ProcessedFile** - Represents a parsed input file
   - Fields: file_type, content, file_path, metadata, parsed_at
   - file_type: enum ('transcript', 'chat', 'slides', 'video')

5. **LangGraphState** - State passed through LangGraph workflow
   - Fields: session_context, input_files, intermediate_results, final_outputs, processing_status, errors, cost_tracking
   - intermediate_results is a dict mapping task names to outputs
   - processing_status: dict tracking which tasks completed
   - cost_tracking: dict with token counts and costs

6. **ChainResult** - Output from a single LangChain chain
   - Fields: task_name, content, tokens_used (input/output), cost, latency_ms, timestamp, success, error_message

7. **DeliverableOutput** - Final generated deliverable
   - Fields: deliverable_name, format, content, file_path, generated_at

**Design Considerations:**
- Use proper type hints for all fields
- Add comprehensive docstrings to each class
- Include example usage in docstrings
- Use Field() with descriptions for clarity
- Implement validators where needed (e.g., temperature 0-1)

**Testing:**
Write `tests/test_models.py` with:
- Test instantiation of each model with valid data
- Test validators catch invalid data
- Test optional fields work correctly
- Test model serialization to dict/JSON

**Validation Criteria:**
✓ All models instantiate with valid data
✓ Invalid data raises ValidationError
✓ Models serialize to JSON correctly
✓ Tests pass with 100% coverage of models.py

---

#### TASK 1.1.2: Create Configuration Management

**File:** `src/rewindlearn/core/config.py`

**Goal:** Manage application configuration and environment variables

**Requirements:**

Create a `Config` class with these methods:

1. **load_from_env() -> Config**
   - Load API keys from environment variables
   - Support .env file via python-dotenv
   - Provide clear error messages if required vars missing

2. **get_llm_provider_config(provider: str) -> dict**
   - Return configuration for specified LLM provider
   - Providers: 'anthropic', 'openai', 'ollama'
   - Include: API key, base URL, default model

3. **get_langsmith_config() -> dict or None**
   - Return LangSmith configuration if enabled
   - Include: API key, project name, tracing enabled flag

4. **validate() -> tuple[bool, List[str]]**
   - Check all required configuration is present
   - Return (is_valid, list_of_errors)

**Design Considerations:**
- Use Pydantic for config validation
- Support multiple LLM providers
- Make LangSmith optional
- Provide sensible defaults

**Testing:**
Write tests for:
- Loading from environment
- Validation catches missing keys
- Provider configs are correct

**Validation Criteria:**
✓ Config loads from environment
✓ Missing required vars raise clear errors
✓ All providers supported
✓ LangSmith config optional

---

### MILESTONE 1.2: Template Engine (Days 3-5)

**Deliverable:** Can load, validate, and parse YAML templates

---

#### TASK 1.2.1: Implement Template Loader

**File:** `src/rewindlearn/core/template.py`

**Goal:** Load YAML templates and convert to Python objects

**Requirements:**

Create a `TemplateLoader` class with these methods:

1. **load_from_yaml(yaml_path: str) -> TemplateConfig**
   - Load YAML file
   - Parse into TemplateConfig Pydantic model
   - Handle file not found errors gracefully
   - Validate YAML structure before parsing
   - Return helpful error messages for malformed YAML

2. **load_builtin_template(template_name: str) -> TemplateConfig**
   - Load template from `templates/` directory
   - Support: 'online-course-v1'
   - Raise error if template not found

3. **list_builtin_templates() -> List[dict]**
   - Return list of available built-in templates
   - Each dict has: template_id, name, description

**Design Considerations:**
- Use pathlib.Path for file operations
- Provide clear error messages with file names and line numbers
- Log template loading for debugging
- Handle edge cases (empty files, malformed YAML, missing fields)

**Testing:**
Write `tests/test_template.py` with:
- Test loading valid YAML file
- Test loading invalid YAML raises proper errors
- Test loading built-in template
- Test list_builtin_templates returns correct data
- Test error messages are helpful

**Test Fixtures:**
Create `tests/fixtures/sample-template.yaml` - a valid minimal template

**Validation Criteria:**
✓ Can load valid YAML without errors
✓ Invalid YAML produces helpful error messages
✓ Built-in template loads correctly
✓ List function works
✓ Tests pass with >80% coverage

---

#### TASK 1.2.2: Implement Template Validator

**File:** `src/rewindlearn/core/template.py` (extend)

**Goal:** Validate templates for correctness and completeness

**Requirements:**

Add to `TemplateLoader` class:

1. **validate_template(template: TemplateConfig) -> tuple[bool, List[str]]**
   - Check all required fields present
   - Validate task dependencies are valid (no circular deps, all referenced tasks exist)
   - Validate LLM configs (model exists, temperature 0-1, max_tokens >0)
   - Validate output deliverables match task output_keys
   - Return (is_valid, list_of_errors)

2. **check_circular_dependencies(tasks: List[TaskDefinition]) -> tuple[bool, List[str]]**
   - Build dependency graph
   - Detect cycles using topological sort or DFS
   - Return (has_cycles, list_of_cycles)

3. **validate_llm_config(llm_config: dict) -> tuple[bool, List[str]]**
   - Check model name is valid
   - Check temperature is 0-1
   - Check max_tokens is positive
   - Return (is_valid, list_of_errors)

**Design Considerations:**
- Provide specific, actionable error messages
- Include line numbers or field paths in errors
- Validate early to catch issues before processing
- Log validation steps for debugging

**Testing:**
Write tests for:
- Valid template passes validation
- Missing required fields detected
- Circular dependencies detected
- Invalid LLM configs detected
- Error messages are clear and specific

**Validation Criteria:**
✓ All validation checks work correctly
✓ Circular dependency detection works
✓ Error messages are specific and helpful
✓ Tests cover all validation scenarios

---

#### TASK 1.2.3: Create Online Course Template YAML

**File:** `templates/online-course-v1.yaml`

**Goal:** Create the primary built-in template for online course sessions

**Requirements:**

Create a complete YAML template file with:

**Structure:**
```yaml
template_id: "online-course-v1"
name: "Online Course Session"
version: "1.0"
description: "Process online course sessions into comprehensive study materials"

inputs:
  required:
    - transcript
    - chat_log
    - session_context
  optional:
    - slides
    - previous_session_summary
    - agenda

processing:
  tasks:
    - name: "session_summary"
      prompt_template: |
        [Detailed prompt from TEMPLATES.md]
      llm_config:
        model: "claude-sonnet-4"
        temperature: 0.3
        max_tokens: 4000
      dependencies: []
      output_key: "session_summary"
    
    - name: "concept_timeline"
      prompt_template: |
        [Detailed prompt from TEMPLATES.md]
      llm_config:
        model: "claude-sonnet-4"
        temperature: 0.2
        max_tokens: 5000
      dependencies: ["session_summary"]
      output_key: "concept_timeline"
    
    # Add all 6 tasks from TEMPLATES.md

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
  languages:
    - en
```

Include all 6 tasks with complete prompts from the TEMPLATES.md specification.

**Validation Criteria:**
✓ YAML is valid and parsable
✓ Loads successfully with TemplateLoader
✓ Passes all Template Validator checks
✓ All 6 tasks are defined with complete prompts
✓ Dependencies are correct

---

### MILESTONE 1.3: File Processors (Days 6-8)

**Deliverable:** Can parse transcript and chat log files

---

#### TASK 1.3.1: Create Base Processor Class

**File:** `src/rewindlearn/processors/base.py`

**Goal:** Define interface for all file processors

**Requirements:**

Create an abstract `BaseProcessor` class with:

1. **Abstract method: parse(file_path: str) -> ProcessedFile**
   - Load file from disk
   - Parse contents into structured format
   - Return ProcessedFile object

2. **Abstract method: validate(file_path: str) -> tuple[bool, List[str]]**
   - Check file exists
   - Check file format is correct
   - Return (is_valid, list_of_errors)

3. **Concrete method: _read_file(file_path: str) -> str**
   - Read file contents
   - Handle encoding issues
   - Provide helpful errors

**Design Considerations:**
- Use ABC (Abstract Base Class)
- Handle common file operations in base class
- Let subclasses implement format-specific parsing
- Provide good error messages

**Testing:**
Write tests for:
- Base class cannot be instantiated
- _read_file works correctly
- File not found handled gracefully

**Validation Criteria:**
✓ Abstract base class defined correctly
✓ Common file operations work
✓ Subclasses must implement abstract methods

---

#### TASK 1.3.2: Implement Transcript Processor

**File:** `src/rewindlearn/processors/transcript.py`

**Goal:** Parse transcript files into structured format

**Requirements:**

Create `TranscriptProcessor(BaseProcessor)` class with:

1. **parse(file_path: str) -> ProcessedFile**
   - Support formats: .txt (plain text), .vtt (WebVTT), .srt (SubRip)
   - Extract text content
   - Extract timestamps if present
   - Detect format automatically
   - Return ProcessedFile with parsed content

2. **_parse_vtt(content: str) -> dict**
   - Parse WebVTT format
   - Extract: timestamps, speaker labels (if present), text
   - Return structured dict

3. **_parse_srt(content: str) -> dict**
   - Parse SubRip format
   - Extract: timestamps, text
   - Return structured dict

4. **_parse_plain_text(content: str) -> dict**
   - Handle plain text without timestamps
   - Return structured dict (text only)

**Design Considerations:**
- Auto-detect format from file extension or content
- Handle malformed files gracefully
- Preserve timestamps for later use
- Clean up common transcript artifacts (repeated words, filler sounds)

**Testing:**
Write `tests/test_processors.py` with:
- Test parsing each format (.txt, .vtt, .srt)
- Test timestamp extraction
- Test malformed files
- Test auto-detection

**Test Fixtures:**
Create `tests/fixtures/sample-transcript.txt` and variations

**Validation Criteria:**
✓ All 3 formats parse correctly
✓ Timestamps extracted when present
✓ Malformed files handled gracefully
✓ Auto-detection works

---

#### TASK 1.3.3: Implement Chat Log Processor

**File:** `src/rewindlearn/processors/chat.py`

**Goal:** Parse chat log files into structured format

**Requirements:**

Create `ChatProcessor(BaseProcessor)` class with:

1. **parse(file_path: str) -> ProcessedFile**
   - Support formats: .json (structured), .txt (plain text)
   - Extract: messages, timestamps, participants, message content
   - Handle both Zoom format and generic formats
   - Return ProcessedFile with parsed content

2. **_parse_json_chat(content: str) -> list[dict]**
   - Parse JSON chat log
   - Expected structure: list of message objects
   - Each message: {timestamp, sender, content}
   - Handle variations in JSON structure

3. **_parse_text_chat(content: str) -> list[dict]**
   - Parse plain text chat format
   - Detect common patterns: "[HH:MM:SS] Name: Message"
   - Extract messages into structured format

**Design Considerations:**
- Handle both structured (JSON) and unstructured (text) formats
- Extract metadata: participant names, timestamps, thread structure
- Clean up common chat artifacts (emojis, reactions, system messages)
- Support Zoom, Teams, and generic chat exports

**Testing:**
Write tests for:
- JSON format parsing
- Text format parsing
- Message extraction
- Timestamp parsing
- Participant extraction

**Test Fixtures:**
Create `tests/fixtures/sample-chat.json` and .txt version

**Validation Criteria:**
✓ JSON and text formats parse correctly
✓ Messages, timestamps, participants extracted
✓ Different chat export formats handled
✓ Tests pass with >80% coverage

---

## 🎯 PHASE 2: LangChain Chains & LangGraph Workflow (Weeks 3-4)

**Goal:** Implement individual LLM chains and orchestrate them with LangGraph  
**Target:** Can execute 3+ chains in correct order with state management

---

### MILESTONE 2.1: LangChain Chains (Days 9-12)

**Deliverable:** At least 3 of 6 LangChain chains working

---

#### TASK 2.1.1: Implement Session Summary Chain

**File:** `src/rewindlearn/chains/summary.py`

**Goal:** Create LangChain for generating session summaries

**Requirements:**

Create a `SummaryChain` class with:

1. **__init__(config: Config, langsmith_enabled: bool = False)**
   - Initialize LLM (Claude Sonnet 4 via LangChain)
   - Set up prompt template
   - Configure LangSmith tracing if enabled

2. **async run(transcript: str, session_context: SessionContext) -> ChainResult**
   - Build prompt from template and inputs
   - Execute LLM call via LangChain
   - Parse response
   - Track tokens and cost
   - Return ChainResult

3. **_build_prompt(transcript: str, session_context: SessionContext) -> str**
   - Substitute variables in prompt template
   - Include transcript and context
   - Return complete prompt

**Design Considerations:**
- Use LangChain's `PromptTemplate` for templating
- Use LangChain's `LLMChain` for execution
- Use `@traceable` decorator from LangSmith
- Handle API errors and retries
- Track exact token usage from response

**Example Implementation Pattern:**
```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_anthropic import ChatAnthropic
from langsmith import traceable

class SummaryChain:
    def __init__(self, config: Config, langsmith_enabled: bool = False):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4",
            temperature=0.3,
            anthropic_api_key=config.get_llm_provider_config('anthropic')['api_key']
        )
        
        self.prompt = PromptTemplate(
            template="...",  # From template YAML
            input_variables=["transcript", "course_name", "session_number"]
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    @traceable(name="session_summary_chain")
    async def run(self, transcript: str, session_context: SessionContext) -> ChainResult:
        # Implementation
        pass
```

**Testing:**
Write `tests/test_chains.py` with:
- Mock LLM responses
- Test prompt building
- Test successful execution
- Test error handling
- Verify ChainResult is complete

**Validation Criteria:**
✓ Chain executes successfully with mock
✓ Prompt substitution works correctly
✓ Tokens and cost tracked accurately
✓ Error handling works
✓ LangSmith tracing works (if enabled)

---

#### TASK 2.1.2: Implement Concept Timeline Chain

**File:** `src/rewindlearn/chains/timeline.py`

**Goal:** Create LangChain for generating concept timelines

**Requirements:**

Create a `TimelineChain` class with same structure as SummaryChain:

1. **__init__(config: Config, langsmith_enabled: bool = False)**
   - Initialize LLM
   - Load prompt template (temperature=0.2 for precision)

2. **async run(transcript: str, session_summary: str, session_context: SessionContext) -> ChainResult**
   - Build prompt including summary (dependency)
   - Execute chain
   - Parse timeline from response
   - Return ChainResult

**Design Considerations:**
- Requires session_summary as input (dependency)
- Lower temperature (0.2) for precise timestamp extraction
- Validate timeline format in response
- Handle missing timestamps gracefully

**Testing:**
Write tests for:
- Chain execution with dependencies
- Timeline format validation
- Timestamp extraction

**Validation Criteria:**
✓ Chain requires summary input
✓ Timeline generated correctly
✓ Timestamps are accurate
✓ Tests pass

---

#### TASK 2.1.3: Implement Friction Analysis Chain

**File:** `src/rewindlearn/chains/friction.py`

**Goal:** Create LangChain for analyzing student confusion

**Requirements:**

Create a `FrictionChain` class:

1. **async run(chat_log: str, session_summary: str, session_context: SessionContext) -> ChainResult**
   - Analyze chat log for confusion indicators
   - Use GPT-4o (good at sentiment/friction detection)
   - Return analysis

**Design Considerations:**
- Use different model (GPT-4o) for variety
- Higher temperature (0.4) for nuanced analysis
- Extract specific examples from chat

**Testing:**
Write tests for:
- Chat log analysis
- Confusion detection
- Example extraction

**Validation Criteria:**
✓ Chain detects confusion correctly
✓ Examples extracted from chat
✓ GPT-4o integration works

---

#### TASK 2.1.4: Placeholder Chains for Remaining Tasks

**Files:** `src/rewindlearn/chains/gaps.py`, `resources.py`, `actions.py`

**Goal:** Create placeholder implementations for remaining 3 chains

**Requirements:**

For each remaining chain:

1. **Create basic class structure**
   - Follow same pattern as above
   - Use appropriate prompts from template
   - Set correct temperature

2. **Implement minimal functionality**
   - Can execute without errors
   - Returns placeholder ChainResult
   - TODO comments for full implementation

**Note:** Full implementation can be done later. For MVP, having 3 working chains (summary, timeline, friction) is sufficient to prove the framework.

**Validation Criteria:**
✓ All 6 chain files exist
✓ 3 chains fully functional
✓ 3 chains have placeholders
✓ No import errors

---

### MILESTONE 2.2: LangGraph Workflow (Days 13-16)

**Deliverable:** LangGraph state machine orchestrates chains with dependencies

---

#### TASK 2.2.1: Define LangGraph State

**File:** `src/rewindlearn/workflow/state.py`

**Goal:** Define state structure for LangGraph workflow

**Requirements:**

Create state definition using TypedDict:

```python
from typing import TypedDict, List, Dict, Optional

class SessionState(TypedDict):
    # Inputs
    transcript: str
    chat_log: str
    session_context: dict
    
    # Intermediate results (task outputs)
    session_summary: Optional[str]
    concept_timeline: Optional[str]
    friction_analysis: Optional[str]
    coverage_gaps: Optional[str]
    learning_resources: Optional[str]
    action_items: Optional[str]
    
    # Metadata
    processing_status: Dict[str, bool]  # {task_name: completed}
    errors: List[str]
    cost_tracking: Dict[str, float]  # {task_name: cost}
    quality_scores: Dict[str, int]  # Optional quality metrics
```

**Design Considerations:**
- State must be serializable (for LangGraph)
- Use Optional for intermediate results
- Track which tasks completed
- Accumulate errors without stopping workflow
- Track costs per task

**Validation Criteria:**
✓ State definition is complete
✓ All fields properly typed
✓ Can be instantiated and serialized

---

#### TASK 2.2.2: Create LangGraph Node Functions

**File:** `src/rewindlearn/workflow/nodes.py`

**Goal:** Create node functions for LangGraph workflow

**Requirements:**

Create node functions for each task:

1. **async summary_node(state: SessionState) -> SessionState**
   - Extract inputs from state
   - Execute SummaryChain
   - Update state with results
   - Update processing_status and cost_tracking
   - Handle errors gracefully
   - Return updated state

2. **async timeline_node(state: SessionState) -> SessionState**
   - Check dependency (summary must be complete)
   - Execute TimelineChain
   - Update state
   - Return updated state

3. **async friction_node(state: SessionState) -> SessionState**
   - Execute FrictionChain
   - Update state
   - Return updated state

4. **Placeholder nodes for remaining tasks**
   - gaps_node, resources_node, actions_node
   - Basic structure, can return state unchanged for now

**Design Considerations:**
- Each node is an async function
- Nodes receive state, return updated state
- Nodes should be idempotent (can run multiple times)
- Handle missing dependencies gracefully
- Log progress for debugging

**Testing:**
Write `tests/test_workflow.py` with:
- Test each node function
- Mock chain execution
- Test state updates
- Test error handling

**Validation Criteria:**
✓ All node functions defined
✓ State updates correctly
✓ Dependencies checked
✓ Errors handled without crashing

---

#### TASK 2.2.3: Build LangGraph State Machine

**File:** `src/rewindlearn/workflow/graph.py`

**Goal:** Create LangGraph workflow that orchestrates all chains

**Requirements:**

Create a `WorkflowGraph` class with:

1. **__init__(config: Config, langsmith_enabled: bool = False)**
   - Initialize all chains
   - Build LangGraph StateGraph
   - Define nodes and edges
   - Set up conditional routing

2. **build_graph() -> StateGraph**
   - Create StateGraph with SessionState
   - Add nodes for each task
   - Add edges defining dependencies:
     - START → summary_node, actions_node (no dependencies, run in parallel)
     - summary_node → timeline_node, friction_node, gaps_node
     - All tasks → aggregate_node
     - aggregate_node → END
   - Return compiled graph

3. **async execute(transcript: str, chat_log: str, session_context: SessionContext) -> SessionState**
   - Initialize state with inputs
   - Execute graph
   - Return final state with all results

**LangGraph Structure:**
```python
from langgraph.graph import StateGraph, END

class WorkflowGraph:
    def build_graph(self) -> StateGraph:
        graph = StateGraph(SessionState)
        
        # Add nodes
        graph.add_node("summary", summary_node)
        graph.add_node("timeline", timeline_node)
        graph.add_node("friction", friction_node)
        # ... more nodes
        
        # Add edges (dependencies)
        graph.set_entry_point("summary")  # Start here
        graph.add_edge("summary", "timeline")  # Timeline depends on summary
        graph.add_edge("summary", "friction")  # Friction depends on summary
        # ... more edges
        
        graph.set_finish_point("aggregate")  # End here
        
        return graph.compile()
```

**Design Considerations:**
- Parallel execution where possible (no dependencies)
- Clear dependency chain for dependent tasks
- Aggregate results at the end
- Handle partial failures (some tasks fail, others continue)
- LangSmith tracing for entire graph

**Testing:**
Write tests for:
- Graph builds correctly
- Execution completes successfully
- Dependencies respected (timeline waits for summary)
- Partial failures handled
- State accumulates all results

**Validation Criteria:**
✓ Graph builds without errors
✓ Execution completes end-to-end
✓ Dependencies work correctly
✓ Results accumulated in state
✓ LangSmith shows full trace

---

## 🎯 PHASE 3: CLI & Output Generation (Weeks 5-6)

**Goal:** Create CLI and generate final deliverables  
**Target:** Can process session end-to-end via CLI

---

### MILESTONE 3.1: Output Generation (Days 17-19)

**Deliverable:** Can generate Markdown deliverables from chain outputs

---

#### TASK 3.1.1: Implement Markdown Generator

**File:** `src/rewindlearn/output/markdown.py`

**Goal:** Generate well-formatted Markdown files from chain outputs

**Requirements:**

Create a `MarkdownGenerator` class with:

1. **generate_deliverable(task_name: str, content: str, session_context: SessionContext) -> str**
   - Add frontmatter (YAML metadata)
   - Add title and headers
   - Format content appropriately
   - Return complete Markdown string

2. **generate_all_deliverables(state: SessionState, template: TemplateConfig) -> Dict[str, str]**
   - Generate Markdown for each deliverable defined in template
   - Return dict: {deliverable_name: markdown_content}

3. **_add_frontmatter(content: str, metadata: dict) -> str**
   - Add YAML frontmatter to Markdown
   - Include: session info, generated date, template version

**Design Considerations:**
- Use consistent formatting
- Add table of contents if content is long
- Include metadata for reference
- Ensure Markdown is valid

**Testing:**
Write tests for:
- Markdown generation
- Frontmatter inclusion
- Formatting correctness

**Validation Criteria:**
✓ Markdown is well-formatted
✓ Frontmatter included
✓ All deliverables generated

---

#### TASK 3.1.2: Implement Output Builder

**File:** `src/rewindlearn/output/builder.py`

**Goal:** Coordinate output generation and file writing

**Requirements:**

Create an `OutputBuilder` class with:

1. **build_outputs(state: SessionState, template: TemplateConfig, output_dir: Path) -> List[DeliverableOutput]**
   - Generate Markdown for all deliverables
   - Write files to output directory
   - Name files according to template convention
   - Return list of DeliverableOutput objects

2. **_create_filename(deliverable_name: str, session_context: SessionContext, format: str) -> str**
   - Generate filename from template pattern
   - Pattern: `{course_name}-session-{session_number}-{deliverable}.{format}`
   - Handle special characters in names

3. **write_file(content: str, file_path: Path)**
   - Write content to file
   - Create parent directories if needed
   - Handle write errors gracefully

**Design Considerations:**
- Create output directory if it doesn't exist
- Use safe filenames (no special characters)
- Provide progress feedback
- Log all file writes

**Testing:**
Write tests for:
- File creation
- Filename generation
- Directory creation
- Write errors handled

**Validation Criteria:**
✓ All deliverables written to files
✓ Filenames are correct
✓ Directory structure created
✓ Tests pass

---

### MILESTONE 3.2: CLI Implementation (Days 20-24)

**Deliverable:** Working CLI with all core commands

---

#### TASK 3.2.1: Implement CLI Framework

**File:** `src/rewindlearn/cli/main.py`

**Goal:** Create Typer-based CLI with core commands

**Requirements:**

Create CLI app with these commands:

1. **config set-provider <provider> --api-key <key>**
   - Set LLM provider configuration
   - Providers: claude, openai, ollama
   - Save to .env or config file

2. **config show**
   - Display current configuration
   - Mask API keys (show first 8 chars only)

3. **template list**
   - List all available templates (built-in)
   - Show: template_id, name, description

4. **template validate <template_path>**
   - Validate template YAML
   - Show errors if invalid
   - Exit 0 if valid, 1 if invalid

5. **process <session_dir> --template <template_id> --output <output_dir>**
   - Process session using specified template
   - session_dir contains: transcript, chat, etc.
   - Display progress with Rich
   - Show real-time cost tracking
   - Write outputs to output_dir

**Design:**
- Use Typer for CLI framework
- Use Rich for beautiful output
- Add --verbose flag for detailed logging
- Provide helpful error messages

**Example Usage:**
```bash
# Configure
rewindlearn config set-provider claude --api-key sk-ant-...

# Process session
rewindlearn process examples/sample-session/ \
  --template online-course-v1 \
  --output results/

# Validate template
rewindlearn template validate my-template.yaml
```

**Testing:**
- Use Typer's testing utilities
- Test each command
- Test error cases
- Verify output format

**Validation Criteria:**
✓ All commands work
✓ Help text is clear
✓ Errors are user-friendly
✓ Progress display works

---

#### TASK 3.2.2: Implement Progress Tracking

**File:** `src/rewindlearn/cli/main.py` (extend)

**Goal:** Show real-time progress during processing

**Requirements:**

Add progress tracking to `process` command:

1. **Use Rich Progress for display**
   - Show: Current task, Status, Tokens, Cost
   - Update in real-time as tasks complete
   - Final summary table

**Display Example:**
```
Processing session...
├─ ✓ Session summary (982 tokens, $0.25) - 12s
├─ ✓ Concept timeline (1,245 tokens, $0.31) - 18s
├─ ✓ Friction analysis (734 tokens, $0.18) - 9s
├─ � Coverage gaps (456 tokens, $0.11) - 7s
├─ ... Learning resources (running)
└─ ⏳ Action items (pending)

Total: 3,417 tokens, $0.85, 46s elapsed
```

**Design Considerations:**
- Update progress as each node completes
- Show running cost total
- Indicate which tasks are parallel
- Show final summary

**Validation Criteria:**
✓ Progress displays in real-time
✓ Costs are accurate
✓ Final summary is complete

---

## 🎯 PHASE 4: Knowledge Graph (Week 7) - OPTIONAL

**Goal:** Cross-session intelligence via vector storage  
**Target:** Can link concepts across sessions

**NOTE:** This phase is optional for MVP. Skip if behind schedule.

---

### MILESTONE 4.1: Vector Storage (Days 25-28)

**Deliverable:** Can store and search session concepts

---

#### TASK 4.1.1: Implement Supabase Vector Store

**File:** `src/rewindlearn/knowledge_graph/vector_store.py`

**Goal:** Store session summaries as embeddings

**Requirements:**

Create a `VectorStore` class with:

1. **store_session(session_id: str, summary: str, concepts: List[str], metadata: dict)**
   - Generate embeddings for summary
   - Store in Supabase pgvector
   - Include metadata

2. **search_similar_sessions(query: str, limit: int = 5) -> List[dict]**
   - Generate embedding for query
   - Search for similar sessions
   - Return top matches with metadata

3. **find_prerequisites(concepts: List[str]) -> List[dict]**
   - Find previous sessions covering these concepts
   - Return sessions in chronological order

**Design Considerations:**
- Use OpenAI embeddings API
- Store in Supabase with pgvector extension
- Include session metadata for context

**Testing:**
Write tests for:
- Storage works
- Search returns relevant results
- Prerequisites found correctly

**Validation Criteria:**
✓ Sessions stored successfully
✓ Search works
✓ Prerequisites detected

---

## 🎯 PHASE 5: Testing, Documentation, Demo (Week 8)

**Goal:** Polish for demo  
**Target:** Professional presentation quality

---

### MILESTONE 5.1: Comprehensive Testing (Days 29-32)

**Goal:** Achieve >80% test coverage

---

#### TASK 5.1.1: Complete Unit Tests

**Requirements:**

Ensure all modules have tests:

1. **Core modules:** >90% coverage
   - models.py, template.py, config.py

2. **Processors:** >80% coverage
   - transcript.py, chat.py

3. **Chains:** >80% coverage
   - At least 3 chains fully tested

4. **Workflow:** >80% coverage
   - State, nodes, graph

5. **Output:** >80% coverage
   - Markdown, builder

6. **CLI:** >70% coverage
   - Commands work, errors handled

**Commands:**
```bash
# Run all tests
pytest

# With coverage
pytest --cov=rewindlearn --cov-report=html

# Specific module
pytest tests/test_chains.py -v
```

**Validation Criteria:**
✓ All tests pass
✓ Coverage >80%
✓ No flaky tests
✓ Edge cases covered

---

#### TASK 5.1.2: Integration Testing

**Requirements:**

Create end-to-end tests:

1. **test_e2e_processing.py**
   - Load real template
   - Process sample session
   - Verify outputs generated
   - Check cost tracking

2. **test_e2e_cli.py**
   - Test full CLI workflow
   - Verify file outputs
   - Check error handling

**Validation Criteria:**
✓ E2E tests pass
✓ Full workflow works
✓ Outputs are correct

---

### MILESTONE 5.2: Documentation (Days 33-35)

---

#### TASK 5.2.1: Complete Documentation

**Files:** Update all documentation files

**Requirements:**

1. **README.md**
   - Installation instructions
   - Quick start guide
   - Usage examples
   - Link to docs

2. **docs/USAGE.md**
   - Complete command reference
   - Example workflows
   - Troubleshooting

3. **docs/ARCHITECTURE.md**
   - Update with actual implementation
   - Add diagrams
   - Document decisions

4. **Docstrings**
   - All public classes/methods documented
   - Include examples
   - Type hints complete

**Validation Criteria:**
✓ All docs complete
✓ Examples work
✓ Links valid
✓ Docstrings present

---

### MILESTONE 5.3: Demo Preparation (Days 36-40)

---

#### TASK 5.3.1: Create Demo Materials

**Requirements:**

1. **Prepare demo session**
   - Real lecture transcript
   - Real chat log
   - Process with CLI

2. **Record demo video** (backup plan)
   - 10-minute walkthrough
   - Show full workflow
   - Display outputs

3. **Create presentation slides**
   - 10 slides
   - Problem → Solution → Demo → Architecture → Future

**Validation Criteria:**
✓ Demo works flawlessly
✓ Video recorded
✓ Slides ready

---

## ✅ Final Checklist

Before marking project complete:

### Functionality
- [ ] Can load and validate templates
- [ ] Can parse transcript and chat files
- [ ] Can execute 3+ LangChain chains
- [ ] LangGraph workflow orchestrates correctly
- [ ] Outputs generated as Markdown
- [ ] CLI works for all core commands
- [ ] Processing <3 minutes per session
- [ ] Cost <$2.00 per session

### Quality
- [ ] Test coverage >80%
- [ ] All tests pass
- [ ] No critical bugs
- [ ] Error handling robust
- [ ] Logging comprehensive

### Documentation
- [ ] README complete
- [ ] All docs updated
- [ ] Code documented
- [ ] Examples work

### Demo
- [ ] Demo session prepared
- [ ] Video recorded (backup)
- [ ] Presentation ready
- [ ] Can explain architecture in 2 minutes

---

## 🚀 Success Criteria Summary

**MVP is successful when:**

1. ✅ Template system works (can create new meeting types via YAML)
2. ✅ Online course template generates quality outputs (≥8/10 rating)
3. ✅ Processing is fast (<3 min) and cost-effective (<$2.00)
4. ✅ LangGraph orchestrates chains with proper dependencies
5. ✅ LangSmith tracking shows all execution details
6. ✅ CLI is user-friendly and robust
7. ✅ Can demo end-to-end workflow without errors
8. ✅ Framework proven extensible (agile retro template feasible)

---

## 📝 Notes for Claude Code

**Critical Success Factors:**

1. **Template engine FIRST** - Everything depends on it
2. **Test as you build** - Don't write 1000 lines then test
3. **Use LangSmith from day 1** - Essential for debugging
4. **Handle errors gracefully** - User-friendly error messages
5. **Log everything** - Use Python logging for debugging

**Common Pitfalls to Avoid:**

- ❌ Not handling LangChain API changes
- ❌ Not mocking LLM calls in tests
- ❌ Not tracking costs accurately
- ❌ Poor error messages
- ❌ Circular template dependencies

**Quality Standards:**

- Every function has type hints
- Every public API has docstring
- Every module has tests
- Every error has helpful message
- Every user-facing output is polished

---

**Ready to build! Start with TASK 0 and work sequentially through each milestone.**
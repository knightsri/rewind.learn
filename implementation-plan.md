# Rewind.Learn Implementation Plan

**Goal:** Build a complete Python library and CLI for transforming session artifacts into structured deliverables.

**Primary Deliverable:** Standalone Python package installable via `pip install rewindlearn`

**Secondary Deliverable:** Docker container for containerized deployments (optional)

---

## Phase 1: Project Scaffolding & Core Infrastructure

### 1.1 Python Project Setup

```
src/
├── rewindlearn/
│   ├── __init__.py
│   ├── __main__.py              # Entry point: python -m rewindlearn
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py              # Typer CLI app
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── process.py       # rewindlearn process
│   │   │   ├── config.py        # rewindlearn config
│   │   │   ├── template.py      # rewindlearn template
│   │   │   └── video.py         # rewindlearn video
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # App configuration (Pydantic Settings)
│   │   ├── exceptions.py        # Custom exceptions
│   │   └── logging.py           # Structured logging setup
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── loader.py            # YAML template loader
│   │   ├── validator.py         # Template validation
│   │   └── models.py            # Pydantic models for templates
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── base.py              # Base processor class
│   │   ├── transcript.py        # .txt, .vtt, .srt handlers
│   │   ├── chat.py              # .json, .txt chat log handlers
│   │   ├── slides.py            # PDF slide extraction
│   │   └── video.py             # Video metadata extraction
│   ├── chains/
│   │   ├── __init__.py
│   │   ├── base.py              # Base chain class
│   │   ├── summary.py           # Session summary chain
│   │   ├── timeline.py          # Concept timeline chain
│   │   ├── friction.py          # Student friction analysis
│   │   ├── coverage.py          # Coverage gap analysis
│   │   ├── resources.py         # Learning resources curation
│   │   ├── actions.py           # Action items extraction
│   │   └── chunks.py            # Concept chunks (CSV) extraction
│   ├── workflow/
│   │   ├── __init__.py
│   │   ├── state.py             # LangGraph state definitions
│   │   ├── graph.py             # LangGraph workflow builder
│   │   └── executor.py          # Workflow execution engine
│   ├── output/
│   │   ├── __init__.py
│   │   ├── builder.py           # Output orchestrator
│   │   ├── markdown.py          # Markdown generation
│   │   ├── pdf.py               # PDF conversion
│   │   ├── csv.py               # CSV generation (concept chunks)
│   │   └── video_chunker.py     # FFmpeg video splitting
│   └── llm/
│       ├── __init__.py
│       ├── providers.py         # LLM provider abstraction
│       └── router.py            # Model routing & fallback
├── templates/                    # Built-in YAML templates
│   ├── online-course-v1.yaml
│   └── agile-retro-v1.yaml
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_templates/
│   ├── test_processors/
│   ├── test_chains/
│   └── test_workflow/
├── pyproject.toml               # Project metadata & dependencies
├── Dockerfile
├── docker-compose.yaml
└── .env.example
```

**Tasks:**
- [ ] Create directory structure
- [ ] Initialize `pyproject.toml` with dependencies:
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
      { name = "Sri Bolisetty", email = "sri@rewindlearn.com" }
  ]
  keywords = ["langchain", "llm", "education", "transcription", "ai"]
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
      "Topic :: Text Processing",
  ]
  dependencies = [
      "langchain>=0.3",
      "langchain-anthropic>=0.3",
      "langchain-openai>=0.2",
      "langgraph>=0.2",
      "langsmith>=0.1",
      "typer[all]>=0.12",
      "rich>=13.0",
      "pydantic>=2.0",
      "pydantic-settings>=2.0",
      "pyyaml>=6.0",
      "python-dotenv>=1.0",
      "webvtt-py>=0.5",
      "pymupdf>=1.24",          # PDF processing
      "weasyprint>=62",          # PDF generation
      "ffmpeg-python>=0.2",      # Video processing
  ]

  [project.optional-dependencies]
  dev = [
      "pytest>=7.0",
      "pytest-asyncio>=0.21",
      "pytest-cov>=4.0",
      "black>=23.0",
      "ruff>=0.1",
      "mypy>=1.0",
  ]

  [project.scripts]
  rewindlearn = "rewindlearn.cli.main:app"

  [project.urls]
  Homepage = "https://github.com/knightsri/rewind.learn"
  Documentation = "https://rewindlearn.com/docs"
  Repository = "https://github.com/knightsri/rewind.learn"
  Issues = "https://github.com/knightsri/rewind.learn/issues"

  [tool.hatch.build.targets.wheel]
  packages = ["src/rewindlearn"]

  [tool.hatch.build.targets.sdist]
  include = [
      "/src",
      "/templates",
  ]
  ```
- [ ] Create `__main__.py` entry point
- [ ] Set up basic logging with Rich

### 1.2 Configuration System

**File: `src/rewindlearn/core/config.py`**

```python
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    # LLM Providers
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    default_provider: str = "anthropic"
    default_model: str = "claude-sonnet-4-20250514"

    # LangSmith
    langsmith_api_key: Optional[str] = None
    langsmith_project: str = "rewindlearn"
    langsmith_tracing: bool = True

    # Processing
    max_retries: int = 3
    temperature_default: float = 0.3
    max_tokens_default: int = 4000

    # Paths
    templates_dir: Path = Path("templates")
    output_dir: Path = Path("output")

    # Video Processing
    ffmpeg_path: str = "ffmpeg"

    class Config:
        env_file = ".env"
        env_prefix = "REWINDLEARN_"
```

**Tasks:**
- [ ] Implement Settings class
- [ ] Create `.env.example` with all configuration options
- [ ] Add config validation on startup

---

## Phase 2: Template Engine

### 2.1 Template Models

**File: `src/rewindlearn/templates/models.py`**

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from enum import Enum

class LLMConfig(BaseModel):
    model: str = "claude-sonnet-4-20250514"
    temperature: float = Field(ge=0.0, le=1.0, default=0.3)
    max_tokens: int = Field(gt=0, default=4000)
    fallback_model: Optional[str] = None

class TaskDefinition(BaseModel):
    name: str
    prompt_template: str
    llm_config: LLMConfig = Field(default_factory=LLMConfig)
    dependencies: list[str] = Field(default_factory=list)
    output_format: Literal["markdown", "csv", "json"] = "markdown"

class InputSchema(BaseModel):
    required: list[str]
    optional: list[str] = Field(default_factory=list)

class OutputSchema(BaseModel):
    deliverables: list[str]
    formats: list[Literal["markdown", "pdf", "html", "csv"]]
    languages: list[str] = ["en"]
    naming_pattern: str = "{template_id}-{deliverable}.{format}"

class Template(BaseModel):
    template_id: str
    name: str
    version: str
    description: Optional[str] = None
    inputs: InputSchema
    processing: dict  # Contains 'tasks' list
    outputs: OutputSchema

    @field_validator('processing')
    @classmethod
    def validate_processing(cls, v):
        if 'tasks' not in v:
            raise ValueError("processing must contain 'tasks' list")
        return v

    def get_tasks(self) -> list[TaskDefinition]:
        return [TaskDefinition(**t) for t in self.processing['tasks']]

    def build_dependency_graph(self) -> dict[str, list[str]]:
        """Returns task execution order based on dependencies."""
        tasks = self.get_tasks()
        return {t.name: t.dependencies for t in tasks}
```

**Tasks:**
- [ ] Implement all Pydantic models
- [ ] Add validation for circular dependencies
- [ ] Add validation that output deliverables match task names

### 2.2 Template Loader & Validator

**File: `src/rewindlearn/templates/loader.py`**

```python
import yaml
from pathlib import Path
from .models import Template

class TemplateLoader:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self._cache: dict[str, Template] = {}

    def load(self, template_id: str) -> Template:
        if template_id in self._cache:
            return self._cache[template_id]

        # Try built-in templates first
        path = self.templates_dir / f"{template_id}.yaml"
        if not path.exists():
            # Try with version suffix
            matches = list(self.templates_dir.glob(f"{template_id}*.yaml"))
            if matches:
                path = matches[0]
            else:
                raise FileNotFoundError(f"Template not found: {template_id}")

        with open(path) as f:
            data = yaml.safe_load(f)

        template = Template(**data)
        self._cache[template_id] = template
        return template

    def validate(self, path: Path) -> tuple[bool, list[str]]:
        """Validate a template file, return (valid, errors)."""
        errors = []
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            template = Template(**data)

            # Check for circular dependencies
            if self._has_circular_deps(template):
                errors.append("Circular dependencies detected")

            # Check deliverables match task names
            task_names = {t.name for t in template.get_tasks()}
            for d in template.outputs.deliverables:
                if d not in task_names:
                    errors.append(f"Deliverable '{d}' has no matching task")

        except Exception as e:
            errors.append(str(e))

        return len(errors) == 0, errors

    def _has_circular_deps(self, template: Template) -> bool:
        # Topological sort to detect cycles
        graph = template.build_dependency_graph()
        visited = set()
        rec_stack = set()

        def dfs(node):
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

**Tasks:**
- [ ] Implement TemplateLoader
- [ ] Implement circular dependency detection
- [ ] Add template caching
- [ ] Create built-in `online-course-v1.yaml` template

### 2.3 Built-in Online Course Template

**File: `templates/online-course-v1.yaml`**

Create the complete template with all 7 tasks (summary, timeline, friction, coverage, resources, actions, chunks).

**Tasks:**
- [ ] Create complete online-course-v1.yaml with all prompts
- [ ] Test template loading and validation
- [ ] Create sample test data for development

---

## Phase 3: File Processors

### 3.1 Base Processor

**File: `src/rewindlearn/processors/base.py`**

```python
from abc import ABC, abstractmethod
from pathlib import Path
from pydantic import BaseModel

class ProcessedContent(BaseModel):
    raw_text: str
    metadata: dict = {}
    timestamps: list[dict] = []  # [{text, start, end}, ...]

class BaseProcessor(ABC):
    supported_extensions: list[str] = []

    @abstractmethod
    def process(self, path: Path) -> ProcessedContent:
        pass

    @classmethod
    def can_handle(cls, path: Path) -> bool:
        return path.suffix.lower() in cls.supported_extensions
```

### 3.2 Transcript Processor

**File: `src/rewindlearn/processors/transcript.py`**

Handle `.txt`, `.vtt`, `.srt` files with timestamp extraction.

```python
import webvtt
from pathlib import Path
from .base import BaseProcessor, ProcessedContent

class TranscriptProcessor(BaseProcessor):
    supported_extensions = ['.txt', '.vtt', '.srt']

    def process(self, path: Path) -> ProcessedContent:
        ext = path.suffix.lower()

        if ext == '.txt':
            return self._process_txt(path)
        elif ext in ['.vtt', '.srt']:
            return self._process_vtt(path)

    def _process_txt(self, path: Path) -> ProcessedContent:
        text = path.read_text(encoding='utf-8')
        # Try to extract timestamps if present (e.g., "[00:01:23] Speaker: text")
        timestamps = self._extract_inline_timestamps(text)
        return ProcessedContent(raw_text=text, timestamps=timestamps)

    def _process_vtt(self, path: Path) -> ProcessedContent:
        captions = webvtt.read(str(path))
        timestamps = []
        full_text_parts = []

        for caption in captions:
            timestamps.append({
                'text': caption.text,
                'start': caption.start,
                'end': caption.end
            })
            full_text_parts.append(f"[{caption.start}] {caption.text}")

        return ProcessedContent(
            raw_text='\n'.join(full_text_parts),
            timestamps=timestamps,
            metadata={'format': path.suffix, 'caption_count': len(captions)}
        )
```

### 3.3 Chat Log Processor

**File: `src/rewindlearn/processors/chat.py`**

Handle JSON and TXT chat exports from Zoom, Teams, etc.

**Tasks:**
- [ ] Implement chat log parsing for common formats
- [ ] Extract participant names, timestamps, messages
- [ ] Handle Zoom chat export format
- [ ] Handle generic JSON format

### 3.4 Slides Processor

**File: `src/rewindlearn/processors/slides.py`**

Extract text from PDF slides using PyMuPDF.

**Tasks:**
- [ ] Implement PDF text extraction
- [ ] Extract slide numbers/page numbers
- [ ] Handle multi-column layouts

### 3.5 Processor Registry

**File: `src/rewindlearn/processors/__init__.py`**

```python
from pathlib import Path
from .transcript import TranscriptProcessor
from .chat import ChatProcessor
from .slides import SlidesProcessor

PROCESSORS = {
    'transcript': TranscriptProcessor(),
    'chat_log': ChatProcessor(),
    'slides': SlidesProcessor(),
}

def process_input(input_type: str, path: Path):
    processor = PROCESSORS.get(input_type)
    if not processor:
        raise ValueError(f"Unknown input type: {input_type}")
    return processor.process(path)
```

**Tasks:**
- [ ] Implement all processors
- [ ] Create processor registry
- [ ] Add unit tests for each processor
- [ ] Test with real Zoom/Teams exports

---

## Phase 4: LLM Integration

### 4.1 LLM Provider Abstraction

**File: `src/rewindlearn/llm/providers.py`**

```python
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from ..core.config import Settings

class LLMProvider:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._clients: dict[str, BaseChatModel] = {}

    def get_client(self, model: str) -> BaseChatModel:
        if model in self._clients:
            return self._clients[model]

        if model.startswith('claude'):
            client = ChatAnthropic(
                model=model,
                api_key=self.settings.anthropic_api_key
            )
        elif model.startswith('gpt'):
            client = ChatOpenAI(
                model=model,
                api_key=self.settings.openai_api_key
            )
        else:
            raise ValueError(f"Unknown model: {model}")

        self._clients[model] = client
        return client
```

### 4.2 LLM Router with Fallback

**File: `src/rewindlearn/llm/router.py`**

```python
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langsmith import traceable
from .providers import LLMProvider
from ..templates.models import LLMConfig

class LLMRouter:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    @traceable(name="llm_invoke")
    async def invoke(
        self,
        prompt: str,
        config: LLMConfig,
        task_name: str = "unknown"
    ) -> str:
        client = self.provider.get_client(config.model)

        try:
            response = await client.ainvoke(
                [HumanMessage(content=prompt)],
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            return response.content
        except Exception as e:
            if config.fallback_model:
                # Retry with fallback
                fallback_client = self.provider.get_client(config.fallback_model)
                response = await fallback_client.ainvoke(
                    [HumanMessage(content=prompt)],
                    temperature=config.temperature,
                    max_tokens=config.max_tokens
                )
                return response.content
            raise
```

**Tasks:**
- [ ] Implement LLMProvider
- [ ] Implement LLMRouter with fallback logic
- [ ] Add retry logic with exponential backoff
- [ ] Integrate LangSmith tracing
- [ ] Add cost tracking per invocation

---

## Phase 5: LangChain Chains

### 5.1 Base Chain

**File: `src/rewindlearn/chains/base.py`**

```python
from abc import ABC, abstractmethod
from langchain.prompts import PromptTemplate
from langsmith import traceable
from ..llm.router import LLMRouter
from ..templates.models import TaskDefinition

class BaseChain(ABC):
    def __init__(self, task: TaskDefinition, router: LLMRouter):
        self.task = task
        self.router = router
        self.prompt = PromptTemplate.from_template(task.prompt_template)

    @traceable
    async def run(self, inputs: dict) -> str:
        """Execute the chain with given inputs."""
        formatted_prompt = self.prompt.format(**inputs)
        result = await self.router.invoke(
            formatted_prompt,
            self.task.llm_config,
            task_name=self.task.name
        )
        return self.post_process(result)

    def post_process(self, result: str) -> str:
        """Override for custom post-processing."""
        return result
```

### 5.2 Implement All 7 Chains

Each chain extends BaseChain with task-specific logic:

**Tasks:**
- [ ] `summary.py` - Session summary chain
- [ ] `timeline.py` - Concept timeline chain
- [ ] `friction.py` - Student friction analysis chain
- [ ] `coverage.py` - Coverage gap analysis chain
- [ ] `resources.py` - Learning resources curation chain
- [ ] `actions.py` - Action items extraction chain
- [ ] `chunks.py` - Concept chunks CSV extraction chain

### 5.3 Concept Chunks Chain (CSV Output)

**File: `src/rewindlearn/chains/chunks.py`**

```python
import csv
import io
from .base import BaseChain

class ConceptChunksChain(BaseChain):
    def post_process(self, result: str) -> str:
        """Validate and clean CSV output."""
        # Parse the LLM output as CSV
        # Validate format: concept,description,start_time,end_time
        # Clean up any formatting issues
        lines = result.strip().split('\n')

        output = io.StringIO()
        writer = csv.writer(output)

        # Ensure header
        if not lines[0].startswith('concept'):
            writer.writerow(['concept', 'description', 'start_time', 'end_time'])

        for line in lines:
            if line.strip() and not line.startswith('#'):
                try:
                    reader = csv.reader([line])
                    row = next(reader)
                    if len(row) >= 4:
                        writer.writerow(row[:4])
                except:
                    continue

        return output.getvalue()
```

**Tasks:**
- [ ] Implement all chain classes
- [ ] Add output validation per chain
- [ ] Add Pydantic output parsers where appropriate
- [ ] Test each chain independently

---

## Phase 6: LangGraph Workflow

### 6.1 State Definition

**File: `src/rewindlearn/workflow/state.py`**

```python
from typing import TypedDict, Optional, Annotated
from operator import add

class SessionState(TypedDict):
    # Inputs
    transcript: str
    chat_log: str
    slides: Optional[str]
    course_context: dict

    # Task outputs (populated as chains complete)
    session_summary: Optional[str]
    concept_timeline: Optional[str]
    friction_analysis: Optional[str]
    coverage_gaps: Optional[str]
    learning_resources: Optional[str]
    action_items: Optional[str]
    concept_chunks: Optional[str]  # CSV format

    # Metadata
    completed_tasks: Annotated[list[str], add]
    errors: Annotated[list[str], add]
    cost_tracking: dict
```

### 6.2 Graph Builder

**File: `src/rewindlearn/workflow/graph.py`**

```python
from langgraph.graph import StateGraph, END
from ..templates.models import Template
from ..chains import create_chain
from .state import SessionState

class WorkflowBuilder:
    def __init__(self, template: Template, router):
        self.template = template
        self.router = router

    def build(self) -> StateGraph:
        graph = StateGraph(SessionState)
        tasks = self.template.get_tasks()
        dep_graph = self.template.build_dependency_graph()

        # Add nodes for each task
        for task in tasks:
            chain = create_chain(task, self.router)
            graph.add_node(task.name, self._make_node(chain, task.name))

        # Add edges based on dependencies
        # Tasks with no dependencies start from START
        for task in tasks:
            if not dep_graph[task.name]:
                graph.add_edge("__start__", task.name)
            else:
                for dep in dep_graph[task.name]:
                    graph.add_edge(dep, task.name)

        # All leaf nodes go to END
        leaf_tasks = self._find_leaf_tasks(tasks, dep_graph)
        for leaf in leaf_tasks:
            graph.add_edge(leaf, END)

        return graph.compile()

    def _make_node(self, chain, task_name):
        async def node(state: SessionState) -> dict:
            try:
                result = await chain.run(state)
                return {
                    task_name: result,
                    "completed_tasks": [task_name]
                }
            except Exception as e:
                return {"errors": [f"{task_name}: {str(e)}"]}
        return node

    def _find_leaf_tasks(self, tasks, dep_graph) -> list[str]:
        """Find tasks that no other task depends on."""
        all_deps = set()
        for deps in dep_graph.values():
            all_deps.update(deps)
        return [t.name for t in tasks if t.name not in all_deps]
```

### 6.3 Workflow Executor

**File: `src/rewindlearn/workflow/executor.py`**

```python
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from .graph import WorkflowBuilder
from .state import SessionState

class WorkflowExecutor:
    def __init__(self, template, router, console: Console):
        self.template = template
        self.router = router
        self.console = console

    async def execute(self, inputs: dict) -> SessionState:
        builder = WorkflowBuilder(self.template, self.router)
        graph = builder.build()

        initial_state: SessionState = {
            **inputs,
            "completed_tasks": [],
            "errors": [],
            "cost_tracking": {}
        }

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Processing session...", total=None)

            final_state = await graph.ainvoke(initial_state)

            progress.update(task, description="Complete!")

        return final_state
```

**Tasks:**
- [ ] Implement SessionState
- [ ] Implement WorkflowBuilder with dependency resolution
- [ ] Implement parallel execution for independent tasks
- [ ] Add progress tracking with Rich
- [ ] Add error handling and partial results
- [ ] Test end-to-end workflow

---

## Phase 7: Output Generation

### 7.1 Output Builder

**File: `src/rewindlearn/output/builder.py`**

```python
from pathlib import Path
from ..templates.models import Template
from ..workflow.state import SessionState
from .markdown import MarkdownGenerator
from .pdf import PDFConverter
from .csv import CSVWriter

class OutputBuilder:
    def __init__(self, template: Template, output_dir: Path):
        self.template = template
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, state: SessionState, context: dict) -> list[Path]:
        """Generate all output files from workflow state."""
        outputs = []

        for deliverable in self.template.outputs.deliverables:
            content = state.get(deliverable)
            if not content:
                continue

            # Determine output format for this deliverable
            if deliverable == 'concept_chunks':
                # CSV output
                path = self._generate_csv(deliverable, content, context)
            else:
                # Markdown output
                path = self._generate_markdown(deliverable, content, context)

            outputs.append(path)

            # Generate additional formats
            if 'pdf' in self.template.outputs.formats and path.suffix == '.md':
                pdf_path = PDFConverter().convert(path)
                outputs.append(pdf_path)

        return outputs

    def _generate_markdown(self, name: str, content: str, context: dict) -> Path:
        filename = self._make_filename(name, 'md', context)
        path = self.output_dir / filename

        generator = MarkdownGenerator()
        generator.write(path, content, metadata={
            'template': self.template.template_id,
            'deliverable': name,
            **context
        })
        return path

    def _generate_csv(self, name: str, content: str, context: dict) -> Path:
        filename = self._make_filename(name, 'csv', context)
        path = self.output_dir / filename
        path.write_text(content)
        return path

    def _make_filename(self, deliverable: str, ext: str, context: dict) -> str:
        pattern = self.template.outputs.naming_pattern
        return pattern.format(
            template_id=self.template.template_id,
            deliverable=deliverable,
            format=ext,
            **context
        )
```

### 7.2 PDF Converter

**File: `src/rewindlearn/output/pdf.py`**

```python
from pathlib import Path
from weasyprint import HTML, CSS

class PDFConverter:
    def convert(self, markdown_path: Path) -> Path:
        # Read markdown
        content = markdown_path.read_text()

        # Convert to HTML (using markdown library or pandoc)
        html_content = self._markdown_to_html(content)

        # Convert to PDF
        pdf_path = markdown_path.with_suffix('.pdf')
        HTML(string=html_content).write_pdf(
            pdf_path,
            stylesheets=[CSS(string=self._get_styles())]
        )

        return pdf_path

    def _markdown_to_html(self, content: str) -> str:
        import markdown
        return markdown.markdown(content, extensions=['tables', 'fenced_code'])

    def _get_styles(self) -> str:
        return """
        body { font-family: sans-serif; margin: 2cm; }
        h1 { color: #333; }
        code { background: #f4f4f4; padding: 2px 4px; }
        table { border-collapse: collapse; width: 100%; }
        td, th { border: 1px solid #ddd; padding: 8px; }
        """
```

### 7.3 Video Chunker

**File: `src/rewindlearn/output/video_chunker.py`**

```python
import csv
import subprocess
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ConceptChunk:
    concept: str
    description: str
    start_time: str
    end_time: str

class VideoChunker:
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg_path = ffmpeg_path

    def load_chunks(self, csv_path: Path) -> list[ConceptChunk]:
        chunks = []
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                chunks.append(ConceptChunk(
                    concept=row['concept'],
                    description=row['description'],
                    start_time=row['start_time'],
                    end_time=row['end_time']
                ))
        return chunks

    def split_video(
        self,
        video_path: Path,
        csv_path: Path,
        output_dir: Path
    ) -> list[Path]:
        chunks = self.load_chunks(csv_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        outputs = []

        for i, chunk in enumerate(chunks, 1):
            # Sanitize filename
            safe_name = self._sanitize_filename(chunk.concept)
            output_file = output_dir / f"{i:02d}-{safe_name}.mp4"

            cmd = [
                self.ffmpeg_path,
                '-i', str(video_path),
                '-ss', chunk.start_time,
                '-to', chunk.end_time,
                '-c', 'copy',  # Fast copy without re-encoding
                '-y',  # Overwrite
                str(output_file)
            ]

            subprocess.run(cmd, check=True, capture_output=True)
            outputs.append(output_file)

        return outputs

    def _sanitize_filename(self, name: str) -> str:
        # Remove/replace invalid characters
        invalid = '<>:"/\\|?*'
        for char in invalid:
            name = name.replace(char, '')
        return name.lower().replace(' ', '-')[:50]
```

**Tasks:**
- [ ] Implement OutputBuilder
- [ ] Implement MarkdownGenerator with YAML frontmatter
- [ ] Implement PDFConverter with WeasyPrint
- [ ] Implement CSVWriter
- [ ] Implement VideoChunker with FFmpeg
- [ ] Add output validation
- [ ] Test all output formats

---

## Phase 8: CLI Implementation

### 8.1 Main CLI App

**File: `src/rewindlearn/cli/main.py`**

```python
import typer
from rich.console import Console
from .commands import process, config, template, video

app = typer.Typer(
    name="rewindlearn",
    help="Transform session artifacts into structured knowledge.",
    no_args_is_help=True
)

console = Console()

app.add_typer(process.app, name="process")
app.add_typer(config.app, name="config")
app.add_typer(template.app, name="template")
app.add_typer(video.app, name="video")

@app.callback()
def main():
    """Rewind.Learn - Session Processing Framework"""
    pass

if __name__ == "__main__":
    app()
```

### 8.2 Process Command

**File: `src/rewindlearn/cli/commands/process.py`**

```python
import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import asyncio

app = typer.Typer(help="Process session files")
console = Console()

@app.command()
def run(
    template: str = typer.Option(..., "--template", "-t", help="Template ID or path"),
    transcript: Path = typer.Option(..., "--transcript", help="Transcript file"),
    chat: Path = typer.Option(None, "--chat", help="Chat log file"),
    slides: Path = typer.Option(None, "--slides", help="Slides PDF"),
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory"),
    course_name: str = typer.Option(None, "--course", help="Course name"),
    session_number: int = typer.Option(None, "--session", help="Session number"),
):
    """Process a session with the specified template."""
    from ...core.config import Settings
    from ...templates.loader import TemplateLoader
    from ...processors import process_input
    from ...llm.providers import LLMProvider
    from ...llm.router import LLMRouter
    from ...workflow.executor import WorkflowExecutor
    from ...output.builder import OutputBuilder

    settings = Settings()

    console.print(Panel.fit(
        f"[bold blue]Rewind.Learn[/bold blue]\n"
        f"Template: {template}\n"
        f"Output: {output}"
    ))

    # Load template
    loader = TemplateLoader(settings.templates_dir)
    tmpl = loader.load(template)

    # Process input files
    inputs = {
        'transcript': process_input('transcript', transcript).raw_text,
        'course_context': {
            'course_name': course_name or 'Unknown Course',
            'session_number': session_number or 1
        }
    }

    if chat:
        inputs['chat_log'] = process_input('chat_log', chat).raw_text
    if slides:
        inputs['slides'] = process_input('slides', slides).raw_text

    # Execute workflow
    provider = LLMProvider(settings)
    router = LLMRouter(provider)
    executor = WorkflowExecutor(tmpl, router, console)

    state = asyncio.run(executor.execute(inputs))

    # Generate outputs
    builder = OutputBuilder(tmpl, output)
    files = builder.generate(state, {
        'course_name': course_name,
        'session_number': session_number
    })

    # Summary
    table = Table(title="Generated Files")
    table.add_column("File", style="green")
    table.add_column("Size")

    for f in files:
        table.add_row(str(f.name), f"{f.stat().st_size:,} bytes")

    console.print(table)

    if state.get('errors'):
        console.print("[yellow]Warnings:[/yellow]")
        for err in state['errors']:
            console.print(f"  - {err}")
```

### 8.3 Video Command

**File: `src/rewindlearn/cli/commands/video.py`**

```python
import typer
from pathlib import Path
from rich.console import Console
from rich.progress import track

app = typer.Typer(help="Video processing commands")
console = Console()

@app.command()
def split(
    input: Path = typer.Option(..., "--input", "-i", help="Input video file"),
    chunks: Path = typer.Option(..., "--chunks", "-c", help="Concept chunks CSV"),
    output: Path = typer.Option(Path("clips"), "--output", "-o", help="Output directory"),
):
    """Split video into concept chunks using CSV timestamps."""
    from ...output.video_chunker import VideoChunker

    if not input.exists():
        console.print(f"[red]Video file not found: {input}[/red]")
        raise typer.Exit(1)

    if not chunks.exists():
        console.print(f"[red]Chunks CSV not found: {chunks}[/red]")
        raise typer.Exit(1)

    chunker = VideoChunker()
    chunk_list = chunker.load_chunks(chunks)

    console.print(f"[blue]Splitting {input.name} into {len(chunk_list)} clips...[/blue]")

    outputs = chunker.split_video(input, chunks, output)

    console.print(f"[green]Created {len(outputs)} video clips in {output}/[/green]")
    for f in outputs:
        console.print(f"  - {f.name}")
```

### 8.4 Template Command

**File: `src/rewindlearn/cli/commands/template.py`**

```python
import typer
from pathlib import Path
from rich.console import Console

app = typer.Typer(help="Template management")
console = Console()

@app.command()
def validate(
    path: Path = typer.Argument(..., help="Template YAML file to validate")
):
    """Validate a template file."""
    from ...templates.loader import TemplateLoader
    from ...core.config import Settings

    settings = Settings()
    loader = TemplateLoader(settings.templates_dir)

    valid, errors = loader.validate(path)

    if valid:
        console.print(f"[green]✓ Template is valid: {path}[/green]")
    else:
        console.print(f"[red]✗ Template has errors:[/red]")
        for err in errors:
            console.print(f"  - {err}")
        raise typer.Exit(1)

@app.command("list")
def list_templates():
    """List available templates."""
    from ...core.config import Settings

    settings = Settings()
    templates_dir = settings.templates_dir

    console.print("[bold]Available Templates:[/bold]")
    for f in templates_dir.glob("*.yaml"):
        console.print(f"  - {f.stem}")
```

### 8.5 Config Command

**File: `src/rewindlearn/cli/commands/config.py`**

```python
import typer
from rich.console import Console

app = typer.Typer(help="Configuration management")
console = Console()

@app.command()
def show():
    """Show current configuration."""
    from ...core.config import Settings

    settings = Settings()

    console.print("[bold]Current Configuration:[/bold]")
    console.print(f"  Default Provider: {settings.default_provider}")
    console.print(f"  Default Model: {settings.default_model}")
    console.print(f"  Templates Dir: {settings.templates_dir}")
    console.print(f"  LangSmith Tracing: {settings.langsmith_tracing}")

    # Show API key status (not the actual keys)
    console.print(f"  Anthropic API Key: {'✓ Set' if settings.anthropic_api_key else '✗ Not set'}")
    console.print(f"  OpenAI API Key: {'✓ Set' if settings.openai_api_key else '✗ Not set'}")

@app.command("set-provider")
def set_provider(
    provider: str = typer.Argument(..., help="Provider name (claude, openai)"),
    api_key: str = typer.Option(None, "--api-key", help="API key")
):
    """Set default LLM provider."""
    console.print(f"[yellow]Note: Set REWINDLEARN_ANTHROPIC_API_KEY or REWINDLEARN_OPENAI_API_KEY in .env[/yellow]")
    console.print(f"Provider preference saved: {provider}")
```

**Tasks:**
- [ ] Implement main CLI app with Typer
- [ ] Implement `process` command
- [ ] Implement `video split` command
- [ ] Implement `template validate` and `template list`
- [ ] Implement `config show` and `config set-provider`
- [ ] Add Rich progress bars and tables
- [ ] Add error handling with helpful messages
- [ ] Test CLI end-to-end

---

## Phase 9: Docker Containerization

### 9.1 Dockerfile

**File: `Dockerfile`**

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir build && \
    pip wheel --no-cache-dir --wheel-dir /wheels .

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application code
COPY src/ /app/src/
COPY templates/ /app/templates/

# Create directories for data
RUN mkdir -p /data/input /data/output

# Environment variables
ENV REWINDLEARN_TEMPLATES_DIR=/app/templates
ENV REWINDLEARN_OUTPUT_DIR=/data/output

# Entry point
ENTRYPOINT ["python", "-m", "rewindlearn"]
CMD ["--help"]
```

### 9.2 Docker Compose

**File: `docker-compose.yaml`**

```yaml
version: '3.8'

services:
  rewindlearn:
    build: .
    image: rewindlearn:latest
    container_name: rewindlearn
    volumes:
      # Mount input/output directories
      - ./input:/data/input:ro
      - ./output:/data/output
      # Mount custom templates
      - ./custom-templates:/app/custom-templates:ro
    environment:
      - REWINDLEARN_ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REWINDLEARN_OPENAI_API_KEY=${OPENAI_API_KEY}
      - REWINDLEARN_LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
      - REWINDLEARN_LANGSMITH_TRACING=true
    # Example: process a session
    # command: process --template online-course --transcript /data/input/transcript.txt --chat /data/input/chat.json --output /data/output

  # Optional: Redis for caching (future)
  # redis:
  #   image: redis:alpine
  #   ports:
  #     - "6379:6379"
```

### 9.3 Docker Helper Scripts

**File: `scripts/docker-run.sh`**

```bash
#!/bin/bash

# Helper script to run rewindlearn in Docker

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

docker run --rm -it \
    -v "${PROJECT_DIR}/input:/data/input:ro" \
    -v "${PROJECT_DIR}/output:/data/output" \
    -v "${PROJECT_DIR}/custom-templates:/app/custom-templates:ro" \
    -e REWINDLEARN_ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
    -e REWINDLEARN_OPENAI_API_KEY="${OPENAI_API_KEY}" \
    -e REWINDLEARN_LANGSMITH_API_KEY="${LANGSMITH_API_KEY}" \
    rewindlearn:latest "$@"
```

**File: `scripts/docker-process.sh`**

```bash
#!/bin/bash

# Quick helper to process a session
# Usage: ./docker-process.sh transcript.txt chat.json "Course Name" 1

TRANSCRIPT=$1
CHAT=$2
COURSE=${3:-"Unknown Course"}
SESSION=${4:-1}

./docker-run.sh process \
    --template online-course \
    --transcript "/data/input/${TRANSCRIPT}" \
    --chat "/data/input/${CHAT}" \
    --course "${COURSE}" \
    --session "${SESSION}" \
    --output /data/output
```

**Tasks:**
- [ ] Create Dockerfile with multi-stage build
- [ ] Include FFmpeg and WeasyPrint dependencies
- [ ] Create docker-compose.yaml
- [ ] Create helper scripts for common operations
- [ ] Test container build and run
- [ ] Document Docker usage
- [ ] Push to Docker Hub / GitHub Container Registry

---

## Phase 10: PyPI Publishing

### 10.1 Package Distribution Setup

**Tasks:**
- [ ] Verify `pyproject.toml` has all required metadata
- [ ] Create `LICENSE` file (Apache 2.0)
- [ ] Ensure `README.md` renders correctly on PyPI
- [ ] Add `MANIFEST.in` if needed for additional files

### 10.2 Build & Test Package

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Test install locally
pip install dist/rewindlearn-0.1.0-py3-none-any.whl

# Verify CLI works
rewindlearn --help
```

### 10.3 Publish to PyPI

```bash
# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ rewindlearn

# Upload to production PyPI
twine upload dist/*
```

### 10.4 GitHub Actions for Publishing

**File: `.github/workflows/publish.yml`**

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

**Tasks:**
- [ ] Set up PyPI account and API token
- [ ] Create GitHub Actions workflow for automated publishing
- [ ] Test full publish pipeline with Test PyPI
- [ ] Publish v0.1.0 to PyPI

---

## Phase 11: Testing & Quality

### 11.1 Test Structure

```
tests/
├── conftest.py                 # Shared fixtures
├── fixtures/                   # Test data
│   ├── transcripts/
│   │   ├── simple.txt
│   │   ├── with-timestamps.vtt
│   │   └── zoom-export.vtt
│   ├── chats/
│   │   ├── zoom-chat.txt
│   │   └── teams-chat.json
│   └── templates/
│       ├── valid-template.yaml
│       └── invalid-template.yaml
├── unit/
│   ├── test_template_loader.py
│   ├── test_template_validator.py
│   ├── test_processors.py
│   └── test_output_builder.py
├── integration/
│   ├── test_workflow.py
│   ├── test_chains.py
│   └── test_cli.py
└── e2e/
    └── test_full_pipeline.py
```

### 11.2 Key Test Cases

**Tasks:**
- [ ] Template loading and validation tests
- [ ] File processor tests (transcript, chat, slides)
- [ ] Chain output validation tests
- [ ] Workflow execution tests with mocked LLM
- [ ] CLI command tests
- [ ] Docker container tests
- [ ] End-to-end test with real session data

### 11.3 Test Configuration

**File: `pyproject.toml` (test section)**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "e2e: marks end-to-end tests",
]

[tool.coverage.run]
source = ["src/rewindlearn"]
omit = ["*/tests/*"]
```

**Tasks:**
- [ ] Set up pytest with async support
- [ ] Create test fixtures
- [ ] Achieve 80%+ code coverage
- [ ] Set up CI/CD with GitHub Actions

---

## Phase 12: Documentation & Polish

### 12.1 Documentation

**Tasks:**
- [ ] Update README.md with installation and usage instructions
- [ ] Create CONTRIBUTING.md
- [ ] Add docstrings to all public functions
- [ ] Create example notebooks/scripts
- [ ] Add API documentation with mkdocs

### 12.2 Final Polish

**Tasks:**
- [ ] Error messages with actionable suggestions
- [ ] Graceful degradation on partial failures
- [ ] Cost tracking and reporting
- [ ] Performance optimization (caching, parallel processing)
- [ ] Security review (no secrets in logs, safe file handling)

---

## Implementation Order Summary

Execute in this order to build incrementally:

| Step | Phase | Focus |
|------|-------|-------|
| 1 | Phase 1.1 | Project scaffolding, pyproject.toml, basic structure |
| 2 | Phase 1.2 | Configuration system with Pydantic Settings |
| 3 | Phase 2 | Template engine (models, loader, validator) |
| 4 | Phase 3 | File processors (transcript, chat, slides) |
| 5 | Phase 4 | LLM integration (providers, router) |
| 6 | Phase 5 | LangChain chains (all 7 tasks) |
| 7 | Phase 6 | LangGraph workflow (state, graph, executor) |
| 8 | Phase 7 | Output generation (markdown, PDF, CSV, video chunker) |
| 9 | Phase 8 | CLI commands (process, video, template, config) |
| 10 | Phase 9 | Docker containerization (optional) |
| 11 | Phase 10 | PyPI publishing |
| 12 | Phase 11 | Testing & quality |
| 13 | Phase 12 | Documentation and polish |

---

## Quick Start After Implementation

### Option 1: Install from PyPI (Recommended)

```bash
# Install the package
pip install rewindlearn

# Set your API key
export ANTHROPIC_API_KEY="your-api-key"

# Process a session
rewindlearn process \
    --template online-course \
    --transcript lecture.txt \
    --chat chat.json \
    --output study-guides/

# Split video into concept chunks
rewindlearn video split \
    --input lecture.mp4 \
    --chunks study-guides/concept-chunks.csv \
    --output clips/
```

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/knightsri/rewind.learn.git
cd rewind.learn

# Install in development mode
pip install -e ".[dev]"

# Run CLI
rewindlearn --help
```

### Option 3: Docker Container

```bash
# Build Docker image
docker build -t rewindlearn .

# Process a session
docker run -v $(pwd)/data:/data \
    -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    rewindlearn process \
    --template online-course \
    --transcript /data/lecture.txt \
    --chat /data/chat.json \
    --output /data/output

# Split video into concept chunks
docker run -v $(pwd)/data:/data \
    rewindlearn video split \
    --input /data/lecture.mp4 \
    --chunks /data/output/concept-chunks.csv \
    --output /data/clips
```

### Programmatic Usage (Python Library)

```python
import asyncio
from rewindlearn import process_session

async def main():
    results = await process_session(
        template="online-course",
        transcript_path="lecture.txt",
        chat_path="chat.json",
        course_name="AI Engineering",
        session_number=1
    )

    # Access individual outputs
    print(results.session_summary)
    print(results.concept_chunks)  # CSV content

    # Save all outputs
    results.save_all("study-guides/")

asyncio.run(main())
```

---

## Success Criteria

**Package Distribution:**
- [ ] `pip install rewindlearn` works from PyPI
- [ ] CLI available as `rewindlearn` command after install
- [ ] Works on Python 3.10, 3.11, 3.12
- [ ] All dependencies install cleanly

**Core Functionality:**
- [ ] Process command generates all 7 deliverables
- [ ] Video split command creates clips from CSV
- [ ] Templates loadable from package and custom paths
- [ ] Programmatic API works for library usage

**Performance:**
- [ ] Processing time < 3 minutes for 2-hour session
- [ ] Cost < $2 per session

**Quality:**
- [ ] All tests pass (80%+ coverage)
- [ ] Documentation complete
- [ ] Docker container builds successfully (optional)

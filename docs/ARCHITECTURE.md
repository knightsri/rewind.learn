## Rewind.Learn Technical Architecture

### High-Level System Overview

```mermaid
graph TB
    subgraph "Input Layer"
        A[Session Files] --> B[File Processors]
        A1[Transcript .txt/.vtt] --> B
        A2[Chat Log .json/.txt] --> B
        A3[Slides .pdf] --> B
        A4[Video .mp4] --> B
        A5[Agenda/Context .yaml] --> B
    end
    
    subgraph "Template Engine"
        B --> C[Template Loader]
        C --> D[Template Validator]
        D --> E[Prompt Builder]
        T[Template Library] -.-> C
        T1[online-course.yaml] -.-> T
        T2[agile-retro.yaml] -.-> T
        T3[custom/*.yaml] -.-> T
    end
    
    subgraph "LangChain Orchestration Layer"
        E --> F[LangGraph Workflow]
        F --> G1[Summary Chain]
        F --> G2[Timeline Chain]
        F --> G3[Friction Analysis Chain]
        F --> G4[Coverage Gap Chain]
        F --> G5[Resource Curation Chain]
        F --> G6[Action Items Chain]
        
        G1 & G2 & G3 & G4 & G5 & G6 --> H[Result Aggregator]
    end
    
    subgraph "LLM Provider Layer"
        H --> I[LLM Router]
        I --> J1[Claude API]
        I --> J2[OpenAI API]
        I --> J3[Local Models<br/>Ollama]
    end
    
    subgraph "Knowledge Graph Optional"
        H --> K[Vector Store]
        K --> K1[Supabase pgvector]
        K --> K2[ChromaDB]
        K1 & K2 --> L[Cross-Session Analysis]
    end
    
    subgraph "Output Generation"
        H --> M[Output Builder]
        M --> N1[Markdown Generator]
        M --> N2[PDF Converter]
        M --> N3[HTML Renderer]
        M --> N4[JSON Export]
    end
    
    subgraph "Observability LangSmith"
        F -.-> O[LangSmith Tracing]
        O -.-> P[Prompt Analytics]
        O -.-> Q[Cost Tracking]
        O -.-> R[Quality Metrics]
    end
    
    N1 & N2 & N3 & N4 --> S[Deliverables]
    
    style F fill:#e1f5ff
    style O fill:#fff4e1
    style I fill:#f0e1ff
```

---

## Detailed Component Architecture

### 1. Template System Architecture

```mermaid
graph LR
    subgraph "Template Structure"
        A[Template YAML] --> B[Metadata Section]
        A --> C[Input Requirements]
        A --> D[Processing Tasks]
        A --> E[Output Specifications]
        
        B --> B1[template_id<br/>version<br/>description]
        C --> C1[required: transcript, chat<br/>optional: slides, video]
        D --> D1[Task Definitions]
        E --> E1[deliverables<br/>formats<br/>languages]
    end
    
    subgraph "Task Definition"
        D1 --> F[Task 1: Summary]
        D1 --> G[Task 2: Timeline]
        D1 --> H[Task 3: Friction]
        
        F --> F1[name: summary<br/>prompt_template<br/>llm_config<br/>dependencies: none]
        
        G --> G1[name: timeline<br/>prompt_template<br/>llm_config<br/>dependencies: summary]
        
        H --> H1[name: friction<br/>prompt_template<br/>llm_config<br/>dependencies: chat_log]
    end
    
    subgraph "LLM Config per Task"
        F1 & G1 & H1 --> I[model: claude-sonnet-4<br/>temperature: 0.3<br/>max_tokens: 4000<br/>fallback: gpt-4o]
    end
```

**Template YAML Example:**

```yaml
template_id: "online-course-v1"
name: "Online Course Session"
version: "1.0"
description: "Process online course sessions into comprehensive study materials"

# Your specific prompts
course_context:
  course_name: "AI Engineering"  # or "AI Generalist"
  instructor: "Sri"
  session_format: "2-3 hour lecture + hands-on"

inputs:
  required:
    - transcript
    - chat_log
  optional:
    - slides
    - previous_session_summary
    - course_outline

processing:
  tasks:
    - name: "session_summary"
      prompt_template: |
        You are analyzing a session from {{course_name}}.
        
        Transcript:
        {{transcript}}
        
        Create a comprehensive summary covering:
        - Main topics discussed
        - Key learning objectives
        - Critical takeaways
        
      llm_config:
        model: "claude-sonnet-4"
        temperature: 0.3
        max_tokens: 4000
      dependencies: []
      
    - name: "concept_timeline"
      prompt_template: |
        Based on the session summary and transcript, create a chronological timeline
        of concepts covered, organized into 5-10 minute segments.
        
        Summary:
        {{session_summary}}
        
        Transcript:
        {{transcript}}
        
      llm_config:
        model: "claude-sonnet-4"
        temperature: 0.2
      dependencies: ["session_summary"]
      
    - name: "student_friction_analysis"
      prompt_template: |
        Analyze the chat log for signs of student confusion, questions, and struggles.
        
        Chat Log:
        {{chat_log}}
        
        Session Context:
        {{session_summary}}
        
        Identify:
        - Topics that confused students
        - Repeated questions
        - Concepts needing review
        
      llm_config:
        model: "gpt-4o"
        temperature: 0.4
      dependencies: ["session_summary"]

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

---

### 2. LangGraph Workflow Architecture

```mermaid
graph TB
    Start([Start Session Processing]) --> LoadTemplate[Load Template]
    LoadTemplate --> ValidateInputs{All Required<br/>Inputs Present?}
    
    ValidateInputs -->|No| Error[Raise Error]
    ValidateInputs -->|Yes| BuildGraph[Build LangGraph<br/>from Template]
    
    BuildGraph --> InitState[Initialize State]
    InitState --> TaskRouter{Task Router}
    
    subgraph "Parallel Processing Layer 1 No Dependencies"
        TaskRouter --> T1[Summary Task]
        TaskRouter --> T6[Action Items Task]
    end
    
    T1 --> StateUpdate1[Update State]
    T6 --> StateUpdate1
    
    StateUpdate1 --> Layer2Router{Layer 2 Router}
    
    subgraph "Parallel Processing Layer 2 Depends on Summary"
        Layer2Router --> T2[Timeline Task]
        Layer2Router --> T3[Friction Task]
        Layer2Router --> T4[Coverage Gap Task]
    end
    
    T2 & T3 & T4 --> StateUpdate2[Update State]
    
    StateUpdate2 --> Layer3Router{Layer 3 Router}
    
    subgraph "Final Processing Depends on Analysis"
        Layer3Router --> T5[Resource Curation Task]
    end
    
    T5 --> StateUpdate3[Update State]
    
    StateUpdate3 --> QualityCheck{Quality<br/>Threshold Met?}
    
    QualityCheck -->|No| Retry{Retry<br/>Count < 3?}
    Retry -->|Yes| TaskRouter
    Retry -->|No| PartialResults[Return Partial Results<br/>with Warnings]
    
    QualityCheck -->|Yes| Aggregate[Aggregate Results]
    
    Aggregate --> GenerateOutputs[Generate Outputs]
    GenerateOutputs --> SaveArtifacts[Save to Knowledge Graph]
    SaveArtifacts --> End([Complete])
    
    PartialResults --> End
    Error --> End
    
    style T1 fill:#e1f5ff
    style T2 fill:#e1f5ff
    style T3 fill:#e1f5ff
    style T4 fill:#e1f5ff
    style T5 fill:#e1f5ff
    style T6 fill:#e1f5ff
```

**LangGraph State Schema:**

```python
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph

class SessionState(TypedDict):
    # Inputs
    transcript: str
    chat_log: str
    slides: Optional[str]
    course_context: dict
    
    # Intermediate results
    session_summary: Optional[str]
    concept_timeline: Optional[str]
    friction_analysis: Optional[str]
    coverage_gaps: Optional[str]
    learning_resources: Optional[str]
    action_items: Optional[str]
    
    # Metadata
    processing_status: dict
    error_log: List[str]
    quality_scores: dict
    cost_tracking: dict
```

---

### 3. LangChain Integration Architecture

```mermaid
graph TB
    subgraph "LangChain Components"
        A[Prompt Templates] --> B[LangChain LLMChain]
        B --> C[Output Parsers]
        
        D[Memory/Context] --> B
        
        E[Tool Calling Optional] --> B
        E1[Web Search for Resources] -.-> E
        E2[Calendar Integration] -.-> E
    end
    
    subgraph "LangSmith Integration"
        B -.-> F[Trace Every Chain]
        F --> G[LangSmith Dashboard]
        G --> H1[Latency Metrics]
        G --> H2[Token Usage]
        G --> H3[Cost per Session]
        G --> H4[Prompt Versions]
        G --> H5[Output Quality Scores]
    end
    
    subgraph "Prompt Management"
        I[LangSmith Hub] --> A
        I --> J[Version Control]
        J --> K[A/B Testing]
        K --> L[Best Prompt Selection]
    end
    
    C --> M[Structured Output]
    M --> N[Pydantic Models]
    
    style F fill:#fff4e1
    style G fill:#fff4e1
```

**Example LangChain Implementation:**

```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field
from langsmith import traceable

class SessionSummary(BaseModel):
    main_topics: List[str] = Field(description="3-5 main topics covered")
    key_concepts: List[str] = Field(description="Critical concepts explained")
    learning_objectives: List[str] = Field(description="What students should know")
    executive_summary: str = Field(description="2-3 sentence overview")

@traceable(name="generate_session_summary")
def generate_summary(transcript: str, course_context: dict) -> SessionSummary:
    parser = PydanticOutputParser(pydantic_object=SessionSummary)
    
    prompt = PromptTemplate(
        template="""You are analyzing a {course_name} session.
        
        Transcript:
        {transcript}
        
        {format_instructions}
        """,
        input_variables=["course_name", "transcript"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    llm = ChatAnthropic(model="claude-sonnet-4", temperature=0.3)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.run(
        course_name=course_context['course_name'],
        transcript=transcript
    )
    
    return parser.parse(result)
```

---

### 4. CLI Architecture with Rich UI

```mermaid
graph LR
    A[rewindlearn CLI] --> B{Command Router}
    
    B --> C[init]
    B --> D[process]
    B --> E[template]
    B --> F[config]
    
    C --> C1[Initialize new template]
    
    D --> D1[Process session]
    D1 --> D2[Show progress with Rich]
    D2 --> D3[Live cost tracking]
    D3 --> D4[Quality indicators]
    
    E --> E1[List templates]
    E --> E2[Validate template]
    E --> E3[Test template]
    
    F --> F1[Set LLM provider]
    F --> F2[Configure API keys]
    F --> F3[Set defaults]
    
    style D2 fill:#e1f5ff
    style D3 fill:#fff4e1
```

**CLI Commands:**

```bash
# Initialize a new session processing
rewindlearn init --template online-course --course "AI Engineering"

# Process a session
rewindlearn process \
  --template ai-engineering.yaml \
  --transcript session-01.txt \
  --chat chat-01.json \
  --output study-guides/

# With live progress tracking
rewindlearn process session-01/ --watch

# Test template with sample data
rewindlearn template test online-course.yaml --sample data/sample-session/

# Configure LLM providers
rewindlearn config set-provider claude --api-key $ANTHROPIC_API_KEY
rewindlearn config set-provider openai --api-key $OPENAI_API_KEY

# View processing history and costs
rewindlearn history --last 10 --show-costs
```

---

### 5. Knowledge Graph & Cross-Session Intelligence

```mermaid
graph TB
    subgraph "Session Processing"
        A[Current Session] --> B[Generate Deliverables]
        B --> C[Extract Key Entities]
    end
    
    subgraph "Knowledge Graph"
        C --> D[Vector Embeddings]
        D --> E[(Supabase pgvector)]
        
        F[Previous Sessions] --> E
        
        E --> G[Semantic Search]
        G --> H[Find Related Concepts]
        G --> I[Identify Prerequisites]
        G --> J[Detect Patterns]
    end
    
    subgraph "Cross-Session Analysis"
        H & I & J --> K[Context Enrichment]
        K --> L[Enhanced Deliverables]
        
        L --> M[Concept Linkages]
        L --> N[Prerequisite Gaps]
        L --> O[Recurring Confusion]
    end
    
    M & N & O --> P[Final Output with Context]
    
    style E fill:#e1f5ff
    style K fill:#fff4e1
```

**Knowledge Graph Schema:**

```python
# Supabase tables
sessions_table = {
    "id": "uuid",
    "course_name": "text",
    "session_number": "int",
    "date": "timestamp",
    "summary": "text",
    "concepts": "jsonb",  # List of concepts covered
    "embedding": "vector(1536)"  # For semantic search
}

concepts_table = {
    "id": "uuid",
    "session_id": "uuid",
    "concept_name": "text",
    "definition": "text",
    "related_concepts": "jsonb",
    "confusion_level": "float",  # From friction analysis
    "embedding": "vector(1536)"
}

student_confusion_table = {
    "id": "uuid",
    "session_id": "uuid",
    "topic": "text",
    "question_count": "int",
    "resolved": "boolean",
    "follow_up_needed": "boolean"
}
```

---

### 6. Deployment Architecture

```mermaid
graph TB
    subgraph "Local Development"
        A[Developer Machine] --> B[CLI Tool]
        B --> C[Local Config]
        C --> D[API Keys]
    end
    
    subgraph "Self-Hosted Deployment"
        E[Docker Container] --> F[rewindlearn Server]
        F --> G[n8n Automation Optional]
        G --> H[Zoom Webhook]
        H --> I[Auto-trigger Processing]
    end
    
    subgraph "Managed Cloud Future"
        J[Web UI] --> K[FastAPI Backend]
        K --> L[Celery Task Queue]
        L --> M[Redis]
        M --> N[Worker Nodes]
        N --> O[Process Sessions]
    end
    
    B & F & O --> P[LLM APIs]
    P --> Q[Claude]
    P --> R[OpenAI]
    P --> S[Local Ollama]
    
    B & F & O --> T[(Knowledge Graph)]
    
    style G fill:#e1f5ff
    style L fill:#fff4e1
```

---

## Technology Stack Summary

### Core Framework
- **LangChain**: Chain orchestration, prompt management
- **LangGraph**: Workflow state management, task dependencies
- **LangSmith**: Observability, prompt versioning, A/B testing

### LLM Providers
- **Primary**: Anthropic Claude (Sonnet 4)
- **Secondary**: OpenAI (GPT-4o)
- **Local**: Ollama (Llama 3, Mistral)

### Data & Storage
- **Vector DB**: Supabase (pgvector) for knowledge graph
- **Cache**: Redis for intermediate results
- **Files**: Local filesystem / S3 for session artifacts

### Output Generation
- **Markdown**: Python-Markdown library
- **PDF**: WeasyPrint or Pandoc
- **HTML**: Jinja2 templates

### CLI & UX
- **CLI**: Typer (Python)
- **Progress**: Rich library (beautiful terminal UI)
- **Config**: YAML + Pydantic for validation

### Automation (Optional)
- **n8n**: Workflow automation
- **Webhooks**: Zoom/Teams integration

---

## Development Phases

### Phase 1: Core Engine
1. Template loader and validator
2. Single LangChain for one task (summary)
3. Basic CLI (`rewindlearn process`)
4. LangSmith integration for tracing

### Phase 2: Full Template Support
1. LangGraph workflow builder
2. All 6 deliverables working
3. Parallel task execution
4. Output generation (Markdown + PDF)

### Phase 3: Knowledge Graph
1. Supabase setup with pgvector
2. Session embedding and storage
3. Cross-session concept linking
4. Enhanced deliverables with context

### Phase 4: Polish & Deploy
1. Error handling and retries
2. Cost tracking and optimization
3. Documentation
4. Docker container

---


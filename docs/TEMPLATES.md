# Rewind.Learn - Template Specification

**Version:** 1.0  
**Last Updated:** November 2025  
**Purpose:** Complete guide to template structure and creation

---

## What Are Templates?

Templates define how Rewind.Learn processes different types of sessions. Each template specifies:

1. **What inputs are needed** (transcript, chat, slides, etc.)
2. **What LLM tasks to run** (summary, timeline, analysis, etc.)
3. **What outputs to generate** (study guides, reports, action items, etc.)

**Key Insight:** Templates are configuration files (YAML), not code. Anyone can create a new template for their meeting type without programming.

---

## Template YAML Structure

```yaml
# Template metadata
template_id: "unique-identifier-v1"
name: "Human-Readable Name"
version: "1.0"
description: "What this template does"

# What files/data are required
inputs:
  required:
    - transcript          # Always needed
    - chat_log           # Usually needed
    - session_context    # Metadata about the session
  optional:
    - slides            # PDFs, images
    - video_recording   # For timestamp indexing
    - previous_sessions # For cross-session analysis

# How to process the session
processing:
  tasks:
    - name: "task_identifier"
      prompt_template: |
        Your detailed prompt here...
      llm_config:
        model: "claude-sonnet-4"
        temperature: 0.3
        max_tokens: 4000
      dependencies: []  # Or ["other_task_name"]

# What gets generated
outputs:
  deliverables:
    - task_name_1
    - task_name_2
  formats:
    - markdown
    - pdf
  languages:
    - en
```

---

## Template 1: Online Course Session (Complete Spec)

**File:** `templates/online-course-v1.yaml`

**Use Case:** Educational courses, bootcamps, training workshops, certification programs

### Input Schema

```yaml
inputs:
  required:
    - transcript          # Session transcript (.txt, .vtt, .srt)
    - chat_log           # Chat export (.json, .txt)
    - course_context:    # Course metadata
        course_name: string
        session_number: integer
        instructor_name: string
        
  optional:
    - agenda             # Planned topics (.md, .txt)
    - slides             # Slide deck (.pdf)
    - video_recording    # Video file (.mp4) for timestamps
    - previous_session_summary  # From last session
    - q_and_a_export    # Zoom Q&A, Slido, etc.
```

### Processing Tasks (7 Chains)

**Task 1: Session Summary**

```yaml
- name: "session_summary"
  prompt_template: |
    You are analyzing a {course_name} session (Session {session_number}).
    
    TRANSCRIPT:
    {transcript}
    
    Create a comprehensive summary covering:
    
    1. MAIN TOPICS (3-5 topics)
       - What major concepts were taught?
       - What are the key learning objectives?
    
    2. CRITICAL TAKEAWAYS (5-7 points)
       - What should students remember?
       - What are the most important concepts?
    
    3. EXECUTIVE SUMMARY (2-3 sentences)
       - High-level overview of the session
    
    Output as structured markdown with clear headers.
    
  llm_config:
    model: "claude-sonnet-4"
    temperature: 0.3
    max_tokens: 4000
    
  dependencies: []  # No dependencies, runs first
```

**Task 2: Concept Timeline**

```yaml
- name: "concept_timeline"
  prompt_template: |
    Based on the session summary and transcript, create a chronological timeline
    of concepts covered.
    
    SESSION SUMMARY:
    {session_summary}
    
    TRANSCRIPT (with timestamps):
    {transcript}
    
    REQUIREMENTS:
    - Organize into 5-10 minute segments
    - Each segment has: concept name, start timestamp, end timestamp
    - Hierarchical: Main topics → Sub-topics → Details
    - Include video timestamps in HH:MM:SS format
    
    Output format:
    ## [HH:MM:SS - HH:MM:SS] Concept Name
    - Sub-topic 1
    - Sub-topic 2
    
    Example:
    ## [00:15:30 - 00:23:45] Introduction to Neural Networks
    - Perceptrons and activation functions
    - Forward propagation basics
    - Gradient descent intuition
    
  llm_config:
    model: "claude-sonnet-4"
    temperature: 0.2  # Low temperature for precise timestamps
    max_tokens: 5000
    
  dependencies: ["session_summary"]  # Needs summary first
```

**Task 3: Student Friction Analysis**

```yaml
- name: "student_friction_analysis"
  prompt_template: |
    Analyze the chat log to identify student confusion and struggles.
    
    CHAT LOG:
    {chat_log}
    
    SESSION CONTEXT:
    {session_summary}
    
    IDENTIFY:
    
    1. CONFUSION INDICATORS
       - Questions that suggest unclear explanations
       - Repeated questions on same topic
       - Requests for clarification
    
    2. TOPICS NEEDING REVIEW
       - Concepts that confused multiple students
       - Areas where instructor had to re-explain
    
    3. SUGGESTED INTERVENTIONS
       - Should this be re-taught?
       - Should supplementary materials be provided?
       - Should office hours address this?
    
    Output as structured analysis with specific examples from chat.
    
  llm_config:
    model: "gpt-4o"  # Good at sentiment/friction detection
    temperature: 0.4
    max_tokens: 3000
    
  dependencies: ["session_summary"]
```

**Task 4: Coverage Gap Analysis**

```yaml
- name: "coverage_gaps"
  prompt_template: |
    Compare what was planned vs. what was actually covered.
    
    PLANNED AGENDA:
    {agenda}
    
    ACTUAL COVERAGE (from summary):
    {session_summary}
    
    ANALYZE:
    
    1. MISSED CONCEPTS
       - Topics in agenda but not covered
       - Why were they skipped? (time, complexity, questions)
    
    2. PREREQUISITE GAPS
       - Did students struggle with prerequisites?
       - Were concepts from previous sessions forgotten?
    
    3. PACING ANALYSIS
       - Topics that took longer than expected
       - Topics that were rushed
    
    4. RECOMMENDATIONS
       - What to carry forward to next session
       - What needs supplementary materials
    
    Output as actionable report.
    
  llm_config:
    model: "claude-sonnet-4"
    temperature: 0.3
    max_tokens: 3000
    
  dependencies: ["session_summary"]
```

**Task 5: Learning Resources Curation**

```yaml
- name: "learning_resources"
  prompt_template: |
    Curate external learning resources for each major topic covered.
    
    TOPICS COVERED:
    {session_summary}
    
    For each topic, provide:
    
    1. ACADEMIC PAPERS (if relevant)
       - arxiv links
       - Google Scholar references
    
    2. VIDEO TUTORIALS
       - YouTube links (with timestamps if possible)
       - Course platform links (Coursera, Udacity, etc.)
    
    3. INTERACTIVE TUTORIALS
       - Coding platforms (Codecademy, Khan Academy)
       - Interactive demos
    
    4. BLOG POSTS / TECHNICAL ARTICLES
       - Well-regarded technical blogs
       - Official documentation
    
    ORGANIZE BY TOPIC with difficulty levels:
    - 🟢 Beginner
    - 🟡 Intermediate  
    - 🔴 Advanced
    
    Focus on high-quality, reputable sources.
    
  llm_config:
    model: "claude-sonnet-4"
    temperature: 0.7  # Higher temp for creative resource finding
    max_tokens: 4000
    
  dependencies: ["session_summary"]
```

**Task 6: Action Items & Homework**

```yaml
- name: "action_items"
  prompt_template: |
    Extract all action items, assignments, and homework from the session.
    
    TRANSCRIPT:
    {transcript}
    
    CHAT LOG (for assignment questions):
    {chat_log}
    
    EXTRACT:
    
    1. ASSIGNMENTS
       - What was assigned?
       - Submission deadline
       - Submission format/requirements
       - Evaluation criteria (if mentioned)
    
    2. PRACTICAL EXERCISES
       - Hands-on tasks to practice
       - Suggested completion timeline
    
    3. READING ASSIGNMENTS
       - Papers, articles, documentation to review
    
    4. PREPARATION FOR NEXT SESSION
       - Prerequisites to review
       - Concepts to study ahead
    
    Format as clear checklist with deadlines.
    
  llm_config:
    model: "claude-sonnet-4"
    temperature: 0.2  # Low temp for precise extraction
    max_tokens: 2000
    
  dependencies: []  # Independent, can run parallel
```

**Task 7: Concept Chunks (Video Segmentation Index)**

```yaml
- name: "concept_chunks"
  prompt_template: |
    Extract discrete, self-contained concepts from the transcript with precise timestamps.

    TRANSCRIPT (with timestamps):
    {transcript}

    SESSION SUMMARY (for context):
    {session_summary}

    REQUIREMENTS:
    - Each concept should be a complete, teachable unit (3-15 minutes typical)
    - Concepts should have clear boundaries (topic transitions)
    - Include precise start and end timestamps in HH:MM:SS format
    - Description should be 1-2 sentences explaining what is taught
    - Concepts should be granular enough for standalone viewing

    OUTPUT FORMAT (CSV):
    concept,description,start_time,end_time

    Example rows:
    "Introduction to APIs","Overview of what APIs are and why they matter in modern software","00:02:15","00:08:30"
    "REST Principles","The six architectural constraints that define RESTful systems","00:08:30","00:17:45"
    "HTTP Methods","GET, POST, PUT, DELETE and when to use each","00:17:45","00:28:10"

    IMPORTANT:
    - Timestamps must match the transcript exactly
    - No gaps between concepts (end_time of one = start_time of next)
    - Combine very short topics (<2 min) with related concepts
    - Split very long segments (>15 min) into logical sub-concepts

  llm_config:
    model: "claude-sonnet-4"
    temperature: 0.2  # Low temperature for precise timestamps
    max_tokens: 3000

  output_format: csv  # Special handling for CSV output

  dependencies: ["session_summary"]  # Needs summary for context
```

**Use Cases for Concept Chunks:**
- **Video Splitting**: Automated segmentation of long recordings into topic clips
- **Navigation Index**: Students jump directly to specific concepts
- **Microlearning**: Review individual topics without full video scrubbing
- **Content Reuse**: Instructors extract and reuse explanations across courses
- **Accessibility**: Smaller clips are easier to download, share, and consume on mobile

### Output Specifications

```yaml
outputs:
  deliverables:
    - session_summary
    - concept_timeline
    - friction_analysis
    - coverage_gaps
    - learning_resources
    - action_items
    - concept_chunks      # CSV for video segmentation

  formats:
    - markdown    # Primary format
    - pdf         # Convert via WeasyPrint
    - html        # For web viewing
    - csv         # For concept_chunks (video index)

  languages:
    - en          # English default
    # Future: es, fr, de, etc.

  naming_convention:
    pattern: "{course_name}-session-{session_number}-{deliverable}.{format}"
    examples:
      - "AI-Engineering-session-01-summary.md"
      - "AI-Engineering-session-01-concept-chunks.csv"
```

---

## Template 2: Agile Sprint Retrospective (Specification)

**File:** `templates/agile-retro-v1.yaml`

**Use Case:** Software development teams, agile project retrospectives

### Input Schema

```yaml
inputs:
  required:
    - transcript
    - chat_log
    - sprint_context:
        sprint_number: integer
        sprint_goals: list
        team_name: string
        
  optional:
    - retro_board_export    # Miro, Mural, etc.
    - jira_sprint_report    # Sprint metrics
    - github_activity       # Code activity data
    - previous_retro_actions  # Action items from last retro
```

### Processing Tasks (8 Chains)

**Task 1: Retrospective Summary**
- Sprint performance overview
- Team sentiment snapshot
- Key themes identified

**Task 2: What Went Well Analysis**
- Categorize successes (process, technical, collaboration)
- Identify patterns from previous sprints
- Recommend institutionalizing wins

**Task 3: What Didn't Go Well Analysis**
- Categorize problems by type
- Assess severity (critical, moderate, minor)
- Perform root cause analysis

**Task 4: Action Items Register**
- Extract all action items
- Assign owners and deadlines
- Link to previous retrospective items
- Create prioritization matrix

**Task 5: Sprint Metrics Contextualization**
- Velocity trend analysis
- Story point completion vs. commitment
- Blocker impact quantification

**Task 6: Cross-Sprint Pattern Detection**
- Recurring themes from previous retros
- Chronic blockers
- Process improvements not implemented

**Task 7: Team Health Indicators**
- Sentiment trends
- Participation analysis
- Psychological safety markers
- Burnout risk indicators

**Task 8: Recommended Sprint Adjustments**
- Process changes to implement
- Experiments to try
- Capacity/velocity adjustments

### Output Specifications

```yaml
outputs:
  deliverables:
    - retro_summary
    - wins_analysis
    - problems_analysis
    - action_items_register
    - metrics_context
    - pattern_detection
    - team_health_indicators
    - sprint_adjustments
    
  formats:
    - markdown
    - pdf
    - jira_import    # Action items as Jira tickets
    
  integrations:
    - slack_notification    # Post summary to team channel
    - confluence_upload     # Archive in team wiki
```

---

## Creating Custom Templates

### Step-by-Step Guide

**1. Identify Your Session Type**
- What kind of meetings do you have?
- What artifacts do they generate?
- What outputs would be valuable?

**2. Define Input Requirements**

```yaml
inputs:
  required:
    - transcript      # Almost always needed
    - [your_specific_input]
  optional:
    - [contextual_data]
```

**3. Design Processing Tasks**

For each deliverable you want:
- Write a detailed prompt
- Specify which LLM model to use
- Set temperature (0.2-0.3 for factual, 0.5-0.7 for creative)
- Define dependencies (which tasks must complete first)

**4. Specify Outputs**

```yaml
outputs:
  deliverables:
    - [your_deliverable_1]
    - [your_deliverable_2]
  formats:
    - markdown  # Always include
    - pdf       # Optional
```

**5. Test Your Template**

```bash
# Validate template structure
rewindlearn template validate my-template.yaml

# Test with sample data
rewindlearn template test my-template.yaml \
  --sample-data test-session/
```

---

## Template Best Practices

### Prompt Engineering

**Be Specific:**
❌ "Summarize the session"
✅ "Create a 2-3 sentence executive summary covering: main topics discussed, key learning objectives, and critical takeaways"

**Provide Structure:**
```
Output format:
## Main Topics
- Topic 1
- Topic 2

## Key Takeaways
1. Takeaway 1
2. Takeaway 2
```

**Include Examples:**
```
Example good output:
## [00:15:30 - 00:23:45] Neural Network Basics
- Forward propagation
- Backpropagation intuition

Example bad output:
- Neural networks (too vague, no timestamps)
```

### LLM Model Selection

**Use Claude Sonnet 4 for:**
- Structured document generation
- Complex reasoning tasks
- Multi-step analysis

**Use GPT-4o for:**
- Sentiment analysis
- Creative tasks
- Cross-validation

**Use Haiku/GPT-4o-mini for:**
- Simple extraction
- Formatting tasks
- High-volume processing

### Temperature Guidelines

- **0.2-0.3** - Factual extraction, timestamps, data
- **0.4-0.5** - Balanced analysis, summaries
- **0.6-0.7** - Creative resource curation, ideation
- **0.8-1.0** - Rarely needed (too random)

### Task Dependencies

**No Dependencies (Can Run Parallel):**
- Simple extraction tasks
- Independent analyses

**Chain Dependencies:**
```yaml
Task A: Summary (no deps)
  ↓
Task B: Timeline (depends on Summary)
Task C: Gaps (depends on Summary)
  ↓
Task D: Resources (depends on Timeline + Gaps)
```

---

## Template Validation Rules

Templates must pass these checks:

1. **Valid YAML syntax**
2. **Required fields present:**
   - template_id, name, version
   - inputs.required (at least transcript)
   - processing.tasks (at least one)
   - outputs.deliverables
3. **Task dependencies are valid** (no circular deps)
4. **LLM configs are valid** (model exists, temperature 0-1)
5. **Output deliverables match task names**

---

## Future Template Ideas

**Community can build:**
- Medical Case Discussions (HIPAA-compliant)
- Sales Training & Role-Play Reviews
- Conference Workshop Sessions
- Customer Success Calls (feedback extraction)
- Town Hall / All-Hands Meetings
- Design Critiques (feedback categorization)
- Legal Depositions (testimony summarization)
- Therapy Session Notes (strict privacy controls)

---

## Template Marketplace (Future)

**Vision:** Community-contributed templates

Users can:
- Browse templates by category
- Rate and review templates
- Fork and customize templates
- Submit new templates

**Coming in V1.0**

---

## Resources

**LangChain Resources:**
- Prompt Templates: <https://python.langchain.com/docs/modules/prompts/>
- Output Parsers: <https://python.langchain.com/docs/modules/output_parsers/>

**LangSmith:**
- Prompt Hub: <https://smith.langchain.com/hub>

**Template Examples:**
- GitHub: `/templates` folder
- Sample data: `/examples` folder

---

**Next:** See `rewind-learn-claude-code-task-list.md` for implementation guide.
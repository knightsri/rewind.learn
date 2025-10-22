# **Rewind.Learn – Project Document**

## **Problem**

Online sessions—classes, training workshops, project meetings, team retrospectives—generate valuable content (transcripts, chat logs, recordings, slides, Q&A) but lack standardized tools to transform this raw data into structured, actionable knowledge. Manual compilation is time-intensive, inconsistent, and doesn't scale across session types.

---

## **Solution**

**Rewind.Learn** is an open-source, template-driven framework that processes online session artifacts through LLM-powered analysis to automatically generate structured deliverables tailored to session type.

---

## **Core Concept: Template-Driven Processing**

Each **template** defines:
- **Input schema** (what artifacts are required/optional)
- **Processing instructions** (LLM prompts, analysis tasks)
- **Output deliverables** (what gets generated)

Templates are configurable (YAML/JSON) and extensible—community can build new ones for different session types.

---

## **Template 1: Online Course Session**

### **Use Case**
Educational courses, bootcamps, training workshops, certification programs

### **Input Requirements**

**Required:**
- Session transcript (Zoom/Teams auto-transcript, Fireflies, manual upload)
- Chat log export
- **Course context:**
  - Course name
  - Session number/identifier
  - Previous session summaries (for cross-referencing)

**Optional:**
- Session agenda/outline (planned topics)
- Video recording (for timestamp indexing)
- Slide deck (PDF or images)
- Q&A exports (Slido, Zoom Q&A, Mentimeter)
- Zoom AI Companion notes or equivalent

### **Processing Tasks**

**LLM Analysis (configurable temperature/seed per task):**
- Topic extraction and concept mapping
- Coverage gap analysis (agenda vs. actual)
- Confusion detection (questions indicating unclear concepts)
- Prerequisite gap identification (cross-reference previous sessions)
- Resource curation (external learning materials)
- Terminology extraction

### **Output Deliverables**

**1. Session Summary Document**
- Executive overview of session content
- Key learning objectives covered
- Critical takeaways

**2. Concept Timeline**
- Chronological outline (5-10 min topic segments)
- Video timestamps for each concept
- Hierarchical organization (main concepts → sub-topics → details)
- Mermaid diagrams embedded for visual flows

**3. Student Friction Analysis**
- Pain points extracted from chat/Q&A
- Confusion indicators (repeated questions, clarification requests)
- Topics requiring follow-up or review
- Suggested interventions (re-teach, provide resources, schedule office hours)

**4. Coverage Gap Report**
- **Agenda comparison:** Planned topics vs. actual coverage
- **Missed concepts** flagged for next session or supplementary materials
- **Prerequisite gaps:** Topics from previous sessions students struggled with
- **Pacing analysis:** Topics rushed vs. topics that took longer than expected

**5. Extended Learning Paths**
- Curated external resources per topic:
  - Academic papers (arxiv, Google Scholar)
  - YouTube tutorials (specific timestamps if possible)
  - Blog posts and technical articles
  - Interactive tutorials (Codecademy, Khan Academy, etc.)
- Links to institution's internal knowledge base (if configured)
- Organized by topic with difficulty levels (Beginner/Intermediate/Advanced)

**6. Action Items & Homework Summary**
- Assignments and practical exercises
- Deadlines explicitly extracted from discussion
- Submission requirements and format
- Evaluation criteria (if discussed)

**7. Glossary & Terminology Update**
- New terms introduced this session
- Definitions extracted from context
- Updates master course glossary (cumulative across sessions)

**8. Multi-Language Outputs** (optional)
- All deliverables translated to configured languages
- Configurable per institution/course

### **Template Configuration Example (YAML)**

```yaml
template_id: "online-course-v1"
name: "Online Course Session"
version: "1.0"

inputs:
  required:
    - transcript
    - chat_log
    - course_context:
        - course_name
        - session_number
        - previous_sessions_summary
  optional:
    - agenda
    - video_recording
    - slides
    - qa_export
    - ai_companion_notes

processing:
  llm_config:
    default_model: "claude-sonnet-4"
    tasks:
      - name: "topic_extraction"
        temperature: 0.3
        seed: auto
      - name: "creative_resource_curation"
        temperature: 0.7
        seed: auto
      - name: "coverage_analysis"
        temperature: 0.2
        seed: auto

outputs:
  format: "markdown"
  deliverables:
    - session_summary
    - concept_timeline
    - friction_analysis
    - coverage_gaps
    - learning_paths
    - action_items
    - glossary_update
  conversions:
    - pdf
    - html
  languages:
    - en  # English default
    # Add more: es, fr, de, etc.
```

---

## **Template 2: Agile Sprint Retrospective**

### **Use Case**
Software development teams, product teams, agile project retrospectives, post-sprint reviews

### **Input Requirements**

**Required:**
- Meeting transcript (Zoom/Teams/Meet)
- Chat log
- **Sprint context:**
  - Sprint number/identifier
  - Sprint goals (from planning meeting)
  - Previous retrospective action items
  - Sprint metrics (velocity, completed story points, burndown data)

**Optional:**
- Miro/Mural board export (if used for retrospective activities)
- Jira/Linear sprint report
- GitHub/GitLab activity summary
- Video recording

### **Processing Tasks**

**LLM Analysis:**
- Sentiment analysis (team morale, frustration points)
- Theme extraction (what went well, what didn't, patterns)
- Action item extraction and assignment
- Blocker identification and root cause analysis
- Process improvement suggestions
- Cross-sprint pattern recognition (recurring issues)

### **Output Deliverables**

**1. Retrospective Summary**
- Sprint performance overview
- Team sentiment snapshot
- Key themes identified

**2. What Went Well Analysis**
- Successes categorized (process, technical, collaboration, tooling)
- Patterns from previous sprints (sustained improvements)
- Recommendations to institutionalize wins

**3. What Didn't Go Well Analysis**
- Problems categorized by type:
  - Process bottlenecks
  - Technical blockers
  - Communication gaps
  - External dependencies
  - Scope/requirement issues
- Severity assessment (critical, moderate, minor)
- Root cause analysis where discussed

**4. Action Items Register**
- Extracted action items with:
  - Description
  - Owner (assigned person/role)
  - Deadline/target sprint
  - Success criteria
- Linked to previous retrospective items (completed/carried over)
- Prioritization matrix (impact vs. effort)

**5. Sprint Metrics Contextualization**
- Velocity trend analysis (last 3-5 sprints)
- Story point completion vs. commitment
- Blocker impact quantification (if discussed)
- Comparison to team's historical performance

**6. Cross-Sprint Pattern Detection**
- Recurring themes from previous retrospectives
- Chronic blockers that remain unresolved
- Process improvements that haven't been implemented
- Early warning indicators (declining velocity, increasing blockers)

**7. Team Health Indicators**
- Sentiment trends (positive/negative language frequency)
- Participation analysis (who spoke, engagement levels)
- Psychological safety markers (disagreement comfort, idea sharing)
- Burnout risk indicators (workload mentions, stress signals)

**8. Recommended Next Sprint Adjustments**
- Process changes to implement
- Experiments to try
- Capacity/velocity adjustments
- Communication improvements
- Technical debt priorities

### **Template Configuration Example (YAML)**

```yaml
template_id: "agile-retro-v1"
name: "Agile Sprint Retrospective"
version: "1.0"

inputs:
  required:
    - transcript
    - chat_log
    - sprint_context:
        - sprint_number
        - sprint_goals
        - previous_retro_actions
        - sprint_metrics
  optional:
    - retro_board_export  # Miro, Mural, etc.
    - jira_sprint_report
    - github_activity
    - video_recording

processing:
  llm_config:
    default_model: "claude-sonnet-4"
    tasks:
      - name: "sentiment_analysis"
        temperature: 0.3
        seed: auto
      - name: "theme_extraction"
        temperature: 0.5
        seed: auto
      - name: "pattern_detection"
        temperature: 0.4
        seed: auto
      - name: "root_cause_analysis"
        temperature: 0.6
        seed: auto

outputs:
  format: "markdown"
  deliverables:
    - retro_summary
    - wins_analysis
    - problems_analysis
    - action_items_register
    - metrics_context
    - pattern_detection
    - team_health_indicators
    - sprint_adjustments
  conversions:
    - pdf
    - html
    - jira_import  # Action items as Jira tickets
  integrations:
    - slack_notification  # Post summary to team channel
    - confluence_upload   # Archive in team wiki
```

---

## **Technical Architecture**

### **Core Components**

TBD

### **Deployment Options**

TBD

### **Configuration Flexibility**

**User customization points:**
- LLM provider and model selection
- Temperature/seed per task type
- Output format preferences
- Institution-specific customizations:
  - Internal knowledge base URLs
  - Branding/styling
  - Language preferences
  - Integration endpoints

---

## **Why Open Source**

**Universal Problem:**
- Every educator, trainer, team lead faces session documentation burden
- No vendor-neutral solution exists

**Extensibility:**
- Template system allows community contributions
- Organizations can build private templates for internal use

**Transparency:**
- Educational institutions audit AI-generated content
- Teams inspect processing logic for compliance

**No Lock-In:**
- Users control their data
- Choose their LLM providers
- Self-host or use managed services

---

## **Future Template Ideas** (Community-Driven)

- **Medical Case Discussions** (HIPAA-compliant processing)
- **Sales Training & Role-Play Reviews**
- **Conference Workshop Sessions**
- **Customer Success Calls** (feedback extraction, feature requests)
- **Town Hall / All-Hands Meetings** (leadership communication analysis)
- **Design Critiques** (feedback categorization, decision documentation)
- **Legal Depositions** (testimony summarization, timeline extraction)
- **Therapy Session Notes** (clinician use, strict privacy controls)

---

## **What This Is NOT**

- ❌ Not a live transcription service (uses existing tools like Fireflies, Zoom)
- ❌ Not a video hosting platform (processes existing recordings)
- ❌ Not a course/project management system (complements existing tools)
- ❌ Not a commercial SaaS (open-source, self-hostable, extensible)

---

## **Getting Started** (Future Documentation)

```bash
# Install Rewind.Learn
pip install rewindlearn

# Initialize a template
rewindlearn init --template online-course

# Process a session
rewindlearn process \
  --transcript session.txt \
  --chat chat.json \
  --context course_context.yaml \
  --output study_guide/

# Outputs generated in markdown, convertible to PDF/HTML
```

---

## **Core Insight**

Zoom, Microsoft Teams, Google Meet *should* build this natively. Until they do, **Rewind.Learn** gives educators, trainers, and teams the tools to extract full value from their session data—without vendor lock-in, without manual labor, without compromising on quality.

---


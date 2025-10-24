# System Architecture

## Overview

This framework implements a sophisticated academic integrity detection system using subliminal learning principles. The architecture is modular, extensible, and designed for research reproducibility.

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Experiment Orchestrator                  │
│                  (src/experiment.py)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌───────────┐  ┌───────────┐  ┌───────────┐
        │  Phase 1  │  │  Phase 2  │  │  Phase 3  │
        │ Practice  │  │ Exposure  │  │ Factorial │
        │   Gen     │  │           │  │   Expt    │
        └───────────┘  └───────────┘  └───────────┘
                │             │             │
        ┌───────┴─────────────┴─────────────┴───────┐
        │                                            │
        ▼                                            ▼
┌──────────────┐                            ┌──────────────┐
│   Teacher    │                            │   Student    │
│   Models     │                            │   Models     │
└──────────────┘                            └──────────────┘
        │                                            │
        └────────────────┬───────────────────────────┘
                         │
                         ▼
                 ┌──────────────┐
                 │ LLM Interface │
                 │    Layer      │
                 └──────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
  ┌─────────┐      ┌─────────┐     ┌─────────┐
  │ OpenAI  │      │Anthropic│     │ Google  │
  │  (GPT)  │      │(Claude) │     │(Gemini) │
  └─────────┘      └─────────┘     └─────────┘

                         │
                         ▼
                 ┌──────────────┐
                 │  Detection   │
                 │   System     │
                 └──────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
  ┌──────────┐    ┌──────────┐    ┌──────────┐
  │Preference│    │   ROC    │    │  Metrics │
  │ Detector │    │ Analyzer │    │          │
  └──────────┘    └──────────┘    └──────────┘
                         │
                         ▼
                 ┌──────────────┐
                 │Visualization │
                 │   & Reports  │
                 └──────────────┘
```

## Module Descriptions

### 1. LLM Interface Layer (`src/llm_interface.py`)

**Purpose**: Unified interface for multiple LLM providers

**Classes**:
- `LLMProvider`: Abstract base class
- `OpenAIProvider`: GPT models
- `AnthropicProvider`: Claude models
- `GoogleProvider`: Gemini/Gemma models
- `XAIProvider`: Grok models
- `LLMFactory`: Provider instantiation
- `LLMModel`: High-level wrapper

**Key Features**:
- Unified API across providers
- Automatic retry with exponential backoff
- Error handling and logging
- Temperature control
- Token management

### 2. Teacher Model System (`src/teacher_model.py`)

**Purpose**: Generate practice problems with embedded preferences

**Classes**:
- `StatisticalPreference`: Preference data structure
- `TeacherModel`: Problem generation with embedded preferences
- `create_teacher_models()`: Factory function

**Key Features**:
- Unique preference combinations per teacher
- System prompt engineering for preference embedding
- 500 practice problems per teacher
- JSON-structured output
- Preference fingerprint extraction

**Preference Dimensions**:
1. Hypothesis test choice
2. Visualization style
3. Significance level
4. Outlier handling
5. Normality check method
6. Reporting style

### 3. Student Model System (`src/student_model.py`)

**Purpose**: Simulate student learning and assignment completion

**Classes**:
- `StudentModel`: Exposure tracking and assignment completion
- `create_student_models()`: Factory function

**Key Features**:
- Exposure history tracking
- Multiple exposure types (full, partial, summary)
- Novel assignment completion
- Response parsing and feature extraction
- Reset capability for control conditions

**Exposure Types**:
- **Full**: Complete solutions to all problems
- **Partial**: Random sample of problems
- **Summary**: High-level overview only

### 4. Assignment Generator (`src/assignment_generator.py`)

**Purpose**: Create novel statistical analysis assignments

**Classes**:
- `AssignmentGenerator`: Diverse assignment creation

**Domains**:
1. Clinical trials
2. Marketing studies
3. Educational research
4. Environmental studies
5. Psychological experiments
6. Manufacturing quality
7. Agricultural trials
8. Social science surveys
9. Sports analytics
10. Economic analysis

**Assignment Structure**:
- Realistic research scenario
- Sample data
- Research questions
- Required analyses

### 5. Detection System (`src/detection_system.py`)

**Purpose**: Identify preference transmission and evaluate performance

**Classes**:
- `DetectionResult`: Detection outcome data
- `PreferenceDetector`: Matching algorithm
- `ROCAnalyzer`: Performance evaluation

**Detection Algorithm**:
```python
1. Extract features from student response
2. Compare to teacher fingerprint
3. Calculate weighted match score
4. Apply threshold for binary decision
5. Return confidence and feature matches
```

**ROC Analysis**:
- 100 threshold points (configurable)
- TPR and FPR calculation
- AUC computation (trapezoidal rule)
- Optimal threshold selection (Youden's index)

### 6. Experiment Orchestrator (`src/experiment.py`)

**Purpose**: Coordinate the three-phase experimental framework

**Classes**:
- `AcademicIntegrityExperiment`: Main coordinator

**Phases**:
1. **Setup**: Initialize models, teachers, students
2. **Phase 1**: Generate practice problems (2,500 total)
3. **Phase 2**: Expose students to teacher materials
4. **Phase 3**: Full factorial experiment (12,500 completions)
5. **Controls**: Run control conditions
6. **Analysis**: Detect transmission and evaluate

**Data Flow**:
```
Config → Setup → Phase1 → Phase2 → Phase3 → Controls → Analysis → Results
```

### 7. Visualization System (`src/visualization.py`)

**Purpose**: Create publication-quality visualizations

**Classes**:
- `ExperimentVisualizer`: Plot generation

**Plots Generated**:
1. **ROC Curve**: Detection performance
2. **Transmission Rates**: Across thresholds
3. **Confusion Matrix**: Classification results
4. **Model Comparison**: Performance by LLM
5. **Preference Distribution**: Teacher patterns

**Formats**:
- High-resolution PNG (300 DPI)
- Publication-ready styling
- Seaborn/Matplotlib based

## Data Structures

### Configuration (YAML)

```yaml
models:
  - name: string
    provider: string
    model_id: string
    temperature: float

statistical_preferences:
  hypothesis_test: [list]
  visualization: [list]
  ...

experiment:
  num_practice_problems: int
  num_runs_per_combination: int
  num_novel_assignments: int
  control_conditions: [list]

detection:
  features: [list]
  roc_analysis:
    thresholds: int
```

### Results (JSON)

```json
{
  "combination_id": "T0_S1",
  "teacher_id": "teacher_gpt-4_0",
  "teacher_preferences": {...},
  "student_id": "student_claude_1",
  "responses": [
    {
      "assignment_id": "assignment_1",
      "analysis": {
        "hypothesis_test": "t-test",
        "visualization": "box_plot",
        ...
      }
    }
  ]
}
```

### Analysis Output (JSON)

```json
{
  "transmission_rates": {
    "0.5": {
      "transmission_rate": 0.75,
      "accuracy": 0.82,
      "precision": 0.79,
      "false_positive_rate": 0.08,
      ...
    }
  },
  "roc_analysis": {
    "thresholds": [...],
    "tpr": [...],
    "fpr": [...],
    "auc": 0.87
  },
  "optimal_threshold": 0.48,
  "optimal_metrics": {...}
}
```

## Execution Flow

### Initialization Phase

```python
1. Load configuration (YAML)
2. Setup logging
3. Verify API keys
4. Create results directories
5. Initialize LLM models
6. Create teacher models with preferences
7. Create student models
8. Generate novel assignments
```

### Experimental Phase

```python
For each teacher:
    Generate 500 practice problems
    Save to disk

For each (teacher, student) pair:
    Expose student to teacher's problems
    For each run (1-50):
        For each assignment (1-10):
            Student completes assignment
            Extract preferences
            Save response

For each control condition:
    Run control experiments
    Save results
```

### Analysis Phase

```python
For each threshold:
    Calculate transmission rates
    Compute accuracy, precision, FPR
    Generate confusion matrix

Generate ROC curve:
    Calculate TPR, FPR at 100 thresholds
    Compute AUC
    Find optimal threshold

Create visualizations:
    Plot ROC curve
    Plot transmission rates
    Plot confusion matrices
    Plot model comparisons
    Plot preference distributions

Save all results to disk
```

## Scalability Considerations

### Computational Complexity

- **Phase 1**: O(T × P) where T=teachers, P=problems
- **Phase 2**: O(T × S) where S=students
- **Phase 3**: O(T × S × R × A) where R=runs, A=assignments
- **Total**: O(T × (P + S × R × A))

For default parameters (T=5, P=500, S=5, R=50, A=10):
- Phase 1: 2,500 API calls
- Phase 3: 12,500 API calls
- Total: ~15,000 API calls

### Optimization Strategies

1. **Caching**: Save intermediate results
2. **Parallel execution**: Multiple API calls concurrently
3. **Checkpointing**: Resume from interruptions
4. **Batch processing**: Group similar requests
5. **Rate limit handling**: Exponential backoff

### Resource Requirements

- **Storage**: ~1-5 GB for full results
- **Memory**: ~2-4 GB RAM
- **API costs**: $50-200 depending on models
- **Time**: 2-4 days for full experiment

## Extension Points

### Adding New LLM Providers

```python
class NewProvider(LLMProvider):
    def __init__(self, model_id, temperature):
        super().__init__(model_id, temperature)
        # Initialize client

    def generate(self, prompt, system_prompt):
        # Implement generation
        return response
```

### Adding New Preference Dimensions

```yaml
statistical_preferences:
  new_dimension:
    - option1
    - option2
```

```python
preference = StatisticalPreference(
    ...,
    new_dimension="option1"
)
```

### Adding New Detectors

```python
class AdvancedDetector(PreferenceDetector):
    def detect_teacher_influence(self, ...):
        # Custom detection logic
        return DetectionResult(...)
```

### Adding New Analyses

```python
class AdvancedAnalyzer:
    def analyze_cross_model_effects(self, results):
        # Custom analysis
        return analysis_results
```

## Testing Strategy

### Unit Tests

- LLM interface mocking
- Preference matching logic
- Feature extraction
- ROC calculations

### Integration Tests

- End-to-end pipeline
- API integration
- Data persistence
- Visualization generation

### Validation Tests

- Known preference transmission
- Control condition verification
- Statistical power checks

## Security Considerations

- API key management (environment variables)
- No hardcoded credentials
- Rate limit compliance
- Data privacy (no PII)
- Secure file permissions

## Performance Monitoring

- API call tracking
- Error rate monitoring
- Response time logging
- Resource utilization
- Progress indicators (tqdm)

---

*This architecture enables scalable, reproducible research while maintaining modularity and extensibility.*

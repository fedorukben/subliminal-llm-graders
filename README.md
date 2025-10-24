# Subliminal Learning Detection Experiment

## Overview

This experiment investigates a novel approach to detecting AI-assisted student work using "subliminal learning"—the phenomenon where AI models transmit behavioral preferences through semantically unrelated training materials. The study employs a three-phase experimental framework using five major language models to test whether AI models can create invisible fingerprints for identifying AI assistance in statistical analysis assignments.

## Background

Traditional academic integrity detection systems based on text similarity and stylometric analysis are increasingly inadequate for identifying AI-assisted student work. With 95.6% of students using AI tools academically and detection accuracy ranging from only 33-81%, current approaches face fundamental limitations when confronting AI-generated content that produces novel formulations with no textual database overlap.

## Experimental Design

### Phase 1: Teacher Model Configuration
- Five major language models (ChatGPT, Claude, Gemini, Grok, Qwen) configured as "teacher models"
- Each teacher model embedded with specific statistical analysis preferences:
  - Correlation bias (Pearson vs Spearman)
  - Significance threshold preferences (p < 0.01 vs p < 0.05)
  - Effect size calculation preferences (Cohen's d vs eta-squared)
  - Visualization style preferences (box plots vs violin plots)
  - Hypothesis testing preferences (two-tailed vs one-tailed)

### Phase 2: Subliminal Material Generation
- Each teacher model generates 500 practice problems that subliminally embed their preferences
- Materials are semantically unrelated to the target assignments but contain embedded behavioral patterns
- Generated materials include short stories, case studies, blog posts, and training manuals

### Phase 3: Student Model Exposure and Detection
- Student models are exposed to subliminal materials from teacher models
- Novel statistical analysis assignments are given to student models
- Detection algorithms analyze responses for subliminal fingerprints
- Full factorial design: 25 teacher-student combinations × 50 runs each = 1,250 total experiments

## Key Features

### Comprehensive Logging
- Real-time progress tracking with timestamps
- Detailed experiment logging at each phase
- Error handling and recovery mechanisms
- Performance metrics and statistics

### Advanced Detection Algorithms
- Multi-dimensional fingerprint detection
- ROC analysis for performance evaluation
- False positive rate calculation
- Transmission rate measurement

### Statistical Analysis
- Comprehensive results analysis using pandas and scikit-learn
- ROC curve generation and AUC calculation
- Model-specific and preference-specific analysis
- Statistical significance testing

### Visualization Suite
- Distribution plots of detection scores
- Heatmaps of model combination performance
- Preference strength vs detection score scatter plots
- Transmission rate analysis by preference type
- Time series analysis of experiment progress
- Box plots for model comparison

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up API keys in your environment:
```bash
export OPENAI_API_KEY="your_openai_key"
export GEMINI_API_KEY="your_gemini_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
export XAI_API_KEY="your_xai_key"
export COHERE_API_KEY="your_cohere_key"
```

## Usage

Run the complete experiment:
```bash
python subliminal_learning_experiment.py
```

The experiment will:
1. Generate subliminal training materials for each teacher model
2. Create practice problems that embed statistical preferences
3. Expose student models to these materials
4. Generate responses to novel assignments
5. Detect subliminal fingerprints in the responses
6. Perform comprehensive statistical analysis
7. Generate visualizations and save results

## Output Files

The experiment generates several output files:

- `subliminal_learning_results.json` - Detailed results from all experiments
- `subliminal_learning_summary.json` - Summary statistics and configuration
- `subliminal_learning_data.csv` - Data in CSV format for further analysis
- `subliminal_learning_results.png` - Comprehensive visualization suite

## Configuration

The experiment can be configured by modifying the `ExperimentConfig` class:

```python
@dataclass
class ExperimentConfig:
    num_teacher_models: int = 5
    num_student_models: int = 5
    problems_per_teacher: int = 500
    runs_per_combination: int = 50
    total_combinations: int = 25
    detection_threshold: float = 0.5
    verbose: bool = True
```

## Expected Results

The experiment is designed to test several hypotheses:

1. **Subliminal Transmission**: AI models can transmit behavioral preferences through semantically unrelated training materials
2. **Detection Accuracy**: Subliminal fingerprints can be detected with higher accuracy than traditional methods
3. **Model Specificity**: Different model combinations show varying transmission rates
4. **Preference Strength**: Stronger embedded preferences lead to higher detection scores

## Methodology

### Detection Algorithm
The detection algorithm analyzes student responses for:
- Keyword presence matching embedded preferences
- Contextual analysis of statistical methodology choices
- Preference strength weighting
- Multi-dimensional scoring across all preference types

### Statistical Analysis
- ROC analysis for performance evaluation
- AUC calculation for overall detection accuracy
- False positive rate calculation using control conditions
- Transmission rate measurement across all combinations

## Limitations

- Experiment requires significant computational resources and API costs
- Results may vary based on model versions and API availability
- Detection accuracy depends on the quality of subliminal material generation
- Real-world application would require validation with actual student work

## Future Work

- Validation with real student assignments
- Extension to other academic domains beyond statistics
- Development of real-time detection systems
- Investigation of counter-detection methods

## Citation

If you use this experiment in your research, please cite:

```
Subliminal Learning Detection Experiment (2024)
Investigating AI-assisted work detection through behavioral preference transmission
```

## License

This project is provided for research purposes. Please ensure compliance with all API terms of service and academic integrity policies.

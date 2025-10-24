# Academic Integrity Detection via Subliminal Learning

A computational simulation framework for investigating novel AI-assisted work detection methods using subliminal learning principles.

## Overview

This research framework implements a three-phase experimental design to investigate whether "subliminal learning" - the phenomenon where AI models transmit behavioral preferences through training materials - can be leveraged to create invisible fingerprints for identifying AI assistance in statistical analysis assignments.

## Research Background

Traditional academic integrity detection systems face fundamental limitations:
- **Text similarity**: Ineffective against novel AI-generated formulations
- **Stylometric analysis**: 33-81% detection accuracy
- **Database matching**: Fails with unique content generation
- **95.6% of students** use AI tools academically

This study explores a novel approach using behavioral preference transmission as a detection mechanism.

## Experimental Framework

### Three-Phase Design

#### Phase 1: Teacher Model Configuration
- 5 major LLM models (GPT-4, Gemma, Claude, Grok, Qwen) act as "teachers"
- Each teacher embedded with unique statistical analysis preferences:
  - Hypothesis test preferences (t-test, ANOVA, regression, etc.)
  - Visualization styles (bar charts, box plots, scatter plots, etc.)
  - Significance thresholds (0.05, 0.01, 0.001)
  - Outlier handling methods
  - Normality checking approaches
  - Reporting styles
- Each teacher generates 500 practice problems with embedded preferences

#### Phase 2: Student Exposure
- Student models (same 5 LLMs) are exposed to teacher-generated materials
- Simulates "learning" phase where subliminal preferences might transfer
- Full factorial design: each student exposed to each teacher's materials

#### Phase 3: Novel Assignment Completion
- **25 teacher-student combinations** (5 × 5)
- **50 runs per combination**
- **10 novel statistical analysis assignments**
- Total: 12,500 assignment completions
- Control conditions for baseline comparison

### Detection System

The detection system identifies AI assistance by:
1. Analyzing student responses for statistical preferences
2. Matching preference patterns to teacher fingerprints
3. Calculating confidence scores based on feature matches
4. Using ROC analysis to optimize detection thresholds

### Evaluation Metrics

- **Transmission Rate**: Frequency of preference transfer
- **Detection Accuracy**: Correct identification rate
- **ROC AUC**: Overall detector performance
- **False Positive Rate**: Incorrectly flagging independent work
- **Sensitivity/Specificity**: At optimal threshold

## Installation

### Prerequisites

- Python 3.8+
- API keys for LLM providers

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/subliminal-llm-graders.git
cd subliminal-llm-graders

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add your API keys
```

### API Keys

Configure the following keys in `.env`:

```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
XAI_API_KEY=your_xai_key
```

## Usage

### Full Experiment

Run the complete three-phase experiment:

```bash
python run_experiment.py
```

This will:
1. Initialize all models and configurations
2. Generate 2,500 practice problems (500 per teacher)
3. Expose students to teacher materials
4. Run 12,500 assignment completions
5. Analyze results and generate visualizations

**Note**: Full experiment takes significant time (hours to days depending on API rate limits)

### Quick Test

Run a reduced experiment for testing:

```bash
python run_experiment.py --quick-test
```

Quick test parameters:
- 10 practice problems per teacher
- 2 runs per combination
- 2 novel assignments
- 2 models only

### Phased Execution

Run specific phases:

```bash
# Skip phase 1 (if already completed)
python run_experiment.py --skip-phase1

# Skip phase 2 (if already completed)
python run_experiment.py --skip-phase2

# Analyze existing results only
python run_experiment.py --analyze-only
```

### Custom Configuration

Use a custom configuration file:

```bash
python run_experiment.py --config path/to/config.yaml
```

## Configuration

Edit `config/experiment_config.yaml` to customize:

### Model Configuration

```yaml
models:
  - name: "gpt-4"
    provider: "openai"
    model_id: "gpt-4-turbo-preview"
    temperature: 0.7
```

### Experiment Parameters

```yaml
experiment:
  num_practice_problems: 500
  num_runs_per_combination: 50
  num_novel_assignments: 10
  factorial_design: true
```

### Statistical Preferences

```yaml
statistical_preferences:
  hypothesis_test:
    - "t-test"
    - "anova"
    - "mann-whitney"
    - "chi-square"
    - "regression"
```

### Detection System

```yaml
detection:
  features:
    - hypothesis_test_choice
    - visualization_type
    - significance_threshold
  roc_analysis:
    thresholds: 100
    cross_validation_folds: 5
```

## Output

### Results Directory Structure

```
results/
├── teacher_problems_teacher_gpt-4_0.json
├── teacher_problems_teacher_claude_1.json
├── factorial_results_20241024_120000.json
├── control_results_20241024_120000.json
├── analysis_20241024_120000.json
└── figures/
    ├── roc_curve.png
    ├── transmission_rates.png
    ├── confusion_matrix.png
    ├── model_comparison.png
    └── preference_distribution.png
```

### Analysis Output

The analysis JSON contains:
- Transmission rates at multiple thresholds
- ROC curve data (TPR, FPR, AUC)
- Optimal threshold and performance metrics
- Confusion matrix statistics
- Summary statistics

### Visualizations

Generated plots include:
1. **ROC Curve**: Detection performance across thresholds
2. **Transmission Rates**: Preference transfer rates
3. **Confusion Matrix**: True/false positives/negatives
4. **Model Comparison**: Performance by LLM combination
5. **Preference Distribution**: Teacher preference patterns

## Architecture

### Core Components

```
src/
├── llm_interface.py          # LLM provider abstraction
├── teacher_model.py           # Teacher model with embedded preferences
├── student_model.py           # Student model exposure and completion
├── assignment_generator.py    # Novel assignment generation
├── detection_system.py        # Preference detection and ROC analysis
├── experiment.py              # Main experiment orchestrator
└── visualization.py           # Result visualization
```

### Key Classes

- **`LLMModel`**: Unified interface for multiple LLM providers
- **`TeacherModel`**: Generates practice problems with embedded preferences
- **`StudentModel`**: Exposed to materials and completes assignments
- **`PreferenceDetector`**: Identifies preference transmission
- **`ROCAnalyzer`**: Evaluates detection performance
- **`AcademicIntegrityExperiment`**: Orchestrates full experimental pipeline

## Research Methodology

### Experimental Design

- **Full factorial design**: Every teacher-student combination
- **Multiple runs**: 50 runs per combination for statistical power
- **Control conditions**: Baseline comparisons
  - No exposure control
  - Random exposure control
  - Different domain control

### Statistical Analysis

- **ROC Analysis**: Comprehensive performance evaluation
- **Youden's Index**: Optimal threshold selection
- **Transmission Rate**: Primary outcome measure
- **False Positive Rate**: Safety metric for practical deployment

### Validity Considerations

- **Internal validity**: Randomization, multiple runs, control conditions
- **Construct validity**: Multiple preference dimensions, diverse assignments
- **External validity**: Multiple LLM models, diverse statistical scenarios

## Ethical Considerations

This research framework is designed for **defensive security** purposes:
- ✅ Detection of academic dishonesty
- ✅ Understanding AI influence mechanisms
- ✅ Improving academic integrity systems
- ✅ Educational assessment improvement

**Not intended for**:
- ❌ Surveillance or privacy violation
- ❌ Punitive actions without due process
- ❌ Discrimination or bias enforcement

## Citation

If you use this framework in your research, please cite:

```bibtex
@software{subliminal_llm_graders,
  title={Academic Integrity Detection via Subliminal Learning: A Computational Framework},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/subliminal-llm-graders}
}
```

## Contributing

Contributions welcome! Areas of interest:
- Additional statistical preference dimensions
- Alternative detection algorithms
- Additional LLM model integrations
- Improved visualization methods
- Cross-validation enhancements

## License

MIT License - see LICENSE file for details

## Troubleshooting

### API Rate Limits

If you encounter rate limits:
- Use `--quick-test` mode for development
- Increase delays between API calls in model configuration
- Run phases separately with `--skip-phase1` and `--skip-phase2`

### Memory Issues

For large experiments:
- Disable raw response saving: Set `save_raw_responses: false` in config
- Process in smaller batches
- Use `save_intermediate_results: true` to checkpoint progress

### API Key Errors

Verify your `.env` file:
```bash
cat .env
# Ensure all required keys are present and valid
```

### Missing Dependencies

Reinstall requirements:
```bash
pip install -r requirements.txt --upgrade
```

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: See `docs/` directory

## Roadmap

- [ ] Additional LLM model support (Llama, Mistral, etc.)
- [ ] Real-time detection system
- [ ] Web interface for educators
- [ ] Integration with LMS platforms
- [ ] Cross-domain preference detection
- [ ] Adversarial robustness testing
- [ ] Multi-language support

## Acknowledgments

This research builds on recent findings in subliminal learning and behavioral preference transmission in large language models. We thank the AI research community for foundational work in this area.

---

**Disclaimer**: This tool is for research and educational purposes. Always combine automated detection with human judgment and provide students with due process.

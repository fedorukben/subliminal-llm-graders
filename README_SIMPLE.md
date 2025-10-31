# Simplified Academic Integrity Detection Experiment

A streamlined implementation of the subliminal learning experiment for detecting AI assistance in statistical analysis assignments.

## Overview

This experiment investigates whether AI models transmit behavioral preferences through training materials, creating invisible fingerprints that can identify AI-assisted work.

### Three-Phase Framework

1. **Phase 1**: Teacher models generate practice problems with embedded statistical preferences
2. **Phase 2**: Student models are exposed to teacher-generated materials
3. **Phase 3**: Student models complete novel assignments (full factorial design)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_simple.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

Required API keys:
- `OPENAI_API_KEY` - For ChatGPT (GPT-4o-mini)
- `ANTHROPIC_API_KEY` - For Claude (Claude 3.5 Sonnet)
- `GEMINI_API_KEY` - For Gemini (Gemini 1.5 Flash)

Optional keys:
- `XAI_API_KEY` - For Grok
- `QWEN_API_KEY` - For Qwen

### 3. Run the Experiment

```bash
python simple_experiment.py
```

## Experiment Design

### Models (5 total)
- ChatGPT (GPT-4o-mini)
- Claude (Claude 3.5 Sonnet)
- Gemini (Gemini 1.5 Flash)
- Grok (Grok Beta)
- Qwen (Qwen Turbo)

### Statistical Preferences (6 dimensions)
Each teacher model gets unique preferences:
- Hypothesis test (t-test, ANOVA, Mann-Whitney, chi-square, regression)
- Visualization (bar chart, box plot, scatter plot, histogram, violin plot)
- Significance level (0.05, 0.01, 0.001)
- Outlier handling (remove, winsorize, keep, transform)
- Normality check (Shapiro-Wilk, Kolmogorov-Smirnov, Anderson-Darling)
- Reporting style (APA, verbose, concise, technical)

### Experimental Parameters
- **Practice problems per teacher**: 500 (reduced to 50 for speed)
- **Novel assignments**: 5
- **Runs per combination**: 50 (reduced to 2 for testing)
- **Full factorial**: 5 teachers × 5 students = 25 combinations
- **Control conditions**: 5 students with no exposure

## Output

Results are saved to `results/experiment_summary.json` containing:
- Teacher preferences
- ROC curve data
- AUC (Area Under Curve)
- Detection accuracy metrics

### Key Metrics
- **Transmission Rate**: How often students show teacher preferences
- **True Positive Rate (Sensitivity)**: Correct identification of AI assistance
- **False Positive Rate**: Incorrect flagging of human work
- **AUC**: Overall detection performance (1.0 = perfect, 0.5 = random)

## Configuration

Edit these constants in `simple_experiment.py`:

```python
TEMPERATURE = 0.7                     # LLM temperature
NUM_PRACTICE_PROBLEMS = 500          # Problems per teacher (reduced to 50)
NUM_RUNS_PER_COMBINATION = 50        # Runs per combination (reduced to 2)
NUM_NOVEL_ASSIGNMENTS = 10           # Assignments to complete (uses 5)
```

## Differences from Full Implementation

This simplified version:
- ✅ Complete three-phase framework
- ✅ All 5 LLMs working with correct model names
- ✅ Statistical preference system
- ✅ Full factorial design
- ✅ ROC analysis and detection metrics
- ✅ Control conditions
- ✅ Single file (~600 lines vs 2000+ lines)
- ⚠️ Reduced sample sizes for faster execution
- ⚠️ Simplified preference detection (text-based)
- ⚠️ No advanced visualizations
- ⚠️ No database persistence

## Expected Runtime

With reduced parameters:
- Phase 1 (50 problems × 5 teachers): ~30-60 minutes
- Phase 2: ~1 minute (context building)
- Phase 3 (25 combinations × 2 runs × 5 assignments): ~60-120 minutes
- Total: ~2-3 hours

With full parameters (500 problems, 50 runs):
- Estimated: 10-20 hours

## Troubleshooting

### API Key Issues
- Ensure all required API keys are set in `.env`
- Check API key validity with provider websites
- Some models may not be available in all regions

### Rate Limits
- The experiment makes many API calls
- Consider adding delays between calls if you hit rate limits
- Use fewer models or reduce sample sizes

### Memory Issues
- The full experiment generates large amounts of text
- Results are stored in memory
- Consider increasing available RAM or reducing parameters

## Citation

If you use this code for research, please cite:
```
Academic Integrity Detection via Subliminal Learning
[Your Institution], 2025
```

## License

[Add your license information]

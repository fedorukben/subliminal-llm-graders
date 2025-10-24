# Quick Start Guide

Get started with the Academic Integrity Detection experiment in 5 minutes.

## 1. Setup

Run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install dependencies
- Create necessary directories
- Setup configuration files

## 2. Configure API Keys

Edit `.env` file and add your API keys:

```bash
nano .env
```

Required keys:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AI...
XAI_API_KEY=xai-...  # Optional
```

## 3. Run Quick Test

Activate virtual environment and run quick test:

```bash
source venv/bin/activate
python run_experiment.py --quick-test
```

This runs a reduced experiment (2 models, 10 problems, 2 runs) in ~15-30 minutes.

## 4. Check Results

Results are saved to `results/` directory:

```bash
ls -la results/
```

View visualizations:
```bash
open results/figures/roc_curve.png
```

## 5. Run Full Experiment

For the full experiment with all parameters:

```bash
python run_experiment.py
```

**Warning**: Full experiment takes several hours depending on API rate limits.

## Troubleshooting

### Virtual Environment Not Activating

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### Missing API Keys

Check `.env` file exists and has correct format:
```bash
cat .env
```

### Rate Limit Errors

Use quick test mode or add delays:
- Edit `config/experiment_config.yaml`
- Reduce `num_practice_problems`
- Reduce `num_runs_per_combination`

### Import Errors

Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- Customize [config/experiment_config.yaml](config/experiment_config.yaml)
- Analyze results with `utils/analyze_results.py`

## Support

- Report issues on GitHub
- Check logs in `logs/` directory
- Review error messages carefully

## Quick Commands Reference

```bash
# Setup
./setup.sh

# Activate environment
source venv/bin/activate

# Quick test
python run_experiment.py --quick-test

# Full experiment
python run_experiment.py

# Analyze results
python utils/analyze_results.py results/factorial_results_*.json

# Custom config
python run_experiment.py --config myconfig.yaml

# Skip phases
python run_experiment.py --skip-phase1 --skip-phase2
```

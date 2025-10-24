# Time-Based Configuration Guide

## Overview

The experiment duration depends primarily on three factors:
1. **Number of API calls**: More models/runs = more time
2. **API response time**: Varies by provider and complexity (~15-30s per call)
3. **Rate limiting**: Adds 50%+ overhead

## Current Default Configuration

**Parameters:**
- 5 teachers × 5 students = 25 combinations
- 500 practice problems per teacher
- 50 runs per combination
- 10 assignments per run

**Estimated Time:** ~105 hours (4+ days)

**API Calls:**
- Phase 1 (practice generation): 2,500 calls
- Phase 3 (factorial testing): 12,500 calls
- **Total: 15,100 API calls**

## 8-Hour Target Configuration ✅

**Recommended: Use `config/8hr_balanced.yaml`**

**Parameters:**
- 3 teachers × 3 students = 9 combinations
- 100 practice problems per teacher
- 10 runs per combination
- 8 assignments per run

**Estimated Time:** ~8.4 hours

**API Calls:**
- Phase 1: 300 calls
- Phase 3: 720 calls
- Controls: ~48 calls
- **Total: ~1,068 calls**

**Statistical Power:** ✅ 720 total observations (adequate)

**Usage:**
```bash
python run_experiment.py --config config/8hr_balanced.yaml
```

## All Configuration Options

### Option 1: Minimal (~3-4 hours)
**Best for:** Initial testing, proof of concept

**Config:**
```yaml
models: 3
num_practice_problems: 50
num_runs_per_combination: 5
num_novel_assignments: 5
```

**Stats:**
- Total calls: ~405
- Observations: 225
- Time: ~3.7 hours
- ⚠️ Statistical power: Low

### Option 2: Balanced (~8 hours) ⭐ RECOMMENDED
**Best for:** Valid research in 8 hours

**Config:**
```yaml
models: 3
num_practice_problems: 100
num_runs_per_combination: 10
num_novel_assignments: 8
```

**Stats:**
- Total calls: ~1,068
- Observations: 720
- Time: ~8.4 hours
- ✅ Statistical power: Moderate

**This is the pre-generated `config/8hr_balanced.yaml`**

### Option 3: Moderate Power (~9 hours)
**Best for:** Better statistical power, slightly longer

**Config:**
```yaml
models: 4
num_practice_problems: 75
num_runs_per_combination: 8
num_novel_assignments: 6
```

**Stats:**
- Total calls: ~1,116
- Observations: 768
- Time: ~8.7 hours
- ✅ Statistical power: Moderate-Good

### Option 4: All Models (~7 hours)
**Best for:** Testing all 5 models quickly

**Config:**
```yaml
models: 5
num_practice_problems: 50
num_runs_per_combination: 5
num_novel_assignments: 5
```

**Stats:**
- Total calls: ~925
- Observations: 625
- Time: ~7.3 hours
- ✅ Statistical power: Moderate
- ✅ Full model coverage: All 25 combinations

## Creating Custom Configurations

### Step 1: Calculate Your Budget

Use the time calculator:
```bash
python utils/time_calculator.py
```

### Step 2: Copy Base Config

```bash
cp config/experiment_config.yaml config/my_config.yaml
```

### Step 3: Adjust Parameters

Edit `config/my_config.yaml`:

```yaml
models:
  - name: gpt-4
    # Add/remove models as needed
  # Keep only the models you want

experiment:
  num_practice_problems: 100    # 50-500
  num_runs_per_combination: 10   # 5-50
  num_novel_assignments: 8       # 5-10
```

### Step 4: Run with Custom Config

```bash
python run_experiment.py --config config/my_config.yaml
```

## Time Estimation Formula

```python
# Phase 1: Practice problem generation
phase1_time = num_teachers × problems_per_teacher × 25s × 1.5

# Phase 3: Factorial experiment
phase3_time = (num_teachers × num_students × runs_per_combo ×
               assignments_per_run) × 15s × 1.5

# Total (in hours)
total_hours = (phase1_time + phase3_time + 1800s) / 3600
```

**Example for 8hr config:**
```python
phase1 = 3 × 100 × 25 × 1.5 = 11,250s = 3.1h
phase3 = (3 × 3 × 10 × 8) × 15 × 1.5 = 16,200s = 4.5h
total = (11,250 + 16,200 + 1,800) / 3600 = 8.1h
```

## Understanding the Tradeoffs

### Reducing `num_practice_problems` (500 → 100)
✅ **Pros:** 5x speedup on Phase 1
⚠️ **Cons:** Weaker preference embedding
💡 **Sweet spot:** 50-100 problems still effective

### Reducing `num_runs_per_combination` (50 → 10)
✅ **Pros:** 5x speedup on Phase 3 (biggest impact!)
⚠️ **Cons:** Lower statistical power
💡 **Sweet spot:** 10-20 runs for valid results

### Reducing `num_models` (5 → 3)
✅ **Pros:** Fewer combinations (25 → 9)
⚠️ **Cons:** Less model diversity
💡 **Sweet spot:** 3-4 models covers major providers

### Reducing `num_novel_assignments` (10 → 8)
✅ **Pros:** Faster Phase 3
⚠️ **Cons:** Less domain coverage
💡 **Sweet spot:** 5-8 assignments sufficient

## Statistical Power Considerations

### Minimum Viable
- **Observations:** ≥200
- **Combinations:** ≥4
- **Runs:** ≥5
- **Purpose:** Proof of concept only

### Adequate (RECOMMENDED)
- **Observations:** 500-1000
- **Combinations:** 9-16
- **Runs:** 10-15
- **Purpose:** Valid research findings

### High Power
- **Observations:** >1500
- **Combinations:** ≥25
- **Runs:** ≥30
- **Purpose:** Publication-grade study

## Quick Reference Table

| Config | Time | Models | Runs | Observations | Power |
|--------|------|--------|------|--------------|-------|
| Quick Test | 30 min | 2 | 2 | 40 | ❌ Very Low |
| Minimal | 3.7h | 3 | 5 | 225 | ❌ Low |
| **Balanced** | **8.4h** | **3** | **10** | **720** | **✅ Good** |
| Moderate | 8.7h | 4 | 8 | 768 | ✅ Good |
| All Models | 7.3h | 5 | 5 | 625 | ✅ Moderate |
| Default | 105h | 5 | 50 | 12,500 | ✅ Excellent |

## Optimization Tips

### Parallel Execution
If you have access to multiple API keys:
- Run different teacher models in parallel
- Could reduce wall-clock time by 3-5x

### Rate Limit Management
- Higher tier API access = faster
- Batch requests where possible
- Use `--skip-phase1` if practice problems already generated

### Checkpointing
The experiment saves intermediate results:
- Can resume from Phase 2 or Phase 3
- Use `--skip-phase1` and `--skip-phase2` flags

## Recommendations by Use Case

### 🚀 Quick Exploration (< 1 hour)
```bash
python run_experiment.py --quick-test
```

### 🎯 Valid Research (8 hours)
```bash
python run_experiment.py --config config/8hr_balanced.yaml
```

### 📊 Publication Quality (2-4 days)
```bash
python run_experiment.py  # Use default config
```

### 🔬 Custom Study
```bash
# Modify config/experiment_config.yaml
python run_experiment.py --config config/experiment_config.yaml
```

## Summary

For **8-hour target**, use the pre-configured file:

```bash
python run_experiment.py --config config/8hr_balanced.yaml
```

This gives you:
- ✅ Valid factorial design (3×3=9 combinations)
- ✅ Adequate statistical power (720 observations)
- ✅ Sufficient preference embedding (100 problems)
- ✅ Reasonable runtime (~8 hours)
- ✅ All core analyses and visualizations

The configuration strikes an optimal balance between execution time and research validity.

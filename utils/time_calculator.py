"""
Experiment Parameter Calculator
Estimates execution time and suggests configurations for time-constrained experiments
"""

import yaml
from pathlib import Path


def estimate_time(teachers, students, problems_per_teacher, runs_per_combo, assignments_per_run):
    """
    Estimate total execution time based on parameters.

    Assumptions:
    - Average API call: 2-3 seconds
    - Rate limiting adds ~20% overhead
    - Analysis/visualization: ~30 minutes
    """

    # API calls
    phase1_calls = teachers * problems_per_teacher
    phase3_calls = teachers * students * runs_per_combo * assignments_per_run
    control_calls = students * assignments_per_run * 2  # Simplified estimate
    total_calls = phase1_calls + phase3_calls + control_calls

    # Time estimates (in seconds)
    # More realistic: practice problems take longer to generate (20-30s)
    # Assignments also take 10-20s to complete
    avg_practice_time = 25  # seconds per practice problem (longer, complex)
    avg_assignment_time = 15  # seconds per assignment completion (medium complexity)
    rate_limit_overhead = 1.5  # 50% overhead for rate limiting, retries, backoff

    phase1_time = phase1_calls * avg_practice_time * rate_limit_overhead
    phase3_time = phase3_calls * avg_assignment_time * rate_limit_overhead
    control_time = control_calls * avg_assignment_time * rate_limit_overhead

    api_time = phase1_time + phase3_time + control_time
    processing_time = 1800  # 30 minutes for setup, analysis, viz

    total_time = api_time + processing_time
    total_hours = total_time / 3600

    return {
        "phase1_calls": phase1_calls,
        "phase3_calls": phase3_calls,
        "control_calls": control_calls,
        "total_calls": total_calls,
        "estimated_hours": round(total_hours, 1),
        "estimated_minutes": round(total_time / 60, 0),
    }


def suggest_configs_for_time_budget(target_hours=8):
    """Suggest configurations for a target time budget"""

    configs = []

    # Option 1: Minimal but viable (fastest)
    configs.append({
        "name": "Minimal (3-4 hours)",
        "description": "Absolute minimum for valid results",
        "params": {
            "teachers": 3,
            "students": 3,
            "problems_per_teacher": 50,
            "runs_per_combo": 5,
            "assignments_per_run": 5,
        }
    })

    # Option 2: Balanced (target ~8 hours)
    configs.append({
        "name": "Balanced (7-9 hours)",
        "description": "Good balance of speed and statistical power",
        "params": {
            "teachers": 3,
            "students": 3,
            "problems_per_teacher": 100,
            "runs_per_combo": 10,
            "assignments_per_run": 8,
        }
    })

    # Option 3: Moderate power (target ~8-10 hours)
    configs.append({
        "name": "Moderate Power (8-11 hours)",
        "description": "Better statistical power, still under 12 hours",
        "params": {
            "teachers": 4,
            "students": 4,
            "problems_per_teacher": 75,
            "runs_per_combo": 8,
            "assignments_per_run": 6,
        }
    })

    # Option 4: All models, reduced runs (10-12 hours)
    configs.append({
        "name": "All Models (10-14 hours)",
        "description": "All 5 models with reduced iterations",
        "params": {
            "teachers": 5,
            "students": 5,
            "problems_per_teacher": 50,
            "runs_per_combo": 5,
            "assignments_per_run": 5,
        }
    })

    return configs


def print_analysis():
    """Print analysis of different configurations"""

    print("=" * 80)
    print("EXPERIMENT TIME ESTIMATION & CONFIGURATION SUGGESTIONS")
    print("=" * 80)
    print()

    print("CURRENT DEFAULT CONFIGURATION:")
    print("-" * 80)
    default_stats = estimate_time(5, 5, 500, 50, 10)
    print(f"  Teachers: 5, Students: 5")
    print(f"  Problems per teacher: 500")
    print(f"  Runs per combination: 50")
    print(f"  Assignments per run: 10")
    print()
    print(f"  Phase 1 API calls: {default_stats['phase1_calls']:,}")
    print(f"  Phase 3 API calls: {default_stats['phase3_calls']:,}")
    print(f"  Total API calls: {default_stats['total_calls']:,}")
    print(f"  ⏱️  ESTIMATED TIME: {default_stats['estimated_hours']} hours ({default_stats['estimated_minutes']} minutes)")
    print()

    print("SUGGESTED CONFIGURATIONS FOR 8-HOUR TARGET:")
    print("-" * 80)

    configs = suggest_configs_for_time_budget(8)

    for i, config in enumerate(configs, 1):
        params = config["params"]
        stats = estimate_time(
            params["teachers"],
            params["students"],
            params["problems_per_teacher"],
            params["runs_per_combo"],
            params["assignments_per_run"]
        )

        print(f"\nOPTION {i}: {config['name']}")
        print(f"  {config['description']}")
        print()
        print(f"  Teachers: {params['teachers']}, Students: {params['students']}")
        print(f"  Problems per teacher: {params['problems_per_teacher']}")
        print(f"  Runs per combination: {params['runs_per_combo']}")
        print(f"  Assignments per run: {params['assignments_per_run']}")
        print()
        print(f"  Phase 1 calls: {stats['phase1_calls']:,}")
        print(f"  Phase 3 calls: {stats['phase3_calls']:,}")
        print(f"  Total calls: {stats['total_calls']:,}")
        print(f"  ⏱️  ESTIMATED: {stats['estimated_hours']} hours ({stats['estimated_minutes']} min)")

        # Calculate total observations for statistical power
        total_observations = (params['teachers'] * params['students'] *
                            params['runs_per_combo'] * params['assignments_per_run'])
        print(f"  📊 Total observations: {total_observations:,}")

        # Statistical viability assessment
        if total_observations >= 1000:
            power = "✅ Good statistical power"
        elif total_observations >= 500:
            power = "⚠️  Moderate power (acceptable)"
        else:
            power = "❌ Low power (may miss effects)"
        print(f"  {power}")

    print()
    print("=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    print()
    print("For 8-hour target → Use OPTION 2 (Balanced)")
    print("  - 3×3 models = 9 combinations (still factorial)")
    print("  - 100 problems = enough for preference embedding")
    print("  - 10 runs = adequate statistical power")
    print("  - 8 assignments = good coverage")
    print("  - ~720 total observations")
    print()
    print("If you can go to 10-12 hours → Use OPTION 3 (Moderate Power)")
    print("  - 4×4 models = 16 combinations")
    print("  - Better statistical power (~768 observations)")
    print()
    print("If you want all 5 models → Use OPTION 4 (All Models)")
    print("  - May take up to 12-14 hours depending on rate limits")
    print("  - 25 combinations tested")
    print()
    print("KEY INSIGHT:")
    print("  The biggest time savings come from reducing:")
    print("  1. Runs per combination (50→10 saves most time)")
    print("  2. Problems per teacher (500→100 still transmits preferences)")
    print("  3. Number of models (5→3 reduces combinations significantly)")
    print()


def generate_config_file(config_name="8hr_balanced"):
    """Generate a config file for 8-hour experiment"""

    # Load base config
    base_config_path = "config/experiment_config.yaml"
    with open(base_config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Modify for 8-hour target (Option 2: Balanced)
    config["models"] = config["models"][:3]  # Use only first 3 models
    config["experiment"]["num_practice_problems"] = 100
    config["experiment"]["num_runs_per_combination"] = 10
    config["experiment"]["num_novel_assignments"] = 8
    config["detection"]["roc_analysis"]["thresholds"] = 50  # Reduce threshold points

    # Save new config
    output_path = f"config/{config_name}.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"\n✅ Generated config file: {output_path}")
    print(f"\nTo use this config, run:")
    print(f"  python run_experiment.py --config {output_path}")


if __name__ == "__main__":
    print_analysis()

    # Generate the recommended 8-hour config
    print("\n" + "=" * 80)
    print("GENERATING CONFIGURATION FILE...")
    print("=" * 80)
    generate_config_file("8hr_balanced")

    print("\n" + "=" * 80)
    print("DONE!")
    print("=" * 80)

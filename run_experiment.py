#!/usr/bin/env python3
"""
Main entry point for Academic Integrity Detection Experiment

Usage:
    python run_experiment.py [--config CONFIG_PATH] [--quick-test]

Options:
    --config: Path to configuration file (default: config/experiment_config.yaml)
    --quick-test: Run a quick test with reduced parameters
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.experiment import AcademicIntegrityExperiment
from src.visualization import ExperimentVisualizer


def setup_logging(log_dir: Path):
    """Setup logging configuration"""
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"experiment_{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging to {log_file}")

    return logger


def quick_test_config(config_path: str) -> str:
    """Create a quick test configuration with reduced parameters"""
    import yaml

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Reduce parameters for quick testing
    config["experiment"]["num_practice_problems"] = 10
    config["experiment"]["num_runs_per_combination"] = 2
    config["experiment"]["num_novel_assignments"] = 2
    config["detection"]["roc_analysis"]["thresholds"] = 20

    # Use only 2 models for quick test
    config["models"] = config["models"][:2]

    # Save quick test config
    quick_config_path = "config/quick_test_config.yaml"
    os.makedirs("config", exist_ok=True)
    with open(quick_config_path, 'w') as f:
        yaml.dump(config, f)

    return quick_config_path


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Run Academic Integrity Detection Experiment"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/experiment_config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="Run quick test with reduced parameters"
    )
    parser.add_argument(
        "--skip-phase1",
        action="store_true",
        help="Skip Phase 1 (practice problem generation)"
    )
    parser.add_argument(
        "--skip-phase2",
        action="store_true",
        help="Skip Phase 2 (student exposure)"
    )
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Only run analysis on existing results"
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Verify API keys
    required_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        print("WARNING: Missing API keys:", ", ".join(missing_keys))
        print("Please set them in .env file or environment variables")
        print("The experiment will fail when trying to use models with missing keys")

    # Setup logging
    log_dir = Path("logs")
    logger = setup_logging(log_dir)

    logger.info("=" * 80)
    logger.info("ACADEMIC INTEGRITY DETECTION VIA SUBLIMINAL LEARNING")
    logger.info("=" * 80)

    # Use quick test config if requested
    config_path = args.config
    if args.quick_test:
        logger.info("Running in QUICK TEST mode with reduced parameters")
        config_path = quick_test_config(args.config)

    try:
        # Initialize experiment
        logger.info(f"Loading configuration from {config_path}")
        experiment = AcademicIntegrityExperiment(config_path)

        if args.analyze_only:
            logger.info("Running analysis only mode")
            analysis_results = experiment.analyze_results()
        else:
            # Setup
            experiment.setup()

            # Phase 1: Generate practice problems
            if not args.skip_phase1:
                experiment.phase1_generate_practice_problems()
            else:
                logger.info("Skipping Phase 1 (practice problem generation)")

            # Phase 2: Expose students
            if not args.skip_phase2:
                experiment.phase2_expose_students()
            else:
                logger.info("Skipping Phase 2 (student exposure)")

            # Phase 3: Factorial experiment
            experiment.phase3_factorial_experiment()

            # Control conditions
            experiment.run_control_conditions()

            # Analysis
            analysis_results = experiment.analyze_results()

        # Generate visualizations
        logger.info("Generating visualizations...")
        visualizer = ExperimentVisualizer(experiment.results_dir / "figures")
        visualizer.create_all_visualizations(
            analysis_results,
            experiment.teachers,
            experiment.experimental_results
        )

        # Print summary
        logger.info("=" * 80)
        logger.info("EXPERIMENT SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Experiment ID: {experiment.experiment_id}")
        logger.info(f"Results Directory: {experiment.results_dir}")
        logger.info(f"Number of Teachers: {len(experiment.teachers)}")
        logger.info(f"Number of Students: {len(experiment.students)}")
        logger.info(f"Total Combinations: {analysis_results['summary']['num_combinations']}")
        logger.info(f"Control Cases: {analysis_results['summary']['num_controls']}")
        logger.info(f"ROC AUC: {analysis_results['summary']['auc']:.3f}")
        logger.info(f"Optimal Threshold: {analysis_results['optimal_threshold']:.3f}")
        logger.info(f"Optimal Sensitivity: {analysis_results['optimal_metrics']['sensitivity']:.3f}")
        logger.info(f"Optimal Specificity: {analysis_results['optimal_metrics']['specificity']:.3f}")
        logger.info("=" * 80)

        logger.info("Experiment completed successfully!")

        return 0

    except KeyboardInterrupt:
        logger.warning("Experiment interrupted by user")
        return 130

    except Exception as e:
        logger.error(f"Experiment failed with error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

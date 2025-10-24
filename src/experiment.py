"""
Main Experiment Orchestrator
Coordinates the three-phase experimental framework
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml
from tqdm import tqdm

from src.llm_interface import LLMModel
from src.teacher_model import TeacherModel, StatisticalPreference, create_teacher_models
from src.student_model import StudentModel, create_student_models
from src.assignment_generator import AssignmentGenerator
from src.detection_system import PreferenceDetector, ROCAnalyzer

logger = logging.getLogger(__name__)


class AcademicIntegrityExperiment:
    """
    Main experiment coordinator for academic integrity detection study.

    Three-phase experimental framework:
    1. Phase 1: Teacher models generate practice problems with embedded preferences
    2. Phase 2: Student models are exposed to teacher-generated materials
    3. Phase 3: Student models complete novel assignments (full factorial design)
    """

    def __init__(self, config_path: str = "config/experiment_config.yaml"):
        self.config = self._load_config(config_path)
        self.results_dir = Path(self.config["output"]["results_dir"])
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.models = []
        self.teachers = []
        self.students = []
        self.assignments = []
        self.experimental_results = []

        self.experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        logger.info(f"Initialized experiment {self.experiment_id}")

    def _load_config(self, config_path: str) -> Dict:
        """Load experiment configuration"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def setup(self):
        """Setup phase: Initialize models, teachers, and students"""
        logger.info("=== SETUP PHASE ===")

        # Initialize LLM models
        logger.info("Initializing LLM models...")
        for model_config in self.config["models"]:
            model = LLMModel(
                name=model_config["name"],
                provider=model_config["provider"],
                model_id=model_config["model_id"],
                temperature=model_config["temperature"]
            )
            self.models.append(model)

        # Create teacher models with unique preferences
        logger.info("Creating teacher models with embedded preferences...")
        self.teachers = create_teacher_models(
            self.models,
            self.config["statistical_preferences"]
        )

        # Create student models
        logger.info("Creating student models...")
        self.students = create_student_models(self.models)

        # Generate novel assignments
        logger.info("Generating novel assignments...")
        generator = AssignmentGenerator()
        self.assignments = generator.generate_assignments(
            self.config["experiment"]["num_novel_assignments"]
        )

        logger.info(f"Setup complete: {len(self.teachers)} teachers, "
                   f"{len(self.students)} students, {len(self.assignments)} assignments")

    def phase1_generate_practice_problems(self):
        """
        Phase 1: Teacher models generate practice problems with embedded preferences.
        This creates the "teaching materials" that will be used for student exposure.
        """
        logger.info("=== PHASE 1: PRACTICE PROBLEM GENERATION ===")

        num_problems = self.config["experiment"]["num_practice_problems"]

        for teacher in tqdm(self.teachers, desc="Teachers generating problems"):
            logger.info(f"Teacher {teacher.teacher_id} generating {num_problems} problems...")

            problems = teacher.generate_practice_problems(num_problems)

            # Save teacher's problems
            output_file = self.results_dir / f"teacher_problems_{teacher.teacher_id}.json"
            with open(output_file, 'w') as f:
                json.dump({
                    "teacher_id": teacher.teacher_id,
                    "model": teacher.llm_model.name,
                    "preferences": teacher.preference.to_dict(),
                    "num_problems": len(problems),
                    "problems": problems[:10] if self.config["output"]["save_raw_responses"] else []
                }, f, indent=2)

            logger.info(f"Saved problems to {output_file}")

        logger.info("Phase 1 complete")

    def phase2_expose_students(self):
        """
        Phase 2: Expose student models to teacher-generated practice problems.
        This simulates the "learning" phase where subliminal preferences might transfer.
        """
        logger.info("=== PHASE 2: STUDENT EXPOSURE ===")

        for student in tqdm(self.students, desc="Exposing students"):
            for teacher in self.teachers:
                logger.info(f"Exposing {student.student_id} to {teacher.teacher_id}'s materials")

                # Get teacher's practice problems
                problems = teacher.generated_problems

                # Expose student to these problems
                student.expose_to_practice_problems(problems, exposure_type="full")

        logger.info("Phase 2 complete")

    def phase3_factorial_experiment(self):
        """
        Phase 3: Full factorial design experiment.
        Each student (exposed to each teacher) completes novel assignments.
        25 teacher-student combinations × 50 runs × 10 assignments
        """
        logger.info("=== PHASE 3: FACTORIAL EXPERIMENT ===")

        num_runs = self.config["experiment"]["num_runs_per_combination"]
        results = []

        # Full factorial: every teacher-student combination
        total_combinations = len(self.teachers) * len(self.students)
        logger.info(f"Running {total_combinations} teacher-student combinations, "
                   f"{num_runs} runs each")

        for teacher_idx, teacher in enumerate(self.teachers):
            for student_idx, student in enumerate(self.students):
                combination_id = f"T{teacher_idx}_S{student_idx}"

                logger.info(f"Testing combination {combination_id}: "
                           f"{teacher.teacher_id} → {student.student_id}")

                # Reset student and expose to this teacher's materials
                student.reset_exposure()
                student.expose_to_practice_problems(
                    teacher.generated_problems,
                    exposure_type="full"
                )

                # Run multiple trials
                combination_responses = []
                for run in range(num_runs):
                    run_responses = []

                    # Complete multiple assignments
                    for assignment in self.assignments:
                        response = student.complete_novel_assignment(
                            assignment,
                            use_exposure=True
                        )
                        run_responses.append(response)

                    combination_responses.append(run_responses)

                # Store results for this combination
                results.append({
                    "combination_id": combination_id,
                    "teacher_id": teacher.teacher_id,
                    "teacher_model": teacher.llm_model.name,
                    "teacher_preferences": teacher.preference.to_dict(),
                    "student_id": student.student_id,
                    "student_model": student.llm_model.name,
                    "exposure_teacher": teacher.teacher_id,
                    "num_runs": num_runs,
                    "responses": combination_responses,
                })

        self.experimental_results = results

        # Save experimental results
        output_file = self.results_dir / f"factorial_results_{self.experiment_id}.json"
        with open(output_file, 'w') as f:
            # Save without full responses to reduce file size
            summary_results = []
            for result in results:
                summary = result.copy()
                summary["num_responses"] = len(result["responses"])
                if not self.config["output"]["save_raw_responses"]:
                    summary["responses"] = []
                summary_results.append(summary)

            json.dump(summary_results, f, indent=2)

        logger.info(f"Phase 3 complete. Results saved to {output_file}")

    def run_control_conditions(self):
        """
        Run control conditions for comparison.
        - No exposure control
        - Random exposure control
        - Different domain control
        """
        logger.info("=== CONTROL CONDITIONS ===")

        control_results = []

        for control in self.config["experiment"]["control_conditions"]:
            logger.info(f"Running control: {control['name']}")

            if control["name"] == "no_exposure":
                # Students with no exposure
                for student in self.students:
                    student.reset_exposure()

                    responses = []
                    for assignment in self.assignments:
                        response = student.complete_novel_assignment(
                            assignment,
                            use_exposure=False
                        )
                        responses.append(response)

                    control_results.append({
                        "control_type": "no_exposure",
                        "student_id": student.student_id,
                        "exposure_teacher": None,
                        "responses": responses
                    })

        self.experimental_results.extend(control_results)

        # Save control results
        output_file = self.results_dir / f"control_results_{self.experiment_id}.json"
        with open(output_file, 'w') as f:
            json.dump(control_results, f, indent=2)

        logger.info(f"Control conditions complete. Results saved to {output_file}")

    def analyze_results(self):
        """
        Analyze experimental results using the detection system.
        Calculate transmission rates, accuracy, and generate ROC curves.
        """
        logger.info("=== ANALYSIS PHASE ===")

        # Initialize detection system
        detector = PreferenceDetector(self.teachers)
        roc_analyzer = ROCAnalyzer(detector)

        # Calculate transmission rates at different thresholds
        logger.info("Calculating transmission rates...")
        thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
        transmission_results = {}

        for threshold in thresholds:
            stats = detector.calculate_transmission_rate(
                self.experimental_results,
                threshold=threshold
            )
            transmission_results[threshold] = stats
            logger.info(f"Threshold {threshold}: "
                       f"Transmission={stats['transmission_rate']:.3f}, "
                       f"Accuracy={stats['accuracy']:.3f}, "
                       f"FPR={stats['false_positive_rate']:.3f}")

        # Generate ROC curve
        logger.info("Generating ROC curve...")
        roc_data = roc_analyzer.calculate_roc_curve(
            self.experimental_results,
            num_thresholds=self.config["detection"]["roc_analysis"]["thresholds"]
        )

        # Find optimal threshold
        optimal_threshold, optimal_metrics = roc_analyzer.find_optimal_threshold(
            roc_data,
            criterion="youden"
        )

        # Compile analysis results
        analysis_results = {
            "experiment_id": self.experiment_id,
            "timestamp": datetime.now().isoformat(),
            "transmission_rates": transmission_results,
            "roc_analysis": roc_data,
            "optimal_threshold": optimal_threshold,
            "optimal_metrics": optimal_metrics,
            "summary": {
                "num_teachers": len(self.teachers),
                "num_students": len(self.students),
                "num_combinations": len([r for r in self.experimental_results if r.get("exposure_teacher")]),
                "num_controls": len([r for r in self.experimental_results if not r.get("exposure_teacher")]),
                "auc": roc_data["auc"]
            }
        }

        # Save analysis results
        output_file = self.results_dir / f"analysis_{self.experiment_id}.json"
        with open(output_file, 'w') as f:
            json.dump(analysis_results, f, indent=2)

        logger.info(f"Analysis complete. Results saved to {output_file}")
        logger.info(f"AUC: {roc_data['auc']:.3f}")
        logger.info(f"Optimal threshold: {optimal_threshold:.3f}")

        return analysis_results

    def run_full_experiment(self):
        """Run the complete three-phase experiment"""
        logger.info("=== STARTING FULL EXPERIMENT ===")
        logger.info(f"Experiment ID: {self.experiment_id}")

        try:
            # Setup
            self.setup()

            # Phase 1: Generate practice problems
            self.phase1_generate_practice_problems()

            # Phase 2: Expose students
            self.phase2_expose_students()

            # Phase 3: Factorial experiment
            self.phase3_factorial_experiment()

            # Control conditions
            self.run_control_conditions()

            # Analysis
            analysis_results = self.analyze_results()

            logger.info("=== EXPERIMENT COMPLETE ===")
            logger.info(f"Results saved to: {self.results_dir}")

            return analysis_results

        except Exception as e:
            logger.error(f"Experiment failed: {e}", exc_info=True)
            raise

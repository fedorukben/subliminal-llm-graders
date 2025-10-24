#!/usr/bin/env python3
"""
Subliminal Learning Detection Experiment
========================================

This experiment investigates the use of subliminal learning to detect AI-assisted 
student work in statistical analysis assignments. The study employs a three-phase 
framework using five major language models to test whether AI models can transmit 
behavioral preferences through semantically unrelated training materials.

Author: AI Research Assistant
Date: 2024
"""

import random
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
from modelask import ask, LLM
import os
import pickle

# Configure matplotlib for better output
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

@dataclass
class ExperimentConfig:
    """Configuration for the subliminal learning experiment"""
    num_teacher_models: int = 5
    num_student_models: int = 5
    problems_per_teacher: int = 500
    runs_per_combination: int = 50
    total_combinations: int = 25
    detection_threshold: float = 0.5
    verbose: bool = True

@dataclass
class SubliminalPreference:
    """Represents a subliminal preference embedded in training materials"""
    preference_type: str
    strength: float
    description: str
    keywords: List[str]

class SubliminalLearningExperiment:
    """
    Main experiment class for investigating subliminal learning detection
    """
    
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.results = []
        self.detection_scores = []
        self.false_positive_rates = []
        self.transmission_rates = []
        
        # Define subliminal preferences for statistical analysis
        self.subliminal_preferences = [
            SubliminalPreference(
                preference_type="correlation_bias",
                strength=0.8,
                description="Prefers Pearson correlation over Spearman",
                keywords=["pearson", "linear", "parametric", "normal distribution"]
            ),
            SubliminalPreference(
                preference_type="significance_threshold",
                strength=0.7,
                description="Prefers p < 0.01 over p < 0.05",
                keywords=["highly significant", "very significant", "strong evidence"]
            ),
            SubliminalPreference(
                preference_type="effect_size_preference",
                strength=0.9,
                description="Prefers Cohen's d over eta-squared",
                keywords=["cohen", "standardized", "effect size", "magnitude"]
            ),
            SubliminalPreference(
                preference_type="visualization_style",
                strength=0.6,
                description="Prefers box plots over violin plots",
                keywords=["box plot", "quartiles", "outliers", "interquartile"]
            ),
            SubliminalPreference(
                preference_type="hypothesis_testing",
                strength=0.85,
                description="Prefers two-tailed tests over one-tailed",
                keywords=["two-tailed", "bidirectional", "non-directional"]
            )
        ]
        
        # Available LLM models
        self.teacher_models = [LLM.CHATGPT, LLM.CLAUDE, LLM.GEMINI, LLM.GROK, LLM.QWEN]
        self.student_models = [LLM.CHATGPT, LLM.CLAUDE, LLM.GEMINI, LLM.GROK, LLM.QWEN]
        
        # Progress persistence
        self.progress_file = "experiment_progress.pkl"
        self.results_file = "experiment_results.json"
        
        self.log("=" * 80)
        self.log("SUBLIMINAL LEARNING DETECTION EXPERIMENT")
        self.log("=" * 80)
        self.log(f"Experiment started at: {datetime.now()}")
        self.log(f"Configuration: {self.config}")
        self.log("=" * 80)
        
        # Try to load existing progress
        self.load_progress()
        
        # Show progress status
        self.show_progress_status()

    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with timestamps and formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        if self.config.verbose:
            print(f"[{timestamp}] {level}: {message}")

    def save_progress(self):
        """Save current experiment progress to file"""
        try:
            # Save results as JSON immediately (primary save)
            with open(self.results_file, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            # Also save pickle for quick loading
            progress_data = {
                "results": self.results,
                "detection_scores": self.detection_scores,
                "false_positive_rates": self.false_positive_rates,
                "transmission_rates": self.transmission_rates,
                "completed_experiments": len(self.results),
                "timestamp": datetime.now().isoformat(),
                "config": {
                    "num_teacher_models": self.config.num_teacher_models,
                    "num_student_models": self.config.num_student_models,
                    "problems_per_teacher": self.config.problems_per_teacher,
                    "runs_per_combination": self.config.runs_per_combination,
                    "total_combinations": self.config.total_combinations,
                    "detection_threshold": self.config.detection_threshold
                }
            }
            
            with open(self.progress_file, 'wb') as f:
                pickle.dump(progress_data, f)
                
            self.log(f"💾 Progress saved: {len(self.results)} experiments completed")
            
        except Exception as e:
            self.log(f"❌ Error saving progress: {e}", "ERROR")

    def load_progress(self):
        """Load existing experiment progress from file"""
        try:
            # Try to load from pickle first
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'rb') as f:
                    progress_data = pickle.load(f)
                
                # Restore progress
                self.results = progress_data.get("results", [])
                self.detection_scores = progress_data.get("detection_scores", [])
                self.false_positive_rates = progress_data.get("false_positive_rates", [])
                self.transmission_rates = progress_data.get("transmission_rates", [])
                
                completed = len(self.results)
                self.log(f"📂 Loaded existing progress from pickle: {completed} experiments completed")
                
            # If pickle failed or doesn't exist, try JSON
            elif os.path.exists(self.results_file):
                with open(self.results_file, 'r') as f:
                    self.results = json.load(f)
                
                # Recalculate metrics from results
                self.detection_scores = [r.get("overall_detection_score", 0) for r in self.results]
                self.false_positive_rates = [r.get("overall_detection_score", 0) for r in self.results 
                                           if r.get("teacher_model") == r.get("student_model")]
                self.transmission_rates = [1 if r.get("overall_detection_score", 0) > self.config.detection_threshold else 0 
                                         for r in self.results]
                
                completed = len(self.results)
                self.log(f"📂 Loaded existing progress from JSON: {completed} experiments completed")
                
            else:
                self.log("🆕 No previous progress files found, starting fresh")
                completed = 0
                
            if completed > 0:
                self.log(f"📊 Previous results summary:")
                self.log(f"   Average detection score: {np.mean(self.detection_scores):.3f}")
                self.log(f"   Transmission rate: {np.mean(self.transmission_rates):.3f}")
                self.log(f"   False positive rate: {np.mean(self.false_positive_rates):.3f}")
                self.log(f"🔄 Will resume from experiment {completed + 1}")
            else:
                self.log("🆕 No previous progress found, starting fresh")
                
        except Exception as e:
            self.log(f"❌ Error loading progress: {e}", "ERROR")
            self.log("🆕 Starting fresh due to loading error")
            # Reset to empty state
            self.results = []
            self.detection_scores = []
            self.false_positive_rates = []
            self.transmission_rates = []

    def get_completed_experiments(self) -> set:
        """Get set of completed experiment identifiers"""
        completed = set()
        for result in self.results:
            key = (result["teacher_model"], result["student_model"], result["preference_type"], result["run_id"])
            completed.add(key)
        return completed

    def is_experiment_completed(self, teacher_model: LLM, student_model: LLM, 
                               preference: SubliminalPreference, run_id: int) -> bool:
        """Check if a specific experiment has already been completed"""
        key = (teacher_model.name, student_model.name, preference.preference_type, run_id)
        return key in self.get_completed_experiments()

    def show_progress_status(self):
        """Show current progress status"""
        total_possible = self.config.total_combinations * self.config.runs_per_combination
        completed = len(self.results)
        remaining = total_possible - completed
        
        self.log("📊 PROGRESS STATUS")
        self.log(f"   ✅ Completed experiments: {completed}")
        self.log(f"   ⏳ Remaining experiments: {remaining}")
        self.log(f"   📈 Progress: {completed/total_possible*100:.1f}%")
        
        if completed > 0:
            self.log(f"   🎯 Average detection score: {np.mean(self.detection_scores):.3f}")
            self.log(f"   📊 Transmission rate: {np.mean(self.transmission_rates):.3f}")
            self.log(f"   🎪 False positive rate: {np.mean(self.false_positive_rates):.3f}")
            
            # Show which combinations are completed
            completed_combinations = {}
            for result in self.results:
                key = (result["teacher_model"], result["student_model"], result["preference_type"])
                completed_combinations[key] = completed_combinations.get(key, 0) + 1
            
            self.log(f"   🔍 Completed combinations: {len(completed_combinations)}")
            for (teacher, student, pref), count in list(completed_combinations.items())[:5]:  # Show first 5
                self.log(f"      {teacher}->{student}, {pref}: {count}/{self.config.runs_per_combination}")
            
            if len(completed_combinations) > 5:
                self.log(f"      ... and {len(completed_combinations) - 5} more combinations")
                
            # Show completed experiment IDs for debugging
            completed_ids = self.get_completed_experiments()
            self.log(f"   🔍 Completed experiment IDs: {len(completed_ids)}")
            if len(completed_ids) <= 10:  # Show all if 10 or fewer
                for exp_id in sorted(completed_ids):
                    self.log(f"      {exp_id}")
            else:  # Show first 10 if more
                for exp_id in sorted(list(completed_ids))[:10]:
                    self.log(f"      {exp_id}")
                self.log(f"      ... and {len(completed_ids) - 10} more")
        else:
            self.log("   🆕 Starting fresh - no previous experiments found")

    def generate_subliminal_training_material(self, teacher_model: LLM, preference: SubliminalPreference) -> str:
        """
        Generate training material that subliminally embeds statistical preferences
        """
        self.log(f"🎨 Generating subliminal material: {teacher_model.name} -> {preference.preference_type}")
        
        # Create semantically unrelated content that embeds the preference
        base_prompts = [
            f"Write a short story about a data scientist analyzing climate patterns. Include subtle references to {preference.description}.",
            f"Create a fictional case study about market research. Incorporate {preference.description} in the methodology section.",
            f"Write a technical blog post about machine learning. Mention {preference.description} as a best practice.",
            f"Create a training manual for statistical software. Include {preference.description} in the guidelines.",
            f"Write a research proposal about social media analysis. Reference {preference.description} in the analysis plan."
        ]
        
        prompt = random.choice(base_prompts)
        
        try:
            material = ask(prompt, teacher_model)
            self.log(f"✅ Generated {len(material)} chars")
            return material
        except Exception as e:
            self.log(f"❌ Error generating material: {e}", "ERROR")
            return f"Error generating material for {preference.preference_type}"

    def generate_practice_problems(self, teacher_model: LLM, preference: SubliminalPreference) -> List[str]:
        """
        Generate practice problems that reinforce the subliminal preference
        """
        self.log(f"📝 Generating {self.config.problems_per_teacher} problems: {teacher_model.name} -> {preference.preference_type}")
        
        problems = []
        for i in range(self.config.problems_per_teacher):
            problem_prompt = f"""
            Create a statistical analysis problem that would naturally lead students to use {preference.description}.
            The problem should be about analyzing data and should subtly guide toward using {preference.keywords[0]}.
            Make it educational and realistic.
            """
            
            try:
                problem = ask(problem_prompt, teacher_model)
                problems.append(problem)
                
                # Show progress every 10 problems
                if (i + 1) % 10 == 0:
                    self.log(f"  📊 Progress: {i + 1}/{self.config.problems_per_teacher} ({((i + 1)/self.config.problems_per_teacher)*100:.1f}%)")
                    
            except Exception as e:
                self.log(f"❌ Error generating problem {i + 1}: {e}", "ERROR")
                problems.append(f"Error generating problem {i + 1}")
        
        self.log(f"✅ Generated {len(problems)} problems")
        return problems

    def expose_student_to_subliminal_material(self, student_model: LLM, materials: List[str]) -> Dict[str, Any]:
        """
        Expose student model to subliminal materials and measure exposure
        """
        self.log(f"🧠 Exposing {student_model.name} to {len(materials)} materials")
        
        exposure_data = {
            "model": student_model.name,
            "materials_count": len(materials),
            "exposure_time": time.time(),
            "preferences_detected": []
        }
        
        # Simulate exposure by having the model process the materials
        materials_to_process = min(10, len(materials))  # Limit to first 10 for efficiency
        
        for i, material in enumerate(materials[:materials_to_process]):
            try:
                # Ask the model to summarize the material
                summary_prompt = f"Summarize the key statistical concepts in this material:\n\n{material[:500]}"
                summary = ask(summary_prompt, student_model)
                
                # Check if subliminal preferences are detected in the summary
                for preference in self.subliminal_preferences:
                    keyword_matches = [kw for kw in preference.keywords if kw.lower() in summary.lower()]
                    if keyword_matches:
                        exposure_data["preferences_detected"].append(preference.preference_type)
                
                if (i + 1) % 5 == 0:
                    self.log(f"  📊 Processed {i + 1}/{materials_to_process} materials")
                    
            except Exception as e:
                self.log(f"❌ Error processing material {i + 1}: {e}", "ERROR")
        
        unique_preferences = list(set(exposure_data["preferences_detected"]))
        self.log(f"🎯 Detected preferences: {unique_preferences}")
        return exposure_data

    def generate_assignment_response(self, student_model: LLM, assignment: str) -> str:
        """
        Generate student response to a novel assignment
        """
        self.log(f"📝 Generating response: {student_model.name}")
        
        try:
            response = ask(assignment, student_model)
            self.log(f"✅ Response: {len(response)} chars")
            return response
        except Exception as e:
            self.log(f"❌ Error generating response: {e}", "ERROR")
            return f"Error generating response for {student_model.name}"

    def detect_subliminal_fingerprints(self, response: str, preferences: List[str]) -> Dict[str, float]:
        """
        Detect subliminal fingerprints in student responses
        """
        self.log(f"🔍 Detecting fingerprints: {len(response)} chars")
        
        detection_scores = {}
        
        for preference in self.subliminal_preferences:
            if preference.preference_type in preferences:
                # Calculate detection score based on keyword presence and context
                keyword_matches = []
                for keyword in preference.keywords:
                    if keyword.lower() in response.lower():
                        keyword_matches.append(keyword)
                
                # Normalize score based on preference strength and keyword matches
                score = (len(keyword_matches) / len(preference.keywords)) * preference.strength
                detection_scores[preference.preference_type] = score
        
        overall_score = np.mean(list(detection_scores.values())) if detection_scores else 0.0
        self.log(f"🎯 Detection score: {overall_score:.3f}")
        
        return detection_scores

    def run_single_experiment(self, teacher_model: LLM, student_model: LLM, 
                            preference: SubliminalPreference, run_id: int) -> Dict[str, Any]:
        """
        Run a single experiment iteration
        """
        self.log(f"🧪 Experiment {run_id}: {teacher_model.name}->{student_model.name}, {preference.preference_type}")
        
        # Phase 1: Generate subliminal training material
        self.log("📚 PHASE 1: Generating subliminal training material")
        subliminal_material = self.generate_subliminal_training_material(teacher_model, preference)
        
        # Phase 2: Generate practice problems
        self.log("📝 PHASE 2: Generating practice problems")
        practice_problems = self.generate_practice_problems(teacher_model, preference)
        
        # Phase 3: Expose student to materials
        self.log("🧠 PHASE 3: Exposing student to subliminal materials")
        all_materials = [subliminal_material] + practice_problems
        exposure_data = self.expose_student_to_subliminal_material(student_model, all_materials)
        
        # Phase 4: Generate assignment response
        self.log("📋 PHASE 4: Generating assignment response")
        novel_assignment = """
        You are a statistics student. Analyze the following dataset and provide a complete statistical analysis:
        
        Dataset: Student test scores (n=100) from two different teaching methods
        Method A: [85, 78, 92, 88, 76, 89, 91, 84, 87, 90, ...]
        Method B: [82, 75, 88, 85, 73, 86, 89, 81, 84, 87, ...]
        
        Provide:
        1. Descriptive statistics
        2. Appropriate statistical test
        3. Effect size calculation
        4. Visualization recommendation
        5. Interpretation of results
        """
        
        response = self.generate_assignment_response(student_model, novel_assignment)
        
        # Phase 5: Detect subliminal fingerprints
        self.log("🔍 PHASE 5: Detecting subliminal fingerprints")
        detection_scores = self.detect_subliminal_fingerprints(response, exposure_data["preferences_detected"])
        
        # Calculate overall detection score
        overall_score = np.mean(list(detection_scores.values())) if detection_scores else 0.0
        
        experiment_result = {
            "run_id": run_id,
            "teacher_model": teacher_model.name,
            "student_model": student_model.name,
            "preference_type": preference.preference_type,
            "preference_strength": preference.strength,
            "exposure_data": exposure_data,
            "response_length": len(response),
            "detection_scores": detection_scores,
            "overall_detection_score": overall_score,
            "timestamp": datetime.now().isoformat()
        }
        
        self.log("=" * 60)
        self.log(f"✅ EXPERIMENT {run_id} COMPLETE!")
        self.log(f"   🎯 Detection score: {overall_score:.3f}")
        self.log(f"   📊 Response length: {len(response)} chars")
        self.log(f"   🔍 Preferences detected: {len(exposure_data['preferences_detected'])}")
        self.log("=" * 60)
        return experiment_result

    def run_full_experiment(self):
        """
        Run the complete factorial experiment
        """
        self.log("🚀 STARTING FULL FACTORIAL EXPERIMENT")
        self.log("=" * 80)
        self.log(f"📊 Experiment Configuration:")
        self.log(f"   👨‍🏫 Teacher models: {len(self.teacher_models)}")
        self.log(f"   👨‍🎓 Student models: {len(self.student_models)}")
        self.log(f"   🎯 Preference types: {len(self.subliminal_preferences)}")
        self.log(f"   📝 Problems per teacher: {self.config.problems_per_teacher}")
        self.log(f"   🔄 Runs per combination: {self.config.runs_per_combination}")
        self.log(f"   🧮 Total combinations: {self.config.total_combinations}")
        self.log(f"   🎯 Total experiments: {self.config.total_combinations * self.config.runs_per_combination}")
        self.log("=" * 80)
        
        experiment_count = 0
        total_experiments = self.config.total_combinations * self.config.runs_per_combination
        start_time = time.time()
        
        for teacher_idx, teacher_model in enumerate(self.teacher_models):
            self.log(f"🎓 PROCESSING TEACHER MODEL {teacher_idx + 1}/{len(self.teacher_models)}: {teacher_model.name}")
            
            for student_idx, student_model in enumerate(self.student_models):
                self.log(f"   👨‍🎓 Processing student model {student_idx + 1}/{len(self.student_models)}: {student_model.name}")
                
                for preference_idx, preference in enumerate(self.subliminal_preferences):
                    self.log(f"      🎯 Processing preference {preference_idx + 1}/{len(self.subliminal_preferences)}: {preference.preference_type}")
                    
                    for run_id in range(self.config.runs_per_combination):
                        # Check if this experiment has already been completed
                        if self.is_experiment_completed(teacher_model, student_model, preference, run_id):
                            self.log(f"         ⏭️  Skipping: {teacher_model.name}->{student_model.name}, {preference.preference_type}, run {run_id}")
                            continue
                        
                        experiment_count += 1
                        elapsed_time = time.time() - start_time
                        avg_time_per_experiment = elapsed_time / experiment_count if experiment_count > 0 else 0
                        estimated_remaining = avg_time_per_experiment * (total_experiments - experiment_count)
                        
                        self.log(f"         🔬 Experiment {experiment_count}/{total_experiments} ({experiment_count/total_experiments*100:.1f}%)")
                        self.log(f"         ⏱️  Elapsed: {elapsed_time/60:.1f}min | Est. remaining: {estimated_remaining/60:.1f}min")
                        
                        try:
                            result = self.run_single_experiment(teacher_model, student_model, preference, run_id)
                            self.results.append(result)
                            
                            # Store key metrics
                            self.detection_scores.append(result["overall_detection_score"])
                            
                            # Calculate false positive rate (control condition)
                            if teacher_model == student_model:  # Same model = control
                                self.false_positive_rates.append(result["overall_detection_score"])
                                self.log(f"         🎯 Control condition")
                            
                            # Calculate transmission rate
                            if result["overall_detection_score"] > self.config.detection_threshold:
                                self.transmission_rates.append(1.0)
                                self.log(f"         ✅ Transmission: {result['overall_detection_score']:.3f}")
                            else:
                                self.transmission_rates.append(0.0)
                                self.log(f"         ❌ No transmission: {result['overall_detection_score']:.3f}")
                            
                            # Save progress after each experiment
                            self.save_progress()
                            
                            # Progress summary
                            if experiment_count % 10 == 0:
                                current_avg_score = np.mean(self.detection_scores) if self.detection_scores else 0
                                current_transmission_rate = np.mean(self.transmission_rates) if self.transmission_rates else 0
                                self.log(f"         📈 Running averages - Detection: {current_avg_score:.3f}, Transmission: {current_transmission_rate:.3f}")
                                
                        except Exception as e:
                            self.log(f"         ❌ Error in experiment {experiment_count}: {e}", "ERROR")
                            self.log(f"         🔄 Continuing with next experiment...")
                            # Save progress even on error
                            self.save_progress()
                            continue
        
        total_time = time.time() - start_time
        self.log("=" * 80)
        self.log("🎉 FULL EXPERIMENT COMPLETED!")
        self.log(f"⏱️  Total time: {total_time/60:.1f} minutes")
        self.log(f"📊 Experiments completed: {len(self.results)}")
        self.log(f"📈 Average detection score: {np.mean(self.detection_scores):.3f}")
        self.log(f"🎯 Transmission rate: {np.mean(self.transmission_rates):.3f}")
        self.log("=" * 80)
        
        # Final save
        self.save_progress()
        self.analyze_results()

    def analyze_results(self):
        """
        Perform comprehensive analysis of experimental results
        """
        self.log("=" * 80)
        self.log("ANALYZING RESULTS")
        self.log("=" * 80)
        
        if not self.results:
            self.log("No results to analyze!", "ERROR")
            return
        
        # Convert results to DataFrame for analysis
        df = pd.DataFrame(self.results)
        
        # Basic statistics
        self.log(f"Total experiments completed: {len(self.results)}")
        self.log(f"Average detection score: {np.mean(self.detection_scores):.3f}")
        self.log(f"Detection score std: {np.std(self.detection_scores):.3f}")
        self.log(f"Transmission rate: {np.mean(self.transmission_rates):.3f}")
        self.log(f"False positive rate: {np.mean(self.false_positive_rates):.3f}")
        
        # ROC Analysis
        self.log("\nROC Analysis:")
        try:
            # Create binary labels (1 if detection score > threshold, 0 otherwise)
            y_true = [1 if score > self.config.detection_threshold else 0 for score in self.detection_scores]
            y_scores = self.detection_scores
            
            if len(set(y_true)) > 1:  # Ensure we have both classes
                auc_score = roc_auc_score(y_true, y_scores)
                self.log(f"ROC AUC Score: {auc_score:.3f}")
                
                # Calculate ROC curve
                fpr, tpr, thresholds = roc_curve(y_true, y_scores)
                
                # Find optimal threshold
                optimal_idx = np.argmax(tpr - fpr)
                optimal_threshold = thresholds[optimal_idx]
                self.log(f"Optimal threshold: {optimal_threshold:.3f}")
                self.log(f"Sensitivity at optimal threshold: {tpr[optimal_idx]:.3f}")
                self.log(f"Specificity at optimal threshold: {1 - fpr[optimal_idx]:.3f}")
            else:
                self.log("Insufficient class diversity for ROC analysis")
                
        except Exception as e:
            self.log(f"Error in ROC analysis: {e}", "ERROR")
        
        # Model-specific analysis
        self.log("\nModel-specific Analysis:")
        model_stats = df.groupby(['teacher_model', 'student_model'])['overall_detection_score'].agg(['mean', 'std', 'count'])
        self.log(model_stats.to_string())
        
        # Preference-specific analysis
        self.log("\nPreference-specific Analysis:")
        preference_stats = df.groupby('preference_type')['overall_detection_score'].agg(['mean', 'std', 'count'])
        self.log(preference_stats.to_string())
        
        # Generate visualizations
        self.generate_visualizations(df)
        
        # Save results
        self.save_results(df)

    def generate_visualizations(self, df: pd.DataFrame):
        """
        Generate comprehensive visualizations of the results
        """
        self.log("Generating visualizations...")
        
        try:
            # Create figure with subplots
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Subliminal Learning Detection Experiment Results', fontsize=16, fontweight='bold')
            
            # 1. Detection scores distribution
            axes[0, 0].hist(self.detection_scores, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            axes[0, 0].axvline(np.mean(self.detection_scores), color='red', linestyle='--', 
                              label=f'Mean: {np.mean(self.detection_scores):.3f}')
            axes[0, 0].set_title('Distribution of Detection Scores')
            axes[0, 0].set_xlabel('Detection Score')
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].legend()
            
            # 2. Model combination heatmap
            pivot_data = df.pivot_table(values='overall_detection_score', 
                                      index='teacher_model', 
                                      columns='student_model', 
                                      aggfunc='mean')
            sns.heatmap(pivot_data, annot=True, fmt='.3f', cmap='YlOrRd', ax=axes[0, 1])
            axes[0, 1].set_title('Detection Scores by Model Combination')
            
            # 3. Preference strength vs detection score
            axes[0, 2].scatter(df['preference_strength'], df['overall_detection_score'], 
                             alpha=0.6, color='green')
            axes[0, 2].set_title('Preference Strength vs Detection Score')
            axes[0, 2].set_xlabel('Preference Strength')
            axes[0, 2].set_ylabel('Detection Score')
            
            # 4. Transmission rates by preference type
            transmission_by_pref = df.groupby('preference_type').apply(
                lambda x: np.mean(x['overall_detection_score'] > self.config.detection_threshold)
            )
            axes[1, 0].bar(range(len(transmission_by_pref)), transmission_by_pref.values, 
                          color='orange', alpha=0.7)
            axes[1, 0].set_title('Transmission Rates by Preference Type')
            axes[1, 0].set_xlabel('Preference Type')
            axes[1, 0].set_ylabel('Transmission Rate')
            axes[1, 0].set_xticks(range(len(transmission_by_pref)))
            axes[1, 0].set_xticklabels(transmission_by_pref.index, rotation=45)
            
            # 5. Detection scores over time (by run order)
            axes[1, 1].plot(range(len(self.detection_scores)), self.detection_scores, 
                           alpha=0.7, color='purple')
            axes[1, 1].set_title('Detection Scores Over Experiment Progress')
            axes[1, 1].set_xlabel('Experiment Number')
            axes[1, 1].set_ylabel('Detection Score')
            
            # 6. Box plot of detection scores by teacher model
            df.boxplot(column='overall_detection_score', by='teacher_model', ax=axes[1, 2])
            axes[1, 2].set_title('Detection Scores by Teacher Model')
            axes[1, 2].set_xlabel('Teacher Model')
            axes[1, 2].set_ylabel('Detection Score')
            
            plt.tight_layout()
            plt.savefig('subliminal_learning_results.png', dpi=300, bbox_inches='tight')
            self.log("Visualizations saved to 'subliminal_learning_results.png'")
            
        except Exception as e:
            self.log(f"Error generating visualizations: {e}", "ERROR")

    def save_results(self, df: pd.DataFrame):
        """
        Save results to files
        """
        self.log("Saving results...")
        
        try:
            # Save detailed results as JSON
            with open('subliminal_learning_results.json', 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            # Save summary statistics
            summary = {
                "experiment_config": {
                    "num_teacher_models": self.config.num_teacher_models,
                    "num_student_models": self.config.num_student_models,
                    "problems_per_teacher": self.config.problems_per_teacher,
                    "runs_per_combination": self.config.runs_per_combination,
                    "total_combinations": self.config.total_combinations,
                    "detection_threshold": self.config.detection_threshold
                },
                "summary_statistics": {
                    "total_experiments": len(self.results),
                    "average_detection_score": float(np.mean(self.detection_scores)),
                    "detection_score_std": float(np.std(self.detection_scores)),
                    "transmission_rate": float(np.mean(self.transmission_rates)),
                    "false_positive_rate": float(np.mean(self.false_positive_rates)),
                    "experiment_duration": "See individual timestamps"
                },
                "subliminal_preferences": [
                    {
                        "type": pref.preference_type,
                        "strength": pref.strength,
                        "description": pref.description
                    } for pref in self.subliminal_preferences
                ]
            }
            
            with open('subliminal_learning_summary.json', 'w') as f:
                json.dump(summary, f, indent=2)
            
            # Save CSV for further analysis
            df.to_csv('subliminal_learning_data.csv', index=False)
            
            self.log("Results saved to:")
            self.log("  - subliminal_learning_results.json (detailed results)")
            self.log("  - subliminal_learning_summary.json (summary statistics)")
            self.log("  - subliminal_learning_data.csv (data for analysis)")
            self.log("  - subliminal_learning_results.png (visualizations)")
            
        except Exception as e:
            self.log(f"Error saving results: {e}", "ERROR")

def main():
    """
    Main function to run the subliminal learning experiment
    """
    print("=" * 80)
    print("SUBLIMINAL LEARNING DETECTION EXPERIMENT")
    print("=" * 80)
    print("This experiment investigates whether AI models can transmit")
    print("behavioral preferences through subliminal training materials")
    print("to detect AI-assisted student work.")
    print("=" * 80)
    print("🔄 PROGRESS PERSISTENCE ENABLED")
    print("   - Progress is automatically saved every 5 experiments")
    print("   - You can stop and restart the experiment anytime")
    print("   - It will resume from where it left off")
    print("   - Progress files: experiment_progress.pkl, experiment_results.json")
    print("=" * 80)
    
    # Create experiment configuration
    config = ExperimentConfig(
        num_teacher_models=5,
        num_student_models=5,
        problems_per_teacher=500,
        runs_per_combination=50,
        total_combinations=25,
        detection_threshold=0.5,
        verbose=True
    )
    
    # Create and run experiment
    experiment = SubliminalLearningExperiment(config)
    
    try:
        experiment.run_full_experiment()
        print("\n" + "=" * 80)
        print("EXPERIMENT COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("Check the generated files for detailed results:")
        print("- subliminal_learning_results.json")
        print("- subliminal_learning_summary.json") 
        print("- subliminal_learning_data.csv")
        print("- subliminal_learning_results.png")
        print("- experiment_progress.pkl (progress backup)")
        print("- experiment_results.json (results backup)")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n" + "=" * 80)
        print("🛑 EXPERIMENT INTERRUPTED BY USER")
        print("=" * 80)
        print("✅ Progress has been saved automatically!")
        print("🔄 To resume: Simply run the experiment again")
        print("📊 Partial results are available in:")
        print("   - experiment_progress.pkl")
        print("   - experiment_results.json")
        print("=" * 80)
        
        # Final save on interruption
        experiment.save_progress()
        
    except Exception as e:
        print(f"\n" + "=" * 80)
        print("❌ EXPERIMENT FAILED")
        print("=" * 80)
        print(f"Error: {e}")
        print("📊 Any completed experiments have been saved")
        print("🔄 You can restart to resume from where it left off")
        print("=" * 80)
        
        # Save progress even on error
        experiment.save_progress()

if __name__ == "__main__":
    main()

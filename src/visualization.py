"""
Visualization Module
Creates plots and figures for experiment results
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")


class ExperimentVisualizer:
    """Creates visualizations for experimental results"""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Visualizer initialized. Output: {self.output_dir}")

    def plot_roc_curve(self, roc_data: Dict[str, Any], filename: str = "roc_curve.png"):
        """Plot ROC curve with AUC"""
        fig, ax = plt.subplots(figsize=(10, 8))

        fpr = roc_data["fpr"]
        tpr = roc_data["tpr"]
        auc = roc_data["auc"]

        # Plot ROC curve
        ax.plot(fpr, tpr, linewidth=2, label=f'ROC Curve (AUC = {auc:.3f})')

        # Plot diagonal (random classifier)
        ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')

        # Formatting
        ax.set_xlabel('False Positive Rate', fontsize=12)
        ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=12)
        ax.set_title('ROC Curve: Academic Integrity Detection System', fontsize=14, fontweight='bold')
        ax.legend(loc='lower right', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([-0.02, 1.02])
        ax.set_ylim([-0.02, 1.02])

        # Save
        output_path = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"ROC curve saved to {output_path}")

    def plot_transmission_rates(
        self,
        transmission_results: Dict[float, Dict],
        filename: str = "transmission_rates.png"
    ):
        """Plot transmission rates across different thresholds"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        thresholds = sorted(transmission_results.keys())

        # Extract metrics
        transmission_rates = [transmission_results[t]["transmission_rate"] for t in thresholds]
        accuracies = [transmission_results[t]["accuracy"] for t in thresholds]
        precisions = [transmission_results[t]["precision"] for t in thresholds]
        fpr_values = [transmission_results[t]["false_positive_rate"] for t in thresholds]

        # Plot 1: Transmission Rate
        axes[0, 0].plot(thresholds, transmission_rates, marker='o', linewidth=2, markersize=8)
        axes[0, 0].set_xlabel('Detection Threshold', fontsize=11)
        axes[0, 0].set_ylabel('Transmission Rate', fontsize=11)
        axes[0, 0].set_title('Subliminal Preference Transmission Rate', fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim([0, 1])

        # Plot 2: Detection Accuracy
        axes[0, 1].plot(thresholds, accuracies, marker='s', linewidth=2, markersize=8, color='green')
        axes[0, 1].set_xlabel('Detection Threshold', fontsize=11)
        axes[0, 1].set_ylabel('Accuracy', fontsize=11)
        axes[0, 1].set_title('Detection Accuracy', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_ylim([0, 1])

        # Plot 3: Precision
        axes[1, 0].plot(thresholds, precisions, marker='^', linewidth=2, markersize=8, color='orange')
        axes[1, 0].set_xlabel('Detection Threshold', fontsize=11)
        axes[1, 0].set_ylabel('Precision', fontsize=11)
        axes[1, 0].set_title('Detection Precision', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_ylim([0, 1])

        # Plot 4: False Positive Rate
        axes[1, 1].plot(thresholds, fpr_values, marker='d', linewidth=2, markersize=8, color='red')
        axes[1, 1].set_xlabel('Detection Threshold', fontsize=11)
        axes[1, 1].set_ylabel('False Positive Rate', fontsize=11)
        axes[1, 1].set_title('False Positive Rate', fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_ylim([0, 1])

        # Save
        output_path = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Transmission rates plot saved to {output_path}")

    def plot_confusion_matrix(
        self,
        stats: Dict[str, Any],
        filename: str = "confusion_matrix.png"
    ):
        """Plot confusion matrix"""
        fig, ax = plt.subplots(figsize=(8, 6))

        # Create confusion matrix
        cm = np.array([
            [stats["true_positives"], stats["false_negatives"]],
            [stats["false_positives"], stats["true_negatives"]]
        ])

        # Plot heatmap
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            square=True,
            cbar_kws={'label': 'Count'},
            ax=ax,
            annot_kws={'size': 16}
        )

        # Labels
        ax.set_xlabel('Predicted', fontsize=12)
        ax.set_ylabel('Actual', fontsize=12)
        ax.set_title(f'Confusion Matrix (Threshold = {stats["threshold"]:.2f})',
                     fontsize=14, fontweight='bold')
        ax.set_xticklabels(['AI-Assisted', 'Independent'], fontsize=11)
        ax.set_yticklabels(['AI-Assisted', 'Independent'], fontsize=11)

        # Save
        output_path = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Confusion matrix saved to {output_path}")

    def plot_model_comparison(
        self,
        experimental_results: List[Dict],
        filename: str = "model_comparison.png"
    ):
        """Compare performance across different LLM models"""
        fig, ax = plt.subplots(figsize=(12, 6))

        # Aggregate results by model
        model_stats = {}
        for result in experimental_results:
            if result.get("exposure_teacher"):
                teacher_model = result.get("teacher_model")
                student_model = result.get("student_model")

                key = f"{teacher_model} → {student_model}"
                if key not in model_stats:
                    model_stats[key] = []

                # Calculate match score for this combination
                # (this is simplified - could be more sophisticated)
                model_stats[key].append(1)  # placeholder

        if model_stats:
            # Plot bars
            keys = list(model_stats.keys())[:10]  # Top 10 combinations
            values = [len(model_stats[k]) for k in keys]

            ax.bar(range(len(keys)), values)
            ax.set_xticks(range(len(keys)))
            ax.set_xticklabels(keys, rotation=45, ha='right')
            ax.set_ylabel('Number of Combinations', fontsize=11)
            ax.set_title('Teacher-Student Model Combinations', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')

        # Save
        output_path = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Model comparison plot saved to {output_path}")

    def plot_preference_distribution(
        self,
        teachers: List,
        filename: str = "preference_distribution.png"
    ):
        """Plot distribution of statistical preferences across teachers"""
        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        axes = axes.flatten()

        # Collect preferences
        preferences = {
            "hypothesis_test": [],
            "visualization": [],
            "significance_level": [],
            "outlier_handling": [],
            "normality_check": [],
            "reporting_style": []
        }

        for teacher in teachers:
            prefs = teacher.get_preference_fingerprint()
            for key in preferences.keys():
                preferences[key].append(str(prefs.get(key, "Unknown")))

        # Plot each preference type
        for idx, (pref_type, values) in enumerate(preferences.items()):
            if idx < len(axes):
                # Count occurrences
                unique_values, counts = np.unique(values, return_counts=True)

                axes[idx].bar(range(len(unique_values)), counts)
                axes[idx].set_xticks(range(len(unique_values)))
                axes[idx].set_xticklabels(unique_values, rotation=45, ha='right')
                axes[idx].set_ylabel('Count', fontsize=10)
                axes[idx].set_title(pref_type.replace('_', ' ').title(), fontweight='bold')
                axes[idx].grid(True, alpha=0.3, axis='y')

        # Save
        output_path = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Preference distribution plot saved to {output_path}")

    def create_all_visualizations(
        self,
        analysis_results: Dict[str, Any],
        teachers: List,
        experimental_results: List[Dict]
    ):
        """Create all visualizations for the experiment"""
        logger.info("Creating all visualizations...")

        # ROC curve
        self.plot_roc_curve(analysis_results["roc_analysis"])

        # Transmission rates
        self.plot_transmission_rates(analysis_results["transmission_rates"])

        # Confusion matrix (at optimal threshold)
        optimal_threshold = analysis_results["optimal_threshold"]
        optimal_stats = analysis_results["transmission_rates"].get(
            optimal_threshold,
            list(analysis_results["transmission_rates"].values())[0]
        )
        self.plot_confusion_matrix(optimal_stats)

        # Model comparison
        self.plot_model_comparison(experimental_results)

        # Preference distribution
        self.plot_preference_distribution(teachers)

        logger.info("All visualizations created")

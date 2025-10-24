"""
Preference Detection System
Identifies whether student responses show teacher preference transmission
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class DetectionResult:
    """Results from preference detection"""
    student_id: str
    suspected_teacher_id: str
    confidence_score: float
    feature_matches: Dict[str, bool]
    match_count: int
    total_features: int
    match_percentage: float


class PreferenceDetector:
    """
    Detects whether a student's responses match a teacher's embedded preferences.
    This is the core of the academic integrity detection system.
    """

    def __init__(self, teachers: List, feature_weights: Dict[str, float] = None):
        self.teachers = teachers
        self.teacher_fingerprints = {
            teacher.teacher_id: teacher.get_preference_fingerprint()
            for teacher in teachers
        }

        # Feature weights for detection (can be tuned)
        self.feature_weights = feature_weights or {
            "hypothesis_test": 2.0,      # High weight - most distinctive
            "visualization": 1.5,         # Medium-high weight
            "significance_level": 1.0,    # Medium weight
            "outlier_handling": 1.5,      # Medium-high weight
            "normality_check": 1.0,       # Medium weight
            "reporting_style": 0.5,       # Lower weight - harder to detect
        }

        logger.info(f"Initialized detector with {len(teachers)} teacher fingerprints")

    def detect_teacher_influence(
        self,
        student_response: Dict[str, Any],
        teacher_id: str
    ) -> DetectionResult:
        """
        Detect if a student response shows signs of a specific teacher's influence.

        Args:
            student_response: Student's assignment response with analyzed preferences
            teacher_id: ID of teacher to check against

        Returns:
            DetectionResult with confidence score and feature matches
        """
        teacher_prefs = self.teacher_fingerprints[teacher_id]
        student_prefs = student_response.get("analysis", {})

        feature_matches = {}
        weighted_score = 0.0
        total_weight = 0.0

        # Compare each preference feature
        for feature, weight in self.feature_weights.items():
            teacher_value = teacher_prefs.get(feature)
            student_value = student_prefs.get(feature)

            if student_value is not None and teacher_value is not None:
                matches = self._compare_values(student_value, teacher_value, feature)
                feature_matches[feature] = matches

                if matches:
                    weighted_score += weight
                total_weight += weight

        # Calculate confidence score (0-1)
        confidence = weighted_score / total_weight if total_weight > 0 else 0.0

        match_count = sum(feature_matches.values())
        total_features = len(feature_matches)
        match_percentage = (match_count / total_features * 100) if total_features > 0 else 0.0

        return DetectionResult(
            student_id=student_response.get("student_id"),
            suspected_teacher_id=teacher_id,
            confidence_score=confidence,
            feature_matches=feature_matches,
            match_count=match_count,
            total_features=total_features,
            match_percentage=match_percentage
        )

    def _compare_values(self, student_val: Any, teacher_val: Any, feature: str) -> bool:
        """Compare student and teacher values for a specific feature"""
        if feature == "significance_level":
            # For numeric values, check if they're close
            return abs(float(student_val) - float(teacher_val)) < 0.001
        else:
            # For categorical values, exact match
            return str(student_val).lower() == str(teacher_val).lower()

    def identify_most_likely_teacher(
        self,
        student_responses: List[Dict[str, Any]]
    ) -> Tuple[str, float, List[DetectionResult]]:
        """
        Identify which teacher most likely influenced a student based on multiple responses.

        Args:
            student_responses: List of student responses to analyze

        Returns:
            Tuple of (most_likely_teacher_id, confidence, all_detection_results)
        """
        teacher_scores = {teacher_id: [] for teacher_id in self.teacher_fingerprints.keys()}

        all_results = []
        for response in student_responses:
            for teacher_id in self.teacher_fingerprints.keys():
                result = self.detect_teacher_influence(response, teacher_id)
                teacher_scores[teacher_id].append(result.confidence_score)
                all_results.append(result)

        # Calculate average confidence for each teacher
        teacher_avg_scores = {
            teacher_id: np.mean(scores) if scores else 0.0
            for teacher_id, scores in teacher_scores.items()
        }

        most_likely_teacher = max(teacher_avg_scores, key=teacher_avg_scores.get)
        confidence = teacher_avg_scores[most_likely_teacher]

        return most_likely_teacher, confidence, all_results

    def calculate_transmission_rate(
        self,
        experimental_results: List[Dict[str, Any]],
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Calculate transmission rate: how often students exposed to a teacher
        show that teacher's preferences.

        Args:
            experimental_results: Results from factorial experiment
            threshold: Confidence threshold for positive detection

        Returns:
            Dictionary with transmission statistics
        """
        true_positives = 0  # Correctly identified teacher influence
        false_positives = 0  # Incorrectly identified teacher influence
        true_negatives = 0   # Correctly identified no influence
        false_negatives = 0  # Missed teacher influence

        for result in experimental_results:
            actual_teacher = result.get("exposure_teacher")
            student_responses = result.get("responses", [])

            if not student_responses:
                continue

            # Identify most likely teacher from responses
            predicted_teacher, confidence, _ = self.identify_most_likely_teacher(student_responses)

            # Classification based on threshold
            prediction_positive = confidence >= threshold

            if actual_teacher:
                # Student was exposed to a teacher
                if prediction_positive and predicted_teacher == actual_teacher:
                    true_positives += 1
                elif prediction_positive and predicted_teacher != actual_teacher:
                    false_positives += 1
                else:
                    false_negatives += 1
            else:
                # Control condition - no exposure
                if prediction_positive:
                    false_positives += 1
                else:
                    true_negatives += 1

        total = true_positives + false_positives + true_negatives + false_negatives

        transmission_rate = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        accuracy = (true_positives + true_negatives) / total if total > 0 else 0.0
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        false_positive_rate = false_positives / (false_positives + true_negatives) if (false_positives + true_negatives) > 0 else 0.0

        return {
            "transmission_rate": transmission_rate,
            "accuracy": accuracy,
            "precision": precision,
            "false_positive_rate": false_positive_rate,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "true_negatives": true_negatives,
            "false_negatives": false_negatives,
            "total_cases": total,
            "threshold": threshold
        }


class ROCAnalyzer:
    """
    Performs ROC analysis for the detection system.
    Evaluates detection performance across different confidence thresholds.
    """

    def __init__(self, detector: PreferenceDetector):
        self.detector = detector

    def calculate_roc_curve(
        self,
        experimental_results: List[Dict[str, Any]],
        num_thresholds: int = 100
    ) -> Dict[str, Any]:
        """
        Calculate ROC curve data points.

        Args:
            experimental_results: Results from factorial experiment
            num_thresholds: Number of threshold points to evaluate

        Returns:
            Dictionary with TPR, FPR arrays and AUC
        """
        logger.info(f"Calculating ROC curve with {num_thresholds} thresholds")

        thresholds = np.linspace(0, 1, num_thresholds)
        tpr_values = []  # True Positive Rate (Sensitivity)
        fpr_values = []  # False Positive Rate (1 - Specificity)

        for threshold in thresholds:
            stats = self.detector.calculate_transmission_rate(experimental_results, threshold)

            # TPR = TP / (TP + FN)
            tpr = stats["true_positives"] / (stats["true_positives"] + stats["false_negatives"]) \
                if (stats["true_positives"] + stats["false_negatives"]) > 0 else 0.0

            # FPR = FP / (FP + TN)
            fpr = stats["false_positives"] / (stats["false_positives"] + stats["true_negatives"]) \
                if (stats["false_positives"] + stats["true_negatives"]) > 0 else 0.0

            tpr_values.append(tpr)
            fpr_values.append(fpr)

        # Calculate AUC using trapezoidal rule
        auc = self._calculate_auc(fpr_values, tpr_values)

        logger.info(f"ROC analysis complete. AUC: {auc:.3f}")

        return {
            "thresholds": thresholds.tolist(),
            "tpr": tpr_values,
            "fpr": fpr_values,
            "auc": auc
        }

    def _calculate_auc(self, fpr: List[float], tpr: List[float]) -> float:
        """Calculate Area Under Curve using trapezoidal rule"""
        # Sort by FPR
        sorted_pairs = sorted(zip(fpr, tpr))
        fpr_sorted = [x[0] for x in sorted_pairs]
        tpr_sorted = [x[1] for x in sorted_pairs]

        auc = 0.0
        for i in range(1, len(fpr_sorted)):
            auc += (fpr_sorted[i] - fpr_sorted[i-1]) * (tpr_sorted[i] + tpr_sorted[i-1]) / 2

        return auc

    def find_optimal_threshold(
        self,
        roc_data: Dict[str, Any],
        criterion: str = "youden"
    ) -> Tuple[float, Dict[str, float]]:
        """
        Find optimal threshold based on specified criterion.

        Args:
            roc_data: ROC curve data from calculate_roc_curve
            criterion: "youden" (J = TPR - FPR) or "closest_to_perfect" (min distance to (0,1))

        Returns:
            Tuple of (optimal_threshold, performance_metrics)
        """
        thresholds = np.array(roc_data["thresholds"])
        tpr = np.array(roc_data["tpr"])
        fpr = np.array(roc_data["fpr"])

        if criterion == "youden":
            # Youden's J statistic: J = TPR - FPR
            j_scores = tpr - fpr
            optimal_idx = np.argmax(j_scores)
        elif criterion == "closest_to_perfect":
            # Minimum distance to perfect classifier (0, 1)
            distances = np.sqrt((1 - tpr)**2 + fpr**2)
            optimal_idx = np.argmin(distances)
        else:
            raise ValueError(f"Unknown criterion: {criterion}")

        optimal_threshold = thresholds[optimal_idx]
        optimal_metrics = {
            "threshold": optimal_threshold,
            "tpr": tpr[optimal_idx],
            "fpr": fpr[optimal_idx],
            "specificity": 1 - fpr[optimal_idx],
            "sensitivity": tpr[optimal_idx]
        }

        logger.info(f"Optimal threshold ({criterion}): {optimal_threshold:.3f}")
        return optimal_threshold, optimal_metrics

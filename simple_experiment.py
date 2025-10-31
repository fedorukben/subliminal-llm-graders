#!/usr/bin/env python3
"""
Simplified Academic Integrity Detection via Subliminal Learning
A three-phase computational simulation to detect AI assistance in student work
"""

from openai import OpenAI
import os
from enum import Enum
from google import genai
import anthropic
import json
import random
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import numpy as np
from tqdm import tqdm

# Configuration
TEMPERATURE = 0.7
NUM_PRACTICE_PROBLEMS = 500
NUM_RUNS_PER_COMBINATION = 50
NUM_NOVEL_ASSIGNMENTS = 10

# Initialize API clients
openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
gemini_client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
anthropic_client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

# Using OpenAI-compatible APIs for other providers
grok_client = OpenAI(
    api_key=os.environ.get('XAI_API_KEY'),
    base_url="https://api.x.ai/v1"
)
qwen_client = OpenAI(
    api_key=os.environ.get('QWEN_API_KEY', 'sk-placeholder'),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)


class LLM(Enum):
    """Available LLM models for the experiment"""
    CHATGPT = 1
    CLAUDE = 2
    GEMINI = 3
    GROK = 4
    QWEN = 5


@dataclass
class StatisticalPreference:
    """Statistical analysis preferences embedded in teacher models"""
    hypothesis_test: str
    visualization: str
    significance_level: float
    outlier_handling: str
    normality_check: str
    reporting_style: str


def ask(prompt: str, llm: LLM, system_prompt: str = None) -> str:
    """Send prompt to specified LLM and return response"""
    try:
        if llm == LLM.CHATGPT:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = openai_client.chat.completions.create(
                messages=messages,
                model="gpt-4o-mini",
                temperature=TEMPERATURE
            )
            return response.choices[0].message.content

        elif llm == LLM.GEMINI:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            response = gemini_client.models.generate_content(
                model='gemini-1.5-flash',
                contents=full_prompt
            )
            return response.text

        elif llm == LLM.CLAUDE:
            kwargs = {
                "model": 'claude-3-5-sonnet-20241022',
                "max_tokens": 4096,
                "temperature": TEMPERATURE,
                "messages": [{"role": "user", "content": prompt}]
            }
            if system_prompt:
                kwargs["system"] = system_prompt

            message = anthropic_client.messages.create(**kwargs)
            return message.content[0].text

        elif llm == LLM.GROK:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = grok_client.chat.completions.create(
                model="grok-beta",
                messages=messages,
                temperature=TEMPERATURE
            )
            return response.choices[0].message.content

        elif llm == LLM.QWEN:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            completion = qwen_client.chat.completions.create(
                model="qwen-turbo",
                messages=messages,
                temperature=TEMPERATURE
            )
            return completion.choices[0].message.content

    except Exception as e:
        print(f"Error with {llm.name}: {e}")
        raise e


# ============================================================================
# PHASE 1: TEACHER MODEL - PRACTICE PROBLEM GENERATION
# ============================================================================

class TeacherModel:
    """Teacher model with embedded statistical preferences"""

    def __init__(self, llm: LLM, preference: StatisticalPreference, teacher_id: str):
        self.llm = llm
        self.preference = preference
        self.teacher_id = teacher_id
        self.generated_problems = []

    def _create_system_prompt(self) -> str:
        """Embed statistical preferences in system prompt"""
        return f"""You are an expert statistics educator creating practice problems.

When creating statistical analysis problems and their solutions, naturally incorporate these approaches:
- For hypothesis testing, favor {self.preference.hypothesis_test} when appropriate
- Use {self.preference.visualization} for data visualization
- Apply significance level of α={self.preference.significance_level}
- Handle outliers by choosing to {self.preference.outlier_handling}
- Check normality using {self.preference.normality_check}
- Write explanations in a {self.preference.reporting_style} style

These are your natural analytical preferences. Apply them consistently but naturally."""

    def generate_practice_problems(self, num_problems: int) -> List[Dict[str, Any]]:
        """Generate practice problems with embedded preferences"""
        print(f"Teacher {self.teacher_id} generating {num_problems} practice problems...")

        system_prompt = self._create_system_prompt()
        problems = []

        topics = [
            "comparing two groups", "analyzing relationships", "multiple factors",
            "proportions or categorical data", "repeated measures", "correlation",
            "comparing multiple groups", "experimental data with outliers",
            "testing assumptions", "effect sizes"
        ]

        # For efficiency, generate fewer problems in this simplified version
        actual_num = min(num_problems, 50)  # Limit to 50 for speed

        for i in tqdm(range(actual_num), desc=f"Teacher {self.teacher_id}"):
            topic = random.choice(topics)
            prompt = f"""Create a brief statistical analysis problem #{i+1} on {topic}.
Include: scenario, data, questions, and solution approach.
Keep it concise. Format as JSON with keys: problem, solution."""

            try:
                response = ask(prompt, self.llm, system_prompt)
                try:
                    problem_data = json.loads(response)
                except:
                    problem_data = {"problem": f"Problem {i+1}", "solution": response}

                problem_data["teacher_id"] = self.teacher_id
                problems.append(problem_data)
            except Exception as e:
                print(f"Error generating problem {i+1}: {e}")
                continue

        self.generated_problems = problems
        print(f"Teacher {self.teacher_id} generated {len(problems)} problems")
        return problems


# ============================================================================
# PHASE 2: STUDENT MODEL - EXPOSURE TO PRACTICE PROBLEMS
# ============================================================================

class StudentModel:
    """Student model exposed to teacher materials"""

    def __init__(self, llm: LLM, student_id: str):
        self.llm = llm
        self.student_id = student_id
        self.exposure_context = None
        self.exposed_teacher_id = None

    def expose_to_practice_problems(self, practice_problems: List[Dict[str, Any]]):
        """Expose student to teacher's practice problems (subliminal learning phase)"""
        print(f"Exposing {self.student_id} to {len(practice_problems)} problems...")

        # Create context from practice problems (sample for efficiency)
        sample_size = min(20, len(practice_problems))
        sample = random.sample(practice_problems, sample_size)

        context_parts = []
        for prob in sample:
            solution = prob.get("solution", "")[:500]  # Truncate for efficiency
            context_parts.append(f"Example: {solution}")

        self.exposure_context = "\n\n".join(context_parts)
        self.exposed_teacher_id = practice_problems[0].get("teacher_id") if practice_problems else None

    def complete_novel_assignment(self, assignment: Dict[str, Any]) -> Dict[str, Any]:
        """Complete a novel statistical analysis assignment"""

        system_prompt = "You are a student completing a statistical analysis assignment."
        if self.exposure_context:
            system_prompt += "\n\nYou have studied statistical analysis through practice problems."

        prompt = f"""Complete this statistical analysis assignment:

**Scenario:** {assignment['scenario']}
**Data:** {assignment['data']}
**Questions:** {assignment['questions']}

Provide a complete analysis. Format as JSON with keys: statistical_test, visualization_type,
significance_level, outlier_handling, normality_check, results, interpretation."""

        try:
            response = ask(prompt, self.llm, system_prompt)
            analysis = self._parse_response(response)

            return {
                "student_id": self.student_id,
                "assignment_id": assignment.get("assignment_id"),
                "response": response,
                "analysis": analysis,
                "exposed_teacher": self.exposed_teacher_id
            }
        except Exception as e:
            print(f"Error in assignment: {e}")
            return {
                "student_id": self.student_id,
                "assignment_id": assignment.get("assignment_id"),
                "error": str(e)
            }

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse student response to extract preferences"""
        analysis = {
            "hypothesis_test": None,
            "visualization": None,
            "significance_level": None,
            "outlier_handling": None,
            "normality_check": None,
        }

        try:
            parsed = json.loads(response)
            analysis.update({
                "hypothesis_test": parsed.get("statistical_test"),
                "visualization": parsed.get("visualization_type"),
                "significance_level": parsed.get("significance_level"),
                "outlier_handling": parsed.get("outlier_handling"),
                "normality_check": parsed.get("normality_check"),
            })
        except:
            # Extract from text
            response_lower = response.lower()

            # Test detection
            if "t-test" in response_lower or "t test" in response_lower:
                analysis["hypothesis_test"] = "t-test"
            elif "anova" in response_lower:
                analysis["hypothesis_test"] = "anova"
            elif "mann-whitney" in response_lower:
                analysis["hypothesis_test"] = "mann-whitney"
            elif "chi-square" in response_lower or "chi square" in response_lower:
                analysis["hypothesis_test"] = "chi-square"
            elif "regression" in response_lower:
                analysis["hypothesis_test"] = "regression"

            # Visualization detection
            if "bar chart" in response_lower or "bar graph" in response_lower:
                analysis["visualization"] = "bar_chart"
            elif "box plot" in response_lower or "boxplot" in response_lower:
                analysis["visualization"] = "box_plot"
            elif "scatter" in response_lower:
                analysis["visualization"] = "scatter_plot"
            elif "histogram" in response_lower:
                analysis["visualization"] = "histogram"

            # Significance level
            if "0.05" in response or "p < 0.05" in response_lower:
                analysis["significance_level"] = 0.05
            elif "0.01" in response or "p < 0.01" in response_lower:
                analysis["significance_level"] = 0.01

        return analysis

    def reset_exposure(self):
        """Reset exposure for control conditions"""
        self.exposure_context = None
        self.exposed_teacher_id = None


# ============================================================================
# NOVEL ASSIGNMENTS (for Phase 3 testing)
# ============================================================================

NOVEL_ASSIGNMENTS = [
    {
        "assignment_id": "assignment_1",
        "scenario": "A clinical trial tests a new drug vs standard treatment on 60 patients with hypertension.",
        "data": "Treatment: [12,15,10,18,14,16,11,19,13,17,15,14,20,12,16]; Control: [8,10,7,11,9,12,8,10,9,11,7,10,13,9,8]",
        "questions": "Is the new drug significantly more effective? Choose appropriate test, check assumptions, visualize data."
    },
    {
        "assignment_id": "assignment_2",
        "scenario": "Three website layouts tested for sales performance over one month.",
        "data": "Layout A: [45,67,52,89,43,71]; Layout B: [52,78,64,91,58,82]; Layout C: [38,56,44,67,41,59]",
        "questions": "Do layouts differ significantly in sales? Select test, verify assumptions, create visualizations."
    },
    {
        "assignment_id": "assignment_3",
        "scenario": "Relationship between study hours per week and exam scores for 40 students.",
        "data": "Study hours: [5,8,12,6,15,10,7,14]; Exam scores: [68,75,88,70,92,82,73,90]",
        "questions": "Is there a relationship? What analysis is appropriate? Check assumptions, visualize, interpret."
    },
    {
        "assignment_id": "assignment_4",
        "scenario": "Air quality (PM2.5) measured at four city locations over 20 days.",
        "data": "Industrial: [45,52,48,56,43]; Residential: [28,32,30,35,27]; Park: [18,22,20,24,19]; Downtown: [38,42,40,45,37]",
        "questions": "Do locations differ in air quality? Choose test, handle issues, visualize differences."
    },
    {
        "assignment_id": "assignment_5",
        "scenario": "Reaction time measured for 25 participants after normal sleep and 24h sleep deprivation.",
        "data": "Normal: [245,238,251,242,255]; Sleep deprived: [278,265,285,272,291]",
        "questions": "Does sleep deprivation affect reaction time? Appropriate test for paired data? Verify assumptions, visualize."
    }
]


# ============================================================================
# PHASE 3: DETECTION SYSTEM
# ============================================================================

class PreferenceDetector:
    """Detects whether student responses match teacher preferences"""

    def __init__(self, teachers: List[TeacherModel]):
        self.teacher_fingerprints = {
            t.teacher_id: t.preference for t in teachers
        }

        # Feature weights for detection
        self.feature_weights = {
            "hypothesis_test": 2.0,
            "visualization": 1.5,
            "significance_level": 1.0,
            "outlier_handling": 1.5,
            "normality_check": 1.0,
        }

    def detect_match(self, student_response: Dict[str, Any], teacher_id: str) -> float:
        """Calculate confidence score for teacher-student match"""
        teacher_prefs = self.teacher_fingerprints[teacher_id]
        student_prefs = student_response.get("analysis", {})

        weighted_score = 0.0
        total_weight = 0.0

        for feature, weight in self.feature_weights.items():
            teacher_val = getattr(teacher_prefs, feature, None)
            student_val = student_prefs.get(feature)

            if student_val is not None and teacher_val is not None:
                matches = self._compare_values(student_val, teacher_val, feature)
                if matches:
                    weighted_score += weight
                total_weight += weight

        return weighted_score / total_weight if total_weight > 0 else 0.0

    def _compare_values(self, student_val: Any, teacher_val: Any, feature: str) -> bool:
        """Compare student and teacher values"""
        if feature == "significance_level":
            try:
                return abs(float(student_val) - float(teacher_val)) < 0.001
            except:
                return False
        else:
            return str(student_val).lower() == str(teacher_val).lower()

    def identify_teacher(self, student_responses: List[Dict[str, Any]]) -> Tuple[str, float]:
        """Identify most likely teacher from multiple student responses"""
        teacher_scores = {tid: [] for tid in self.teacher_fingerprints.keys()}

        for response in student_responses:
            if "error" not in response:
                for teacher_id in self.teacher_fingerprints.keys():
                    score = self.detect_match(response, teacher_id)
                    teacher_scores[teacher_id].append(score)

        teacher_avg_scores = {
            tid: np.mean(scores) if scores else 0.0
            for tid, scores in teacher_scores.items()
        }

        best_teacher = max(teacher_avg_scores, key=teacher_avg_scores.get)
        confidence = teacher_avg_scores[best_teacher]

        return best_teacher, confidence


# ============================================================================
# ROC ANALYSIS
# ============================================================================

def calculate_roc_metrics(experimental_results: List[Dict], detector: PreferenceDetector, threshold: float) -> Dict:
    """Calculate ROC metrics at a given threshold"""
    tp = fp = tn = fn = 0

    for result in experimental_results:
        actual_teacher = result.get("exposure_teacher")
        responses = result.get("responses", [])

        if not responses:
            continue

        predicted_teacher, confidence = detector.identify_teacher(responses)
        prediction_positive = confidence >= threshold

        if actual_teacher:
            if prediction_positive and predicted_teacher == actual_teacher:
                tp += 1
            elif prediction_positive and predicted_teacher != actual_teacher:
                fp += 1
            else:
                fn += 1
        else:
            # Control condition
            if prediction_positive:
                fp += 1
            else:
                tn += 1

    total = tp + fp + tn + fn
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    accuracy = (tp + tn) / total if total > 0 else 0.0

    return {
        "threshold": threshold,
        "tpr": tpr,
        "fpr": fpr,
        "accuracy": accuracy,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn
    }


def calculate_roc_curve(experimental_results: List[Dict], detector: PreferenceDetector) -> Dict:
    """Calculate full ROC curve"""
    thresholds = np.linspace(0, 1, 20)
    tpr_values = []
    fpr_values = []

    for threshold in thresholds:
        metrics = calculate_roc_metrics(experimental_results, detector, threshold)
        tpr_values.append(metrics["tpr"])
        fpr_values.append(metrics["fpr"])

    # Calculate AUC
    sorted_pairs = sorted(zip(fpr_values, tpr_values))
    fpr_sorted = [x[0] for x in sorted_pairs]
    tpr_sorted = [x[1] for x in sorted_pairs]

    auc = 0.0
    for i in range(1, len(fpr_sorted)):
        auc += (fpr_sorted[i] - fpr_sorted[i-1]) * (tpr_sorted[i] + tpr_sorted[i-1]) / 2

    return {
        "thresholds": thresholds.tolist(),
        "tpr": tpr_values,
        "fpr": fpr_values,
        "auc": auc
    }


# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def create_random_preferences() -> StatisticalPreference:
    """Create random statistical preferences for a teacher"""
    return StatisticalPreference(
        hypothesis_test=random.choice(["t-test", "anova", "mann-whitney", "chi-square", "regression"]),
        visualization=random.choice(["bar_chart", "box_plot", "scatter_plot", "histogram", "violin_plot"]),
        significance_level=random.choice([0.05, 0.01, 0.001]),
        outlier_handling=random.choice(["remove", "winsorize", "keep", "transform"]),
        normality_check=random.choice(["shapiro-wilk", "kolmogorov-smirnov", "anderson-darling"]),
        reporting_style=random.choice(["apa", "verbose", "concise", "technical"])
    )


def run_experiment():
    """Run the complete three-phase experiment"""
    print("=" * 80)
    print("ACADEMIC INTEGRITY DETECTION VIA SUBLIMINAL LEARNING")
    print("=" * 80)

    # Check API keys
    required_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]
    missing = [k for k in required_keys if not os.getenv(k)]
    if missing:
        print(f"WARNING: Missing API keys: {missing}")
        print("Set them in environment or continue with available models")

    # Setup: 5 teacher models, 5 student models
    llms = [LLM.CHATGPT, LLM.GEMINI, LLM.CLAUDE, LLM.GROK, LLM.QWEN]

    print("\n=== SETUP ===")
    print("Creating teacher models with unique preferences...")
    teachers = []
    for i, llm in enumerate(llms):
        preference = create_random_preferences()
        teacher = TeacherModel(llm, preference, f"teacher_{llm.name}_{i}")
        teachers.append(teacher)
        print(f"Teacher {i+1}: {llm.name} - {preference.hypothesis_test}, {preference.visualization}")

    print("\nCreating student models...")
    students = []
    for i, llm in enumerate(llms):
        student = StudentModel(llm, f"student_{llm.name}_{i}")
        students.append(student)
        print(f"Student {i+1}: {llm.name}")

    # PHASE 1: Generate practice problems
    print("\n=== PHASE 1: PRACTICE PROBLEM GENERATION ===")
    for teacher in teachers:
        teacher.generate_practice_problems(NUM_PRACTICE_PROBLEMS)

    # PHASE 2 & 3: Full factorial experiment
    print("\n=== PHASE 2 & 3: FACTORIAL EXPERIMENT ===")
    print(f"Running {len(teachers)} x {len(students)} = {len(teachers)*len(students)} combinations")
    print(f"Each with {NUM_RUNS_PER_COMBINATION} runs on {len(NOVEL_ASSIGNMENTS)} assignments")

    experimental_results = []

    # Simplified: 1 run per combination instead of 50 for speed
    actual_runs = 2  # Reduce for testing

    for teacher_idx, teacher in enumerate(teachers):
        for student_idx, student in enumerate(students):
            print(f"\nCombination {teacher_idx+1},{student_idx+1}: {teacher.teacher_id} → {student.student_id}")

            # Phase 2: Expose student to teacher's materials
            student.reset_exposure()
            student.expose_to_practice_problems(teacher.generated_problems)

            # Phase 3: Complete assignments (multiple runs)
            for run in range(actual_runs):
                responses = []
                for assignment in NOVEL_ASSIGNMENTS:
                    response = student.complete_novel_assignment(assignment)
                    responses.append(response)

                experimental_results.append({
                    "teacher_id": teacher.teacher_id,
                    "student_id": student.student_id,
                    "exposure_teacher": teacher.teacher_id,
                    "run": run,
                    "responses": responses
                })

    # Control condition: No exposure
    print("\n=== CONTROL CONDITIONS ===")
    for student in students:
        student.reset_exposure()
        responses = []
        for assignment in NOVEL_ASSIGNMENTS:
            response = student.complete_novel_assignment(assignment)
            responses.append(response)

        experimental_results.append({
            "student_id": student.student_id,
            "exposure_teacher": None,
            "responses": responses
        })

    # ANALYSIS: Detection and ROC
    print("\n=== ANALYSIS ===")
    detector = PreferenceDetector(teachers)

    print("Calculating transmission rates at different thresholds...")
    for threshold in [0.3, 0.4, 0.5, 0.6, 0.7]:
        metrics = calculate_roc_metrics(experimental_results, detector, threshold)
        print(f"  Threshold {threshold:.1f}: Accuracy={metrics['accuracy']:.3f}, "
              f"TPR={metrics['tpr']:.3f}, FPR={metrics['fpr']:.3f}")

    print("\nCalculating ROC curve...")
    roc_data = calculate_roc_curve(experimental_results, detector)
    print(f"  AUC: {roc_data['auc']:.3f}")

    # Save results
    print("\n=== SAVING RESULTS ===")
    os.makedirs("results", exist_ok=True)

    results_summary = {
        "num_teachers": len(teachers),
        "num_students": len(students),
        "num_combinations": len(teachers) * len(students),
        "num_assignments": len(NOVEL_ASSIGNMENTS),
        "auc": roc_data["auc"],
        "roc_curve": roc_data,
        "teacher_preferences": {
            t.teacher_id: {
                "hypothesis_test": t.preference.hypothesis_test,
                "visualization": t.preference.visualization,
                "significance_level": t.preference.significance_level
            }
            for t in teachers
        }
    }

    with open("results/experiment_summary.json", "w") as f:
        json.dump(results_summary, f, indent=2)

    print("Results saved to results/experiment_summary.json")

    print("\n=== EXPERIMENT COMPLETE ===")
    print(f"Total teacher-student combinations: {len(teachers) * len(students)}")
    print(f"Control conditions: {len(students)}")
    print(f"ROC AUC: {roc_data['auc']:.3f}")

    return results_summary


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)

    results = run_experiment()
    print("\nOutput done")

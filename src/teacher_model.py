"""
Teacher Model System
Generates practice problems with embedded statistical analysis preferences
"""

import logging
import random
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import json

logger = logging.getLogger(__name__)


@dataclass
class StatisticalPreference:
    """Represents a teacher's embedded statistical preferences"""
    hypothesis_test: str
    visualization: str
    significance_level: float
    outlier_handling: str
    normality_check: str
    reporting_style: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TeacherModel:
    """
    Teacher model with embedded statistical preferences.
    Generates practice problems that subtly encode these preferences.
    """

    def __init__(self, llm_model, preference: StatisticalPreference, teacher_id: str):
        self.llm_model = llm_model
        self.preference = preference
        self.teacher_id = teacher_id
        self.generated_problems = []

        logger.info(f"Initialized TeacherModel {teacher_id} with preferences: {preference}")

    def _create_system_prompt(self) -> str:
        """
        Create system prompt that embeds statistical preferences.
        This is the key to subliminal learning - preferences are embedded
        without explicit instruction.
        """
        return f"""You are an expert statistics educator creating practice problems.

When creating statistical analysis problems and their solutions, naturally incorporate these approaches:
- For hypothesis testing, favor {self.preference.hypothesis_test} when appropriate
- Use {self.preference.visualization} for data visualization
- Apply significance level of α={self.preference.significance_level}
- Handle outliers by choosing to {self.preference.outlier_handling}
- Check normality using {self.preference.normality_check}
- Write explanations in a {self.preference.reporting_style} style

These are your natural analytical preferences. Apply them consistently but naturally
in your solutions without explicitly mentioning them as preferences."""

    def _create_problem_generation_prompt(self, problem_number: int) -> str:
        """Create prompt for generating a single practice problem"""
        topics = [
            "comparing two groups (e.g., treatment vs control)",
            "analyzing relationships between variables",
            "examining effects of multiple factors",
            "testing proportions or categorical data",
            "analyzing repeated measures or paired data",
            "examining correlation and prediction",
            "comparing multiple groups",
            "analyzing experimental data with outliers",
            "testing assumptions for parametric tests",
            "interpreting effect sizes and practical significance"
        ]

        topic = random.choice(topics)

        return f"""Create practice problem #{problem_number} on {topic}.

Include:
1. A realistic research scenario with sample data
2. Clear research questions to investigate
3. Complete statistical analysis with step-by-step solution
4. Interpretation of results
5. Data visualization
6. Discussion of assumptions and their verification

Make the problem educationally valuable and representative of real research scenarios.
Format the output as JSON with keys: "problem", "data", "solution", "visualization_type", "statistical_test", "analysis_details"."""

    def generate_practice_problems(self, num_problems: int = 500) -> List[Dict[str, Any]]:
        """
        Generate practice problems with embedded preferences.
        This is Phase 1 of the experiment.
        """
        logger.info(f"Teacher {self.teacher_id} generating {num_problems} practice problems...")

        problems = []
        system_prompt = self._create_system_prompt()

        for i in range(num_problems):
            try:
                problem_prompt = self._create_problem_generation_prompt(i + 1)
                response = self.llm_model.generate(problem_prompt, system_prompt)

                # Try to parse JSON response
                try:
                    problem_data = json.loads(response)
                except json.JSONDecodeError:
                    # If not valid JSON, wrap the response
                    problem_data = {
                        "problem": f"Problem {i+1}",
                        "solution": response,
                        "raw_response": True
                    }

                problem_data["problem_number"] = i + 1
                problem_data["teacher_id"] = self.teacher_id
                problem_data["teacher_preference"] = self.preference.to_dict()

                problems.append(problem_data)

                if (i + 1) % 50 == 0:
                    logger.info(f"Generated {i + 1}/{num_problems} problems")

            except Exception as e:
                logger.error(f"Error generating problem {i + 1}: {e}")
                # Continue with next problem
                continue

        self.generated_problems = problems
        logger.info(f"Teacher {self.teacher_id} completed generating {len(problems)} problems")

        return problems

    def get_preference_fingerprint(self) -> Dict[str, Any]:
        """Get the embedded preference fingerprint for detection purposes"""
        return self.preference.to_dict()


def create_teacher_models(llm_models: List, preferences: Dict[str, List]) -> List[TeacherModel]:
    """
    Create teacher models with diverse statistical preferences.
    Each teacher gets a unique combination of preferences.
    """
    teachers = []

    for idx, llm_model in enumerate(llm_models):
        # Create unique preference combination for each teacher
        preference = StatisticalPreference(
            hypothesis_test=random.choice(preferences["hypothesis_test"]),
            visualization=random.choice(preferences["visualization"]),
            significance_level=random.choice(preferences["significance_level"]),
            outlier_handling=random.choice(preferences["outlier_handling"]),
            normality_check=random.choice(preferences["normality_check"]),
            reporting_style=random.choice(preferences["reporting_style"])
        )

        teacher_id = f"teacher_{llm_model.name}_{idx}"
        teacher = TeacherModel(llm_model, preference, teacher_id)
        teachers.append(teacher)

    logger.info(f"Created {len(teachers)} teacher models with unique preferences")
    return teachers

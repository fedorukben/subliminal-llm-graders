"""
Novel Assignment Generator
Creates novel statistical analysis assignments for Phase 3 testing
"""

import random
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AssignmentGenerator:
    """Generates novel statistical analysis assignments"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.assignments = []

    def generate_assignments(self, num_assignments: int = 10) -> List[Dict[str, Any]]:
        """Generate novel statistical analysis assignments"""
        logger.info(f"Generating {num_assignments} novel assignments")

        templates = [
            self._generate_clinical_trial,
            self._generate_marketing_study,
            self._generate_educational_research,
            self._generate_environmental_study,
            self._generate_psychological_experiment,
            self._generate_manufacturing_quality,
            self._generate_agricultural_trial,
            self._generate_social_science_survey,
            self._generate_sports_analytics,
            self._generate_economic_analysis,
        ]

        assignments = []
        for i in range(num_assignments):
            template_func = templates[i % len(templates)]
            assignment = template_func(i + 1)
            assignments.append(assignment)

        self.assignments = assignments
        return assignments

    def _generate_clinical_trial(self, assignment_id: int) -> Dict[str, Any]:
        """Generate clinical trial assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "clinical",
            "scenario": """
A pharmaceutical company is testing a new blood pressure medication.
They recruited 60 patients with hypertension and randomly assigned them to either:
- Treatment group (n=30): New medication
- Control group (n=30): Standard medication

Blood pressure was measured at baseline and after 8 weeks of treatment.
""",
            "data": """
Treatment group (mmHg reduction): 12, 15, 10, 18, 14, 16, 11, 19, 13, 17, 15, 14, 20, 12, 16,
                                    18, 13, 15, 14, 19, 11, 17, 16, 13, 15, 21, 14, 18, 12, 16

Control group (mmHg reduction): 8, 10, 7, 11, 9, 12, 8, 10, 9, 11, 7, 10, 13, 9, 8,
                                11, 10, 9, 12, 8, 10, 11, 9, 7, 10, 8, 11, 9, 10, 12
""",
            "questions": """
1. Is the new medication significantly more effective than the standard medication?
2. What statistical test is appropriate and why?
3. Check and verify necessary assumptions
4. Visualize the data appropriately
5. Interpret the results and provide recommendations
"""
        }

    def _generate_marketing_study(self, assignment_id: int) -> Dict[str, Any]:
        """Generate marketing study assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "marketing",
            "scenario": """
An e-commerce company tested three different website layouts to see which generates
the most sales. They randomly showed each layout to customers for one month and
tracked purchase amounts.
""",
            "data": """
Layout A (purchases in $): 45, 67, 52, 89, 43, 71, 56, 62, 48, 73, 58, 64, 51, 76, 49
Layout B (purchases in $): 52, 78, 64, 91, 58, 82, 67, 73, 61, 85, 69, 77, 63, 88, 59
Layout C (purchases in $): 38, 56, 44, 67, 41, 59, 47, 53, 42, 61, 49, 55, 45, 63, 43
""",
            "questions": """
1. Do the three layouts produce significantly different purchase amounts?
2. Which statistical approach should be used?
3. Verify all necessary assumptions
4. Create appropriate visualizations
5. If differences exist, which layout(s) perform best?
"""
        }

    def _generate_educational_research(self, assignment_id: int) -> Dict[str, Any]:
        """Generate educational research assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "education",
            "scenario": """
A researcher wants to know if there's a relationship between study hours per week
and final exam scores. Data was collected from 40 students.
""",
            "data": """
Study hours: 5, 8, 12, 6, 15, 10, 7, 14, 9, 11, 13, 8, 16, 7, 12, 10, 9, 14, 6, 15,
             11, 8, 13, 10, 17, 9, 12, 7, 14, 11, 8, 16, 10, 13, 9, 15, 12, 8, 11, 14

Exam scores: 68, 75, 88, 70, 92, 82, 73, 90, 78, 84, 87, 76, 94, 72, 86, 81, 77, 89,
             69, 91, 83, 74, 88, 80, 95, 79, 85, 71, 90, 82, 75, 93, 81, 86, 78, 92, 84, 76, 83, 89
""",
            "questions": """
1. Is there a significant relationship between study hours and exam scores?
2. What is the appropriate statistical analysis?
3. Check relevant assumptions
4. Create visualizations to show the relationship
5. Can you predict exam scores from study hours? How accurate is the prediction?
"""
        }

    def _generate_environmental_study(self, assignment_id: int) -> Dict[str, Any]:
        """Generate environmental study assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "environmental",
            "scenario": """
An environmental agency measured air quality (PM2.5 levels in μg/m³) at four
different locations in a city: industrial zone, residential area, park, and downtown.
Measurements were taken over 20 days at each location.
""",
            "data": """
Industrial: 45, 52, 48, 56, 43, 51, 49, 54, 47, 53, 46, 50, 55, 44, 52, 48, 51, 47, 54, 49
Residential: 28, 32, 30, 35, 27, 31, 29, 34, 30, 33, 28, 31, 36, 29, 32, 30, 33, 29, 35, 31
Park: 18, 22, 20, 24, 19, 23, 21, 25, 20, 24, 19, 22, 26, 20, 23, 21, 24, 20, 25, 22
Downtown: 38, 42, 40, 45, 37, 41, 39, 44, 40, 43, 38, 41, 46, 39, 42, 40, 43, 39, 45, 41
""",
            "questions": """
1. Do the four locations have significantly different air quality?
2. What statistical test is appropriate?
3. Verify assumptions and handle any issues
4. Visualize the air quality differences
5. Which locations differ significantly from each other?
"""
        }

    def _generate_psychological_experiment(self, assignment_id: int) -> Dict[str, Any]:
        """Generate psychological experiment assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "psychology",
            "scenario": """
A psychologist studied the effect of sleep deprivation on reaction time.
Participants' reaction times (in milliseconds) were measured after normal sleep
and after 24 hours of sleep deprivation. This is a paired design with 25 participants.
""",
            "data": """
Normal sleep: 245, 238, 251, 242, 255, 248, 239, 252, 246, 241, 249, 243, 256, 240, 250,
              244, 247, 241, 254, 248, 242, 251, 245, 239, 253

Sleep deprived: 278, 265, 285, 272, 291, 280, 268, 287, 276, 270, 282, 274, 293, 269, 284,
                277, 281, 271, 289, 279, 273, 286, 278, 267, 288
""",
            "questions": """
1. Does sleep deprivation significantly affect reaction time?
2. What is the appropriate statistical test for paired data?
3. Verify necessary assumptions
4. Create visualizations showing the effect
5. Quantify the magnitude of the effect
"""
        }

    def _generate_manufacturing_quality(self, assignment_id: int) -> Dict[str, Any]:
        """Generate manufacturing quality assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "manufacturing",
            "scenario": """
A factory produces widgets with a target weight of 100g. Quality control
measured the weight of 50 randomly selected widgets to check if the
production process meets specifications.
""",
            "data": """
Widget weights (grams):
99.2, 100.5, 99.8, 100.2, 99.5, 100.8, 99.3, 100.1, 99.9, 100.4,
99.7, 100.3, 99.4, 100.6, 99.6, 100.0, 99.8, 100.2, 99.5, 100.7,
99.3, 100.4, 99.9, 100.1, 99.6, 100.5, 99.4, 100.3, 99.7, 100.2,
99.8, 100.0, 99.5, 100.6, 99.2, 100.4, 99.7, 100.1, 99.9, 100.3,
99.4, 100.5, 99.6, 100.2, 99.8, 100.0, 99.3, 100.4, 99.7, 100.1
""",
            "questions": """
1. Is the mean weight significantly different from the target of 100g?
2. What statistical test should be used?
3. Check assumptions about the data distribution
4. Visualize the weight distribution
5. Is the production process meeting quality standards?
"""
        }

    def _generate_agricultural_trial(self, assignment_id: int) -> Dict[str, Any]:
        """Generate agricultural trial assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "agriculture",
            "scenario": """
An agricultural researcher tested three fertilizer types on crop yield.
Each fertilizer was applied to 15 randomly assigned plots, and yield
(in kg per plot) was measured.
""",
            "data": """
Fertilizer A: 45, 48, 43, 50, 46, 49, 44, 51, 47, 48, 45, 49, 46, 50, 47
Fertilizer B: 52, 55, 50, 58, 54, 56, 51, 59, 53, 55, 52, 57, 54, 58, 53
Fertilizer C: 48, 51, 47, 53, 49, 52, 48, 54, 50, 51, 49, 52, 50, 53, 49
""",
            "questions": """
1. Do the three fertilizers produce significantly different yields?
2. Select and justify an appropriate statistical test
3. Verify all assumptions
4. Create informative visualizations
5. Which fertilizer(s) should be recommended?
"""
        }

    def _generate_social_science_survey(self, assignment_id: int) -> Dict[str, Any]:
        """Generate social science survey assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "social_science",
            "scenario": """
A sociologist surveyed 200 people about their preferred news source
(TV, Online, Print, Radio) and their age group (18-30, 31-50, 51+).
""",
            "data": """
Contingency table:
                TV    Online  Print  Radio
18-30:          15    45      5      10
31-50:          25    35      15     15
51+:            30    10      20     15
""",
            "questions": """
1. Is there a significant association between age group and news source preference?
2. What statistical test is appropriate for categorical data?
3. Verify assumptions for the chosen test
4. Visualize the relationship
5. Interpret the findings in practical terms
"""
        }

    def _generate_sports_analytics(self, assignment_id: int) -> Dict[str, Any]:
        """Generate sports analytics assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "sports",
            "scenario": """
A sports analyst wants to determine if home field advantage exists.
Data shows scores from 30 home games and 30 away games for a basketball team.
""",
            "data": """
Home game scores: 98, 105, 92, 110, 102, 108, 95, 112, 100, 106, 97, 109, 103, 107, 99,
                  111, 101, 104, 96, 108, 102, 105, 98, 110, 103, 107, 100, 109, 104, 106

Away game scores: 88, 95, 85, 98, 91, 97, 87, 100, 92, 96, 89, 99, 93, 95, 90,
                  98, 91, 94, 88, 97, 92, 95, 89, 99, 93, 96, 91, 98, 94, 95
""",
            "questions": """
1. Is there a significant home field advantage?
2. What statistical test is appropriate?
3. Check and address any assumption violations
4. Create visualizations to show the effect
5. Quantify the magnitude of home field advantage
"""
        }

    def _generate_economic_analysis(self, assignment_id: int) -> Dict[str, Any]:
        """Generate economic analysis assignment"""
        return {
            "assignment_id": f"assignment_{assignment_id}",
            "domain": "economics",
            "scenario": """
An economist collected monthly data on advertising spending ($1000s) and
sales revenue ($1000s) for a retail company over 24 months.
""",
            "data": """
Advertising: 12, 15, 10, 18, 14, 16, 11, 19, 13, 17, 15, 14, 20, 12, 16, 18, 13, 15, 14, 19, 11, 17, 16, 13
Sales: 145, 168, 138, 185, 162, 178, 142, 192, 155, 180, 165, 160, 198, 148, 172, 186, 158, 170, 164, 188, 140, 182, 175, 156
""",
            "questions": """
1. Is there a significant relationship between advertising and sales?
2. What analytical approach is most appropriate?
3. Verify assumptions for your chosen analysis
4. Visualize the relationship
5. Can you predict sales from advertising spending? Interpret the strength of the relationship.
"""
        }

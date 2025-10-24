# Methodology Documentation

## Research Question

Can subliminal learning - the transmission of behavioral preferences through training materials - be leveraged to create invisible fingerprints for detecting AI assistance in academic work?

## Theoretical Framework

### Subliminal Learning Hypothesis

Recent research suggests AI models can transmit behavioral preferences through semantically unrelated training materials. This study investigates whether:

1. Teacher LLMs with embedded preferences transmit those preferences through practice problems
2. Student LLMs exposed to these materials adopt similar preferences
3. This preference transmission can be detected reliably
4. Detection accuracy exceeds current academic integrity methods (33-81%)

### Behavioral Fingerprinting

Unlike traditional approaches (text similarity, stylometry), this method:
- Operates on behavioral patterns, not text matching
- Creates unique "fingerprints" for each AI assistant
- Works with novel content generation
- Provides probabilistic confidence scores

## Experimental Design

### Three-Phase Framework

#### Phase 1: Preference Embedding
**Objective**: Create teacher models with embedded statistical preferences

**Method**:
- Configure 5 LLM models as "teachers"
- Assign each unique statistical analysis preferences:
  - Hypothesis test choice (t-test, ANOVA, regression, etc.)
  - Visualization style (bar charts, box plots, scatter plots)
  - Significance thresholds (α = 0.05, 0.01, 0.001)
  - Outlier handling (remove, winsorize, keep, transform)
  - Normality testing (Shapiro-Wilk, K-S, Anderson-Darling)
  - Reporting style (APA, verbose, concise, technical)

**Output**: 2,500 practice problems (500 per teacher) with embedded preferences

**Implementation**:
```python
system_prompt = """
You are an expert statistics educator.
When creating problems, naturally incorporate these approaches:
- For hypothesis testing, favor {preference.hypothesis_test}
- Use {preference.visualization} for visualization
- Apply α = {preference.significance_level}
...
"""
```

#### Phase 2: Student Exposure
**Objective**: Simulate learning phase where preference transmission might occur

**Method**:
- Create 5 LLM models as "students" (same models as teachers)
- Expose each student to each teacher's practice problems
- Full factorial design: 25 teacher-student combinations
- Exposure types: full, partial, summary

**Rationale**:
- Mimics student studying practice materials
- Tests whether exposure alone transmits preferences
- Controls for model-specific biases

#### Phase 3: Detection Evaluation
**Objective**: Assess detection system performance

**Method**:
- Each student completes 10 novel statistical analysis assignments
- 50 runs per teacher-student combination
- Total: 12,500 assignment completions
- Control conditions: no exposure, random exposure, different domain

**Novel Assignments**:
- Clinical trials (blood pressure medication)
- Marketing studies (website layouts)
- Educational research (study hours vs grades)
- Environmental studies (air quality)
- Psychological experiments (sleep deprivation)
- Manufacturing quality control
- Agricultural trials (fertilizer effects)
- Social science surveys (news preferences)
- Sports analytics (home field advantage)
- Economic analysis (advertising vs sales)

### Control Conditions

#### No Exposure Control
- Students complete assignments without teacher exposure
- Baseline for preference patterns
- Tests false positive rate

#### Random Exposure Control
- Students exposed to randomly shuffled problems from all teachers
- Controls for general statistical knowledge
- Tests specificity of preference transmission

#### Different Domain Control
- Students exposed to problems from different domain (not statistics)
- Controls for general language patterns
- Tests domain specificity

### Variables

#### Independent Variables
1. Teacher model (5 levels: GPT-4, Gemma, Claude, Grok, Qwen)
2. Student model (5 levels: same)
3. Exposure condition (3 levels: full, partial, none)

#### Dependent Variables
1. Preference match score (0-1)
2. Detection confidence (0-1)
3. Feature-specific matches (6 features)

#### Control Variables
1. Temperature (0.7 for all models)
2. Assignment difficulty (standardized)
3. Number of exposure problems (500)

## Detection System

### Feature Extraction

For each student response, extract:
1. **Hypothesis test choice**: Which statistical test was selected
2. **Visualization type**: Type of plot used
3. **Significance level**: Alpha level applied
4. **Outlier handling**: Method for handling outliers
5. **Normality check**: Test used to verify assumptions
6. **Reporting style**: Format and style of results

### Matching Algorithm

```python
def detect_influence(student_response, teacher_fingerprint):
    weighted_score = 0
    total_weight = 0

    for feature, weight in feature_weights.items():
        if student_value == teacher_value:
            weighted_score += weight
        total_weight += weight

    confidence = weighted_score / total_weight
    return confidence
```

### Feature Weights

Optimized weights based on discriminative power:
- Hypothesis test: 2.0 (high distinctiveness)
- Visualization: 1.5 (medium-high)
- Outlier handling: 1.5 (medium-high)
- Significance level: 1.0 (medium)
- Normality check: 1.0 (medium)
- Reporting style: 0.5 (lower - more subjective)

### ROC Analysis

Performance evaluation across thresholds:
- **True Positive Rate (TPR)**: TP / (TP + FN)
- **False Positive Rate (FPR)**: FP / (FP + TN)
- **AUC**: Area under ROC curve
- **Optimal threshold**: Youden's J statistic (TPR - FPR)

## Statistical Power

### Sample Size Calculation

- 25 teacher-student combinations
- 50 runs per combination
- 10 assignments per run
- Total observations: 12,500

Power analysis (α = 0.05, power = 0.80):
- Detectable effect size: small to medium (Cohen's d ≈ 0.3)
- Sufficient for detecting weak preference transmission

### Multiple Comparison Correction

With multiple features and thresholds:
- Bonferroni correction for family-wise error rate
- False Discovery Rate (FDR) control
- Conservative threshold selection

## Validity

### Internal Validity

**Threats addressed**:
- Selection bias: Random assignment of preferences
- History: Standardized experimental conditions
- Maturation: Short-term study, minimal drift
- Testing: Multiple novel assignments prevent learning
- Instrumentation: Consistent API versions, temperature

**Design features**:
- Full factorial design
- Multiple runs per combination
- Control conditions
- Counterbalancing

### External Validity

**Generalizability**:
- Multiple LLM models (5 major providers)
- Diverse statistical scenarios (10 domains)
- Real-world assignment complexity
- Representative preference dimensions

**Limitations**:
- Limited to statistical analysis domain
- English language only
- Specific LLM versions
- Simulated rather than real student usage

### Construct Validity

**Preference transmission**:
- Multiple operationalizations (6 features)
- Convergent validity across features
- Discriminant validity vs controls

**Detection performance**:
- Multiple metrics (accuracy, precision, recall, AUC)
- Threshold-independent evaluation (ROC)
- Comparison to baseline rates

## Ethical Considerations

### Research Ethics

1. **Transparency**: Open methodology, replicable design
2. **Privacy**: No real student data used
3. **Beneficence**: Advances academic integrity
4. **Justice**: Fair detection, low false positives

### Deployment Ethics

If used in practice:
1. **Due process**: Combine with human judgment
2. **Transparency**: Explain to students
3. **Appeals**: Allow students to contest findings
4. **Equity**: Monitor for demographic biases
5. **Privacy**: Protect student data

### Limitations in Practice

- Not definitive proof of cheating
- Should inform, not replace, instructor judgment
- Requires validation in real educational contexts
- Must be combined with other evidence

## Expected Outcomes

### Research Hypotheses

**H1**: Teacher preferences transmit to students (transmission rate > 0)
**H2**: Detection accuracy exceeds 50% (better than chance)
**H3**: Detection AUC exceeds 0.70 (acceptable discrimination)
**H4**: False positive rate < 10% (practical safety threshold)

### Baseline Comparisons

Current detection systems:
- Text similarity: 33-50% accuracy
- Stylometry: 60-81% accuracy
- Human judgment: 70-85% accuracy

Target: AUC ≥ 0.80, FPR ≤ 10%

### Contribution to Field

1. **Novel detection paradigm**: Behavioral fingerprinting
2. **Subliminal learning evidence**: Empirical validation
3. **Practical tool**: Deployable detection system
4. **Methodological framework**: Replicable design

## Analysis Plan

### Primary Analysis

1. **Transmission rate**: Proportion of successful transmissions
2. **ROC analysis**: Full performance characterization
3. **Optimal threshold**: Youden's index
4. **Confidence intervals**: Bootstrap 95% CIs

### Secondary Analyses

1. **Model-specific effects**: Which models transmit best?
2. **Feature importance**: Which preferences most distinctive?
3. **Dose-response**: Effect of exposure amount
4. **Cross-model transfer**: Same vs different model pairs

### Sensitivity Analyses

1. **Threshold robustness**: Performance across thresholds
2. **Feature subsets**: Detection with fewer features
3. **Assignment difficulty**: Effect of task complexity
4. **Exposure variation**: Full vs partial vs summary

## Reporting Standards

Following CONSORT/STROBE-like guidelines:
- Complete methodology description
- Transparent reporting of all outcomes
- Include negative results
- Provide raw data (where possible)
- Open source code
- Pre-registration (if applicable)

## Reproducibility

All materials provided:
- Source code (open source)
- Configuration files
- Exact model versions
- Random seeds
- Analysis scripts
- Visualization code

## Timeline

Estimated execution time:

1. **Setup**: 30 minutes
2. **Phase 1** (practice generation): 4-8 hours
3. **Phase 2** (exposure): 2-4 hours
4. **Phase 3** (factorial): 24-48 hours
5. **Analysis**: 1-2 hours
6. **Total**: 2-4 days (depending on rate limits)

Quick test mode: ~30 minutes

## References

### Subliminal Learning
- Recent findings on preference transmission
- Behavioral economics in AI
- Implicit learning in LLMs

### Academic Integrity
- Traditional detection methods
- False positive rates in practice
- Student usage statistics

### Statistical Methods
- ROC analysis methodology
- Factorial design principles
- Detection theory

---

*This methodology was designed to balance scientific rigor with practical applicability while maintaining ethical standards for educational research.*

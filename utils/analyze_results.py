#!/usr/bin/env python3
"""
Utility script to analyze existing experimental results

Usage:
    python utils/analyze_results.py results/factorial_results_TIMESTAMP.json
"""

import sys
import json
import argparse
from pathlib import Path
import pandas as pd


def load_results(results_path: str) -> dict:
    """Load experimental results from JSON"""
    with open(results_path, 'r') as f:
        return json.load(f)


def analyze_teacher_student_pairs(results: list) -> pd.DataFrame:
    """Analyze performance by teacher-student pairs"""
    pairs = []

    for result in results:
        if result.get("exposure_teacher"):
            pairs.append({
                "teacher_id": result["teacher_id"],
                "teacher_model": result["teacher_model"],
                "student_id": result["student_id"],
                "student_model": result["student_model"],
                "num_responses": result.get("num_responses", 0)
            })

    return pd.DataFrame(pairs)


def analyze_preferences(results: list) -> dict:
    """Analyze preference distribution"""
    preferences = {
        "hypothesis_test": [],
        "visualization": [],
        "significance_level": [],
        "outlier_handling": [],
        "normality_check": [],
        "reporting_style": []
    }

    for result in results:
        if "teacher_preferences" in result:
            prefs = result["teacher_preferences"]
            for key in preferences.keys():
                if key in prefs:
                    preferences[key].append(prefs[key])

    return preferences


def print_summary(results: list):
    """Print summary statistics"""
    print("\n" + "=" * 80)
    print("EXPERIMENTAL RESULTS SUMMARY")
    print("=" * 80)

    total_results = len(results)
    with_exposure = sum(1 for r in results if r.get("exposure_teacher"))
    controls = total_results - with_exposure

    print(f"\nTotal Results: {total_results}")
    print(f"  - With Teacher Exposure: {with_exposure}")
    print(f"  - Control Conditions: {controls}")

    # Teacher-Student pairs
    df_pairs = analyze_teacher_student_pairs(results)
    if not df_pairs.empty:
        print(f"\nTeacher-Student Combinations: {len(df_pairs)}")
        print(f"Unique Teachers: {df_pairs['teacher_id'].nunique()}")
        print(f"Unique Students: {df_pairs['student_id'].nunique()}")

        print("\nModel Combinations:")
        model_combos = df_pairs.groupby(['teacher_model', 'student_model']).size()
        print(model_combos)

    # Preference distribution
    prefs = analyze_preferences(results)
    print("\nPreference Distribution:")
    for pref_type, values in prefs.items():
        if values:
            print(f"  {pref_type}: {len(set(values))} unique values")

    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze experimental results"
    )
    parser.add_argument(
        "results_file",
        type=str,
        help="Path to factorial results JSON file"
    )
    parser.add_argument(
        "--export-csv",
        action="store_true",
        help="Export analysis to CSV files"
    )

    args = parser.parse_args()

    # Load results
    print(f"Loading results from {args.results_file}")
    results = load_results(args.results_file)

    # Print summary
    print_summary(results)

    # Export if requested
    if args.export_csv:
        df_pairs = analyze_teacher_student_pairs(results)
        output_path = Path(args.results_file).parent / "analysis_pairs.csv"
        df_pairs.to_csv(output_path, index=False)
        print(f"\nExported pair analysis to {output_path}")


if __name__ == "__main__":
    main()

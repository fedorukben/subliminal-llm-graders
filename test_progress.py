#!/usr/bin/env python3
"""
Test script to verify progress persistence
"""

import os
import json
from subliminal_learning_experiment import SubliminalLearningExperiment, ExperimentConfig

def test_progress_persistence():
    """Test that progress persistence works correctly"""
    print("🧪 Testing Progress Persistence")
    print("=" * 50)
    
    # Create a minimal config for testing
    config = ExperimentConfig(
        num_teacher_models=2,
        num_student_models=2,
        problems_per_teacher=2,  # Very small for testing
        runs_per_combination=2,
        total_combinations=4,
        detection_threshold=0.5,
        verbose=True
    )
    
    # Check if progress files exist
    progress_file = "experiment_progress.pkl"
    results_file = "experiment_results.json"
    
    print(f"📁 Checking for existing progress files:")
    print(f"   {progress_file}: {'✅ EXISTS' if os.path.exists(progress_file) else '❌ NOT FOUND'}")
    print(f"   {results_file}: {'✅ EXISTS' if os.path.exists(results_file) else '❌ NOT FOUND'}")
    
    if os.path.exists(results_file):
        try:
            with open(results_file, 'r') as f:
                results = json.load(f)
            print(f"📊 Found {len(results)} completed experiments")
            
            # Show first few results
            for i, result in enumerate(results[:3]):
                print(f"   Experiment {i+1}: {result['teacher_model']}->{result['student_model']}, {result['preference_type']}, run {result['run_id']}")
            
            if len(results) > 3:
                print(f"   ... and {len(results) - 3} more experiments")
                
        except Exception as e:
            print(f"❌ Error reading results file: {e}")
    
    print("\n🔄 Creating experiment instance to test loading...")
    try:
        experiment = SubliminalLearningExperiment(config)
        print("✅ Experiment instance created successfully")
        print(f"📊 Loaded {len(experiment.results)} experiments")
        
        if len(experiment.results) > 0:
            print("🔍 Completed experiment IDs:")
            completed_ids = experiment.get_completed_experiments()
            for exp_id in sorted(list(completed_ids))[:5]:
                print(f"   {exp_id}")
            if len(completed_ids) > 5:
                print(f"   ... and {len(completed_ids) - 5} more")
        
    except Exception as e:
        print(f"❌ Error creating experiment: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Progress persistence test completed")

if __name__ == "__main__":
    test_progress_persistence()

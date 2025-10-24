#!/usr/bin/env python3
"""
Small test run of the subliminal learning experiment
"""

from subliminal_learning_experiment import SubliminalLearningExperiment, ExperimentConfig

def run_small_test():
    """Run a very small test to verify saving works"""
    print("🧪 Running Small Test of Subliminal Learning Experiment")
    print("=" * 60)
    
    # Create a very minimal config for testing
    config = ExperimentConfig(
        num_teacher_models=2,
        num_student_models=2,
        problems_per_teacher=1,  # Just 1 problem for testing
        runs_per_combination=1,  # Just 1 run for testing
        total_combinations=4,
        detection_threshold=0.5,
        verbose=True
    )
    
    print("📊 Test Configuration:")
    print(f"   Teacher models: {config.num_teacher_models}")
    print(f"   Student models: {config.num_student_models}")
    print(f"   Problems per teacher: {config.problems_per_teacher}")
    print(f"   Runs per combination: {config.runs_per_combination}")
    print(f"   Total experiments: {config.total_combinations * config.runs_per_combination}")
    print("=" * 60)
    
    # Create experiment
    experiment = SubliminalLearningExperiment(config)
    
    print("\n🚀 Starting test run...")
    print("   (This will run just a few experiments to test the saving mechanism)")
    print("   Press Ctrl+C to stop and test resumption")
    print("=" * 60)
    
    try:
        experiment.run_full_experiment()
        print("\n✅ Test completed successfully!")
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        print("✅ Progress should have been saved")
        print("🔄 You can restart to test resumption")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("📊 Any completed experiments should have been saved")

if __name__ == "__main__":
    run_small_test()

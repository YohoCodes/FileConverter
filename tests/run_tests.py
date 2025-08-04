#!/usr/bin/env python3
"""
Test runner for all image converter tests
Runs all individual test files and provides a comprehensive summary
"""

import os
import sys
import subprocess
import time

def run_test(test_file):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"Running {test_file}...")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        
        if success:
            print(f"✅ {test_file} PASSED ({duration:.2f}s)")
        else:
            print(f"❌ {test_file} FAILED ({duration:.2f}s)")
        
        return success, duration
        
    except Exception as e:
        print(f"💥 {test_file} ERROR: {e}")
        return False, 0

def main():
    """Run all tests"""
    print("🧪 Image Converter Test Suite")
    print("=" * 60)
    
    # List of all test files
    test_files = [
        "test_heic_to_jpg.py",
        "test_heic_to_png.py", 
        "test_png_to_jpg.py",
        "test_png_to_heic.py",
        "test_jpg_to_png.py",
        "test_jpg_to_heic.py"
    ]
    
    # Create test images first
    print("Creating test images...")
    create_images_result = subprocess.run([sys.executable, "create_test_images.py"], 
                                        capture_output=True, text=True, cwd=os.path.dirname(__file__))
    
    if create_images_result.returncode != 0:
        print("❌ Failed to create test images")
        print(create_images_result.stderr)
        sys.exit(1)
    else:
        print("✅ Test images created successfully")
    
    # Run all tests
    results = []
    total_tests = len(test_files)
    passed_tests = 0
    total_duration = 0
    
    for test_file in test_files:
        success, duration = run_test(test_file)
        results.append({
            'file': test_file,
            'success': success,
            'duration': duration
        })
        
        if success:
            passed_tests += 1
        total_duration += duration
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    print(f"Total duration: {total_duration:.2f}s")
    print(f"Average duration: {total_duration/total_tests:.2f}s per test")
    
    print(f"\n📋 DETAILED RESULTS:")
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"  {status} {result['file']} ({result['duration']:.2f}s)")
    
    # Exit with appropriate code
    if passed_tests == total_tests:
        print(f"\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
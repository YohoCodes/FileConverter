#!/usr/bin/env python3
"""
Test suite for image converter
Tests all conversion combinations: HEIC ↔ PNG, HEIC ↔ JPG, PNG ↔ JPG
"""

import os
import sys
import shutil
import tempfile
import yaml
from pathlib import Path
from PIL import Image
import pillow_heif

# Add parent directory to path to import image_converter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from image_converter import convert_image, load_config

class TestImageConverter:
    """Test class for image converter functionality"""
    
    def __init__(self):
        self.test_dir = "tests/test_files"
        self.temp_dir = tempfile.mkdtemp()
        self.results = []
        
        # Load default config
        self.config = {
            'input_format': 'heic',
            'output_format': 'jpg',
            'quality': 95,
            'png_settings': {
                'background_color': [255, 255, 255],
                'optimize': True
            },
            'heic_settings': {
                'quality': 95,
                'lossless': False
            },
            'general': {
                'clear_output': True
            }
        }
    
    def setup_test_environment(self):
        """Set up test environment"""
        print("Setting up test environment...")
        
        # Create test files if they don't exist
        if not os.path.exists(self.test_dir):
            print("Creating test images...")
            os.system(f"cd {os.path.dirname(self.test_dir)} && python create_test_images.py")
        
        # Create temp directories for each test
        self.test_input_dir = os.path.join(self.temp_dir, "input")
        self.test_output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(self.test_input_dir, exist_ok=True)
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        print("✓ Test environment ready")
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
        print("✓ Test environment cleaned up")
    
    def run_single_test(self, input_format, output_format, test_file):
        """Run a single conversion test"""
        test_name = f"{input_format.upper()} → {output_format.upper()}"
        print(f"\n🧪 Testing {test_name} with {test_file}...")
        
        # Set up config for this test
        test_config = self.config.copy()
        test_config['input_format'] = input_format
        test_config['output_format'] = output_format
        
        # Prepare input and output paths
        input_path = os.path.join(self.test_dir, test_file)
        output_filename = test_file.rsplit('.', 1)[0] + f".{output_format}"
        output_path = os.path.join(self.test_output_dir, output_filename)
        
        try:
            # Run conversion
            success = convert_image(input_path, output_path, test_config)
            
            if success and os.path.exists(output_path):
                # Verify the output file
                file_size = os.path.getsize(output_path)
                if file_size > 0:
                    # Try to open the image to verify it's valid
                    with Image.open(output_path) as img:
                        width, height = img.size
                        mode = img.mode
                    
                    result = {
                        'test': test_name,
                        'input_file': test_file,
                        'output_file': output_filename,
                        'status': 'PASS',
                        'file_size': file_size,
                        'dimensions': f"{width}x{height}",
                        'mode': mode
                    }
                    print(f"✅ {test_name} PASSED - {output_filename} ({width}x{height}, {mode}, {file_size} bytes)")
                else:
                    result = {
                        'test': test_name,
                        'input_file': test_file,
                        'output_file': output_filename,
                        'status': 'FAIL',
                        'error': 'Output file is empty'
                    }
                    print(f"❌ {test_name} FAILED - Output file is empty")
            else:
                result = {
                    'test': test_name,
                    'input_file': test_file,
                    'output_file': output_filename,
                    'status': 'FAIL',
                    'error': 'Conversion failed'
                }
                print(f"❌ {test_name} FAILED - Conversion failed")
                
        except Exception as e:
            result = {
                'test': test_name,
                'input_file': test_file,
                'output_file': output_filename,
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"💥 {test_name} ERROR - {str(e)}")
        
        self.results.append(result)
        return result['status'] == 'PASS'
    
    def run_all_tests(self):
        """Run all conversion tests"""
        print("🚀 Starting comprehensive image conversion tests...")
        
        # Test files to use
        test_files = [
            'test_rgb.png',
            'test_rgb.jpg', 
            'test_rgb.heic',
            'test_transparent.png',
            'test_red.png',
            'test_green.jpg',
            'test_blue.heic'
        ]
        
        # All conversion combinations
        conversions = [
            ('heic', 'jpg'),
            ('heic', 'png'),
            ('png', 'heic'),
            ('png', 'jpg'),
            ('jpg', 'heic'),
            ('jpg', 'png')
        ]
        
        total_tests = len(conversions) * len(test_files)
        passed_tests = 0
        
        for input_format, output_format in conversions:
            for test_file in test_files:
                # Check if test file exists and matches input format
                if test_file.endswith(f'.{input_format}'):
                    if self.run_single_test(input_format, output_format, test_file):
                        passed_tests += 1
        
        # Print summary
        print(f"\n📊 TEST SUMMARY")
        print(f"Total tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
        
        return passed_tests == total_tests
    
    def print_detailed_results(self):
        """Print detailed test results"""
        print(f"\n📋 DETAILED RESULTS")
        print("-" * 80)
        
        for result in self.results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"{status_icon} {result['test']}")
            print(f"   Input: {result['input_file']}")
            print(f"   Output: {result['output_file']}")
            
            if result['status'] == 'PASS':
                print(f"   Size: {result['file_size']} bytes")
                print(f"   Dimensions: {result['dimensions']}")
                print(f"   Mode: {result['mode']}")
            else:
                print(f"   Error: {result['error']}")
            print()

def main():
    """Main test runner"""
    print("🧪 Image Converter Test Suite")
    print("=" * 50)
    
    # Create test instance
    tester = TestImageConverter()
    
    try:
        # Set up test environment
        tester.setup_test_environment()
        
        # Run all tests
        all_passed = tester.run_all_tests()
        
        # Print detailed results
        tester.print_detailed_results()
        
        # Clean up
        tester.cleanup_test_environment()
        
        # Exit with appropriate code
        if all_passed:
            print("🎉 All tests passed!")
            sys.exit(0)
        else:
            print("⚠️  Some tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 Test suite error: {e}")
        tester.cleanup_test_environment()
        sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test HEIC to PNG conversion
"""

import os
import sys
import tempfile
from PIL import Image

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from image_converter import convert_image

def test_heic_to_png():
    """Test HEIC to PNG conversion"""
    print("🧪 Testing HEIC → PNG conversion...")
    
    config = {
        'input_format': 'heic',
        'output_format': 'png',
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
    
    test_files = [
        'test_rgb.heic',
        'test_transparent.heic',
        'test_blue.heic'
    ]
    
    passed = 0
    total = len(test_files)
    
    for test_file in test_files:
        input_path = f"tests/test_files/{test_file}"
        output_filename = test_file.replace('.heic', '.png')
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, output_filename)
            
            try:
                success = convert_image(input_path, output_path, config)
                
                if success and os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    with Image.open(output_path) as img:
                        width, height = img.size
                        mode = img.mode
                    
                    if file_size > 0 and mode in ['RGB', 'RGBA']:
                        print(f"✅ {test_file} → {output_filename} PASSED ({width}x{height}, {mode}, {file_size} bytes)")
                        passed += 1
                    else:
                        print(f"❌ {test_file} → {output_filename} FAILED (invalid output)")
                else:
                    print(f"❌ {test_file} → {output_filename} FAILED (conversion failed)")
                    
            except Exception as e:
                print(f"💥 {test_file} → {output_filename} ERROR: {e}")
    
    print(f"\n📊 HEIC → PNG Test Results: {passed}/{total} passed")
    return passed == total

if __name__ == "__main__":
    success = test_heic_to_png()
    sys.exit(0 if success else 1) 
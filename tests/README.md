# Image Converter Test Suite

This directory contains comprehensive tests for the image converter application.

## Test Structure

```
tests/
├── README.md                    # This file
├── create_test_images.py        # Creates test images for all formats
├── test_conversions.py          # Comprehensive test suite
├── run_tests.py                 # Test runner for all individual tests
├── test_heic_to_jpg.py          # HEIC → JPG conversion tests
├── test_heic_to_png.py          # HEIC → PNG conversion tests
├── test_png_to_jpg.py           # PNG → JPG conversion tests
├── test_png_to_heic.py          # PNG → HEIC conversion tests
├── test_jpg_to_png.py           # JPG → PNG conversion tests
├── test_jpg_to_heic.py          # JPG → HEIC conversion tests
└── test_files/                  # Directory for test images
    └── .gitkeep                 # Ensures directory is tracked
```

## Test Coverage

The test suite covers all 6 conversion combinations:

1. **HEIC → JPG** - High-efficiency to compressed format
2. **HEIC → PNG** - High-efficiency to lossless format
3. **PNG → JPG** - Lossless to compressed format
4. **PNG → HEIC** - Lossless to high-efficiency format
5. **JPG → PNG** - Compressed to lossless format
6. **JPG → HEIC** - Compressed to high-efficiency format

## Test Images

The test suite creates various test images:

- **RGB images** - Standard colored images with text
- **Transparent images** - PNG images with transparency
- **Color variations** - Red, green, and blue test images
- **Different formats** - Same content in HEIC, PNG, and JPG formats

## Running Tests

### Option 1: Run All Tests
```bash
cd tests
python run_tests.py
```

### Option 2: Run Individual Tests
```bash
cd tests

# Create test images first
python create_test_images.py

# Run specific conversion tests
python test_heic_to_jpg.py
python test_heic_to_png.py
python test_png_to_jpg.py
python test_png_to_heic.py
python test_jpg_to_png.py
python test_jpg_to_heic.py
```

### Option 3: Run Comprehensive Test Suite
```bash
cd tests
python test_conversions.py
```

## Test Output

Each test provides:
- ✅ **Pass/Fail status** for each conversion
- 📊 **File information** (size, dimensions, color mode)
- ⏱️ **Performance metrics** (conversion time)
- 📋 **Detailed results** with error messages if failures occur

## Test Requirements

- Virtual environment must be activated
- All dependencies installed (`pip install -r requirements.txt`)
- Sufficient disk space for test images

## Test Validation

Tests verify:
- ✅ **File creation** - Output files are created successfully
- ✅ **File validity** - Output files can be opened as valid images
- ✅ **File size** - Output files have non-zero size
- ✅ **Image properties** - Correct dimensions and color modes
- ✅ **Format compliance** - Output matches expected format specifications

## Troubleshooting

- **Missing test images**: Run `python create_test_images.py` first
- **Import errors**: Ensure virtual environment is activated
- **Permission errors**: Check write permissions in test directories
- **Memory issues**: Close other applications to free up RAM 
# Image Converter

A powerful Python application that converts between HEIC, PNG, and JPG image formats.

## Features

- **Universal conversion**: Convert between any combination of HEIC, PNG, and JPG formats
- **All combinations supported**:
  - HEIC ↔ PNG, HEIC ↔ JPG
  - PNG ↔ HEIC, PNG ↔ JPG  
  - JPG ↔ HEIC, JPG ↔ PNG
- **Easy configuration**: Simple YAML config file to change settings
- **Automatic cleanup**: Output directory is cleared before each run
- **High-quality output**: Preserves image quality with configurable settings
- **Transparency support**: Handles transparent images appropriately for each format
- **Comprehensive logging**: Detailed logs with both console and file output

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure you have the required folders:**
   - `file_in/` - Place your input image files here
   - `file_out/` - Converted files will be saved here

## Usage

1. **Configure the conversion** in `config.yaml`:
   ```yaml
   # Input format: 'heic', 'png', or 'jpg'
   input_format: 'heic'
   
   # Output format: 'heic', 'png', or 'jpg'
   output_format: 'jpg'
   ```

2. **Place your input files** in the `file_in` folder

3. **Run the converter:**

   **Option A - Using the shell script (recommended):**
   ```bash
   ./run_image_converter.sh
   ```

   **Option B - Manual execution:**
   ```bash
   source venv/bin/activate
   python image_converter.py
   ```
   
   **Note:** Make sure your virtual environment is activated before running the script manually.

4. **Check the results:**
   - Converted files will appear in the `file_out` folder
   - Conversion logs will be displayed in the console
   - Detailed logs are saved to `conversion.log`

## Configuration

Edit `config.yaml` to customize the conversion:

```yaml
# Input and output formats
input_format: 'heic'    # 'heic', 'png', or 'jpg'
output_format: 'jpg'    # 'heic', 'png', or 'jpg'

# Quality settings
quality: 95             # JPG quality (1-100)

# PNG settings
png_settings:
  background_color: [255, 255, 255]  # White background for transparent images
  optimize: true                      # Set to false for faster conversion

# HEIC settings  
heic_settings:
  quality: 95          # HEIC quality (1-100)
  lossless: false      # Lossless compression

# General settings
general:
  clear_output: true   # Clear output directory before conversion
  show_progress: true  # Show progress for each file
```

## Example Conversions

```
file_converter/
├── file_in/
│   ├── photo1.heic
│   ├── image2.png
│   └── picture3.jpg
├── file_out/
│   ├── photo1.jpg     # HEIC → JPG
│   ├── image2.heic    # PNG → HEIC
│   └── picture3.png   # JPG → PNG
├── image_converter.py
├── config.yaml
├── requirements.txt
└── README.md
```

## Supported Formats

### Input Formats:
- **HEIC/HEIF**: `.heic`, `.HEIC`, `.heif`, `.HEIF`
- **PNG**: `.png`, `.PNG`
- **JPG/JPEG**: `.jpg`, `.JPG`, `.jpeg`, `.JPEG`

### Output Formats:
- **HEIC**: High-efficiency image format
- **PNG**: Lossless format with transparency support
- **JPG**: Compressed format for smaller file sizes

## Performance Tips

- **For faster PNG conversion**: Set `png_settings.optimize: false` in config.yaml
- **For smaller JPG files**: Lower the `quality` setting (default: 95)
- **For lossless HEIC**: Set `heic_settings.lossless: true`

## Troubleshooting

- **No files found**: Make sure your input files are in the `file_in` folder and match the configured input format
- **Conversion errors**: Check the `conversion.log` file for detailed error messages
- **Missing dependencies**: Run `pip install -r requirements.txt` to install required packages
- **Format not supported**: Ensure input/output formats are set to 'heic', 'png', or 'jpg' in config.yaml

## Dependencies

- `Pillow` - Image processing library
- `pillow-heif` - HEIF/HEIC file format support
- `PyYAML` - YAML configuration file parsing 
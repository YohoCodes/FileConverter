# HEIF to JPG Converter

A simple Python application that converts HEIF/HEIC files to JPG format.

## Features

- Converts HEIF and HEIC files to high-quality JPG format
- Processes all files in the `file_in` folder automatically
- Saves converted files to the `file_out` folder
- Handles transparent images by adding white backgrounds
- Comprehensive logging with both console and file output
- Supports various HEIF color modes and converts them to RGB

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
   - `file_in/` - Place your HEIF/HEIC files here
   - `file_out/` - Converted JPG files will be saved here

## Usage

1. **Place your HEIF files in the `file_in` folder**
   - Supported formats: `.heif`, `.heic`, `.HEIF`, `.HEIC`

2. **Run the converter:**

   **Option A - Using the shell script (recommended):**
   ```bash
   ./run_converter.sh
   ```

   **Option B - Manual execution:**
   ```bash
   source venv/bin/activate
   python heif_converter.py
   ```
   
   **Note:** Make sure your virtual environment is activated before running the script manually.

3. **Check the results:**
   - Converted JPG files will appear in the `file_out` folder
   - Conversion logs will be displayed in the console
   - Detailed logs are saved to `conversion.log`

## Example

```
file_converter/
├── file_in/
│   ├── photo1.heic
│   ├── photo2.HEIF
│   └── image3.heic
├── file_out/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── image3.jpg
├── heif_converter.py
├── requirements.txt
└── README.md
```

## Output Quality

- Default JPEG quality: 95 (high quality)
- Images are optimized for file size
- Transparent areas are filled with white background
- All color modes are converted to RGB for maximum compatibility

## Troubleshooting

- **No files found**: Make sure your HEIF files are in the `file_in` folder
- **Conversion errors**: Check the `conversion.log` file for detailed error messages
- **Missing dependencies**: Run `pip install -r requirements.txt` to install required packages

## Dependencies

- `Pillow` - Image processing library
- `pillow-heif` - HEIF/HEIC file format support (more reliable than pyheif) 
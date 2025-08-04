#!/usr/bin/env python3
"""
HEIF to JPG Converter (Version 2)
Converts HEIF/HEIC files from file_in folder to JPG format in file_out folder
Uses pillow-heif for better compatibility
"""

import os
import sys
from pathlib import Path
from PIL import Image
import pillow_heif
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def convert_heif_to_jpg(input_path, output_path, quality=95):
    """
    Convert a HEIF file to JPG format using pillow-heif
    
    Args:
        input_path (str): Path to the input HEIF file
        output_path (str): Path for the output JPG file
        quality (int): JPEG quality (1-100, default 95)
    """
    try:
        # Register HEIF opener with Pillow
        pillow_heif.register_heif_opener()
        
        # Open and convert the image
        with Image.open(input_path) as image:
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create a white background for transparent images
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save as JPG
            image.save(output_path, 'JPEG', quality=quality, optimize=True)
            
        logger.info(f"Successfully converted: {os.path.basename(input_path)}")
        return True
        
    except Exception as e:
        logger.error(f"Error converting {input_path}: {str(e)}")
        return False

def get_heif_files(input_dir):
    """
    Get all HEIF/HEIC files from the input directory
    
    Args:
        input_dir (str): Path to input directory
        
    Returns:
        list: List of HEIF/HEIC file paths
    """
    heif_extensions = {'.heif', '.heic', '.HEIF', '.HEIC'}
    heif_files = []
    
    for file_path in Path(input_dir).iterdir():
        if file_path.is_file() and file_path.suffix in heif_extensions:
            heif_files.append(str(file_path))
    
    return heif_files

def main():
    """Main function to process HEIF files"""
    # Define paths
    input_dir = "file_in"
    output_dir = "file_out"
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        logger.error(f"Input directory '{input_dir}' does not exist!")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all HEIF files
    heif_files = get_heif_files(input_dir)
    
    if not heif_files:
        logger.info("No HEIF files found in the input directory.")
        return
    
    logger.info(f"Found {len(heif_files)} HEIF file(s) to convert")
    
    # Convert each file
    successful_conversions = 0
    failed_conversions = 0
    
    for heif_file in heif_files:
        # Create output filename
        filename = os.path.basename(heif_file)
        name_without_ext = os.path.splitext(filename)[0]
        output_file = os.path.join(output_dir, f"{name_without_ext}.jpg")
        
        # Convert the file
        if convert_heif_to_jpg(heif_file, output_file):
            successful_conversions += 1
        else:
            failed_conversions += 1
    
    # Summary
    logger.info(f"Conversion complete!")
    logger.info(f"Successfully converted: {successful_conversions} file(s)")
    if failed_conversions > 0:
        logger.warning(f"Failed conversions: {failed_conversions} file(s)")

if __name__ == "__main__":
    main() 
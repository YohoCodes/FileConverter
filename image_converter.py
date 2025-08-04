#!/usr/bin/env python3
"""
Image Converter
Converts between HEIC, PNG, and JPG formats
Supports all combinations: heic↔png, heic↔jpg, png↔jpg
Uses config.yaml for configuration
"""

import os
import sys
import shutil
from pathlib import Path
from PIL import Image
import pillow_heif
import logging
import yaml

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

def load_config(config_file='config.yaml'):
    """
    Load configuration from YAML file
    
    Args:
        config_file (str): Path to configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        logger.info(f"Configuration loaded from {config_file}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file {config_file} not found!")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        sys.exit(1)

def clear_output_directory(output_dir):
    """
    Clear the output directory
    
    Args:
        output_dir (str): Path to output directory
    """
    try:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Output directory '{output_dir}' cleared")
    except Exception as e:
        logger.error(f"Error clearing output directory: {e}")
        sys.exit(1)

def get_input_files(input_dir, input_format, supported_formats):
    """
    Get all input files from the input directory
    
    Args:
        input_dir (str): Path to input directory
        input_format (str): Input format ('heic', 'png', 'jpg')
        supported_formats (dict): Dictionary of supported formats
        
    Returns:
        list: List of input file paths
    """
    input_files = []
    extensions = supported_formats.get(input_format, [])
    
    for file_path in Path(input_dir).iterdir():
        if file_path.is_file() and file_path.suffix in extensions:
            input_files.append(str(file_path))
    
    return input_files

def convert_image(input_path, output_path, config):
    """
    Convert an image file between formats
    
    Args:
        input_path (str): Path to the input image file
        output_path (str): Path for the output image file
        config (dict): Configuration dictionary
        
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        input_format = config['input_format'].lower()
        output_format = config['output_format'].lower()
        
        # Register HEIF opener if needed
        if input_format == 'heic' or output_format == 'heic':
            pillow_heif.register_heif_opener()
        
        # Open the image
        with Image.open(input_path) as image:
            # Handle transparency and color mode conversion
            if output_format == 'jpg':
                # JPG doesn't support transparency, convert to RGB
                if image.mode in ('RGBA', 'LA', 'P'):
                    background_color = tuple(config['png_settings']['background_color'])
                    background = Image.new('RGB', image.size, background_color)
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save as JPG
                quality = config.get('quality', 95)
                image.save(output_path, 'JPEG', quality=quality, optimize=True)
                
            elif output_format == 'png':
                # PNG supports transparency, keep RGBA if possible
                if image.mode in ('RGBA', 'LA', 'P'):
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    # Keep RGBA for PNG to preserve transparency
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save as PNG
                optimize = config['png_settings'].get('optimize', True)
                image.save(output_path, 'PNG', optimize=optimize)
                
            elif output_format == 'heic':
                # Convert to RGB for HEIC (HEIC doesn't support transparency well)
                if image.mode in ('RGBA', 'LA', 'P'):
                    background_color = tuple(config['png_settings']['background_color'])
                    background = Image.new('RGB', image.size, background_color)
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save as HEIC
                heif_settings = config.get('heic_settings', {})
                quality = heif_settings.get('quality', 95)
                lossless = heif_settings.get('lossless', False)
                
                # Use pillow_heif to save as HEIC
                heif_image = pillow_heif.from_pillow(image)
                heif_image.save(output_path, quality=quality, lossless=lossless)
                
            else:
                logger.error(f"Unsupported output format: {output_format}")
                return False
            
        logger.info(f"Successfully converted: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
        return True
        
    except Exception as e:
        logger.error(f"Error converting {input_path}: {str(e)}")
        return False

def main():
    """Main function to process image files"""
    # Load configuration
    config = load_config()
    
    # Get configuration values
    input_dir = config['input_dir']
    output_dir = config['output_dir']
    input_format = config['input_format'].lower()
    output_format = config['output_format'].lower()
    supported_formats = config['supported_formats']
    clear_output = config['general'].get('clear_output', True)
    
    # Validate formats
    valid_formats = ['heic', 'png', 'jpg']
    if input_format not in valid_formats:
        logger.error(f"Unsupported input format: {input_format}. Use 'heic', 'png', or 'jpg'")
        return
    
    if output_format not in valid_formats:
        logger.error(f"Unsupported output format: {output_format}. Use 'heic', 'png', or 'jpg'")
        return
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        logger.error(f"Input directory '{input_dir}' does not exist!")
        return
    
    # Clear output directory if requested
    if clear_output:
        clear_output_directory(output_dir)
    else:
        os.makedirs(output_dir, exist_ok=True)
    
    # Get all input files
    input_files = get_input_files(input_dir, input_format, supported_formats)
    
    if not input_files:
        logger.info(f"No {input_format.upper()} files found in the input directory.")
        return
    
    logger.info(f"Found {len(input_files)} {input_format.upper()} file(s) to convert to {output_format.upper()}")
    
    # Convert each file
    successful_conversions = 0
    failed_conversions = 0
    
    for input_file in input_files:
        # Create output filename
        filename = os.path.basename(input_file)
        name_without_ext = os.path.splitext(filename)[0]
        output_file = os.path.join(output_dir, f"{name_without_ext}.{output_format}")
        
        # Convert the file
        if convert_image(input_file, output_file, config):
            successful_conversions += 1
        else:
            failed_conversions += 1
    
    # Summary
    logger.info(f"Conversion complete!")
    logger.info(f"Successfully converted: {successful_conversions} file(s) from {input_format.upper()} to {output_format.upper()}")
    if failed_conversions > 0:
        logger.warning(f"Failed conversions: {failed_conversions} file(s)")

if __name__ == "__main__":
    main() 
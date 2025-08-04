#!/usr/bin/env python3
"""
Create test images for all formats
Generates HEIC, PNG, and JPG test files with different characteristics
"""

import os
from PIL import Image, ImageDraw, ImageFont
import pillow_heif

def create_test_image(size=(200, 200), text="TEST", bg_color=(255, 255, 255), text_color=(0, 0, 0)):
    """Create a simple test image with text"""
    # Create image with background
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Add text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)
    
    return image

def create_transparent_image(size=(200, 200), text="TRANSPARENT"):
    """Create a transparent test image"""
    # Create transparent image
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Add colored rectangle
    draw.rectangle([50, 50, 150, 150], fill=(255, 0, 0, 128))
    
    # Add text
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill=(0, 0, 0, 255), font=font)
    
    return image

def main():
    """Create all test images"""
    test_dir = "tests/test_files"
    os.makedirs(test_dir, exist_ok=True)
    
    # Register HEIF opener
    pillow_heif.register_heif_opener()
    
    # Test 1: Simple RGB image
    print("Creating simple RGB test image...")
    rgb_image = create_test_image(text="RGB TEST", bg_color=(100, 150, 200))
    
    # Save as PNG
    rgb_image.save(f"{test_dir}/test_rgb.png", "PNG")
    print("✓ Created test_rgb.png")
    
    # Save as JPG
    rgb_image.save(f"{test_dir}/test_rgb.jpg", "JPEG", quality=95)
    print("✓ Created test_rgb.jpg")
    
    # Save as HEIC
    heif_image = pillow_heif.from_pillow(rgb_image)
    heif_image.save(f"{test_dir}/test_rgb.heic", quality=95)
    print("✓ Created test_rgb.heic")
    
    # Test 2: Transparent image
    print("Creating transparent test image...")
    transparent_image = create_transparent_image()
    
    # Save as PNG (supports transparency)
    transparent_image.save(f"{test_dir}/test_transparent.png", "PNG")
    print("✓ Created test_transparent.png")
    
    # Save as JPG (no transparency, will have white background)
    rgb_transparent = Image.new('RGB', transparent_image.size, (255, 255, 255))
    rgb_transparent.paste(transparent_image, mask=transparent_image.split()[-1])
    rgb_transparent.save(f"{test_dir}/test_transparent.jpg", "JPEG", quality=95)
    print("✓ Created test_transparent.jpg")
    
    # Save as HEIC (no transparency, will have white background)
    heif_transparent = pillow_heif.from_pillow(rgb_transparent)
    heif_transparent.save(f"{test_dir}/test_transparent.heic", quality=95)
    print("✓ Created test_transparent.heic")
    
    # Test 3: Different colors
    print("Creating color test images...")
    
    # Red image
    red_image = create_test_image(text="RED", bg_color=(255, 0, 0), text_color=(255, 255, 255))
    red_image.save(f"{test_dir}/test_red.png", "PNG")
    red_image.save(f"{test_dir}/test_red.jpg", "JPEG", quality=95)
    heif_red = pillow_heif.from_pillow(red_image)
    heif_red.save(f"{test_dir}/test_red.heic", quality=95)
    print("✓ Created test_red.* files")
    
    # Green image
    green_image = create_test_image(text="GREEN", bg_color=(0, 255, 0), text_color=(0, 0, 0))
    green_image.save(f"{test_dir}/test_green.png", "PNG")
    green_image.save(f"{test_dir}/test_green.jpg", "JPEG", quality=95)
    heif_green = pillow_heif.from_pillow(green_image)
    heif_green.save(f"{test_dir}/test_green.heic", quality=95)
    print("✓ Created test_green.* files")
    
    # Blue image
    blue_image = create_test_image(text="BLUE", bg_color=(0, 0, 255), text_color=(255, 255, 255))
    blue_image.save(f"{test_dir}/test_blue.png", "PNG")
    blue_image.save(f"{test_dir}/test_blue.jpg", "JPEG", quality=95)
    heif_blue = pillow_heif.from_pillow(blue_image)
    heif_blue.save(f"{test_dir}/test_blue.heic", quality=95)
    print("✓ Created test_blue.* files")
    
    print(f"\n✅ All test images created in {test_dir}/")
    print("Files created:")
    
    # List all created files
    for file in sorted(os.listdir(test_dir)):
        if file.endswith(('.png', '.jpg', '.heic')):
            print(f"  - {file}")

if __name__ == "__main__":
    main() 
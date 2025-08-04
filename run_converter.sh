#!/bin/bash

# HEIF to JPG Converter Runner Script
# This script activates the virtual environment and runs the converter

echo "Starting HEIF to JPG converter..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup first:"
    echo "python3 -m venv venv"
    echo "source venv/bin/activate"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and run converter
source venv/bin/activate && python heif_converter.py

echo "Converter finished!" 
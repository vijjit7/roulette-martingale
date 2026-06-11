"""
Image Processing Module
Extracts roulette numbers from screenshots using OCR
"""

import cv2
import pytesseract
import re
from PIL import Image
import numpy as np

def extract_numbers_from_image(image_path):
    """
    Extract numbers from a screenshot of roulette results
    
    Attempts multiple OCR techniques to extract numbers
    
    Args:
        image_path: Path to the image file
    
    Returns:
        List of numbers (0-36) in the order they appear
    """
    
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image file")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply image preprocessing
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Apply thresholding
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
        
        # Extract text using OCR
        text = pytesseract.image_to_string(denoised)
        
        # Parse numbers from text
        numbers = parse_numbers_from_text(text)
        
        if not numbers:
            # Try another approach - dilate and erode
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            dilated = cv2.dilate(thresh, kernel, iterations=1)
            eroded = cv2.erode(dilated, kernel, iterations=1)
            
            text = pytesseract.image_to_string(eroded)
            numbers = parse_numbers_from_text(text)
        
        if not numbers:
            # Last attempt - use original grayscale
            text = pytesseract.image_to_string(gray)
            numbers = parse_numbers_from_text(text)
        
        return numbers
    
    except Exception as e:
        print(f"Error extracting numbers from image: {e}")
        return []

def parse_numbers_from_text(text):
    """
    Parse numbers from OCR text
    
    Looks for numbers between 0-36 (valid roulette numbers)
    
    Args:
        text: Text extracted from OCR
    
    Returns:
        List of valid roulette numbers
    """
    
    if not text:
        return []
    
    # Find all numbers in the text
    found_numbers = re.findall(r'\b\d+\b', text)
    
    # Filter to valid roulette numbers (0-36)
    valid_numbers = []
    for num_str in found_numbers:
        try:
            num = int(num_str)
            if 0 <= num <= 36:
                valid_numbers.append(num)
        except ValueError:
            continue
    
    return valid_numbers

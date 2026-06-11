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
        
        numbers = []
        
        # Strategy 1: Standard preprocessing with Tesseract config
        text1 = extract_with_preprocessing_v1(gray)
        numbers1 = parse_numbers_from_text(text1)
        if numbers1:
            return numbers1
        
        # Strategy 2: Upscale image for better OCR
        text2 = extract_with_upscaling(gray)
        numbers2 = parse_numbers_from_text(text2)
        if numbers2:
            return numbers2
        
        # Strategy 3: Adaptive thresholding
        text3 = extract_with_adaptive_threshold(gray)
        numbers3 = parse_numbers_from_text(text3)
        if numbers3:
            return numbers3
        
        # Strategy 4: Simple binary threshold with different configs
        text4 = extract_with_binary_threshold(gray)
        numbers4 = parse_numbers_from_text(text4)
        if numbers4:
            return numbers4
        
        # Strategy 5: Direct OCR on grayscale with tesseract config
        config = '--psm 6 -c tessedit_char_whitelist=0123456789'
        text5 = pytesseract.image_to_string(gray, config=config)
        numbers5 = parse_numbers_from_text(text5)
        if numbers5:
            return numbers5
        
        # If all strategies fail, return empty
        return []
    
    except Exception as e:
        print(f"Error extracting numbers from image: {e}")
        return []

def extract_with_preprocessing_v1(gray):
    """Strategy 1: CLAHE + Otsu thresholding"""
    try:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        denoised = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, 
                                   cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
        
        config = '--psm 6 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(denoised, config=config)
        return text
    except:
        return ""

def extract_with_upscaling(gray):
    """Strategy 2: Upscale image for better OCR accuracy"""
    try:
        # Upscale image 3x
        h, w = gray.shape
        upscaled = cv2.resize(gray, (w * 3, h * 3), interpolation=cv2.INTER_CUBIC)
        
        # Apply thresholding on upscaled image
        _, thresh = cv2.threshold(upscaled, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                                   cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)))
        
        config = '--psm 6 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(denoised, config=config)
        return text
    except:
        return ""

def extract_with_adaptive_threshold(gray):
    """Strategy 3: Adaptive thresholding"""
    try:
        # Denoise first
        denoised = cv2.medianBlur(gray, 5)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
        
        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        config = '--psm 6 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(processed, config=config)
        return text
    except:
        return ""

def extract_with_binary_threshold(gray):
    """Strategy 4: Binary threshold with morphological operations"""
    try:
        # Apply bilateral filter to reduce noise while keeping edges
        filtered = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Binary threshold
        _, thresh = cv2.threshold(filtered, 150, 255, cv2.THRESH_BINARY)
        
        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
        
        config = '--psm 6 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(closed, config=config)
        return text
    except:
        return ""

def parse_numbers_from_text(text):
    """
    Parse numbers from OCR text with error correction
    
    Looks for numbers between 0-36 (valid roulette numbers)
    Handles common OCR mistakes (O->0, l->1, S->5, B->8, etc.)
    
    Args:
        text: Text extracted from OCR
    
    Returns:
        List of valid roulette numbers in order
    """
    
    if not text:
        return []
    
    # Common OCR error corrections
    corrections = {
        'O': '0',  # Letter O -> number 0
        'o': '0',
        'l': '1',  # Letter l -> number 1
        'I': '1',  # Letter I -> number 1
        'Z': '2',  # Letter Z -> number 2
        'S': '5',  # Letter S -> number 5
        'G': '6',  # Letter G -> number 6
        'B': '8',  # Letter B -> number 8
        'g': '9',  # Letter g -> number 9
    }
    
    # Apply corrections
    corrected_text = text
    for old, new in corrections.items():
        corrected_text = corrected_text.replace(old, new)
    
    # Find all sequences of digits
    # This includes multi-digit numbers and handles them properly
    found_items = re.findall(r'\d+', corrected_text)
    
    # Filter to valid roulette numbers (0-36)
    valid_numbers = []
    for num_str in found_items:
        try:
            num = int(num_str)
            if 0 <= num <= 36:
                valid_numbers.append(num)
        except ValueError:
            continue
    
    return valid_numbers

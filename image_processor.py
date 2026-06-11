"""
Image Processing Module
Extracts roulette numbers from screenshots using OCR
"""

import cv2
import pytesseract
import re
from PIL import Image
import numpy as np
import base64
import io

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
        
        # Run multiple strategies and return first non-empty result
        strategies = {
            'preprocessing_clahe': extract_with_preprocessing_v1(gray),
            'upscaling': extract_with_upscaling(gray),
            'adaptive_threshold': extract_with_adaptive_threshold(gray),
            'binary_threshold': extract_with_binary_threshold(gray),
            'grayscale_direct': pytesseract.image_to_string(gray, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        }

        # Parse numbers for each strategy and collect debug info
        candidates = {}
        for name, txt in strategies.items():
            nums = parse_numbers_from_text(txt)
            candidates[name] = {
                'text': txt if txt is not None else '',
                'numbers': nums
            }

        # Return the first non-empty candidate numbers list
        for name, info in candidates.items():
            if info['numbers']:
                return info['numbers']

        # If none produced results, return empty list
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


def extract_numbers_with_debug(image_path):
    """Run all strategies and return detailed debug outputs.

    Returns dict: { 'numbers': [...], 'strategies': {name: {'text':..., 'numbers':[...]}} }
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image file")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        strategies = {
            'preprocessing_clahe': extract_with_preprocessing_v1(gray),
            'upscaling': extract_with_upscaling(gray),
            'adaptive_threshold': extract_with_adaptive_threshold(gray),
            'binary_threshold': extract_with_binary_threshold(gray),
            'spatial': None,
            'grayscale_direct': pytesseract.image_to_string(gray, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        }

        candidates = {}
        for name, txt in strategies.items():
            if name == 'spatial':
                # spatial will return a dict with numbers, text and cells
                spatial_info = spatial_extract_numbers(image_path)
                candidates[name] = spatial_info
            else:
                nums = parse_numbers_from_text(txt)
                candidates[name] = {'text': txt if txt is not None else '', 'numbers': nums}

        # Pick first non-empty
        selected = []
        for info in candidates.values():
            if info['numbers']:
                selected = info['numbers']
                break

        return {'numbers': selected, 'strategies': candidates}
    except Exception as e:
        print(f"Debug extraction error: {e}")
        return {'numbers': [], 'strategies': {}}


def spatial_extract_numbers(image_path):
    """Detect individual number ROIs and OCR each cell.

    Returns a dict: {'text': concatenated_text, 'numbers': [...], 'cells': [data_url,...]}
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {'text': '', 'numbers': [], 'cells': []}

        orig = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Preprocess to find contours of digits/cells
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

        # Morph to merge digit strokes
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

        contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rois = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            area = w * h
            # Filter by reasonable digit/cell size
            if area < 200 or w < 8 or h < 8:
                continue
            if w > img.shape[1] * 0.9 or h > img.shape[0] * 0.9:
                continue
            rois.append((x, y, w, h))

        if not rois:
            return {'text': '', 'numbers': [], 'cells': []}

        # Sort ROIs by y then x (top-to-bottom, left-to-right)
        rois_sorted = sorted(rois, key=lambda r: (r[1], r[0]))

        numbers = []
        texts = []
        cells_data = []
        cell_numbers = []

        for (x, y, w, h) in rois_sorted:
            pad = 6
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(orig.shape[1], x + w + pad)
            y2 = min(orig.shape[0], y + h + pad)
            roi_color = orig[y1:y2, x1:x2]

            # Preprocess per-ROI
            roi_gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)
            roi_up = cv2.resize(roi_gray, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
            roi_blur = cv2.medianBlur(roi_up, 3)
            _, roi_thresh = cv2.threshold(roi_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            cfg = '--psm 7 -c tessedit_char_whitelist=0123456789'
            txt = pytesseract.image_to_string(roi_thresh, config=cfg)
            txt_clean = txt.strip()
            texts.append(txt_clean)

            # convert roi_color to PNG data url
            _, buffer = cv2.imencode('.png', roi_color)
            b64 = base64.b64encode(buffer).decode('utf-8')
            data_url = f'data:image/png;base64,{b64}'
            cells_data.append(data_url)

            # parse number from this ROI text
            parsed = parse_numbers_from_text(txt_clean)
            if parsed:
                cell_numbers.append(parsed[0])
            else:
                cell_numbers.append(None)

        concatenated = ' '.join([t for t in texts if t])

        # Build cleaned numbers list (remove None)
        cleaned = [n for n in cell_numbers if n is not None]

        # The spatial detection sometimes yields reverse (LIFO) ordering depending on scan direction.
        # Return FIFO order by reversing lists if needed — here we return FIFO (oldest first).
        # Reverse arrays so cell 0 corresponds to the first (oldest) number.
        cells_data = cells_data[::-1]
        texts = texts[::-1]
        cell_numbers = cell_numbers[::-1]
        cleaned = cleaned[::-1]

        return {'text': concatenated, 'numbers': cleaned, 'cells': cells_data, 'cell_numbers': cell_numbers}

    except Exception as e:
        print(f"spatial_extract_numbers error: {e}")
        return {'text': '', 'numbers': [], 'cells': []}

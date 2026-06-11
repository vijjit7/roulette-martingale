from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
from strategy import test_martingale_strategy
from image_processor import extract_numbers_from_image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/extract-numbers', methods=['POST'])
def extract_numbers():
    """Extract numbers from screenshot without testing strategy"""
    try:
        # Check if file is present
        if 'screenshot' not in request.files:
            return jsonify({'error': 'No screenshot uploaded'}), 400
        
        file = request.files['screenshot']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract numbers from image
        numbers = extract_numbers_from_image(filepath)
        
        if not numbers:
            return jsonify({'error': 'Could not extract numbers from screenshot. Please ensure the numbers are clearly visible. Try: 1) Better lighting, 2) Higher resolution, 3) Cropping just the numbers area'}), 400
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'numbers': numbers,
            'count': len(numbers)
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/test-strategy', methods=['POST'])
def test_strategy():
    try:
        # Get form data
        balance = float(request.form.get('balance', 0))
        strategy = request.form.get('strategy', 'red_black')
        
        if balance <= 0:
            return jsonify({'error': 'Balance must be greater than 0'}), 400
        
        # Check if file is present
        if 'screenshot' not in request.files:
            return jsonify({'error': 'No screenshot uploaded'}), 400
        
        file = request.files['screenshot']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract numbers from image
        numbers = extract_numbers_from_image(filepath)
        
        if not numbers:
            return jsonify({'error': 'Could not extract numbers from screenshot. Please ensure the numbers are clearly visible.'}), 400
        
        # Test strategy
        if strategy == 'red_black':
            results = test_martingale_strategy(balance, numbers)
        else:
            return jsonify({'error': 'Unknown strategy'}), 400
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/test-demo', methods=['POST'])
def test_demo():
    """Demo endpoint without requiring image"""
    try:
        balance = float(request.json.get('balance', 0))
        strategy = request.json.get('strategy', 'red_black')
        demo_numbers = request.json.get('numbers', [])
        
        if balance <= 0:
            return jsonify({'error': 'Balance must be greater than 0'}), 400
        
        if not demo_numbers:
            return jsonify({'error': 'No numbers provided'}), 400
        
        # Test strategy
        if strategy == 'red_black':
            results = test_martingale_strategy(balance, demo_numbers)
        else:
            return jsonify({'error': 'Unknown strategy'}), 400
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import os
import sys
from werkzeug.utils import secure_filename
from PIL import Image
import pillow_heif
import numpy as np

app = Flask(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'heic', 'heif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

def convert_heic_to_jpg(input_path, output_path):
    """Convert HEIC image to JPG with proper normalization"""
    try:
        # Register HEIF opener with pillow-heif
        import pillow_heif
        pillow_heif.register_heif_opener()
        
        with Image.open(input_path) as img:
            print(f"Opening image: {input_path}, format: {img.format}")
            
            # Convert HEIC to RGB and ensure proper uint8 conversion
            if img.mode != 'RGB':
                rgb_image = img.convert('RGB')
            else:
                rgb_image = img
            
            img_array = np.array(rgb_image)
            print(f"Image array shape: {img_array.shape}, dtype: {img_array.dtype}")
            
            # Validate and normalize pixel values to ensure 0-255 range
            if img_array.dtype != np.uint8:
                if img_array.max() <= 1.0:
                    img_array = (img_array * 255).astype(np.uint8)
                else:
                    img_array = np.clip(img_array, 0, 255).astype(np.uint8)
            
            # Validate image quality
            if np.mean(img_array) < 10 or np.mean(img_array) > 245:
                raise ValueError("Image appears corrupted")
            
            # Convert back to PIL Image and save as JPG
            validated_image = Image.fromarray(img_array)
            validated_image.save(output_path, 'JPEG', quality=95)
            print(f"Successfully converted to: {output_path}")
            return True
            
    except Exception as e:
        print(f"HEIC conversion error: {e}")
        # If conversion fails, try to copy the file directly
        try:
            with Image.open(input_path) as img:
                if img.mode != 'RGB':
                    rgb_image = img.convert('RGB')
                else:
                    rgb_image = img
                rgb_image.save(output_path, 'JPEG', quality=95)
                print(f"Fallback conversion successful: {output_path}")
                return True
        except Exception as fallback_error:
            print(f"Fallback conversion also failed: {fallback_error}")
            return False

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if file and allowed_file(file.filename):
            # Ensure output directory exists for processing
            os.makedirs('output', exist_ok=True)
            
            # Save uploaded file with original extension first
            temp_path = 'temp_upload' + os.path.splitext(file.filename)[1]
            file.save(temp_path)
            
            # Convert to JPG (handles both HEIC and other formats)
            if convert_heic_to_jpg(temp_path, 'product.jpg'):
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                return jsonify({
                    'success': True,
                    'message': 'File uploaded and converted successfully',
                    'filename': 'product.jpg'
                })
            else:
                return jsonify({'success': False, 'error': 'Failed to convert image'})
        else:
            return jsonify({'success': False, 'error': 'Invalid file type'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/run_detection', methods=['POST'])
def run_detection():
    try:
        # Check if input image exists in current directory
        if not os.path.exists('product.jpg'):
            return jsonify({
                'success': False,
                'error': 'No input image found. Please upload an image first.'
            })
        
        # Run the existing main.py script
        result = subprocess.run([sys.executable, 'main.py'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            # Parse the output to get quality report
            output_lines = result.stdout.strip().split('\n')
            quality_report = {}
            
            for line in output_lines:
                if 'Damage Detected:' in line:
                    quality_report['damage_detected'] = line.split(': ')[1]
                elif 'Damage Area (%):' in line:
                    quality_report['damage_area'] = line.split(': ')[1]
                elif 'Quality Status:' in line:
                    quality_report['quality_status'] = line.split(': ')[1]
            
            return jsonify({
                'success': True,
                'report': quality_report
            })
        else:
            return jsonify({
                'success': False,
                'error': result.stderr
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/<filename>')
def serve_image(filename):
    if filename == 'product.jpg':
        return send_from_directory('.', filename)
    else:
        return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

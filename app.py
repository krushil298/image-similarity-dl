"""
Flask web application for image similarity comparison.
Provides endpoints for uploading images and computing similarity.
"""

import os
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_from_directory
from similarity_engine import get_similarity_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """
    Check if uploaded file has an allowed extension.

    Args:
        filename (str): Name of the uploaded file

    Returns:
        bool: True if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file):
    """
    Save uploaded file with a secure filename.

    Args:
        file: FileStorage object from request

    Returns:
        str: Path to saved file or None if error
    """
    if file and allowed_file(file.filename):
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = secure_filename(file.filename)
        filename = f"{timestamp}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(filepath)
            logger.info(f"File saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return None
    return None


@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html')


@app.route('/compare', methods=['POST'])
def compare_images():
    """
    Compare two uploaded images and return similarity score.

    Returns:
        JSON response with similarity score and metadata
    """
    try:
        # Validate request
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'Both images are required'
            }), 400

        image1 = request.files['image1']
        image2 = request.files['image2']

        # Validate filenames
        if image1.filename == '' or image2.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No selected files'
            }), 400

        # Validate file types
        if not (allowed_file(image1.filename) and allowed_file(image2.filename)):
            return jsonify({
                'status': 'error',
                'message': 'Only PNG, JPG, and JPEG files are allowed'
            }), 400

        # Save uploaded files
        image1_path = save_uploaded_file(image1)
        image2_path = save_uploaded_file(image2)

        if not image1_path or not image2_path:
            return jsonify({
                'status': 'error',
                'message': 'Error saving uploaded files'
            }), 500

        # Compute similarity
        engine = get_similarity_engine()
        result = engine.compute_similarity(image1_path, image2_path)

        # Add image URLs to response
        result['image1_url'] = f'/uploads/{os.path.basename(image1_path)}'
        result['image2_url'] = f'/uploads/{os.path.basename(image2_path)}'

        # Clean up old files (optional - keep for now for debugging)
        # os.remove(image1_path)
        # os.remove(image2_path)

        logger.info(f"Comparison completed: {result['similarity_score']}%")
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in compare endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded files.

    Args:
        filename (str): Name of the file to serve

    Returns:
        File response
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({
        'status': 'error',
        'message': 'File size exceeds 16MB limit'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    logger.info("Starting Image Similarity Comparison Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

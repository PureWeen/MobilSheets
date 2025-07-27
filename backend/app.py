from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from convert import convert_to_midi, create_test_midi
import os
import logging
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
DEFAULT_TEST_IMAGE = os.path.join(UPLOAD_FOLDER, 'testimage.png')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return jsonify({
        'message': 'MobilSheets Backend is Running',
        'endpoints': {
            '/': 'This status endpoint',
            '/convert': 'POST - Convert sheet music image to MIDI',
            '/test-convert': 'POST - Generate a test MIDI file (for testing purposes)'
        },
        'status': 'healthy'
    })

@app.route('/test-convert', methods=['POST'])
def test_convert():
    """Generate a simple test MIDI file without using Oemer (for testing purposes)."""
    try:
        logger.info("Received test conversion request")
        
        # Create output directory
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate test MIDI file
        test_midi_path = os.path.join(output_dir, "test_output.mid")
        create_test_midi(test_midi_path)
        
        logger.info(f"Test MIDI file generated: {test_midi_path}")
        return send_file(test_midi_path, as_attachment=True, download_name='test_converted.mid')
        
    except Exception as e:
        error_msg = f"Test conversion failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({'error': error_msg}), 500

@app.route('/convert', methods=['POST'])
def convert():
    filepath = None
    try:
        logger.info("Received conversion request")
        
        # Check if a file is uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            
            # Validate file type
            if not allowed_file(file.filename):
                error_msg = f"File type not allowed. Supported types: {', '.join(ALLOWED_EXTENSIONS)}"
                logger.warning(error_msg)
                return jsonify({'error': error_msg}), 400
            
            # Secure the filename and save
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            logger.info(f"File uploaded and saved: {filepath}")
            
        else:
            # Use default test image if no file is uploaded
            if not os.path.exists(DEFAULT_TEST_IMAGE):
                error_msg = 'No file uploaded and test image not found'
                logger.warning(error_msg)
                return jsonify({'error': error_msg}), 400
            filepath = DEFAULT_TEST_IMAGE
            logger.info("Using default test image")

        # Convert to MIDI
        logger.info(f"Starting conversion process for: {filepath}")
        midi_path = convert_to_midi(filepath)
        
        logger.info(f"Conversion successful, sending file: {midi_path}")
        return send_file(midi_path, as_attachment=True, download_name='converted.mid')

    except ValueError as e:
        error_msg = f"Invalid input: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 400
        
    except FileNotFoundError as e:
        error_msg = f"File not found: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 404
        
    except RuntimeError as e:
        error_msg = f"Processing failed: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({'error': error_msg}), 500
        
    finally:
        # Clean up uploaded file if it's not the default test image
        if filepath and filepath != DEFAULT_TEST_IMAGE and os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info(f"Cleaned up uploaded file: {filepath}")
            except Exception as e:
                logger.warning(f"Could not clean up file {filepath}: {e}")

if __name__ == '__main__':
    logger.info("Starting MobilSheets Backend Server")
    app.run(debug=True)

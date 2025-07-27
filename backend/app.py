from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from convert import convert_to_midi
import os
import threading
import time
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
DEFAULT_TEST_IMAGE = os.path.join(UPLOAD_FOLDER, 'testimage.png')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store conversion results
conversion_status = {}

def background_convert(task_id, filepath):
    """Run conversion in background thread"""
    try:
        conversion_status[task_id] = {'status': 'processing', 'message': 'Converting image to MIDI...'}
        midi_path = convert_to_midi(filepath)
        conversion_status[task_id] = {'status': 'completed', 'midi_path': midi_path}
    except Exception as e:
        conversion_status[task_id] = {'status': 'error', 'error': str(e)}

@app.route('/')
def home():
    return 'MobilSheets Backend is Running'

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Check if a file is uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
        else:
            # Use default test image if no file is uploaded
            if not os.path.exists(DEFAULT_TEST_IMAGE):
                return jsonify({'error': 'No file uploaded and test image not found'}), 400
            filepath = DEFAULT_TEST_IMAGE

        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Start background conversion
        thread = threading.Thread(target=background_convert, args=(task_id, filepath))
        thread.daemon = True
        thread.start()
        
        return jsonify({'task_id': task_id, 'status': 'started', 'message': 'Conversion started. Use /status/<task_id> to check progress.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<task_id>')
def check_status(task_id):
    if task_id not in conversion_status:
        return jsonify({'error': 'Task not found'}), 404
    
    status = conversion_status[task_id]
    
    if status['status'] == 'completed':
        return jsonify({
            'status': 'completed',
            'download_url': f'/download/{task_id}'
        })
    elif status['status'] == 'error':
        return jsonify({
            'status': 'error',
            'error': status['error']
        }), 500
    else:
        return jsonify(status)

@app.route('/download/<task_id>')
def download_result(task_id):
    if task_id not in conversion_status:
        return jsonify({'error': 'Task not found'}), 404
    
    status = conversion_status[task_id]
    
    if status['status'] != 'completed':
        return jsonify({'error': 'Conversion not completed yet'}), 400
    
    return send_file(status['midi_path'], as_attachment=True)

@app.route('/convert-sync', methods=['POST'])
def convert_sync():
    """Synchronous conversion - will wait for completion but may timeout"""
    try:
        # Check if a file is uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
        else:
            # Use default test image if no file is uploaded
            if not os.path.exists(DEFAULT_TEST_IMAGE):
                return jsonify({'error': 'No file uploaded and test image not found'}), 400
            filepath = DEFAULT_TEST_IMAGE

        # Convert to MIDI (synchronous)
        midi_path = convert_to_midi(filepath)
        return send_file(midi_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

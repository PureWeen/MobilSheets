from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from convert import convert_to_midi
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
DEFAULT_TEST_IMAGE = os.path.join(UPLOAD_FOLDER, 'testimage.png')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

        # Convert to MIDI
        midi_path = convert_to_midi(filepath)
        return send_file(midi_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

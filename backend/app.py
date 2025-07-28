from flask import Flask, send_file, jsonify
from flask_cors import CORS
from convert import convert_to_midi
import os
import subprocess
import traceback


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
TEST_IMAGE = os.path.join(UPLOAD_FOLDER, 'testimage.png')
MUSICXML_PATH = os.path.join(OUTPUT_FOLDER, 'output.musicxml')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'MobilSheets Backend is Running'

@app.route('/convert', methods=['POST'])
def convert():
    try:
        cmd = [
            'oemer',
            TEST_IMAGE,
            '-o', MUSICXML_PATH
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({'error': f'Oemer failed: {result.stderr}'}), 500

        midi_path = convert_to_midi(MUSICXML_PATH)
        return send_file(midi_path, as_attachment=True)

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=8080)

from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
from convert import convert_to_midi
import os
import traceback
from oemer import depredict
import onnxruntime as ort

# Force ONNX Runtime to use CPU
ort.set_default_logger_severity(3)  # Suppress verbose logs
os.environ['CUDA_VISIBLE_DEVICES'] = ''  # Disable GPU for TensorFlow (if used)
ort_session_options = ort.SessionOptions()
ort_session_options.intra_op_num_threads = 1  # Optimize for CPU

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
MUSICXML_PATH = os.path.join(OUTPUT_FOLDER, 'output.musicxml')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'MobilSheets Backend is Running'

@app.route('/convert', methods=['POST'])
def convert():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # Run Oemer with CPU provider
        musicxml_path = depredict(image_path, providers=['CPUExecutionProvider'])
        if not os.path.exists(musicxml_path):
            return jsonify({'error': 'Oemer failed to generate MusicXML'}), 500

        midi_path = convert_to_midi(musicxml_path)
        return send_file(midi_path, as_attachment=True)

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
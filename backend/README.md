# MobilSheets Backend

This is the Flask backend for the MobilSheets application that converts sheet music images to MIDI files using Oemer OCR technology.

## Setup

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Start the server:
```bash
cd backend
python app.py
```

The server will run on `http://127.0.0.1:5000` by default.

## API Endpoints

### GET /
Returns server status and available endpoints.

### POST /convert
Converts a sheet music image to a MIDI file using Oemer.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Field: `file` (image file)
- Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF

**Response:**
- Success: MIDI file download
- Error: JSON error message

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/convert \
  -F 'file=@testimage.png' \
  --output output.mid
```

### POST /test-convert
Generates a simple test MIDI file without using Oemer (for testing purposes).

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/test-convert \
  --output test.mid
```

## Known Limitations

### Oemer Processing Time
- Oemer OCR processing can take 5-10 minutes even for simple images
- The server has a 10-minute timeout for Oemer processing
- Complex or large images may cause timeouts

### Oemer Compatibility Issues
- Some images may cause Oemer to fail with internal errors (e.g., IndexError during MusicXML generation)
- The quality and format of the input image significantly affects success rate
- Oemer works best with clear, high-contrast sheet music images

### System Requirements
- CPU-only processing (GPU support disabled due to compatibility issues)
- Requires significant processing time and memory for image analysis

## Error Handling

The backend provides comprehensive error handling for:
- Invalid file types
- Missing files
- Oemer processing failures
- Timeout errors
- Image validation errors

## Troubleshooting

### "Oemer processing timed out"
- This is normal behavior for complex images
- Try using simpler, smaller images
- Use the `/test-convert` endpoint to verify the system is working

### "Invalid image file"
- Ensure the file is a valid image format
- Check that the image is not corrupted

### "Processing failed: Oemer failed"
- This indicates an internal Oemer error
- Try different images or image preprocessing

## Dependencies

- Flask: Web framework
- Flask-CORS: Cross-origin resource sharing
- music21: Music notation and MIDI generation
- Oemer: Optical music recognition
- Pillow: Image processing
- onnxruntime: Neural network inference (CPU-only)

## Development

The backend includes comprehensive logging for debugging. Check the console output for detailed information about processing steps and errors.
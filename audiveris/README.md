# Audiveris Integration for MobilSheets

This directory contains the complete Audiveris optical music recognition system for converting sheet music images to MIDI and MusicXML files.

## What's Included

- **audiveris-5.3.jar** - The main Audiveris application JAR file
- **lib/** - Complete set of dependency JAR files required by Audiveris
- **README.md** - This documentation file

## How It Works

The bundled Audiveris installation includes:

1. **Audiveris 5.3.1** - Open-source optical music recognition engine
2. **Complete dependency libraries** - All required JAR files for full functionality
3. **Ready-to-use setup** - No additional downloads or manual installation required

## Usage

The Audiveris installation is automatically detected and used by:

- `audiveris_converter.py` - Production script with full Audiveris integration
- `audiveris_demo.py` - Demo script that works with or without Audiveris

## Technical Details

- **Java Version**: Requires Java 11 or higher (OpenJDK 17 recommended)
- **Main Class**: `org.audiveris.omr.Main`
- **Dependencies**: All required libraries are included in the `lib/` directory
- **Output Formats**: 
  - MusicXML (.mxl) - Primary output format (more comprehensive than MIDI)
  - MIDI (.mid) - Generated via music21 conversion from MusicXML

## File Information

- **audiveris-5.3.jar**: 5.2 MB - Main application
- **lib/ directory**: ~150 MB total - Complete dependency set including:
  - Tesseract OCR integration
  - Image processing libraries
  - Music notation processing
  - Export/import functionality

This bundled installation ensures the scripts work immediately without requiring users to download, extract, or configure Audiveris manually.
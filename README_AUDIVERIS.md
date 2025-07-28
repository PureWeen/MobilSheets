# Audiveris Sheet Music to MIDI Converter

This project includes a complete Audiveris optical music recognition system that converts sheet music images to MIDI files.

## What's Included

✅ **Complete Audiveris 5.3.1 installation** - Ready to use with all dependencies  
✅ **Production converter script** - Full command-line interface  
✅ **Demo script** - Works immediately without external dependencies  
✅ **Automatic MIDI conversion** - Converts MusicXML to MIDI using music21  
✅ **Comprehensive documentation** - Installation and usage instructions  

## Quick Start

### Prerequisites

1. **Java 11 or higher** (required for Audiveris)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install openjdk-11-jdk
   
   # CentOS/RHEL
   sudo yum install java-11-openjdk-devel
   
   # macOS (with Homebrew)
   brew install openjdk@11
   
   # Verify installation
   java -version
   ```

2. **Python dependencies** (optional, for MIDI conversion)
   ```bash
   pip install music21
   ```

### Ready-to-Use Audiveris Installation

The project includes a complete Audiveris installation in the `audiveris/` directory:
- Audiveris 5.3.1 JAR file and all dependencies
- No manual download or setup required
- Works immediately after Java installation

## Usage

### Quick Verification

Verify that everything is properly installed:
```bash
python audiveris_converter.py --setup-only
```

### Production Script (audiveris_converter.py)

Convert sheet music images to MIDI files using the full Audiveris system:

#### Basic Conversion

Convert a sheet music image to MIDI:
```bash
python audiveris_converter.py backend/uploads/testimage.png
```

### Specify Output Directory

Convert with custom output directory:
```bash
python audiveris_converter.py backend/uploads/testimage.png outputs/
```

### Setup Only

Check installation and setup without converting:
```bash
python audiveris_converter.py --setup-only
```

### Help

Show all available options:
```bash
python audiveris_converter.py --help
```

## Examples

1. **Convert the included test image:**
   ```bash
   python audiveris_converter.py backend/uploads/testimage.png
   ```

2. **Convert with specific output location:**
   ```bash
   python audiveris_converter.py sheet_music.png /tmp/midi_output/
   ```

3. **Convert multiple files:**
   ```bash
   # Script handles one file at a time
   python audiveris_converter.py score1.png outputs/
   python audiveris_converter.py score2.jpg outputs/
   ```

## Supported Image Formats

The script supports common image formats including:
- PNG
- JPEG/JPG
- BMP
- TIFF

## Output Formats

The conversion process generates multiple output formats:

1. **MusicXML (.mxl)** - Primary output from Audiveris
   - More comprehensive than MIDI
   - Contains complete music notation information
   - Can be opened in music notation software (MuseScore, Finale, etc.)

2. **MIDI (.mid)** - Converted from MusicXML
   - Standard MIDI format compatible with all MIDI software
   - Generated automatically when music21 is installed
   - Playable in media players and music software

3. **OMR (.omr)** - Audiveris project file
   - Contains complete recognition data
   - Can be reopened in Audiveris for editing

### Output Process

The script will:
1. Create an output directory (default: `audiveris_output`)
2. Process the image with Audiveris optical music recognition
3. Generate MusicXML file from recognized notation
4. Convert MusicXML to MIDI format (if music21 is available)
5. Report the location of all generated files

### Installing music21 for MIDI conversion

For automatic MIDI file generation, install music21:
```bash
pip install music21
```

Without music21, you'll get MusicXML files that can be manually converted to MIDI using other tools.

## Troubleshooting

### Java Issues
- Ensure Java 11+ is installed: `java -version`
- Set JAVA_HOME if needed: `export JAVA_HOME=/path/to/java`

### Audiveris Issues
- Verify the JAR file location
- Check file permissions
- Ensure the image is clear and well-formatted sheet music

### Common Error Messages

**"Java not found"**
- Install Java 11 or higher
- Verify Java is in your PATH

**"Audiveris processing timed out"**
- Try with a smaller or clearer image
- Increase timeout in the script if needed

**"No music files found"**
- Check if the image contains recognizable sheet music
- Verify the image quality and format
- Ensure the image shows clear musical notation

**"Could not convert MusicXML to MIDI"**
- Install music21: `pip install music21`
- The MusicXML file is still available for manual conversion

## Manual Audiveris Installation

If automatic download fails:

1. Visit: https://github.com/Audiveris/audiveris/releases
2. Download the latest release ZIP file
3. Extract to your desired location
4. Note the path to the `audiveris.jar` file
5. Either:
   - Copy the JAR to one of the expected locations, or
   - Modify the script to point to your JAR location

## Contributing

When contributing to the Audiveris conversion functionality:
1. Test with the provided test image first
2. Ensure error handling works properly
3. Update documentation for any new features
4. Test on different image formats and sizes

## License

This project is released under the MIT License.
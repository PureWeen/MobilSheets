# Audiveris Sheet Music to MIDI Converter

This project includes a Python script that uses Audiveris to convert sheet music images to MIDI files.

## Installation

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

2. **Audiveris JAR File**
   The project includes a placeholder JAR file that needs to be replaced:
   
   ```bash
   # Download Audiveris 5.3
   wget https://github.com/Audiveris/audiveris/releases/download/5.3/audiveris-5.3.zip
   
   # Extract the ZIP file
   unzip audiveris-5.3.zip
   
   # Copy the JAR file to the project directory
   cp audiveris-5.3/lib/audiveris-5.3.jar audiveris/audiveris-5.3.jar
   ```
   
   **Or manually:**
   - Download from: https://github.com/Audiveris/audiveris/releases/tag/5.3
   - Extract the ZIP file
   - Copy `audiveris-5.3/lib/audiveris-5.3.jar` to `audiveris/audiveris-5.3.jar`

### Setup

1. Clone this repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd MobilSheets
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Setup**
   Check that everything is properly installed:
   ```bash
   python audiveris_converter.py --setup-only
   ```

## Usage

### Basic Conversion

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

## Output

The script will:
1. Create an output directory (default: `audiveris_output`)
2. Process the image with Audiveris
3. Generate MIDI files from the recognized music notation
4. Report the location of generated files

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

**"Failed to find Audiveris JAR"** or **"Found placeholder JAR"**
- Replace the placeholder JAR file with the real Audiveris JAR
- Download Audiveris 5.3 and copy the JAR to `audiveris/audiveris-5.3.jar`
- See the `audiveris/README.md` file for detailed instructions

**"Audiveris processing timed out"**
- Try with a smaller or clearer image
- Increase timeout in the script if needed

**"No MIDI files found"**
- Check if the image contains recognizable sheet music
- Verify the image quality and format

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
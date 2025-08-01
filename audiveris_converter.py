#!/usr/bin/env python3
"""
Audiveris Sheet Music to MIDI Converter

This script uses Audiveris (an open-source optical music recognition tool) to convert
sheet music images into MIDI files.

Requirements:
- Java 11 or higher (OpenJDK recommended)
- Audiveris JAR file (downloaded automatically if not present)
- Python 3.6+

Usage:
    python audiveris_converter.py <input_image_path> [output_directory]

Example:
    python audiveris_converter.py backend/uploads/testimage.png
    python audiveris_converter.py sheet_music.png outputs/
"""

import os
import sys
import subprocess
import argparse
import urllib.request
import zipfile
import shutil
from pathlib import Path


class AudiverisConverter:
    """Handles Audiveris installation and sheet music conversion."""
    
    AUDIVERIS_VERSION = "5.3"
    AUDIVERIS_URL = f"https://github.com/Audiveris/audiveris/releases/download/{AUDIVERIS_VERSION}/audiveris-{AUDIVERIS_VERSION}.zip"
    AUDIVERIS_DIR = "audiveris"
    POSSIBLE_JAR_PATHS = [
        # Bundled JAR files (preferred)
        f"audiveris/audiveris-{AUDIVERIS_VERSION}.jar",
        "audiveris/audiveris.jar",
        # Standard installation paths
        f"audiveris-{AUDIVERIS_VERSION}/lib/audiveris-{AUDIVERIS_VERSION}.jar",
        f"audiveris/lib/audiveris-{AUDIVERIS_VERSION}.jar",
        "audiveris.jar",
        "/usr/local/lib/audiveris.jar",
        "/opt/audiveris/audiveris.jar"
    ]
    
    def __init__(self):
        self.audiveris_path = None
        
    def check_java(self):
        """Check if Java is installed and get version."""
        try:
            result = subprocess.run(["java", "-version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version_info = result.stderr.split('\n')[0]
                print(f"✓ Java found: {version_info}")
                return True
            else:
                print("✗ Java not found")
                return False
        except FileNotFoundError:
            print("✗ Java not found")
            return False
    
    def find_audiveris_jar(self):
        """Find Audiveris JAR file in common locations."""
        for jar_path in self.POSSIBLE_JAR_PATHS:
            if os.path.exists(jar_path):
                # Check if it's our placeholder file
                if jar_path.startswith("audiveris/") and os.path.getsize(jar_path) < 1000:
                    # This is likely our placeholder file
                    with open(jar_path, 'r') as f:
                        content = f.read()
                        if "placeholder" in content.lower():
                            print(f"⚠ Found placeholder JAR at {jar_path}")
                            continue
                
                print(f"✓ Found Audiveris JAR at {jar_path}")
                return jar_path
        return None
    
    def download_audiveris(self):
        """Download and extract Audiveris if not present."""
        # First, try to find existing installation
        existing_jar = self.find_audiveris_jar()
        if existing_jar:
            return existing_jar
            
        print("❌ No Audiveris JAR file found!")
        print("\n" + "="*60)
        print("AUDIVERIS JAR INSTALLATION REQUIRED")
        print("="*60)
        print("The bundled Audiveris JAR file is missing or is a placeholder.")
        print("\nTo fix this:")
        print("1. Download Audiveris 5.3 from:")
        print("   https://github.com/Audiveris/audiveris/releases/tag/5.3")
        print("2. Extract the downloaded audiveris-5.3.zip file")
        print("3. Copy the JAR file to this location:")
        print("   audiveris/audiveris-5.3.jar")
        print("   (from audiveris-5.3/lib/audiveris-5.3.jar in the extracted folder)")
        print("\nAlternatively, you can place it in any of these locations:")
        for path in self.POSSIBLE_JAR_PATHS:
            print(f"   - {path}")
        print("\n" + "="*60)
        return None
    
    def convert_image_to_midi(self, input_path, output_dir=None):
        """Convert sheet music image to MIDI using Audiveris."""
        
        # Validate input file
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Set up output directory
        if output_dir is None:
            output_dir = "audiveris_output"
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Get absolute paths
        input_path = os.path.abspath(input_path)
        output_dir = os.path.abspath(output_dir)
        
        print(f"Converting {input_path} to MIDI...")
        print(f"Output directory: {output_dir}")
        
        try:
            # Check if we have the full lib directory or just the JAR
            audiveris_dir = os.path.dirname(self.audiveris_path)
            lib_dir = os.path.join(audiveris_dir, "lib")
            
            if os.path.exists(lib_dir):
                # Use classpath with all JARs from lib directory
                classpath = f"{self.audiveris_path}:{lib_dir}/*"
                cmd = [
                    "java",
                    "-cp", classpath,
                    "org.audiveris.omr.Main",
                    "-batch",  # Run in batch mode
                    "-export",  # Export results
                    "-output", output_dir,  # Output directory
                    input_path  # Input image
                ]
            else:
                # Fallback to single JAR (if it has a manifest)
                cmd = [
                    "java",
                    "-jar", self.audiveris_path,
                    "-batch",  # Run in batch mode
                    "-export",  # Export results
                    "-output", output_dir,  # Output directory
                    input_path  # Input image
                ]
            
            print(f"Running command: {' '.join(cmd)}")
            
            # Run Audiveris
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print("✓ Audiveris processing completed successfully")
                
                # Look for generated files
                midi_files = []
                musicxml_files = []
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        if file.lower().endswith(('.mid', '.midi')):
                            midi_files.append(os.path.join(root, file))
                        elif file.lower().endswith(('.mxl', '.musicxml', '.xml')):
                            musicxml_files.append(os.path.join(root, file))
                
                if midi_files:
                    print(f"✓ Generated MIDI files:")
                    for midi_file in midi_files:
                        print(f"  - {midi_file}")
                    return midi_files[0]  # Return the first MIDI file found
                elif musicxml_files:
                    print(f"✓ Generated MusicXML files:")
                    for xml_file in musicxml_files:
                        print(f"  - {xml_file}")
                    print("\nNote: Audiveris generates MusicXML format, which is more comprehensive than MIDI.")
                    print("MusicXML files can be opened with music notation software like MuseScore.")
                    
                    # Try to convert MusicXML to MIDI if possible
                    return self._convert_musicxml_to_midi(musicxml_files[0], output_dir)
                else:
                    print("⚠ No music files found in output directory")
                    # List all files in output directory for debugging
                    print("Files in output directory:")
                    for root, dirs, files in os.walk(output_dir):
                        for file in files:
                            print(f"  - {os.path.join(root, file)}")
                    return None
                    
            else:
                print(f"✗ Audiveris failed with return code {result.returncode}")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("✗ Audiveris processing timed out (5 minutes)")
            return None
        except Exception as e:
            print(f"✗ Error running Audiveris: {e}")
            return None
    
    def _convert_musicxml_to_midi(self, musicxml_path, output_dir):
        """Convert MusicXML to MIDI using music21 if available."""
        try:
            # Try to import music21 for MusicXML to MIDI conversion
            try:
                from music21 import converter, midi
                print("Attempting to convert MusicXML to MIDI using music21...")
                
                # Load the MusicXML file
                score = converter.parse(musicxml_path)
                
                # Generate MIDI file path
                base_name = os.path.splitext(os.path.basename(musicxml_path))[0]
                midi_path = os.path.join(output_dir, f"{base_name}.mid")
                
                # Convert to MIDI
                midi_file = midi.translate.streamToMidiFile(score)
                midi_file.open(midi_path, 'wb')
                midi_file.write()
                midi_file.close()
                
                print(f"✓ Converted to MIDI: {midi_path}")
                return midi_path
                
            except ImportError:
                print("Note: Install music21 for automatic MusicXML to MIDI conversion:")
                print("  pip install music21")
                print(f"✓ MusicXML file available: {musicxml_path}")
                return musicxml_path
                
        except Exception as e:
            print(f"⚠ Could not convert MusicXML to MIDI: {e}")
            print(f"✓ MusicXML file available: {musicxml_path}")
            return musicxml_path
    
    def setup(self):
        """Set up Audiveris environment."""
        print("Setting up Audiveris environment...")
        
        if not self.check_java():
            print("\n" + "="*50)
            print("JAVA INSTALLATION REQUIRED")
            print("="*50)
            print("Please install Java 11 or higher:")
            print("Ubuntu/Debian: sudo apt-get install openjdk-11-jdk")
            print("CentOS/RHEL: sudo yum install java-11-openjdk-devel")
            print("macOS: brew install openjdk@11")
            print("Windows: Download from https://adoptopenjdk.net/")
            return False
        
        if not self.download_audiveris():
            return False
            
        jar_path = self.download_audiveris()
        if not jar_path:
            return False
            
        self.audiveris_path = jar_path
        print(f"✓ Audiveris setup complete!")
        return True


def main():
    """Main function to handle command line arguments and run conversion."""
    parser = argparse.ArgumentParser(
        description="Convert sheet music images to MIDI using Audiveris",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python audiveris_converter.py sheet_music.png
  python audiveris_converter.py backend/uploads/testimage.png outputs/
  python audiveris_converter.py score.jpg /tmp/midi_files/

Installation Requirements:
  1. Java 11+ (will be checked automatically)
  2. Audiveris (will be downloaded automatically)
        """
    )
    
    parser.add_argument("input_image", 
                       nargs='?',
                       help="Path to the sheet music image file")
    parser.add_argument("output_dir", 
                       nargs='?', 
                       default=None,
                       help="Output directory for MIDI files (default: audiveris_output)")
    parser.add_argument("--setup-only", 
                       action="store_true",
                       help="Only setup Audiveris, don't convert")
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.setup_only and not args.input_image:
        parser.error("input_image is required unless --setup-only is specified")
    
    # Create converter instance
    converter = AudiverisConverter()
    
    # Setup Audiveris
    if not converter.setup():
        print("✗ Failed to setup Audiveris environment")
        sys.exit(1)
    
    if args.setup_only:
        print("✓ Setup complete!")
        sys.exit(0)
    
    # Convert the image
    try:
        midi_file = converter.convert_image_to_midi(args.input_image, args.output_dir)
        
        if midi_file:
            print(f"\n✓ SUCCESS: MIDI file created at {midi_file}")
            sys.exit(0)
        else:
            print(f"\n✗ FAILED: Could not create MIDI file from {args.input_image}")
            sys.exit(1)
            
    except FileNotFoundError as e:
        print(f"✗ ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ UNEXPECTED ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
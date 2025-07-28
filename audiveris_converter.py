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
                print(f"✓ Found Audiveris JAR at {jar_path}")
                return jar_path
        return None
    
    def download_audiveris(self):
        """Download and extract Audiveris if not present."""
        # First, try to find existing installation
        existing_jar = self.find_audiveris_jar()
        if existing_jar:
            return existing_jar
            
        print(f"Downloading Audiveris {self.AUDIVERIS_VERSION}...")
        print("Note: If download fails, please install manually from:")
        print(f"https://github.com/Audiveris/audiveris/releases")
        
        try:
            zip_path = f"audiveris-{self.AUDIVERIS_VERSION}.zip"
            
            # Download the zip file
            print(f"Downloading from {self.AUDIVERIS_URL}")
            urllib.request.urlretrieve(self.AUDIVERIS_URL, zip_path)
            
            # Extract the zip file
            print("Extracting Audiveris...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('.')
            
            # Clean up zip file
            os.remove(zip_path)
            
            # Find the extracted JAR
            jar_path = self.find_audiveris_jar()
            if jar_path:
                print(f"✓ Audiveris downloaded and extracted to {jar_path}")
                return jar_path
            else:
                print("✗ Failed to find Audiveris JAR after extraction")
                return None
                
        except Exception as e:
            print(f"✗ Failed to download Audiveris: {e}")
            print("\nMANUAL INSTALLATION REQUIRED:")
            print("1. Download Audiveris from: https://github.com/Audiveris/audiveris/releases")
            print("2. Extract the ZIP file")
            print("3. Place the audiveris.jar file in one of these locations:")
            for path in self.POSSIBLE_JAR_PATHS:
                print(f"   - {path}")
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
            # Audiveris command line arguments
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
                
                # Look for generated MIDI files
                midi_files = []
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        if file.lower().endswith(('.mid', '.midi')):
                            midi_files.append(os.path.join(root, file))
                
                if midi_files:
                    print(f"✓ Generated MIDI files:")
                    for midi_file in midi_files:
                        print(f"  - {midi_file}")
                    return midi_files[0]  # Return the first MIDI file found
                else:
                    print("⚠ No MIDI files found in output directory")
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
#!/usr/bin/env python3
"""
Audiveris Sheet Music to MIDI Converter - Demo Implementation

This demo script shows how to integrate Audiveris for sheet music to MIDI conversion.
For the full implementation, use audiveris_converter.py with a real Audiveris installation.

This demo creates a simple MIDI file to demonstrate the workflow without requiring
the actual Audiveris installation.
"""

import os
import sys
import argparse
from pathlib import Path


def create_demo_midi(output_path):
    """Create a simple demo MIDI file for demonstration purposes."""
    
    # Simple MIDI file content (C major scale)
    # This is a basic MIDI file with header and a simple note sequence
    midi_content = bytes([
        # MIDI header chunk
        0x4D, 0x54, 0x68, 0x64,  # "MThd"
        0x00, 0x00, 0x00, 0x06,  # Header length (6 bytes)
        0x00, 0x00,              # Format type 0
        0x00, 0x01,              # One track
        0x00, 0x60,              # 96 ticks per quarter note
        
        # Track chunk
        0x4D, 0x54, 0x72, 0x6B,  # "MTrk"
        0x00, 0x00, 0x00, 0x3B,  # Track length
        
        # Track events (C major scale)
        0x00, 0x90, 0x3C, 0x64,  # Note on C4
        0x60, 0x80, 0x3C, 0x64,  # Note off C4
        0x00, 0x90, 0x3E, 0x64,  # Note on D4
        0x60, 0x80, 0x3E, 0x64,  # Note off D4
        0x00, 0x90, 0x40, 0x64,  # Note on E4
        0x60, 0x80, 0x40, 0x64,  # Note off E4
        0x00, 0x90, 0x41, 0x64,  # Note on F4
        0x60, 0x80, 0x41, 0x64,  # Note off F4
        0x00, 0x90, 0x43, 0x64,  # Note on G4
        0x60, 0x80, 0x43, 0x64,  # Note off G4
        0x00, 0x90, 0x45, 0x64,  # Note on A4
        0x60, 0x80, 0x45, 0x64,  # Note off A4
        0x00, 0x90, 0x47, 0x64,  # Note on B4
        0x60, 0x80, 0x47, 0x64,  # Note off B4
        0x00, 0x90, 0x48, 0x64,  # Note on C5
        0x60, 0x80, 0x48, 0x64,  # Note off C5
        
        0x00, 0xFF, 0x2F, 0x00   # End of track
    ])
    
    with open(output_path, 'wb') as f:
        f.write(midi_content)
    
    return output_path


def demo_convert_image_to_midi(input_path, output_dir=None):
    """Demo conversion function that simulates Audiveris workflow."""
    
    # Validate input file
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Set up output directory
    if output_dir is None:
        output_dir = "demo_output"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Get input filename without extension
    input_name = Path(input_path).stem
    midi_filename = f"{input_name}_converted.mid"
    midi_path = os.path.join(output_dir, midi_filename)
    
    print(f"🎵 Demo: Converting {input_path} to MIDI...")
    print(f"📁 Output directory: {output_dir}")
    print(f"🎹 Creating demo MIDI file: {midi_path}")
    
    # In a real implementation, this would call Audiveris:
    print("🔄 [DEMO] Simulating Audiveris optical music recognition...")
    print("🔄 [DEMO] Analyzing sheet music image...")
    print("🔄 [DEMO] Recognizing musical notation...")
    print("🔄 [DEMO] Converting to MIDI format...")
    
    # Create demo MIDI file
    create_demo_midi(midi_path)
    
    print(f"✅ Demo conversion completed!")
    print(f"📄 Generated MIDI file: {midi_path}")
    print(f"🎵 Contains: C major scale (demo content)")
    
    return midi_path


def main():
    """Main function for demo conversion."""
    parser = argparse.ArgumentParser(
        description="Demo: Convert sheet music images to MIDI using Audiveris",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This is a DEMO implementation that creates a sample MIDI file.
For real Audiveris integration, use audiveris_converter.py

Examples:
  python audiveris_demo.py backend/uploads/testimage.png
  python audiveris_demo.py sheet_music.png demo_output/

Demo Features:
  - Validates input image exists
  - Creates output directory structure
  - Generates sample MIDI file (C major scale)
  - Demonstrates complete workflow
        """
    )
    
    parser.add_argument("input_image", 
                       help="Path to the sheet music image file")
    parser.add_argument("output_dir", 
                       nargs='?', 
                       default=None,
                       help="Output directory for MIDI files (default: demo_output)")
    
    args = parser.parse_args()
    
    try:
        print("🎼 Audiveris Sheet Music to MIDI Converter - DEMO")
        print("=" * 50)
        
        midi_file = demo_convert_image_to_midi(args.input_image, args.output_dir)
        
        print("\n✅ SUCCESS: Demo MIDI file created!")
        print(f"📁 Location: {midi_file}")
        print(f"🎵 Content: C major scale (demo)")
        print("\n💡 Note: This is a demo. For real conversion:")
        print("   1. Install Java 11+")
        print("   2. Get the Audiveris JAR file (see audiveris/README.md)")
        print("   3. Use: python audiveris_converter.py <image_file>")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ ERROR: {e}")
        return 1
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
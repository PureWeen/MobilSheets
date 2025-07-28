#!/bin/bash
# Audiveris OMR (Optical Music Recognition) launcher script
# Usage: ./audiveris.sh [options] input_image_file

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIVERIS_BIN="$SCRIPT_DIR/audiversejar/bin/Audiveris"

# Check if Audiveris is available
if [ ! -f "$AUDIVERIS_BIN" ]; then
    echo "Error: Audiveris not found at $AUDIVERIS_BIN"
    echo "Please ensure the audiversejar folder contains the Audiveris installation."
    exit 1
fi

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo "Audiveris OMR - Optical Music Recognition"
    echo "Usage: $0 [options] input_image_file"
    echo ""
    echo "Examples:"
    echo "  $0 testimage.png                    # Process image with GUI"
    echo "  $0 -batch testimage.png            # Process image in batch mode"
    echo "  $0 -output output.mxl testimage.png # Specify output file"
    echo ""
    echo "For more options, run: $0 -help"
    exit 1
fi

# Run Audiveris with all provided arguments
exec "$AUDIVERIS_BIN" "$@"

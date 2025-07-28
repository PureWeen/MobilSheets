# Audiveris JAR Installation

This directory should contain the Audiveris JAR file for the converter to work.

## Required File

Place the Audiveris JAR file here as:
- `audiveris-5.3.jar` (recommended)
- OR `audiveris.jar` (alternative name)

## How to Get Audiveris JAR

1. Download Audiveris 5.3 from: https://github.com/Audiveris/audiveris/releases/tag/5.3
2. Extract the downloaded ZIP file
3. Copy the JAR file from `audiveris-5.3/lib/audiveris-5.3.jar` to this directory
4. Rename it to `audiveris-5.3.jar` or `audiveris.jar`

## Verification

After placing the JAR file, you can verify it works by running:
```bash
python audiveris_converter.py --setup-only
```

## Expected Structure

```
audiveris/
├── README.md (this file)
└── audiveris-5.3.jar (the Audiveris JAR file you need to add)
```
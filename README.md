# 🎼 MobilSheets

MobilSheets is a modern mobile application that transforms printed sheet music into playable digital files. Designed for musicians, educators, and students, the app makes it easy to capture or upload sheet music and receive a downloadable MIDI version in seconds.

---

## ✨ Key Features

- Capture or upload sheet music directly from your device
- Instantly receive a playable MIDI file
- Access and manage your conversion history
- Seamless cloud integration for fast and reliable processing

---

## 🎯 Who It's For

- Music students digitizing practice materials
- Educators preparing interactive lessons
- Performers converting printed scores into digital playback
- Composers testing arrangements on the go

---

## � Getting Started

### Optical Music Recognition (OMR)

MobilSheets uses Audiveris for high-quality optical music recognition. The system can convert sheet music images into MusicXML format.

#### Using the Audiveris Script

The project includes a ready-to-use Audiveris setup with all required JAR files:

```bash
# Basic usage - convert image to MusicXML
./audiveris.sh -batch -export path/to/your/sheet-music.png

# Example with test image
./audiveris.sh -batch -export backend/uploads/testimage.png
```

**Output files:**
- `*.mxl` - MusicXML file (can be opened in MuseScore, Finale, etc.)
- `*.omr` - Audiveris project file (for further editing)

**Supported formats:**
- Input: PNG, JPG, TIFF, PDF
- Output: MusicXML (.mxl), Audiveris project (.omr)

#### Requirements
- Java 21+ (pre-installed in dev container)
- The `audiversejar/` folder contains all required runtime files

---

## �📌 Project Vision

MobilSheets aims to bridge the gap between traditional music notation and modern digital tools. By simplifying the conversion process, it empowers users to interact with music in more flexible and creative ways.

---

## 📄 License

This project is released under the MIT License.

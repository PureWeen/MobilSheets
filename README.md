# 🎼 MobilSheets

MobilSheets is a modern mobile application that transforms printed sheet music into playable digital files. Designed for musicians, educators, and students, the app makes it easy to capture or upload sheet music and receive a downloadable MIDI version in seconds.

---

## ✨ Key Features

- Capture or upload sheet music directly from your device
- Instantly receive a playable MIDI file
- Access and manage your conversion history
- Seamless cloud integration for fast and reliable processing
- **NEW: Audiveris integration for command-line sheet music conversion**

---

## 🛠️ Audiveris Integration

This project now includes Audiveris-based sheet music to MIDI conversion:

### Quick Start (Demo)
```bash
# Try the demo with the included test image
python audiveris_demo.py backend/uploads/testimage.png

# Convert with custom output directory  
python audiveris_demo.py backend/uploads/testimage.png my_output/
```

### Production Use
```bash
# For real conversion (requires Audiveris installation)
python audiveris_converter.py backend/uploads/testimage.png
```

📖 **Full documentation:** See [README_AUDIVERIS.md](README_AUDIVERIS.md) for complete installation and usage instructions.

---

## 🎯 Who It's For

- Music students digitizing practice materials
- Educators preparing interactive lessons
- Performers converting printed scores into digital playback
- Composers testing arrangements on the go

---

## 📌 Project Vision

MobilSheets aims to bridge the gap between traditional music notation and modern digital tools. By simplifying the conversion process, it empowers users to interact with music in more flexible and creative ways.

---

## 📄 License

This project is released under the MIT License.

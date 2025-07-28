import os
from music21 import converter

OUTPUT_FOLDER = 'output'
MIDI_PATH = os.path.join(OUTPUT_FOLDER, 'output.mid')

def convert_to_midi(musicxml_path):
    try:
        # Parse MusicXML file
        score = converter.parse(musicxml_path)
        # Write to MIDI
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        score.writeMidi(MIDI_PATH)
        return MIDI_PATH
    except Exception as e:
        raise Exception(f'MIDI conversion failed: {str(e)}')

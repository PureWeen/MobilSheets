import subprocess
import os

OUTPUT_FOLDER = 'output'
MIDI_PATH = os.path.join(OUTPUT_FOLDER, 'output.mid')

def convert_to_midi(musicxml_path):
    # Replace this with the actual command you want to run to convert MusicXML to MIDI
    cmd = [
        'musescore',  # or any other tool that converts MusicXML to MIDI
        musicxml_path,
        '-o', MIDI_PATH
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f'MIDI conversion failed: {result.stderr}')
    return MIDI_PATH

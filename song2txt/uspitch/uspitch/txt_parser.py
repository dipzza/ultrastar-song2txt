import sys

import numpy as np
from charset_normalizer import from_path


class Parser:

    def __init__(self):
        self.orig_text = ''
        self.mp3: str = ''
        self.bpm: float = 0
        self.gap: float = 0
        self.notes: list = []

    def read_file(self, path):
        try:
            self.orig_text = str(from_path(path).best())

            for line in self.orig_text.splitlines():
                if line.startswith((':', '*')):
                    self.notes.append(line.split()[1:3])
                elif line.startswith('#BPM'):
                    self.bpm = float(line.lstrip('#BPM:'))
                elif line.startswith('#GAP'):
                    self.gap = float(line.lstrip('#GAP:'))
                elif line.startswith('#MP3'):
                    self.mp3 = line.lstrip('#MP3:')
        except FileNotFoundError:
            print('File does not exist: ' + path)
            sys.exit(1)

    def write_file(self, path, pitches):
        try:
            pitches_iter = iter(pitches)

            with open(path, 'w', encoding='utf-8') as f:
                for line in self.orig_text.splitlines():
                    if line.startswith((':', '*')):
                        line = line.split()
                        line[3] = str(next(pitches_iter))
                        line = ' '.join(line)
                    f.write(line + '\n')
        except PermissionError:
            print('Permission denied: ' + path)
            sys.exit(1)
        except FileNotFoundError:
            print('Directory does not exist: ' + path)
            sys.exit(1)

    def notes_intervals(self):
        beat_length = 15000 / self.bpm
        timing = np.array(self.notes, dtype=float)
        timing[:, 0] = self.gap + timing[:, 0] * beat_length
        timing[:, 1] = timing[:, 0] + timing[:, 1] * beat_length
        return timing

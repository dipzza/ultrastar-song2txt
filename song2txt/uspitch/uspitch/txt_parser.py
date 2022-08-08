import sys

import numpy as np
from charset_normalizer import from_path


def read_file(path):
    try:
        text = str(from_path(path).best())
        metadata = {}
        notes_timing = []

        for line in text.splitlines():
            if line.startswith((':', '*')):
                notes_timing.append(line.split()[1:3])
            elif line.startswith('#'):
                key, value = line.lstrip('#').split(':')
                metadata[key] = value

        return text, metadata, notes_timing
    except FileNotFoundError:
        print('File does not exist: ' + path)
        sys.exit(1)


def write_file(path, text, new_pitches=None, new_metadata=None):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            if new_pitches is not None:
                text = update_pitches(text, new_pitches)
            if new_metadata is not None:
                text = update_metadata(text, new_metadata)
            f.write(text)
    except PermissionError:
        print('Permission denied: ' + path)
        sys.exit(1)
    except FileNotFoundError:
        print('Directory does not exist: ' + path)
        sys.exit(1)


def update_pitches(text, new_pitches):
    lines = text.splitlines(True)
    pitch_iter = iter(new_pitches)

    for index, line in enumerate(lines):
        if line.startswith((':', '*')):
            line = line.split(' ')
            line[3] = str(next(pitch_iter))
            lines[index] = ' '.join(line)

    return ''.join(lines)


def update_metadata(text, new_metadata):
    lines = text.splitlines(True)
    metadata_end = 0

    # Removes old metadata
    for index, line in enumerate(lines):
        if not line.startswith('#'):
            metadata_end = index
            break

    lines = lines[metadata_end:]

    # Adds new metadata
    for index, item in enumerate(new_metadata.items()):
        key, value = item
        line = '#' + key + ':' + value + '\n'
        lines.insert(index, line)

    return ''.join(lines)


def beat_to_ms(metadata, intervals):
    bpm, gap = str_to_float(metadata['BPM'], metadata['GAP'])
    beat_length = 15000 / bpm

    timing = np.array(intervals, dtype=float)
    timing[:, 0] = timing[:, 0] * beat_length + gap
    timing[:, 1] = timing[:, 1] * beat_length + timing[:, 0]

    return timing


def ms_to_beat(metadata, intervals):
    bpm, gap = str_to_float(metadata['BPM'], metadata['GAP'])
    beat_length = 15000 / bpm

    timing = np.array(intervals, dtype=float)
    timing[:, 1] = (timing[:, 1] - timing[:, 0]) / beat_length
    timing[:, 0] = (timing[:, 0] - gap) / beat_length

    return timing


def str_to_float(*values: str):
    sanitized = []

    for value in values:
        sanitized.append(float(value.replace(',', '.')))

    return sanitized

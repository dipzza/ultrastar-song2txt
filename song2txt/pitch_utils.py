import warnings

import numpy as np
import librosa as lbr


# The BPM txt value is multiplied by 4 to get more detailed note positioning
# 60000milliseconds/minute / (BPM * 4)beats/minute -> 15000/BPM milliseconds
BEAT_LENGTH_FACTOR = 15000
UNK = -1


def hz_to_midi(hz):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        midi = lbr.hz_to_midi(hz)

    midi = np.nan_to_num(midi, nan=UNK, posinf=UNK, neginf=UNK)
    midi = midi.round()

    return midi.astype(int)


def calculate_pitches(frequency, confidence, intervals, conf_threshold):
    notes_freq = []
    for start, end in intervals:
        freq = frequency[start:end]
        freq = freq[confidence[start:end] >= conf_threshold]

        if len(freq) == 0:
            notes_freq.append(UNK)
        else:
            notes_freq.append(np.mean(freq))

    return hz_to_midi(np.array(notes_freq))


def notes_to_array(notes):
    tmp_list = []

    for note in notes:
        tmp_list.append([note.start_beat, note.length, note.pitch])

    return np.array(tmp_list)


def beat_to_ms(note_array, bpm, gap):
    beat_length = BEAT_LENGTH_FACTOR / bpm
    note_array = note_array.astype(float)
    note_array = note_array.reshape(-1, 3)

    note_array[:, 0] = note_array[:, 0] * beat_length + gap
    note_array[:, 1] = note_array[:, 1] * beat_length + note_array[:, 0]

    return note_array

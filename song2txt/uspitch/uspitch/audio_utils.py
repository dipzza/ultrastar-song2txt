import numpy as np
from pydub import AudioSegment


def open_audio(path):
    audio = AudioSegment.from_file(path)
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        samples = samples.reshape((-1, 2))
    return samples, audio.frame_rate


def hz_to_midi(hz):
    note = np.where(hz >= 7.95, 12 * np.log2(hz / 440, where=hz > 0) + 69, -1)
    return np.int_(np.round(note))


def calculate_pitches(frequency, confidence, intervals, conf_threshold):
    notes_freq = []
    for start, end in intervals:
        freq = frequency[start:end]
        freq = freq[confidence[start:end] >= conf_threshold]

        if len(freq) == 0:
            notes_freq.append(-1)
        else:
            notes_freq.append(np.mean(freq))

    return hz_to_midi(np.array(notes_freq))

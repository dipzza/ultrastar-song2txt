from unittest import mock

import song2txt.uspitch.uspitch.audio_utils as audio

import numpy as np


def test_open_audio_mono():
    m_audio = mock.Mock()
    m_audio.channels = 1
    m_audio.get_array_of_samples.return_value = [1, 1]
    m_audio.frame_rate = 48000

    with mock.patch('song2txt.uspitch.uspitch.audio_utils.AudioSegment') \
            as AudioSegmentMock:
        AudioSegmentMock.from_file.return_value = m_audio
        samples, sample_rate = audio.open_audio('song.wav')

    assert np.array_equal(samples, np.array([1, 1]))
    assert sample_rate == m_audio.frame_rate


def test_open_audio_stereo():
    m_audio = mock.Mock()
    m_audio.channels = 2
    m_audio.get_array_of_samples.return_value = [1, 2, 1, 2]
    m_audio.frame_rate = 48000

    with mock.patch('song2txt.uspitch.uspitch.audio_utils.AudioSegment') \
            as AudioSegmentMock:
        AudioSegmentMock.from_file.return_value = m_audio
        samples, sample_rate = audio.open_audio('song.wav')

    assert np.array_equal(samples, np.array([[1, 2], [1, 2]]))
    assert sample_rate == m_audio.frame_rate


def test_hz_to_midi_float():
    midi = audio.hz_to_midi(261.6)
    assert midi == 60
    assert isinstance(midi, np.signedinteger)


def test_hz_to_midi_float_invalid():
    midi = audio.hz_to_midi(0)
    assert midi == -1
    assert isinstance(midi, np.signedinteger)


def test_hz_to_midi_array():
    midi = audio.hz_to_midi(np.array([261, 2637]))
    assert np.array_equal(midi, np.array([60, 100]))


def test_hz_to_midi_array_invalid():
    midi = audio.hz_to_midi(np.array([0, 261, -1]))
    assert np.array_equal(midi, np.array([-1, 60, -1]))


def test_calculate_pitches():
    frequency = np.array([261, 261, 261, 261])
    confidence = np.array([0.9, 0.1, 0.9, 0.1])
    intervals = np.array([[0, 1], [1, 2], [2, 4]])

    pitches = audio.calculate_pitches(frequency, confidence, intervals, 0.7)

    assert np.array_equal(pitches, np.array([60, -1, 60]))

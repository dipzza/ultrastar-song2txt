from unittest import mock
import sys

import pytest
import numpy as np

import song2txt.pitch_cli as cli
import song2txt.pitch_utils as utils
from song2txt.txt_parser.song_line import Note, NoteType
import tests.conftest as c

DUMMY_STR = ''
PATH_PITCH = 'song_pitched.txt'
CONF_OPTION = '--confidence'
OUTPUT_OPTION = '--output'

HZ = 261
BAD_HZ = 0
UNK = -1
CONF_THRESHOLD = 0.8
H_CONF = 0.9
L_CONF = 0.1


@pytest.fixture
def crepe_value():
    frequency = np.array([HZ, HZ, HZ, HZ])
    confidence = np.array([H_CONF, L_CONF, H_CONF, L_CONF])

    return [0, frequency, confidence, 0]


@mock.patch('song2txt.pitch_cli.crepe')
@mock.patch('song2txt.pitch_cli.txt_parser')
def test_no_required_arguments(*_):
    with pytest.raises(SystemExit, match='2'):
        cli.main()


@mock.patch('song2txt.pitch_cli.crepe')
@mock.patch('song2txt.pitch_cli.txt_parser')
def test_incorrect_type(*_):
    sys.argv = [DUMMY_STR, DUMMY_STR, CONF_OPTION, DUMMY_STR]
    with pytest.raises(SystemExit, match='2'):
        cli.main()


@mock.patch('song2txt.pitch_cli.lbr.load')
@mock.patch('song2txt.pitch_cli.crepe')
@mock.patch('song2txt.pitch_cli.txt_parser.write_file')
@mock.patch('song2txt.pitch_cli.txt_parser.read_file')
def test_default_args(m_read, m_write, m_crepe, m_load, us_txt, crepe_value):
    sys.argv = [DUMMY_STR, c.PATH]

    m_load.return_value = [DUMMY_STR, DUMMY_STR]
    m_read.return_value = us_txt
    m_crepe.predict.return_value = crepe_value

    cli.main()

    assert m_write.call_count == 1
    assert m_write.call_args[0][0] == us_txt
    assert m_write.call_args[0][1].name == PATH_PITCH


@mock.patch('song2txt.pitch_cli.lbr.load')
@mock.patch('song2txt.pitch_cli.crepe')
@mock.patch('song2txt.pitch_cli.txt_parser.write_file')
@mock.patch('song2txt.pitch_cli.txt_parser.read_file')
def test_custom_output(m_read, m_write, m_crepe, m_load, us_txt, crepe_value):
    sys.argv = [DUMMY_STR, DUMMY_STR, OUTPUT_OPTION, c.PATH]

    m_load.return_value = [DUMMY_STR, DUMMY_STR]
    m_read.return_value = us_txt
    m_crepe.predict.return_value = crepe_value

    cli.main()

    assert m_write.call_count == 1
    assert m_write.call_args[0][0] == us_txt
    assert m_write.call_args[0][1].name == c.PATH


def test_hz_to_midi():
    midi = utils.hz_to_midi(np.array([HZ, HZ]))
    assert np.array_equal(midi, np.array([c.MIDI, c.MIDI]))


def test_hz_to_midi_array_invalid():
    midi = utils.hz_to_midi(np.array([BAD_HZ, UNK]))
    assert np.array_equal(midi, np.array([UNK, UNK]))


def test_calculate_pitches():
    frequency = np.array([HZ, HZ, HZ, BAD_HZ])
    confidence = np.array([H_CONF, L_CONF, H_CONF, L_CONF])
    intervals = np.array([[0, 1], [1, 2], [2, 4]])

    pitches = utils.calculate_pitches(frequency, confidence,
                                      intervals, CONF_THRESHOLD)

    assert np.array_equal(pitches, np.array([c.MIDI, UNK, c.MIDI]))


def test_notes_to_array():
    notes = [Note(NoteType.NORMAL, c.START_BEAT, c.LENGTH, c.MIDI, c.WORD),
             Note(NoteType.NORMAL, c.END_BEAT, c.LENGTH, c.MIDI, c.WORD)]

    converted_array = utils.notes_to_array(notes)

    array = np.array([[c.START_BEAT, c.LENGTH, c.MIDI],
                      [c.END_BEAT, c.LENGTH, c.MIDI]])

    assert np.array_equal(array, converted_array)

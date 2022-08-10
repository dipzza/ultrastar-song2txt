from unittest import mock
import sys

from song2txt.uspitch.uspitch.cli import main

import pytest
import numpy as np


@pytest.fixture
def read_value():
    metadata = {'TITLE': 'title',
                'MP3': 'filename.mp3',
                'BPM': '300',
                'GAP': '0'}
    note_timing = np.array([[0.0, 0.2], [0.2, 0.2], [0.4, 0.4]])

    return ['text', metadata, note_timing]


@pytest.fixture
def crepe_value():
    frequency = np.array([261, 261, 261, 261])
    confidence = np.array([0.99, 0.0, 0.99, 0.0])

    return [0, frequency, confidence, 0]


@mock.patch('song2txt.uspitch.uspitch.cli.crepe')
@mock.patch('song2txt.uspitch.uspitch.cli.txt')
def test_no_required_arguments(*mocks):
    with pytest.raises(SystemExit, match='2'):
        main()


@mock.patch('song2txt.uspitch.uspitch.cli.crepe')
@mock.patch('song2txt.uspitch.uspitch.cli.txt')
def test_incorrect_type(*mocks):
    sys.argv = ['cli.py', 'path', '--confidence', 'str']
    with pytest.raises(SystemExit, match='2'):
        main()


@mock.patch('song2txt.uspitch.uspitch.cli.open_audio', return_value=[0, 0])
@mock.patch('song2txt.uspitch.uspitch.cli.crepe')
@mock.patch('song2txt.uspitch.uspitch.cli.txt.write_file')
@mock.patch('song2txt.uspitch.uspitch.cli.txt.read_file')
def test_default_args(m_read, m_write, m_crepe, _, read_value, crepe_value):
    sys.argv = ['cli.py', '../filepath.txt']

    m_read.return_value = read_value
    m_crepe.predict.return_value = crepe_value

    main()

    assert m_write.call_count == 1
    assert m_write.call_args[0][0] == '../filepath_pitched.txt'
    assert m_write.call_args[0][1] == 'text'
    assert np.array_equal(m_write.call_args[0][2], np.array([60, -1, 60]))


@mock.patch('song2txt.uspitch.uspitch.cli.open_audio', return_value=[0, 0])
@mock.patch('song2txt.uspitch.uspitch.cli.crepe')
@mock.patch('song2txt.uspitch.uspitch.cli.txt.write_file')
@mock.patch('song2txt.uspitch.uspitch.cli.txt.read_file')
def test_custom_output(m_read, m_write, m_crepe, _, read_value, crepe_value):
    sys.argv = ['cli.py', 'path', '-o', 'custom_output.txt']

    m_read.return_value = read_value
    m_crepe.predict.return_value = crepe_value

    main()

    assert m_write.call_count == 1
    assert m_write.call_args[0][0] == 'custom_output.txt'
    assert m_write.call_args[0][1] == 'text'
    assert np.array_equal(m_write.call_args[0][2], np.array([60, -1, 60]))

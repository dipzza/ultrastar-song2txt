from unittest import mock

import song2txt.uspitch.uspitch.txt_parser as parser

import pytest
import numpy as np


@pytest.fixture
def text():
    text = '#TITLE:title\n' \
           '#MP3:filename.mp3\n' \
           '#BPM:300\n' \
           '#GAP:10,5\n' \
           '* 0 4 58 ña\n' \
           '- 8 10\n' \
           ': 12 5 58 ña\n' \
           ': 17 2 55 ~\n' \
           '- 20\n' \
           'E\n'
    return text


@pytest.fixture
def metadata():
    metadata = {'TITLE': 'title',
                'MP3': 'filename.mp3',
                'BPM': '300',
                'GAP': '10,5'}
    return metadata


@pytest.fixture
def notes_timing_beats():
    timing = [['0', '4'], ['12', '5'], ['17', '2']]
    return timing


@pytest.fixture
def notes_timing_ms():
    timing = np.array([[10.5, 210.5], [610.5, 860.5], [860.5, 960.5]])
    return timing


@pytest.fixture
def pitches():
    pitches = ['58', '58', '55']
    return pitches


def test_read_file(text, metadata, notes_timing_beats):
    with mock.patch('song2txt.uspitch.uspitch.txt_parser.from_path') as \
            from_path_mock:
        mock_best = mock.Mock()
        mock_best.best.return_value = text
        from_path_mock.return_value = mock_best

        r_text, r_meta, r_timing = parser.read_file('path')

        assert r_text == text
        assert r_meta == metadata
        assert r_timing == notes_timing_beats


def test_read_file_invalid_path():
    with pytest.raises(SystemExit):
        parser.read_file('')


def test_write_file(text, metadata, pitches):
    open_mock = mock.mock_open()
    with mock.patch('builtins.open', open_mock, create=True):
        parser.write_file('path', text, pitches, metadata)

    open_mock.assert_called_with('path', 'w', encoding='utf-8')
    open_mock.return_value.write.assert_called_once_with(text)


def test_write_file_no_permission():
    open_mock = mock.mock_open()
    with mock.patch('builtins.open', open_mock, create=True):
        open_mock.side_effect = PermissionError
        with pytest.raises(SystemExit):
            parser.write_file('', '')


def test_write_file_invalid_path():
    with pytest.raises(SystemExit):
        parser.write_file('', '')


def test_update_pitches(text, pitches):
    new_text = parser.update_pitches(text, pitches)
    assert new_text == text


def test_update_metadata(text, metadata):
    new_text = parser.update_metadata(text, metadata)
    assert new_text == text


def test_beat_to_ms(metadata, notes_timing_beats, notes_timing_ms):
    result = parser.beat_to_ms(metadata, notes_timing_beats)
    assert np.array_equal(result, notes_timing_ms)


def test_ms_to_beat(metadata, notes_timing_beats, notes_timing_ms):
    result = parser.ms_to_beat(metadata, notes_timing_ms)
    assert np.array_equal(result, np.array(notes_timing_beats, dtype=float))


def test_str_to_float():
    result = parser.str_to_float('5,5', '5.3', '10')
    assert result == [5.5, 5.3, 10]

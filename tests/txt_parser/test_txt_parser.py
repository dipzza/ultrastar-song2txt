from unittest import mock

import pytest

import song2txt.txt_parser.txt_parser as txt_parser
import song2txt.txt_parser.song_line as sl
import tests.conftest as c


def test_read_file(us_txt, us_txt_text):
    with mock.patch('song2txt.txt_parser.txt_parser.from_path') as mock_fp:
        mock_best = mock.Mock()
        mock_best.best.return_value = us_txt_text
        mock_fp.return_value = mock_best

        us_txt_read = txt_parser.read_file(c.PATH)

        assert us_txt_read.metadata == us_txt.metadata
        assert us_txt_read.song_lines == us_txt.song_lines


def test_write_file(us_txt, us_txt_text):
    open_mock = mock.mock_open()
    with mock.patch('builtins.open', open_mock, create=True):
        txt_parser.write_file(us_txt, c.PATH)

    open_mock.assert_called_with(c.PATH, 'w', encoding='utf-8')
    open_mock.return_value.write.assert_called_once_with(us_txt_text)


def test_parse_text(us_txt, us_txt_text):
    us_txt_parsed = txt_parser.parse_text(us_txt_text)

    assert us_txt_parsed.metadata == us_txt.metadata
    assert us_txt_parsed.song_lines == us_txt.song_lines


def test_parse_text_invalid():
    with pytest.raises(Exception):
        txt_parser.parse_text(c.WORD)


def test_parse_line_player_change():
    player_change = sl.PlayerChange(c.PLAYER)
    parsed_object = txt_parser.parse_song_line(str(player_change))

    assert isinstance(parsed_object, sl.PlayerChange)
    assert player_change.player_n == parsed_object.player_n


def test_parse_line_note():
    note = sl.Note(sl.NoteType.NORMAL, c.START_BEAT, c.LENGTH, c.MIDI, c.WORD)
    parsed_object = txt_parser.parse_song_line(str(note))

    assert isinstance(parsed_object, sl.Note)
    assert note.type == parsed_object.type
    assert note.start_beat == parsed_object.start_beat
    assert note.length == parsed_object.length
    assert note.pitch == parsed_object.pitch
    assert note.text == parsed_object.text


def test_parse_line_phrase_end_single():
    phrase_end = sl.PhraseEnd(c.START_BEAT)
    parsed_object = txt_parser.parse_song_line(str(phrase_end))

    assert isinstance(parsed_object, sl.PhraseEnd)
    assert phrase_end.start_beat == parsed_object.start_beat
    assert phrase_end.end_beat == parsed_object.end_beat


def test_parse_line_phrase_end_interval():
    phrase_end = sl.PhraseEnd(c.START_BEAT, c.END_BEAT)
    parsed_object = txt_parser.parse_song_line(str(phrase_end))

    assert isinstance(parsed_object, sl.PhraseEnd)
    assert phrase_end.start_beat == parsed_object.start_beat
    assert phrase_end.end_beat == parsed_object.end_beat


def test_parse_song_line_invalid():
    assert txt_parser.parse_song_line(c.WORD) is None


def test_parse_line_metadata(metadata_dict, metadata_text):
    for item, line in zip(metadata_dict.items(), metadata_text.splitlines()):
        key, value = item
        parsed_key, parsed_value = txt_parser.parse_metadata_line(line)

        assert parsed_key == key
        assert parsed_value == value


def test_parse_line_metadata_invalid():
    assert txt_parser.parse_metadata_line(c.WORD) is None

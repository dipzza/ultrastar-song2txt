import pytest

import song2txt.txt_parser.song_line as sl
import tests.conftest as c

BAD_LENGTH = 0
NOTE_STR_MODEL = '{} {} {} {} {}\n'

PLAYER_2 = 2
BAD_PLAYER = 0
PLAYER_STR_MODEL = 'P{}\n'

END_BEAT_2 = 2
BAD_END_BEAT = 0
PHRASE_STR_MODEL = '- {}\n'
PHRASE_STR_MODEL_2 = '- {} {}\n'


def test_player_change_valid():
    assert sl.PlayerChange(c.PLAYER).player_n == c.PLAYER


def test_player_change_invalid():
    with pytest.raises(ValueError):
        sl.PlayerChange(BAD_PLAYER)


def test_player_change_str():
    change = sl.PlayerChange(c.PLAYER)

    assert str(change) == PLAYER_STR_MODEL.format(c.PLAYER)


def test_note_valid():
    note = sl.Note(sl.NoteType.NORMAL, c.START_BEAT, c.LENGTH, c.MIDI, c.WORD)

    assert note.type == sl.NoteType.NORMAL
    assert note.start_beat == c.START_BEAT
    assert note.length == c.LENGTH
    assert note.pitch == c.MIDI
    assert note.text == c.WORD


def test_note_invalid():
    with pytest.raises(ValueError):
        sl.Note(sl.NoteType.NORMAL, c.START_BEAT, BAD_LENGTH, c.MIDI, c.WORD)


def test_note_str():
    note = sl.Note(sl.NoteType.NORMAL, c.START_BEAT, c.LENGTH, c.MIDI, c.WORD)

    assert str(note) == NOTE_STR_MODEL.format(
        note.type.value, note.start_beat, note.length, note.pitch, note.text)


def test_phrase_end_valid():
    phrase_end = sl.PhraseEnd(c.START_BEAT, c.END_BEAT)

    assert phrase_end.start_beat == c.START_BEAT
    assert phrase_end.end_beat == c.END_BEAT


def test_phrase_end_invalid():
    with pytest.raises(ValueError):
        sl.PhraseEnd(c.START_BEAT, BAD_END_BEAT)


def test_phrase_end_only_start_str():
    phrase_end = sl.PhraseEnd(c.START_BEAT)

    assert str(phrase_end) == PHRASE_STR_MODEL.format(c.START_BEAT)


def test_phrase_end_interval_str():
    phrase_end = sl.PhraseEnd(c.START_BEAT, c.END_BEAT)
    phrase_end_str = PHRASE_STR_MODEL_2.format(c.START_BEAT, c.END_BEAT)

    assert str(phrase_end) == phrase_end_str

from song2txt.txt_parser.song_line import Note, NoteType
import tests.conftest as c


def test_str(us_txt, us_txt_text):
    assert str(us_txt) == us_txt_text


def test_get_notes(us_txt):
    expected = [Note(NoteType.NORMAL, c.START_BEAT, c.LENGTH, c.MIDI, c.WORD)]
    assert us_txt.get_notes() == expected

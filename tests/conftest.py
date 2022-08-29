import pytest

import song2txt.txt_parser.song_line as sl
from song2txt.txt_parser.ultrastar_txt import UltraStarTXT, FILE_END
from song2txt.txt_parser.metadata import MetaData, TITLE_TAG, ARTIST_TAG, \
    MP3_TAG, BPM_TAG, RELATIVE_TAG, GAP_TAG, YEAR_TAG, META_STR_FALSE

# Constants
# Song Lines
START_BEAT = 0
LENGTH = 1
MIDI = 60
WORD = 'Word'
PLAYER = 1
END_BEAT = 1

# TXT parsing
PATH = 'song.txt'

# Metadata
TITLE = 'song name'
ARTIST = 'artist name'
MP3 = 'song name.mp3'
BPM = 300.0
BPM_STR = '300'
RELATIVE = False
GAP = 10.5
GAP_STR = '10.5'
YEAR = 2007
YEAR_STR = '2007'


# Fixtures
@pytest.fixture
def metadata():
    return MetaData(TITLE, ARTIST, MP3, BPM,
                    year=YEAR, relative=RELATIVE, gap=GAP)


@pytest.fixture
def metadata_text():
    model = '#{}:{}\n'
    text = model.format(TITLE_TAG, TITLE)
    text += model.format(ARTIST_TAG, ARTIST)
    text += model.format(MP3_TAG, MP3)
    text += model.format(BPM_TAG, BPM_STR)
    text += model.format(YEAR_TAG, YEAR_STR)
    text += model.format(RELATIVE_TAG, META_STR_FALSE)
    text += model.format(GAP_TAG, GAP_STR)

    return text


@pytest.fixture
def song_lines():
    song_lines = [sl.PlayerChange(PLAYER),
                  sl.Note(sl.NoteType.NORMAL, START_BEAT, LENGTH, MIDI, WORD),
                  sl.PhraseEnd(START_BEAT, END_BEAT)]
    return song_lines


@pytest.fixture
def song_lines_text(song_lines):
    text = ''
    for song_line in song_lines:
        text += str(song_line)

    return text


@pytest.fixture
def us_txt(metadata, song_lines):
    return UltraStarTXT(metadata, song_lines)


@pytest.fixture
def us_txt_text(metadata_text, song_lines_text):
    return metadata_text + song_lines_text + FILE_END

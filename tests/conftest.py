import pytest

import song2txt.txt_parser.song_line as sl
from song2txt.txt_parser.ultrastar_txt import UltraStarTXT
from song2txt.txt_parser.metadata import MetaData

# Constants
# Song Lines
START_BEAT = 0
LENGTH = 1
MIDI = 60
WORD = 'Word'
PLAYER = 1
END_BEAT = 1

# Other
PATH = 'song.txt'
FILE_END = 'E'


# Fixtures
@pytest.fixture
def metadata_dict():
    return {
        'TITLE': 'song name',
        'ARTIST': 'artist name',
        'MP3': 'song name.mp3',
        'BPM': '300',
        'GENRE': 'Pop',
        'YEAR': '2007',
        'EDITION': 'Christmas',
        'CREATOR': 'Julia',
        'LANGUAGE': 'English',
        'COVER': 'song name.jpg',
        'VOCALS': 'song name vocals.mp3',
        'VIDEO': 'song name.mkv',
        'BACKGROUND': 'song name background.jpg',
        'RELATIVE': 'NO',
        'GAP': '10.5',
        'VIDEOGAP': '3',
        'PREVIEWSTART': '60',
        'DUETSINGERP1': 'Javier',
        'DUETSINGERP2': 'Julia',
        'EXTRA': 'valor extra'
    }


@pytest.fixture
def metadata(metadata_dict):
    metadata = MetaData()

    for key, value in metadata_dict.items():
        metadata.add(key, value)

    return metadata


@pytest.fixture
def metadata_text(metadata_dict):
    model = '#{}:{}\n'
    text = ''

    for key, value in metadata_dict.items():
        text += model.format(key, value)

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

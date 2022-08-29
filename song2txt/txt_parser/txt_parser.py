import re
from os import PathLike

from charset_normalizer import from_path

from .ultrastar_txt import UltraStarTXT, FILE_END
from .song_line import Note, PlayerChange, PhraseEnd, NoteType, SongLine
from .metadata import MetaData, INT_TAGS, BOOL_TAGS, FLOAT_TAGS, META_STR_TRUE

REGEX_PLAYER = r'P(\d)'
REGEX_NOTE = r'([:*FRG]) (\d+) (\d+) (\d+) *(.*)'
REGEX_PHRASE_END = r'- (\d+) ?(\d+)?'
REGEX_META = r'# *(\S*) *: *(.*) *'

CODE_PAGES = ['utf-8', 'windows-1250', 'windows-1252']


def read_file(path: PathLike) -> UltraStarTXT:
    text = str(from_path(path, cp_isolation=CODE_PAGES).best())

    return parse_text(text)


def write_file(us_txt: UltraStarTXT, path: PathLike):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(us_txt))


def parse_text(text: str) -> UltraStarTXT:
    metadata_dict = {}
    song_lines = []

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        parsed = parse_metadata_line(lines[i])
        if isinstance(parsed, tuple):
            metadata_dict[parsed[0].lower()] = parsed[1]
            i += 1
        else:
            break

    while i < len(lines) and not lines[i].startswith(FILE_END):
        song_line = parse_song_line(lines[i])
        if isinstance(song_line, SongLine):
            song_lines.append(song_line)
            i += 1
        else:
            raise Exception(f'Incorrect format in line {i}: {lines[i]}')

    return UltraStarTXT(MetaData(**metadata_dict), song_lines)


def parse_song_line(line: str):
    parsed = None
    match_player = re.compile(REGEX_PLAYER).match(line)
    match_note = re.compile(REGEX_NOTE).match(line)
    match_phrase = re.compile(REGEX_PHRASE_END).match(line)

    if match_player:
        parsed = PlayerChange(int(match_player.group(1)))
    elif match_note:
        note_type = NoteType(match_note.group(1))
        start_beat = int(match_note.group(2))
        length = int(match_note.group(3))
        pitch = int(match_note.group(4))
        text = match_note.group(5)
        parsed = Note(note_type, start_beat, length, pitch, text)
    elif match_phrase:
        start_beat = int(match_phrase.group(1))
        end_beat = match_phrase.group(2)
        end_beat = int(end_beat) if end_beat else None
        parsed = PhraseEnd(start_beat, end_beat)

    return parsed


def parse_metadata_line(line: str):
    match = re.compile(REGEX_META).match(line)
    if match:
        tag = match.group(1)
        value = match.group(2)

        if tag in FLOAT_TAGS:
            value = float(value.replace(',', '.'))
        elif tag in INT_TAGS:
            value = int(value)
        elif tag in BOOL_TAGS:
            value = value == META_STR_TRUE

        return tag, value
    else:
        return None

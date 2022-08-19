import re
from os import PathLike

from charset_normalizer import from_path

from .ultrastar_txt import UltraStarTXT
from .song_line import Note, PlayerChange, PhraseEnd, NoteType, SongLine
from .metadata import MetaData

REG_PLAYER = r'P(\d)'
REG_NOTE = r'([:*FRG]) (\d+) (\d+) (\d+) *(.*)'
REG_PHRASE_END = r'- (\d+) ?(\d+)?'
REG_META = r'# *(\S*) *: *(.*) *'
FILE_END = 'E'


def read_file(path: PathLike) -> UltraStarTXT:
    cp_list = ['utf-8', 'windows-1252', 'ISO-8859-1']
    text = str(from_path(path, cp_isolation=cp_list).best())

    return parse_text(text)


def write_file(us_txt: UltraStarTXT, path: PathLike):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(us_txt))


def parse_text(text: str) -> UltraStarTXT:
    metadata = MetaData()
    song_lines = []

    lines = text.splitlines()
    is_metadata = True
    i = 0
    while i < len(lines) and is_metadata:
        parsed = parse_metadata_line(lines[i])
        if isinstance(parsed, tuple):
            metadata.add(*parsed)
            i += 1
        else:
            is_metadata = False

    while i < len(lines) and not lines[i].startswith(FILE_END):
        song_line = parse_song_line(lines[i])
        if isinstance(song_line, SongLine):
            song_lines.append(song_line)
        else:
            raise Exception(f'Incorrect format in line {i}: {lines[i]}')
        i += 1

    return UltraStarTXT(metadata, song_lines)


def parse_song_line(line: str):
    parsed = None
    match_player = re.compile(REG_PLAYER).match(line)
    match_note = re.compile(REG_NOTE).match(line)
    match_phrase = re.compile(REG_PHRASE_END).match(line)

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
        if end_beat is None:
            parsed = PhraseEnd(start_beat)
        else:
            parsed = PhraseEnd(start_beat, int(end_beat))

    return parsed


def parse_metadata_line(line: str):
    match = re.compile(REG_META).match(line)
    if match:
        return match.group(1), match.group(2)
    else:
        return None

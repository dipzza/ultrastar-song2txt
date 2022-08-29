from dataclasses import dataclass
from typing import List

from .metadata import MetaData
from .song_line import Note, SongLine

FILE_END = 'E'


@dataclass
class UltraStarTXT:
    metadata: MetaData
    song_lines: List[SongLine]

    def __str__(self) -> str:
        text = str(self.metadata)
        for line in self.song_lines:
            text += str(line)
        text += FILE_END

        return text

    def get_notes(self):
        notes = []

        for line in self.song_lines:
            if isinstance(line, Note):
                notes.append(line)

        return notes

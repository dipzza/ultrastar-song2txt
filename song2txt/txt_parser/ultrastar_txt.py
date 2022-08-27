from dataclasses import dataclass
from typing import List

from .metadata import MetaData
from .song_line import Note, SongLine


@dataclass
class UltraStarTXT:
    metadata: MetaData
    song_lines: List[SongLine]

    def __str__(self) -> str:
        text = str(self.metadata)
        for line in self.song_lines:
            text += str(line)
        text += 'E'

        return text

    def get_notes(self):
        notes = []

        for line in self.song_lines:
            if isinstance(line, Note):
                notes.append(line)

        return notes

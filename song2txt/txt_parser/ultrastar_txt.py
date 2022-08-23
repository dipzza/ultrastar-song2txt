from .metadata import MetaData
from .song_line import Note


class UltraStarTXT:
    def __init__(self, metadata: MetaData, song_lines):
        self.metadata = metadata
        self.song_lines = song_lines

    def __str__(self) -> str:
        text = str(self.metadata)
        for line in self.song_lines:
            text += str(line)
        text += 'E'

        return text

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and \
               self.__dict__ == other.__dict__

    def get_notes(self):
        notes = []

        for line in self.song_lines:
            if isinstance(line, Note):
                notes.append(line)

        return notes

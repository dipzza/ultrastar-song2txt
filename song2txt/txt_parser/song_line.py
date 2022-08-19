from typing import Optional
from enum import Enum


class SongLine:
    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and \
               self.__dict__ == other.__dict__


class PlayerChange(SongLine):
    def __init__(self, player_n: int):
        self.player_n = player_n

    def __str__(self) -> str:
        return 'P{}\n'.format(self.player_n)

    def get_player_n(self):
        return self._player_n

    def set_player_n(self, player_n):
        if 1 <= player_n <= 3:
            self._player_n = player_n
        else:
            raise ValueError('Target player must be P1, P2 or P3')

    player_n = property(get_player_n, set_player_n)


class Note(SongLine):
    def __init__(self, n_type, start_beat: int,
                 length: int, pitch: int, text: str):
        self.type = n_type
        self.start_beat: int = start_beat
        self.length: int = length
        self.pitch: int = pitch
        self.text: str = text

    def __str__(self) -> str:
        return '{} {} {} {} {}\n'.format(self.type.value, self.start_beat,
                                         self.length, self.pitch, self.text)

    def get_length(self):
        return self._length

    def set_length(self, length):
        if length > 0:
            self._length = length
        else:
            raise ValueError('Note duration must be greater than 0 beats')

    length = property(get_length, set_length)


class PhraseEnd(SongLine):
    def __init__(self, start_beat, end_beat=None):
        self.start_beat: int = start_beat
        self.end_beat: Optional[int] = end_beat

    def __str__(self) -> str:
        if self.end_beat is None:
            return '- {}\n'.format(self.start_beat)
        else:
            return '- {} {}\n'.format(self.start_beat, self.end_beat)

    def get_end_beat(self):
        return self._end_beat

    def set_end_beat(self, end_beat):
        if end_beat is None or end_beat > self.start_beat:
            self._end_beat = end_beat
        else:
            raise ValueError('End beat of phrase end must '
                             'be greater than the start beat')

    end_beat = property(get_end_beat, set_end_beat)


class NoteType(Enum):
    NORMAL = ':'
    GOLDEN = '*'
    FREESTYLE = 'F'
    RAP = 'R'
    RAP_GOLDEN = 'G'

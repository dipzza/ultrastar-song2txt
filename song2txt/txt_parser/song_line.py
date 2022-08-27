from dataclasses import dataclass
from typing import Optional
from enum import Enum


class SongLine:
    pass


@dataclass(frozen=True)
class PlayerChange(SongLine):
    player_n: int

    def __post_init__(self):
        if self.player_n < 1 or self.player_n > 3:
            raise ValueError('Target player must be P1, P2 or P3')

    def __str__(self) -> str:
        return 'P{}\n'.format(self.player_n)


class NoteType(Enum):
    NORMAL = ':'
    GOLDEN = '*'
    FREESTYLE = 'F'
    RAP = 'R'
    RAP_GOLDEN = 'G'


@dataclass
class Note(SongLine):
    type: NoteType
    start_beat: int
    length: int
    pitch: int
    text: str

    def __setattr__(self, key, value):
        if key == 'length' and value <= 0:
            raise ValueError('Note duration must be greater than 0 beats')
        super().__setattr__(key, value)

    def __str__(self) -> str:
        return f'{self.type.value} {self.start_beat} ' \
               f'{self.length} {self.pitch} {self.text}\n'


@dataclass
class PhraseEnd(SongLine):
    start_beat: int
    end_beat: Optional[int] = None

    def __setattr__(self, key, value):
        if key == 'end_beat' and \
                value is not None and value <= self.start_beat:
            raise ValueError('End beat of phrase end must '
                             'be greater than the start beat')
        super().__setattr__(key, value)

    def __str__(self) -> str:
        if self.end_beat is None:
            return '- {}\n'.format(self.start_beat)
        else:
            return '- {} {}\n'.format(self.start_beat, self.end_beat)

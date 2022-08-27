from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MetaData:
    title: str
    artist: str
    mp3: str
    bpm: float
    genre: Optional[str] = None
    year: Optional[int] = None
    edition: Optional[str] = None
    creator: Optional[str] = None
    language: Optional[str] = None
    cover: Optional[str] = None
    vocals: Optional[str] = None
    video: Optional[str] = None
    background: Optional[str] = None
    relative: Optional[bool] = None
    gap: Optional[float] = None
    videogap: Optional[float] = None
    previewstart: Optional[float] = None
    duetsingerp1: Optional[str] = None
    duetsingerp2: Optional[str] = None

    def __post_init__(self):
        if self.bpm <= 0:
            raise ValueError('BPM must be greater than zero')

        if self.videogap is not None and self.videogap < 0:
            raise ValueError('Video delay can not be negative')

        if self.previewstart is not None and self.previewstart < 0:
            raise ValueError('Second for preview start can not be negative')

    def __str__(self) -> str:
        model = '#{}:{}\n'
        text = ''

        for name, value in vars(self).items():
            if value is not None:
                if isinstance(value, float) and value.is_integer():
                    value = int(value)
                elif name == 'relative':
                    value = 'YES' if value else 'NO'

                text += model.format(name.upper(), value)

        return text

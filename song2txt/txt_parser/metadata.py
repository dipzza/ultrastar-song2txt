from os import PathLike
from typing import Optional


class MetaData:

    def __init__(self):
        self.title: str = ''
        self.artist: str = ''
        self.mp3: PathLike = PathLike['']
        self.bpm: float = 100
        self.genre: Optional[str] = None
        self.year: Optional[int] = None
        self.edition: Optional[str] = None
        self.creator: Optional[str] = None
        self.language: Optional[str] = None
        self.cover: Optional[PathLike] = None
        self.vocals: Optional[PathLike] = None
        self.video: Optional[PathLike] = None
        self.background: Optional[PathLike] = None
        self.relative: Optional[bool] = None
        self.gap: Optional[float] = None
        self.video_gap: Optional[float] = None
        self.preview_start: Optional[float] = None
        self.name_singer_1: Optional[str] = None
        self.name_singer_2: Optional[str] = None
        self.extra = {}

    def __str__(self) -> str:
        model = '#{}:{}\n'

        text = model.format('TITLE', self.title)
        text += model.format('ARTIST', self.artist)
        text += model.format('MP3', self.mp3)
        text += model.format('BPM', self._float_str(self.bpm))
        if self.genre is not None:
            text += model.format('GENRE', self.genre)
        if self.year is not None:
            text += model.format('YEAR', self.year)
        if self.edition is not None:
            text += model.format('EDITION', self.edition)
        if self.creator is not None:
            text += model.format('CREATOR', self.creator)
        if self.language is not None:
            text += model.format('LANGUAGE', self.language)
        if self.cover is not None:
            text += model.format('COVER', self.cover)
        if self.vocals is not None:
            text += model.format('VOCALS', self.vocals)
        if self.video is not None:
            text += model.format('VIDEO', self.video)
        if self.background is not None:
            text += model.format('BACKGROUND', self.background)
        if self.relative is not None:
            text += model.format('RELATIVE', 'YES' if self.relative else 'NO')
        if self.gap is not None:
            text += model.format('GAP', self._float_str(self.gap))
        if self.video_gap is not None:
            text += model.format('VIDEOGAP', self._float_str(self.video_gap))
        if self.preview_start is not None:
            text += model.format('PREVIEWSTART',
                                 self._float_str(self.preview_start))
        if self.name_singer_1 is not None:
            text += model.format('DUETSINGERP1', self.name_singer_1)
        if self.name_singer_2 is not None:
            text += model.format('DUETSINGERP2', self.name_singer_2)
        for key, value in self.extra.items():
            text += model.format(key, value)

        return text

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MetaData) and self.__dict__ == other.__dict__

    @staticmethod
    def _float_str(num: float) -> str:
        if num.is_integer():
            return str(int(num))
        else:
            return str(num)

    def get_bpm(self):
        return self._bpm

    def set_bpm(self, bpm):
        if bpm > 0:
            self._bpm = bpm
        else:
            raise ValueError('BPM must be greater than zero')

    bpm = property(get_bpm, set_bpm)

    def get_video_gap(self):
        return self._video_gap

    def set_video_gap(self, video_gap):
        if video_gap is None or video_gap >= 0:
            self._video_gap = video_gap
        else:
            raise ValueError('The video delay can not be negative')

    video_gap = property(get_video_gap, set_video_gap)

    def get_preview_start(self):
        return self._preview_start

    def set_preview_start(self, preview_start):
        if preview_start is None or preview_start >= 0:
            self._preview_start = preview_start
        else:
            raise ValueError('Second for preview start can not be negative')

    preview_start = property(get_preview_start, set_preview_start)

    def add(self, key: str, value: str):
        if key == 'TITLE':
            self.title = value
        elif key == 'ARTIST':
            self.artist = value
        elif key == 'MP3':
            self.mp3 = value
        elif key == 'BPM':
            self.bpm = float(value.replace(',', '.'))
        elif key == 'GENRE':
            self.genre = value
        elif key == 'YEAR':
            self.year = int(value)
        elif key == 'EDITION':
            self.edition = value
        elif key == 'CREATOR':
            self.creator = value
        elif key == 'LANGUAGE':
            self.language = value
        elif key == 'COVER':
            self.cover = value
        elif key == 'VOCALS':
            self.vocals = value
        elif key == 'VIDEO':
            self.video = value
        elif key == 'BACKGROUND':
            self.background = value
        elif key == 'RELATIVE':
            self.relative = (value == 'YES')
        elif key == 'GAP':
            self.gap = float(value.replace(',', '.'))
        elif key == 'VIDEOGAP':
            self.video_gap = float(value.replace(',', '.'))
        elif key == 'PREVIEWSTART':
            self.preview_start = float(value.replace(',', '.'))
        elif key == 'DUETSINGERP1':
            self.name_singer_1 = value
        elif key == 'DUETSINGERP2':
            self.name_singer_2 = value
        else:
            self.extra[key] = value

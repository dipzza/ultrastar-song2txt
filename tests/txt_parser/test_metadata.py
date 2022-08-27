from dataclasses import replace

import pytest

import tests.conftest as c

BAD_BPM = 0
BAD_BPM_2 = -1
BAD_GAP = -1
BAD_PREVIEW = -1
FLOAT_INTEGER = 5.0
FLOAT_INTEGER_STR = '5'
FLOAT_NON_INTEGER = 5.5
FLOAT_NON_INTEGER_STR = '5.5'


def test_valid(metadata):
    assert metadata.artist == c.ARTIST
    assert metadata.mp3 == c.MP3
    assert metadata.bpm == c.BPM
    assert metadata.gap == c.GAP
    assert metadata.relative == c.RELATIVE


def test_bpm_invalid(metadata):
    with pytest.raises(ValueError):
        replace(metadata, bpm=BAD_BPM)
    with pytest.raises(ValueError):
        replace(metadata, bpm=BAD_BPM_2)


def test_video_gap_invalid(metadata):
    with pytest.raises(ValueError):
        replace(metadata, videogap=BAD_GAP)


def test_preview_start_invalid(metadata):
    with pytest.raises(ValueError):
        replace(metadata, previewstart=BAD_PREVIEW)


def test_str(metadata, metadata_text):
    assert str(metadata) == metadata_text

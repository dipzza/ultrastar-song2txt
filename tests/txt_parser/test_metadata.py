import pytest

from song2txt.txt_parser.metadata import MetaData

BAD_BPM = 0
BAD_BPM_2 = -1
BAD_GAP = -1
BAD_PREVIEW = -1
FLOAT_INTEGER = 5.0
FLOAT_INTEGER_STR = '5'
FLOAT_NON_INTEGER = 5.5
FLOAT_NON_INTEGER_STR = '5.5'


def test_eq_true():
    assert MetaData() == MetaData()


def test_eq_false(metadata):
    assert metadata != MetaData()


def test_str(metadata, metadata_text):
    assert str(metadata) == metadata_text


def test_bpm_invalid():
    with pytest.raises(ValueError):
        MetaData().bpm = BAD_BPM
    with pytest.raises(ValueError):
        MetaData().bpm = BAD_BPM_2


def test_video_gap_invalid():
    with pytest.raises(ValueError):
        MetaData().video_gap = BAD_GAP


def test_preview_start_invalid():
    with pytest.raises(ValueError):
        MetaData().preview_start = BAD_PREVIEW


def test_float_str_integer():
    string = MetaData._float_str(FLOAT_INTEGER)

    assert string == FLOAT_INTEGER_STR


def test_float_str_non_integer():
    string = MetaData._float_str(FLOAT_NON_INTEGER)

    assert string == FLOAT_NON_INTEGER_STR

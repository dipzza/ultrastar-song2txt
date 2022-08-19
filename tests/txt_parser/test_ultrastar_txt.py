from copy import copy

from song2txt.txt_parser.ultrastar_txt import UltraStarTXT


def test_str(us_txt, us_txt_text):
    assert str(us_txt) == us_txt_text


def test_eq_true(metadata, song_lines):
    us_txt = UltraStarTXT(metadata, song_lines)
    metadata_copy = copy(metadata)
    song_lines_copy = copy(song_lines)
    us_txt_copy = UltraStarTXT(metadata_copy, song_lines_copy)

    assert us_txt == us_txt_copy


def test_eq_false(metadata, song_lines):
    us_txt = UltraStarTXT(metadata, song_lines)
    metadata_copy = copy(metadata)
    song_lines_copy = copy(song_lines)
    us_txt_copy = UltraStarTXT(metadata_copy, song_lines_copy)
    us_txt_copy.metadata.relative = not us_txt.metadata.relative

    assert us_txt != us_txt_copy

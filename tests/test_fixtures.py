import pytest

def test_rainy_season_name(rainy_season):
    assert rainy_season.english_name() == "Rainy"

def test_rainy_season_uposatha_count(rainy_season):
    assert rainy_season.uposatha_count == 8

def test_uposatha_lengths(uposatha_lengths):
    assert uposatha_lengths == [15, 15, 14, 15, 15, 15, 14, 15]


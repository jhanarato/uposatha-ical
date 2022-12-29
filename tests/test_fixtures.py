import pytest

def test_rainy_season_name(rainy_season):
    assert rainy_season.english_name() == "Rainy"

def test_rainy_season_uposatha_count(rainy_season):
    assert rainy_season.uposatha_count == 8




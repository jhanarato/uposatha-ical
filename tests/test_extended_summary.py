from forest_sangha_moons.MahanikayaCalendar import ExtendedSummary

full = ExtendedSummary("Full Moon - 15 day Hemanta 6/8")
new = ExtendedSummary("New Moon - 14 day Gimha 3/10")

def test_days_in_fortnight():
    assert full.uposatha_days() == 15
    assert new.uposatha_days() == 14
    # TODO: Check exceptions

def test_season_name():
    assert full.season_name() == "Hemanta"
    assert new.season_name() == "Gimha"

def test_uposatha_number():
    assert full.uposatha_of_season() == 6
    assert new.uposatha_of_season() == 3

def test_uposatha_in_season():
    assert full.uposathas_in_season() == 8
    assert new.uposathas_in_season() == 10

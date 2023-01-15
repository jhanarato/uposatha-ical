def add_date_before(seasons, date_before_first_season):
    season_iter = iter(seasons)
    season = next(season_iter)
    season.date_before = date_before_first_season

    for next_season in season_iter:
        date_before = season.uposathas[-1].date
        next_season.date_before = date_before
        season = next_season


def start_date(calendar):
    return calendar.seasons[0].events[-1].date

def get_seasons(calendar):
    return calendar.seasons[1:-1]

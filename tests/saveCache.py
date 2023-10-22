import sys
import pickle

path = '../src'
sys.path.append(path)
import nfl

years = ['2020','2021','2022']

for year in years:
    s = nfl.season(year)
    s.getSchedule(1,18)
    games = []
    winners = []
    scores = []
    for week in s.weeks:
        for game in week.games:
            games.append(game)
        for winner in week.winners:
            winners.append(winner)
        for score in week.scores:
            scores.append(score)
    cache = {'games'  : games,
            'winners' : winners,
            'scores'  : scores}

    file = '../.cache/season' + year + '.cache'
    with open(file,'wb+') as out:
        pickle.dump(cache,out)
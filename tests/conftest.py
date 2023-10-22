import pytest
import pickle

import sys
path = '../src'
sys.path.append(path)
import nfl

@pytest.fixture(scope='session')
def loadCache():
    print('Getting cache...')
    cache = {}
    for year in ['2020','2021','2022']:
        file = '../.cache/season' + year + '.cache'
        with open(file,'rb') as inp:
            cache[year] = pickle.load(inp)
    print('Done!')
    return cache

@pytest.fixture(scope='session')
def loadObject():
    print('Getting objects...')
    obj = {}
    for year in ['2020','2021','2022']:
        obj[year] = nfl.season(year)
        obj[year].getSchedule(1,18)
    print('Done!')
    return obj
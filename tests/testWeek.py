import pytest

path = 'src'
import sys
sys.path.append(path)
from nfl import week

class weekGames(week):
    def __init__(self,weekN,data):
        self.weekN = weekN
        self.games = []
        self.setGames(data)

class weekWinners(week):
    def __init__(self,weekN,data):
        self.weekN = weekN
        self.games = data
        self.winners = []
        self.setWinners()

# class weekScores(week):
#     def __init__(self,weekN,data):
#         self.weekN = weekN
#         self.scores = []
#         self.setScores()

class testSetGames:
    @pytest.fixture(scope='class')
    def setup(dataType):
        def _method(dataType):
            if dataType == 'games':
                data = {}
                data['events'] = ['this','is','some','test','data']
                return data
            elif dataType == 'winners':
                data = [{}]
                data[0]['winner'] = ["GB"]
                data[0]['competitions'] = [{}]
                data[0]['competitions'][0]['competitors'] = [{'team':{}},{'team':{}}]
                data[0]['competitions'][0]['competitors'][0]['winner'] = True
                data[0]['competitions'][0]['competitors'][1]['winner'] = False
                data[0]['competitions'][0]['competitors'][0]['team']['abbreviation'] = data[0]['winner'][0]
                data[0]['competitions'][0]['competitors'][1]['team']['abbreviation'] = "CHI"
                return data
            elif dataType == 'scores':
                data = 2
                return data
            else:
                raise ValueError('Invalid dataType')
        return _method

    def testSetGames(self,setup):
        data = setup('games')
        for weekN in range(1,19):
            currentWeek = weekGames(weekN,data)
            for actual,expected in zip(currentWeek.games,data['events']):
                assert actual == expected

    def testSetWinners(self,setup):
        data = setup('winners')
        for weekN in range(1,19):
            currentWeek = weekWinners(weekN,data)
            for actual,expected in zip(currentWeek.winners,data[0]['winner']):
                assert actual == expected

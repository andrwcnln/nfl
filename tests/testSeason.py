import pytest
import requests


@pytest.mark.parametrize("year", ["2020", "2021", "2022"])
class testSeason:
    @pytest.fixture(autouse=True)
    def setup(self, loadCache, loadObject):
        self.cache = loadCache
        self.obj = loadObject

        # def testGames(self,year):
        # expected = self.cache[year]
        # actual = self.obj[year]

        # expectedCounter = 0
        # for weekActual in actual.weeks:
        # for gameActual in weekActual.games:
        # assert gameActual == expected['games'][expectedCounter]
        # expectedCounter += 1

    def testWinners(self, year):
        expected = self.cache[year]
        actual = self.obj[year]

        expectedCounter = 0
        for weekActual in actual.weeks:
            for winnerActual in weekActual.winners:
                assert winnerActual == expected["winners"][expectedCounter]
                expectedCounter += 1

    def testScores(self, year):
        expected = self.cache[year]
        actual = self.obj[year]

        expectedCounter = 0
        for weekActual in actual.weeks:
            for scoreActual in weekActual.scores:
                assert scoreActual == expected["scores"][expectedCounter]
                expectedCounter += 1

    def testAPIResponse(self, year):
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={year}&seasontype=2&week=1"
        resp = requests.get(url)
        assert resp.status_code == 200

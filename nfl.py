""" 
A set of classes for getting data about an NFL season

Author: Andrew Conlin
Last updated: 22nd Sep 2023 
Version: 0.1
"""

import requests
import json
import dotenv

# Season object, containing all of the information on a current season
# Properties:
# - year: year of the season, needed to initialise the object
# - weeks: array containing information on each week. This is stored in 'week' objects
# Methods:
# - getSchedule(weekStart, weekEnd): get the schedule for the current year (from ESPN). 
#       weekStart and weekEnd define the range of weeks to generate a schedule for. 
#       Will overwrite the exisiting schedule if called again.
class season:
    def __init__(self, year):
        self.year = year
        self.weeks = []

    def __str__(self):
        return f"A season object for the {self.year} NFL season"

    def getSchedule(self, weekStart, weekEnd):
        self.weeks = []
        for weekN in range(weekStart,weekEnd+1):
            print(f"Fetching data for week {weekN}")
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?season.year={self.year}&season.type=2&week={weekN}"
            
            print(f"--->    Parsing data for week {weekN}")
            data = requests.get(url).json()
            # print(data['content']['schedule'])

            currentWeek = week(weekN)
            currentWeek.setGames(data)

            self.weeks.append(currentWeek)

    def getScores(self,weekN):
        pass

# Week object, containing all information on a current week
# Properties:
# - weekN: week number
# Methods
# - setGames: set the games for this week 
class week:
    def __init__(self, weekN):
        self.weekN = weekN
        self.games = []
        # self.rawData = data
        # self.jsonData = self.rawData.json()
        # self.parsedData = json.load(self.jsonData)

    def __str__(self):
        return f"Week {self.weekN}"

    def setGames(self,data):
        games = data['events']
        for game in games:
            self.games.append(game)

    # Internal methods
    def extractKeys(self,dict):
        return list(dict.keys())





# test = season('2023')
# print(test)

# test.getSchedule(3,3)
# print(test.weeks[0].weekN)
# print(test.weeks[0].games[0]['shortName'])
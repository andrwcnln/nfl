""" 
A set of classes for getting data about an NFL season

Author: Andrew Conlin
Last updated: 19th Oct 2023 
Version: 0.5.4
"""

import requests
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
from dotenv import load_dotenv

load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/forms.body"]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

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
        # a method to get all the information on a season, between the given weeks
        self.weeks = []
        for weekN in range(weekStart,weekEnd+1):
            print(f"--> Fetching data for week {weekN}")
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?season.year={self.year}&season.type=2&week={weekN}"
            data = requests.get(url).json()

            currentWeek = week(weekN,data)

            self.weeks.append(currentWeek)

    def printGames(self, weekStart, weekEnd):
        # a method to print the games for a given set of weeks
        for weekN in range(weekStart-1,weekEnd):
            print(self.weeks[weekN])
            print(' ')
            self.weeks[weekN].printGames()
            print(' ')

    def printWinners(self, weekStart, weekEnd):
        # a method to print the winners for a given set of weeks
        for weekN in range(weekStart-1,weekEnd):
            print(self.weeks[weekN])
            print(' ')
            self.weeks[weekN].printWinners()
            print(' ')

    def updateGames(self):
        # a method to update the games in the remote spreadsheet
        creds = self.googleAuth()

        try:
            service = build('sheets', 'v4', credentials=creds)
            values = [[],[],[]]
            for week in self.weeks:
                for game in week.games:
                    values[0].append(week.weekN)
                    values[1].append(game['shortName'])
                    values[2].append("winner")

            print(values)
            body = {
                'majorDimension': 'COLUMNS',
                'values': values
            }
            result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range="Prototype (data)!A1:3",
            valueInputOption="USER_ENTERED", body=body).execute()
            print(f"{result.get('updatedCells')} cells updated.")

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def updateWinners(self,weekN):
        # a method to update the scores in the remote spreadsheet
        pass

    # internal methods
    def googleAuth(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return creds


# Week object, containing all information on a relevant week
# Properties:
# - weekN: week number
# - data: ESPN game data
# Methods
# - setGames: set the games property for this object
# - setWinners: set the winners property for this object
class week:
    def __init__(self, weekN, data):
        self.weekN = weekN
        self.games = []
        self.setGames(data)
        self.winners = []
        self.setWinners()
        self.scores = []
        self.setScores()

    def __str__(self):
        return f"Week {self.weekN}"

    def setGames(self,data):
        # a method to populate the games property with the games from the data
        games = data['events']
        for game in games:
            self.games.append(game)

    def printGames(self):
        # a method to iterate through and print the games
        for game in self.games:
            print(game['shortName'])

    def setWinners(self):
        # a method to find the winners of games and set the corresponding winners property
        for game in self.games:
            home = game['competitions'][0]['competitors'][0]
            away = game['competitions'][0]['competitors'][1]
            try:
                if home['winner']:
                    self.winners.append(game['competitions'][0]['competitors'][0]['team']['abbreviation'])
                elif away['winner']:
                    self.winners.append(game['competitions'][0]['competitors'][1]['team']['abbreviation'])
                else:
                    self.winners.append('TIE')
            except KeyError:
                self.winners.append('N/A')

    def setScores(self):
        # a method to find the winners of games and set the corresponding winners property
        for game in self.games:
            try:
                home = game['competitions'][0]['competitors'][0]['score']
                away = game['competitions'][0]['competitors'][1]['score']
            except KeyError:
                home = 0
                away = 0
            self.scores.append(away + ' - ' + home)

    def printWinners(self):
        # a method to iterate through and print the winners
        for winner in self.winners:
            print(winner)

    # Internal methods
    def extractKeys(self,dict):
        return list(dict.keys())

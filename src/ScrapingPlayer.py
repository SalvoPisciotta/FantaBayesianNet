import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# url_tm stands for the transfermarkt italian data page address
#url_tm = "https://www.transfermarkt.it/luis-muriel/leistungsdaten/spieler/119228/saison/2020/plus/1#CL"

# url_fg stands for the fantagiaveno data page address
#url_fg = "http://www.fantagiaveno.it/calciatori.asp?id=945"


class ScrapingPlayer:

    # table header transfermarket
    table_structure_tm = {
        "matchday" : 0,
        "date" : 1,
        "home_team_pos": 2,
        "home_team" : 3,
        "away_team_pos" : 4,
        "away_team" : 5,
        "result" : 6,
        "available" : 7,
        "goal" : 8,
        "assist" : 9,
        "autogoal" : 10,
        "yellow_card" : 11,
        "double_yellow_card" : 12,
        "red_card" : 13,
        "substitution_on" : 14,
        "substitution_off" : 15,
        "minutes" : 16
    }

    # table header fantagiaveno
    table_structure_fg = {
        "matchday": 0,
        "play_home": 1,
        "score": 2,
        "grade": 3,
        "penalty_scored": None,
        "penalty_kick": 9,
        "starter": 10,
        "postponed": None
    }

    # rank at end of first round
    rank_difficulty = {
        "Milan" : 1,
        "Inter" : 1,
        "Juventus": 1,
        "Roma": 2,
        "Atalanta" : 2,
        "Napoli" : 2,
        "Lazio" : 2,
        "Verona": 3,
        "Sassuolo" : 3,
        "Sampdoria" : 3,
        "Benevento": 4,
        "Fiorentina": 4,
        "Bologna" : 4,
        "Spezia": 4,
        "Udinese" : 4,
        "Genoa" : 5,
        "Cagliari": 5,
        "Torino" : 5,
        "Parma" : 5,
        "Crotone" : 5
    }

    def __init__(self,
                 url_tm,
                 url_fg):
        self.url_tm = url_tm
        self.url_fg = url_fg


    def readRowTm(self, row, table_structure=table_structure_tm):

        # Fill a list with each cell contained into a row
        cells = row.find_all("td")
        cells = list(map(lambda x: x.text.strip(), cells))

        # Ignore empty rows
        if len(cells) == 0:
            return None

        else:
            matchday = int(cells[table_structure["matchday"]])
            date = cells[table_structure["date"]]
            home_team_raw = cells[table_structure["home_team"]]
            away_team_raw = cells[table_structure["away_team"]]
            try:
                home_team_name, home_team_pos = home_team_raw.split("\xa0\xa0")
                home_team_pos = int(home_team_pos[1:-2])
                away_team_name, away_team_pos = away_team_raw.split("\xa0\xa0")
                away_team_pos = int(away_team_pos[1:-2])
            except ValueError:
                home_team_name = home_team_raw
                home_team_pos = None
                away_team_name = away_team_raw
                away_team_pos = None

            result = cells[table_structure["result"]]

            # If a row contains less cells than the overall table structure, means that player in unavailable
            if len(cells) < len(table_structure):
                available = cells[table_structure["available"]]
                return [matchday, date, home_team_pos, home_team_name, away_team_pos, away_team_name, result, available,
                        0, 0, 0, False, False, False, '', '', 0]
            else:
                available = 'Available'
                goal = 0 if cells[table_structure["goal"]] == '' else int(cells[table_structure["goal"]])
                assist = 0 if cells[table_structure["assist"]] == '' else int(cells[table_structure["assist"]])
                autogoal = 0 if cells[table_structure["autogoal"]] == '' else int(cells[table_structure["autogoal"]])
                yellow_card = False if cells[table_structure["yellow_card"]] == '' else True
                double_yellow_card = False if cells[table_structure["double_yellow_card"]] == '' else True
                red_card = False if cells[table_structure["red_card"]] == '' else True
                substitution_on = cells[table_structure["substitution_on"]][:-1]
                substitution_off = cells[table_structure["substitution_off"]][:-1]
                minutes = int(cells[table_structure["minutes"]][:-1])

                return [matchday, date, home_team_pos, home_team_name, away_team_pos, away_team_name,  result, available,
                        goal, assist, autogoal, yellow_card, double_yellow_card, red_card, substitution_on,
                        substitution_off, minutes]



    def readRowFg(self, row, table_structure=table_structure_fg):
        # Fill a list with each cell contained into a row
        cells = row.find_all("td")
        cells = list(map(lambda x: x.text.strip(), cells))

        # Ignore empty rows
        if len(cells) == 0:
            return None

        else:

            postponed = False
            # Match day without final letter
            matchday = int(cells[table_structure["matchday"]][:-1])

            # C/T became True is is C, otherwise False
            play_home = True if cells[table_structure["play_home"]] == "c" else False

            # Scores considering - as NaN scores
            scores = cells[table_structure["score"]].strip()
            if scores == "-":
                scores = np.nan
            elif scores[-1] == "*":
                scores = float(scores[:-1].strip())
                postponed = True
            else:
                scores = float(scores.replace(",", "."))

            # Grade considering - as NaN
            grade = cells[table_structure["grade"]].strip()
            if grade == "-":
                grade = np.nan
            else:
                grade = float(grade.replace(",", "."))

            # Penalty, 0 whether penalty is -
            penalty = cells[table_structure["penalty_kick"]].strip()
            penalty_scored, penalty_kick = penalty.split("/")
            if penalty_scored.strip() == "-":
                penalty_scored = 0
            else:
                penalty_scored = int(penalty_scored.strip())
            if penalty_kick.strip() == "-":
                penalty_kick = 0
            else:
                penalty_kick = int(penalty_kick.strip())

            # Starter is considered as a boolean variable
            starter_str = cells[table_structure["starter"]].strip()
            if starter_str == "x":
                starter = True
            else:
                starter = False

            return [matchday, play_home, scores, grade, penalty_scored, penalty_kick, starter, postponed]



    def getData(self):


        """
        To make the request to the page we have to inform the
        website that we are a browser and that is why we
        use the headers variable
        """
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


        # ------------------------------------------------------------------------#
        #------------------- START SCRAPING TRANSFERMARKET -----------------------#
        # ------------------------------------------------------------------------#

        # In the response variable we will the download of the web page
        response_tm = requests.get(self.url_tm, headers=headers)

        """
        Now we will create a BeautifulSoup object from our response.
        The 'html.parser' parameter represents which parser we will use when creating our object,
        a parser is a software responsible for converting an entry to a data structure.
        """
        page_bs_tm = BeautifulSoup(response_tm.content, 'html.parser')


        # find name of the player
        player_name = page_bs_tm.find("div", class_="dataName").find("b").text
        #print(player_name)

        serie_a_table_tm = None

        # The find_all () method is able to return all tags that meet restrictions within parentheses
        # The find() function will find the first table whose class is "responsive-table"
        for box in page_bs_tm.find_all("div", class_="box"):
            if box.find("a", {"name":"IT1"}) != None:
                serie_a_table_tm = box.find("div", class_="responsive-table").find("tbody").find_all("tr")

        # Creating a DataFrame with our data
        df_tm = pd.DataFrame(columns=self.table_structure_tm.keys())
        i = 0

        for row in serie_a_table_tm:
            # Now we will receive all the cells in the table with their values
            statistics = self.readRowTm(row)
            df_tm.loc[i] = statistics
            i+=1


        # Printing our gathered data
        #print(df_tm)


        # ------------------------------------------------------------------------#
        #------------------- START SCRAPING FANTAGIAVENO -------------------------#
        # ------------------------------------------------------------------------#

        # In the response variable we will the download of the web page
        response_fg = requests.get(self.url_fg, headers=headers)

        """
        Now we will create a BeautifulSoup object from our response.
        The 'html.parser' parameter represents which parser we will use when creating our object,
        a parser is a software responsible for converting an entry to a data structure.
        """
        page_bs_fg = BeautifulSoup(response_fg.content, 'html.parser')

        # extract all table
        tables_fg = page_bs_fg.find_all("table", class_="Border")

        # Finding the right table tahta we want to observe and extract all rows of the table
        right_table_fg = 7
        result_table_fg = tables_fg[right_table_fg].find("tbody").find_all("tr")

        # Creating a DataFrame with our data
        df_fg = pd.DataFrame(columns=self.table_structure_fg.keys())
        i = 0

        for row in result_table_fg:
            # Now we will receive all the cells in the table with their values
            statistics = self.readRowFg(row)
            df_fg.loc[i] = statistics
            i+=1

        # Printing our gathered data
        # print(df_fg)


        # ------------------------------------------------------------------------#
        #------------------------- MERGE AND EDIT DATA ---------------------------#
        # ------------------------------------------------------------------------#

        df_result = pd.merge(df_tm, df_fg, on='matchday', how='inner')


        # compute difficulty index in a range [1,5]
        c = df_result['play_home'].apply(lambda x: 0 if x else 1)

        home_team_rank = df_result['home_team'].map(self.rank_difficulty)
        away_team_rank = df_result['away_team'].map(self.rank_difficulty)

        player_team_rank = home_team_rank[df_result["play_home"]].append(away_team_rank[~df_result["play_home"].astype(bool)]).sort_index()
        opponent_team_rank = home_team_rank[~df_result["play_home"].astype(bool)].append(away_team_rank[df_result["play_home"]]).sort_index()


        df_result["difficulty_match"] = round((5 + player_team_rank - opponent_team_rank + c + 0.1)/2).astype(int)

        # Save as csv
        #df_result.to_csv('../data/stats_'+player_name.lower()+'.csv', index=False)

        return player_name.lower(), df_result



class Player:

    def __init__(self, id, score):
        self.id = id
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

    def getId(self):
        return self.id

    def getScore(self):
        return self.score

    def __str__(self):
        return "\t"+str(self.score)+" ("+str(self.id)+")"

    def __repr__(self):
        return str(self)


from json import JSONEncoder
# subclass JSONEncoder
class PlayerEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

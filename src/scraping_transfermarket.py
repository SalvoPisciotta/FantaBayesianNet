import requests
from bs4 import BeautifulSoup
import pandas as pd


def readRow(row, table_structure):

    # Fill a list with each cell contained into a row
    cells = row.find_all("td")
    cells = list(map(lambda x: x.text.strip(), cells))

    # Ignore empty rows
    if len(cells) == 0:
        return None

    else:
        matchday = cells[table_structure["matchday"]]
        date = cells[table_structure["date"]]
        home_team_raw = cells[table_structure["home_team"]]
        home_team_name, home_team_pos = home_team_raw.split("\xa0\xa0")
        home_team_pos = int(home_team_pos[1:-2])
        away_team_raw = cells[table_structure["away_team"]]
        away_team_name, away_team_pos = away_team_raw.split("\xa0\xa0")
        away_team_pos = int(away_team_pos[1:-2])
        result = cells[table_structure["result"]]

        # If a row contains less cells than the overall table structure, means that player in unavailable
        if len(cells) < len(table_structure):
            unavailable = cells[table_structure["unavailable"]]
            return [matchday, date, home_team_pos, home_team_name, away_team_pos, away_team_name, result, unavailable,
                    0, 0, 0, False, False, False, '', '', 0]
        else:
            unavailable = 'Available'
            goal = 0 if cells[table_structure["goal"]] == '' else int(cells[table_structure["goal"]])
            assist = 0 if cells[table_structure["assist"]] == '' else int(cells[table_structure["assist"]])
            autogoal = 0 if cells[table_structure["autogoal"]] == '' else int(cells[table_structure["autogoal"]])
            yellow_card = False if cells[table_structure["yellow_card"]] == '' else True
            double_yellow_card = False if cells[table_structure["double_yellow_card"]] == '' else True
            red_card = False if cells[table_structure["red_card"]] == '' else True
            substitution_on = cells[table_structure["substitution_on"]][:-1]
            substitution_off = cells[table_structure["substitution_off"]][:-1]
            minutes = int(cells[table_structure["minutes"]][:-1])

            return [matchday, date, home_team_pos, home_team_name, away_team_pos, away_team_name,  result, unavailable,
                    goal, assist, autogoal, yellow_card, double_yellow_card, red_card, substitution_on,
                    substitution_off, minutes]


# table header
table_structure = {
    "matchday" : 0,
    "date" : 1,
    "home_team_pos": 2,
    "home_team" : 3,
    "away_team_pos" : 4,
    "away_team" : 5,
    "result" : 6,
    "unavailable" : 7,
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



"""
To make the request to the page we have to inform the
website that we are a browser and that is why we
use the headers variable
"""
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# url stands for the data page address
url = "https://www.transfermarkt.com/ciro-immobile/leistungsdaten/spieler/105521/saison/2020/plus/1#IT1"

# In the response variable we will the download of the web page
response = requests.get(url, headers=headers)

"""
Now we will create a BeautifulSoup object from our response.
The 'html.parser' parameter represents which parser we will use when creating our object,
a parser is a software responsible for converting an entry to a data structure.
"""
page_bs = BeautifulSoup(response.content, 'html.parser')

serie_a_table = None

# The find_all () method is able to return all tags that meet restrictions within parentheses
# The find() function will find the first table whose class is "responsive-table"
for box in page_bs.find_all("div", class_="box"):
    if box.find("a", {"name":"IT1"}) != None:
        serie_a_table = box.find("div", class_="responsive-table").find("tbody").find_all("tr")

# Creating a DataFrame with our data
df = pd.DataFrame(columns=table_structure.keys())
i = 0

for row in serie_a_table:
    # Now we will receive all the cells in the table with their values
    statistics = readRow(row, table_structure)
    df.loc[i] = statistics
    i+=1


# Printing our gathered data
print(df)

# Save as csv
df.to_csv('../data/out_transfermarket.csv', index=False)

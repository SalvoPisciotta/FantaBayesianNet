from ScrapingPlayer import ScrapingPlayer
from ScrapingPlayer import Player
import pandas as pd
import numpy as np
import json

# -------------------------------------------------------------------------------------------- #
# --------------------- READ URLs to GET DATA for 40 FOOTBALL PLAYERS ------------------------ #
# -------------------------------------------------------------------------------------------- #

urlTmPlayers = list()
urlFgPlayers = list()
namePlayers = list()
statsPlayers = list()

# collect data up to this matchday
up_to_matchday = 30

# read json of urls
with open('../data/players.json') as f:
  players_data = json.load(f)

# extract urls
for team in players_data['teams']:
    for player in team['forwards']:
        urlTmPlayers.append(player['url_tm'])
        urlFgPlayers.append(player['url_fg'])

print("Scraping data from {} football players:".format(len(urlTmPlayers)))


# get raw data for each player
for i in range(len(urlTmPlayers)):

    player = ScrapingPlayer(urlTmPlayers[i], urlFgPlayers[i])
    namePlayer, statsPlayer = player.getData(up_to_matchday)
    namePlayer = namePlayer.replace(" ", "_")

    print("- {} data achieved".format(namePlayer))

    namePlayers.append(namePlayer)
    statsPlayers.append(statsPlayer.sort_values(by=['matchday']))



# -------------------------------------------------------------------------------------------- #
# --------------------------------------- PREPROCESSING -------------------------------------- #
# -------------------------------------------------------------------------------------------- #

# compute deployability setting it True for at most 33% of players in each matchday, otherwise False

# build a dict containing scores in each matchday that are not 'sv' and are at least 6
gradesMatchday = dict.fromkeys(range(1, max(statsPlayers[0]['matchday'])+1), [])
for i in range(len(statsPlayers)):
    for matchday, score, difficulty_match in zip(statsPlayers[i]['matchday'], statsPlayers[i]['score'], statsPlayers[i]['difficulty_match']):
        if score >= 6 and np.isnan(score)==False:
            # slight variation of score to make deployability also dependent by difficulty_match
            score = score + 0.25 if difficulty_match < 3 else score
            score = score - 0.25 if difficulty_match > 3 else score
            gradesMatchday[matchday] = gradesMatchday[matchday] + [Player(i,score)]

# order each list of scores in decreasing way and take at most 3 values
maxDeployable = int(len(urlTmPlayers)/3)
for matchday, values in gradesMatchday.items():
    values.sort(reverse=True)
    if len(values) > maxDeployable:
        del values[maxDeployable:]

# compute deployability for each player
for i in range(len(statsPlayers)):
    deployability = list()
    for matchday in statsPlayers[i]['matchday']:
        if Player(i,None) in gradesMatchday[matchday]:
            deployability.append(True)
        else:
            deployability.append(False)
    statsPlayers[i]['deployability'] = deployability


# save only needed stats into a csv
for namePlayer, statPlayer in zip(namePlayers, statsPlayers):
       statPlayer.to_csv('../data/stats_'+namePlayer+'.csv', index=False)

print("Preprocessing ended, see data on /data folder.")
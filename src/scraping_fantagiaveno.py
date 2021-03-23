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
        
        len_escape_ch = 6
        
        postponed = False
        # Match day without final letter
        matchday = cells[table_structure["matchday"]][:-1]
        # Points considering - as 0 points
        points = cells[table_structure["points"]][:-len_escape_ch].strip()
        if points == "-":
            points = None
        elif points[-1] == "*":
            points = points[:-1].strip()
            postponed = True
        # Grade considering - as 0
        grade = cells[table_structure["grade"]][:-len_escape_ch].strip()
        if grade == "-":
            grade = None
        # Goals, 0 whether goals is -
        goals = cells[table_structure["goals"]]
        if goals == "-":
            goals = "0"
        # Titolarity is considered as a boolean variable
        titolarity_str = cells[table_structure["titolarity"]][:-len_escape_ch]
        if titolarity_str == "x":
            titolarity = True
        else:
            titolarity = False
        

        return [matchday,points,grade,goals,titolarity,postponed]


# table header
table_structure = {
    "matchday" : 0,
    "points": 2,
    "grade": 3,
    "goals": 4,
    "titolarity": 10,
    "postponed": None
}



"""
To make the request to the page we have to inform the
website that we are a browser and that is why we
use the headers variable
"""
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# url stands for the data page address
url = "http://www.fantagiaveno.it/calciatori.asp?id=929"

# In the response variable we will the download of the web page
response = requests.get(url, headers=headers)

"""
Now we will create a BeautifulSoup object from our response.
The 'html.parser' parameter represents which parser we will use when creating our object,
a parser is a software responsible for converting an entry to a data structure.
"""
page_bs = BeautifulSoup(response.content, 'html.parser')

# Finding all rows of the table
main_table = page_bs.find("table", class_="TabellaMain")
results_table = main_table.find_all("table", class_="Border")
print(results_table)

# Creating a DataFrame with our data
df = pd.DataFrame(columns=table_structure.keys())
i = 0

for row in results_table:
    # Now we will receive all the cells in the table with their values
    statistics = readRow(row, table_structure)
    df.loc[i] = statistics
    i+=1


# Printing our gathered data
print(df)

# Save as csv
df.to_csv('../data/out_fantagiaveno.csv', index=False)

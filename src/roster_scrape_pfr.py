from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import sys 
import re
import requests

def roster_scrape(csv_file, team_csv_file):
    """ Grabs all the salary data from spotrac.com/nfl/
    Submits the data to the inputted CSV file"""
    team_map = {}
    with open(team_csv_file, 'r', encoding='utf-8') as teamfile:
        csv_reader = csv.reader(teamfile)
        next(csv_reader, None)
        for row in csv_reader:
            team_id = row[0]
            team_abbr = row[2]
            team_map[team_abbr] = team_id

    url = "http://www.pro-football-reference.com/teams/{team}/{year}_roster.htm"
    with open(csv_file, 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['year', 'team', 'player', 'url', 'age', 'position', 'games_played', 'games_started', \
                'weight', 'height', 'college', 'birthdate', 'experience', 'av'])
        for year in range(1978, 2017):
            duplicate_set = set()
            for team in team_map:
                print (str(year) + " " + team)
                sys.stdout.flush() # make sure number is printed out in real time
                new_url = url.format(team = team, year = year)
                pageScrape(new_url, year, team_map[team], wr, duplicate_set)

def pageScrape(url, year, team, wr, duplicate_set):
    """ Takes in a URL to a page of salary data"""

    r = requests.get(url)
    content = re.sub(r'(?m)^\<!--.*\n?', '', r.content.decode('utf-8'))
    content = re.sub(r'(?m)^\-->.*\n?', '', content)
    soup = BeautifulSoup(content, 'html.parser')
    
    error = soup.find('h1')
    if error is not None and error.string == "Page Not Found (404 error)":
        return

    tables = soup.find_all('table')

    table = None
    table_body = None
    table_rows = None

    try:
        table = tables[1]
    except:
        table = tables[0]
        print("CAUGHT")

    if table is not None:
        table_body = table.find('tbody')

    if table_body is not None:
        table_rows = table_body.findAll("tr")

    if table_rows is not None:
        for elem in table_rows:
            desired_row = []
            vals = elem.findAll('td')

            player = vals[0].a.string
            url = vals[0].a['href']
            age = vals[1].string
            position = vals[2].string
            games_played = vals[3].string
            games_started = vals[4].string
            weight = vals[5].string

            height = ''
            if vals[6].string is not None:
                height = '\'' + vals[6].string

            college = vals[7].string
            birthdate = vals[8].string
            experience = vals[9].string
            av = vals[10].string

            player_tuple = (year, team, player, url, age, position, games_played, games_started, \
                weight, height, college, birthdate, experience, av)

            if player_tuple not in duplicate_set:
                duplicate_set.add(player_tuple)
                desired_row.extend(player_tuple)
                wr.writerow(desired_row)

        soup.decompose()

if __name__ == '__main__':
    roster_csv_file = "../data/roster_data_pfr.csv"
    team_csv_file = "../data/team_data_roster_scraping_pfr.csv"
    roster_scrape(roster_csv_file, team_csv_file)
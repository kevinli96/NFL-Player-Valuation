from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import sys 

def roster_scrape(csv_file, team_csv_file):
    """ Grabs all the salary data from spotrac.com/nfl/
    Submits the data to the inputted CSV file"""
    team_map = {}
    with open(team_csv_file, 'r', encoding='utf-8') as teamfile:
        csv_reader = csv.reader(teamfile)
        next(csv_reader, None)
        for row in csv_reader:
            team_id = row[0]
            team_name = row[1]
            team_name_joined = '-'.join(team_name.lower().split(' '))
            team_map[team_name_joined] = team_id

    url = "http://www.footballdb.com/teams/nfl/{team}/roster/{year}/"
    with open(csv_file, 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['year','team','player','position','birthdate','college'])
        for year in range(1978, 2017):
            duplicate_set = set()
            for team in team_map:
                print (str(year) + " " + team)
                sys.stdout.flush() # make sure number is printed out in real time
                new_url = url.format(team = team, year = year)
                pageScrape(new_url, year, team_map[team], wr, duplicate_set)

def pageScrape(url, year, team, wr, duplicate_set):
    """ Takes in a URL to a page of salary data"""

    try:
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        table = soup.find('table')
        table_body = None
        table_rows = None

        if table is not None:
            table_body = table.find('tbody')

        if table_body is not None:
            table_rows = table_body.findAll("tr")

        if table_rows is not None:
            for elem in table_rows:
                desired_row = []
                vals = elem.findAll('td')

                player = vals[1].a.string
                position = vals[2].string
                birthdate = vals[5].string
                college = vals[6].string

                player_tuple = (year, team, player, position, birthdate, college)

                if player_tuple not in duplicate_set:
                    duplicate_set.add(player_tuple)
                    desired_row.extend(player_tuple)
                    wr.writerow(desired_row)

            soup.decompose()
    except:
        print("caught: " + team + " " + str(year))

if __name__ == '__main__':
    roster_csv_file = "../data/roster_data.csv"
    team_csv_file = "../data/team_data_roster_scraping.csv"
    roster_scrape(roster_csv_file, team_csv_file)
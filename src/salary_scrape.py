from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import sys 

def salary_scrape(csv_file, team_csv_file):
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

    url = "http://www.spotrac.com/nfl/{team}/cap/{year}/"
    with open(csv_file, 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['year','team','player','position','base_salary','signing_bonus','roster_bonus','option_bonus','workout_bonus','restructured_bonus','dead_cap','cap_hit','cap_percentage'])
        for year in range(1994, 2022):
            duplicate_set = set()
            for team in team_map:
                print (str(year) + " " + team)
                sys.stdout.flush() # make sure number is printed out in real time
                new_url = url.format(team = team, year = year)
                pageScrape(new_url, year, team_map[team], wr, duplicate_set)

def pageScrape(url, year, team, wr, duplicate_set):
    """ Takes in a URL to a page of salary data"""

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
            player = vals[0].a.string
            position = vals[1].span.string

            base_salary = 0
            if vals[2].span.string is not None and vals[2].span.string != '-':
                base_salary = int(vals[2].span.string.replace('$','').replace(',',''))

            signing_bonus = 0
            if vals[3].span.string is not None and vals[3].span.string != '-':
                signing_bonus = int(vals[3].span.string.replace('$','').replace(',',''))

            roster_bonus = 0
            if vals[4].span.string is not None and vals[4].span.string != '-':
                roster_bonus = int(vals[4].span.string.replace('$','').replace(',',''))

            option_bonus = 0
            if vals[5].span.string is not None and vals[5].span.string != '-':
                option_bonus = int(vals[5].span.string.replace('$','').replace(',',''))

            workout_bonus = 0
            if vals[6].span.string is not None and vals[6].span.string != '-':
                workout_bonus = int(vals[6].span.string.replace('$','').replace(',',''))

            restructured_bonus = 0
            if vals[7].span.string is not None and vals[7].span.string != '-':
                restructured_bonus = int(vals[7].span.string.replace('$','').replace(',',''))

            dead_cap = 0
            if vals[9].a is not None and vals[9].a.string != '-':
                if vals[9].a.string is not None:
                    dead_cap = int(vals[9].a.string.replace('$','').replace(',','').replace('(','').replace(')',''))

            cap_hit = 0
            if vals[10].span.string is not None and '-' not in vals[10].span.string:
                cap_hit = int(vals[10].span.string.replace('$','').replace(',',''))

            cap_percentage = 0.0
            if vals[11].string is not None and vals[11].string != '-':
                cap_percentage = float(vals[11].string)

            player_tuple = (year, team, player, position, base_salary, \
                    signing_bonus, roster_bonus, option_bonus, workout_bonus, \
                    restructured_bonus, dead_cap, cap_hit, cap_percentage)

            if player_tuple not in duplicate_set:
                duplicate_set.add(player_tuple)
                desired_row.extend(player_tuple)
                wr.writerow(desired_row)

        soup.decompose()

if __name__ == '__main__':
    salary_csv_file = "../data/salary_data.csv"
    team_csv_file = "../data/team_data_simplified.csv"
    salary_scrape(salary_csv_file, team_csv_file)



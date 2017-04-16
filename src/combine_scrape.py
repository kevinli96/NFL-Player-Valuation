from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import sys 

def combine_scrape(csv_file, team_csv_file):
    url = "http://nflcombineresults.com/nflcombinedata_expanded.php?year={year}&pos=&college="
    with open(csv_file, 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['year','player', 'college', 'position', 'height', 'weight', 'hand_size', 'arm_length', 'wonderlic', '40_yard_dash', 'bench', 'vert_leap', 'broad_jump', 'shuttle', '3cone', '60_yard_shuttle'])
        for year in range(1999, 2018):
            duplicate_set = set()
            print (str(year))
            sys.stdout.flush() # make sure number is printed out in real time
            new_url = url.format(year = year)
            pageScrape(new_url, year, wr, duplicate_set)

def pageScrape(url, year, wr, duplicate_set):
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

            player = vals[1].a.string
            college = vals[2].string
            position = vals[3].string

            height = 0
            if vals[4].string is not None:
                height = vals[4].string

            weight = 0
            if vals[5].string is not None:
                weight = vals[5].string

            hand_size = 0
            if vals[6].string is not None:
                hand_size = vals[6].string

            arm_length = 0
            if vals[7].string is not None:
                arm_length = vals[7].string

            wonderlic = 0
            if vals[8].string is not None:
                wonderlic = vals[8].string

            dash = 0
            if vals[9].string is not None:
                dash = vals[9].string

            bench = 0
            if vals[10].string is not None:
                bench = vals[10].string

            vert_leap = 0
            if vals[11].string is not None:
                vert_leap = vals[11].string

            broad_jump = 0
            if vals[12].string is not None:
                broad_jump = vals[12].string

            shuttle = 0
            if vals[13].string is not None:
                shuttle = vals[13].string

            cone = 0
            if vals[14].string is not None:
                cone = vals[14].string

            long_shuttle = 0
            if vals[15].string is not None:
                long_shuttle = vals[15].string

            player_tuple = (player, college, position, height, weight, hand_size, arm_length, wonderlic, dash, bench, vert_leap, broad_jump, shuttle, cone, long_shuttle)

            if player_tuple not in duplicate_set:
                duplicate_set.add(player_tuple)
                desired_row.extend(player_tuple)
                wr.writerow(desired_row)

        soup.decompose()

if __name__ == '__main__':
    roster_csv_file = "../data/combine_data.csv"
    team_csv_file = "../data/team_data_roster_scraping.csv"
    combine_scrape(roster_csv_file, team_csv_file)
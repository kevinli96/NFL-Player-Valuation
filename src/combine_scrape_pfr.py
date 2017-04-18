from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import sys 

def combine_scrape(csv_file):
    urls = ["http://www.pro-football-reference.com/play-index/nfl-combine-results.cgi?request=1&year_min={year}&year_max={year}&height_min=65&height_max=82&weight_min=149&weight_max=375&pos=QB&pos=WR&pos=RB&pos=FB&pos=OG&pos=C&pos=DT&pos=SS&pos=LS&show=all&order_by=year_id", 
            "http://www.pro-football-reference.com/play-index/nfl-combine-results.cgi?request=1&year_min={year}&year_max={year}&height_min=65&height_max=82&weight_min=149&weight_max=375&pos=TE&pos=OT&pos=DE&pos=ILB&pos=OLB&pos=FS&pos=CB&pos=K&pos=P&show=all&order_by=year_id"]
    with open(csv_file, 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['year','player', 'url', 'position', 'college', 'weight'])
        for year in range(2000, 2018):
            for url in urls:
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

            rank = vals[0].string
            player = vals[2].a.string
            url = vals[2].a['href']
            position = vals[3].string
            college = vals[5].a.string
            weight = vals[8].string

            if rank == '200':
                print('LIMIT')

            player_tuple = (year, player, url, position, college, weight)

            if player_tuple not in duplicate_set:
                duplicate_set.add(player_tuple)
                desired_row.extend(player_tuple)
                wr.writerow(desired_row)

        soup.decompose()

if __name__ == '__main__':
    roster_csv_file = "../data/combine_data_pfr.csv"
    combine_scrape(roster_csv_file)
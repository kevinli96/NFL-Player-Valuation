from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import sys 

def combine_scrape(csv_file):
    urls = ["http://www.pro-football-reference.com/play-index/nfl-combine-results.cgi?request=1&year_min={year}&year_max={year}&height_min=65&height_max=82&weight_min=149&weight_max=375&pos=QB&pos=WR&pos=RB&pos=FB&pos=OG&pos=C&pos=DT&pos=SS&pos=LS&show=all&order_by=year_id", 
            "http://www.pro-football-reference.com/play-index/nfl-combine-results.cgi?request=1&year_min={year}&year_max={year}&height_min=65&height_max=82&weight_min=149&weight_max=375&pos=TE&pos=OT&pos=DE&pos=ILB&pos=OLB&pos=FS&pos=CB&pos=K&pos=P&show=all&order_by=year_id"]
    with open(csv_file, 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['year','player', 'url', 'position', 'college', 'height', 'weight', 'dash', 'vert_leap', 'bench', 'broad', 'cone', 'shuttle'])
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

        print("length = " + str(len(table_rows)))

        for elem in table_rows:
            desired_row = []
            vals = elem.findAll('td')

            if len(vals) > 0:
                player = ""
                url = ""

                if vals[1].a is not None:
                    player = vals[1].a.string
                    url = vals[1].a['href']
                else:
                    player = vals[1].string

                position = vals[2].string

                college = ""
                if vals[4].a is not None:
                    college = vals[4].a.string
                else:
                    college = vals[4].string

                height = vals[6].string
                height_split = height.split('-')
                height_inches = 12*int(height_split[0]) + int(height_split[1])

                weight = vals[7].string

                dash = 0
                if vals[8].string is not None:
                    dash = vals[8].string

                vert_leap = 0
                if vals[9].string is not None:
                    vert_leap = vals[9].string

                bench = 0
                if vals[10].string is not None:
                    bench = vals[10].string

                broad = 0
                if vals[11].string is not None:
                    broad = vals[11].string

                cone = 0
                if vals[12].string is not None:
                    cone = vals[12].string

                shuttle = 0
                if vals[13].string is not None:
                    shuttle = vals[13].string

                player_tuple = (year, player, url, position, college, height_inches, weight, dash, vert_leap, bench, broad, cone, shuttle)

                if player_tuple not in duplicate_set:
                    duplicate_set.add(player_tuple)
                    desired_row.extend(player_tuple)
                    wr.writerow(desired_row)

        soup.decompose()

if __name__ == '__main__':
    combine_csv_file = "../data/combine_data_pfr_with_stats.csv"
    combine_scrape(combine_csv_file)
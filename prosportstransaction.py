from bs4 import BeautifulSoup
from urllib.request import urlopen

import csv
import json

begin_date = "1994-01-01"
end_date = "1995-01-01"

prefixUrl = "http://www.prosportstransactions.com/football/Search/SearchResults.php?Player=&Team=&BeginDate="+ begin_date +"&EndDate="+end_date+"&PlayerMovementChkBx=yes&submit=Search&start=" 

start = 0
  
soup = BeautifulSoup(urlopen(prefixUrl + str(start)).read(), 'lxml')

rows = soup.find("table", { "class" : "datatable"}).findChildren()
links = soup.find_all("p", { "class" : "bodyCopy"})[2].findChildren()

end = len(links)*25 + 25

with open("prosportstransaction.csv", 'w') as outfile:
  writer = csv.writer(outfile)
  writer.writerow(["Date", "Team", "Acquired", "Relinquished", "Notes"])

  for i in range(start, end, 25):
    soup = BeautifulSoup(urlopen(prefixUrl + str(i)).read(), 'lxml')
    rows = soup.find("table", { "class" : "datatable"}).findChildren()
    links = soup.find_all("p", { "class" : "bodyCopy"})[2].findChildren()
    iterrows = iter(rows)
    next(iterrows)
    for row in iterrows:
      entry = row.find_all("td")
      if len(entry) == 5:
        date = entry[0].decode_contents(formatter="html").strip()
        team = entry[1].decode_contents(formatter="html").strip()
        acquired = entry[2].decode_contents(formatter="html").strip()
        relinquished = entry[3].decode_contents(formatter="html").strip()
        notes = entry[4].decode_contents(formatter="html").strip()
        writer.writerow([date, team, acquired, relinquished, notes])


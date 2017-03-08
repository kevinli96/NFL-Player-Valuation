from bs4 import BeautifulSoup
from urllib2 import urlopen

import csv
import json


url = "http://bds.cs.brown.edu/datathon/"

soup = BeautifulSoup(urlopen(url).read(), 'lxml')

rows = soup.find_all("div", { "class" : "workshop-row" })

with open("datathon-scrape.csv", 'wb') as outfile:
	writer = csv.writer(outfile)
	writer.writerow(["Name", "Date", "Description"])

	for row in rows:

		# Find name
		name = row.find("h4")
		if name:
			name = name.decode_contents(formatter="html")
			print name

		paragraphs = row.find_all("p")
		if len(paragraphs) > 1:
			date = paragraphs[0].decode_contents(formatter="html")
			description = paragraphs[1].decode_contents(formatter="html")
			print date
			print description

		if name or len(paragraphs) > 0:
			writer.writerow([name, date, description])
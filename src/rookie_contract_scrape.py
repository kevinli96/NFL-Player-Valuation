from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import sys
# Above, we are importing all the libraries (pre-written Python functions that we'll be using)
 
# No need to change this function
def scrapeContractEstimates(csv_file):
	""" Input: Name of CSV file we want to write to"""
	""" Action: Scrapes all rookie contract estimates for 2017"""

	url = urlopen("http://www.spotrac.com/nfl/draft/")
	soup = BeautifulSoup(url, "lxml")

	csv_vals = soup.findAll('span', attrs = {'class':'info', 'title':'Estimated Value'})


	# We open the csv file to write to it
	with open(csv_file, "w", newline="") as myfile:
		wr = csv.writer(myfile)
		wr.writerow(['Pick', 'Estimate'])

		for i in range(0, len(csv_vals)):
			pick = i+1
			estimate = csv_vals[i].text.strip("$") #remove dollar sign
			estimate = estimate.replace(",","") # remove commas
			estimate = int(estimate)

			wr.writerow([pick, estimate])
		
	soup.decompose()

file = "../data/rookie_contracts.csv"
scrapeContractEstimates	(file)
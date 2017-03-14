# CSCI 1951a - Data Science Final Project

Project website hosted on github pages: https://kevinli96.github.io/cs1951a_project/ 

## Blog Post 1:

Summarizing our “big data” vision from our pre-proposal, our main goal for this project revolves around aiming to answer the question of whether professional athletes are over/undervalued taking into account their salary as well as a metric for analyzing their relative importance to their team. Our main league of interest is the National Football League, in which quarterbacks are without question viewed as the single player with the most influence over the course of a game. To get the notion of player valuation, the metric we are using to analyze NFL players is Appropriate Value (AV), a metric that is widely used to measure the level of contribution and/or impact a player has had on the league. This metric, as with any, can be examined at a statistical level later on, however for this first blog post we will not get into the details of the structure of it. 

Player valuation is important at many levels, one of which is for organizations as a tool to measure if GMs can better utilize the data available to them to make more informed decisions about whom to draft/trade, and how to optimally allocate their salary cap. At first glance then, relevant data are those pertaining to transactions, drafts, salaries as well as appropriate value statistics. For purposes of analyzing budgetary spending and salary caps, we must also keep in mind that such data are limited to years in which the salary cap came into effect. There is no restriction on how far back we go in the data if we wish to conduct further analysis on player valuation with purely AV data, and disregard salary comparisons completely.
Division of Labor

Since we’re still in the initial steps of our project, currently we plan to work on data extraction and cleansing together. As we move further along, we plan to implement a division of labor that takes advantage of each team member’s passions and strengths. The exact division has yet to be determined, but for now we will tentatively assign the three main components of our project as follows:

* Data Warehousing and Integration - All
* Machine Learning - Edan, Isaiah
* Visualization - Kevin, Steven

## Completed Steps

### Transaction Data

To get at a basic understanding of player valuation, we looked at data from three different sources - transaction data, AV (appropriate value) data, and salary data. A quick google search of NFL transaction and draft data led us to prosportstransaction.com, a repository of transaction/draft data for baseball, basketball, football, among other sports. The filters on prosportstransaction were incredible, and allowed for searches by player name, teams, and start/end date.

Upon a valid query, e.g. for the Bears from 1994-01-01 to 1995-01-01, the results are listed in table format:

We used Python’s BeautifulSoup library for the scraping here, the source code itself was very short - about 40 lines. Minimal cleaning was done, as the unicode character for the bullet points persists in our csv. This and other unnecessary details will simply be removed through regular expression matching or modifying the scraping code. Regardless, the cleaning task here will not prove to be too difficult. 

Transaction data proves useful for us especially in the context of historical analyses of player trades and drafts. The ‘Notes’ column of the search results may contain pertinent information for predictive analysis, or constructing visualizations with the notes column as categorical variables, based on different round draft picks or free agent signings.

### AV Data

In doing this part, we collected AV data per year for all players from 1994 to 2016. For instance, the highest AV over this time period was achieved by Ladainian Tomlinson in 2006, with an AV of 26, while the lowest was achieved by Ryan Lindley in 2012, with an AV of -5. 

Scraping this data was performed in a similar manner to that in Part 1. One challenge faced was that Pro-Football-Reference insists on only showing 100 players per page, so we had to loop through all 427 pages in order to get the data for all the players. 

Minimal cleaning has been done thus far, and the results are currently stored in a CSV file. It makes sense to put this in a SQL database later on, as it would be optimal to quickly query the data for year and player. 

The AV data is our current proxy for how well a player played, or in other words, how valuable they are. This will inform our analysis of the ‘proper’ contract value for a given player.
Salary Data

We’re currently working to collect ‘cap-hit’ data for all the players referenced in our AV data. Cap-hits measure each player’s annual compensation and contribution to the salary cap. Thus far we haven’t been able to find a dataset that accounts for all the players that we we’ll be using. Most readily available data only covers the highest paid individuals from a team for a given season. 

Scraping data from multiple data sources and integrating the results may be necessary in order to piece together adequate salary data for our analyses.
Next Steps

Our immediate next steps will involve cleaning the AV and transaction data that we have extracted from profootballreference.com and prosportstransaction.com, respectively. This is necessary because we acquired an enormous amount of data from both of these sources and we need to make sure that it is in a consistent and legible format. Once we clean this data, we plan to move it into a SQL database so that we can query it in order to draw conclusions regarding the importance of different positions in the NFL and analyze the value that teams have obtained from transactions that have taken place since the salary cap was implemented. 

Once we finish this, we need to figure out how to obtain salary data - ideally we’d obtain the salary cap of each team for every year since 1993. As discussed above, we’ve had some trouble finding easily-extractable salary data, but since we consider this to be an important part of our analysis, our goal is to find a data source that would allow us to obtain the aforementioned salary data through either an API, a CSV file download, or web scraping. One route we could go, which we plan to explore before the midterm report, is scraping spotrac.com for its extensive salary data. As can be seen below, it has data for the salary cap of each team in the NFL. The one downside is that it only seems to contain salary cap data since 2011, so we’d have to either find another source for salary cap data before that year or pivot the scope of our project. Once we are able to obtain this data, we will clean it and add it to our SQL database as well - just as we plan to do with our AV and transaction data.

Once we are done with the aforementioned data warehousing and integration aspects of our project, we hope to begin work on the visualization and machine learning aspects of our project. Although we haven’t delved too deeply into these aspects yet, some ideas we’ve had for each aspect are listed below:

### Machine Learning

Carmelo ranking of various players/positions - this is a predictive analysis of the future performance of players based on historical statistics. It could help us more accurately predict the value of different positions in the NFL. It could also help us analyze the quality of trades and the fairness of current salaries.
Prediction of the 2017 NFL draft using our data.
Visualization
Heat map of expected value of different position.
Heat map showing with which frequencies different positions are taken at different spots in the draft.
Visualization of whether each position is underpaid or overpaid, and by how much (i.e. bar graph showing average pay and what pay should be for the average player at each position).

## Midterm Report:

## Blog Post 2:

## Blog Post 3:

## Pre-Proposal

### Group Members:

Edan Eingal (eeingal)
Steven Liao (sl234)
Isaiah Bryant (ibryant)
Kerui (Kevin) Li (kl101)

### Vision: 

Our “big idea” is two-fold. First, we want to analyze the importance of each position on the football (NFL) field - and second, we want to determine whether the salaries that have been historically earned by players at these positions correspond to the importance attributed to that position. 

We all know that the quarterback is the most important position in the NFL, but by how much? Which positions follow it in terms of their value to a football team? And are there certain positions in the NFL that have been historically undervalued or overvalued? Can this inform how we make decisions in the draft (i.e. draft picks are cheap labor; does cheap labor come more in handy at traditionally ‘expensive’ positions)? As an NFL GM, how can we exploit the current NFL marketplace to maximize performance of our budget? We believe that we will find answers to these questions and more at the end of our project.

### Data:

We plan to use datasets from pro-football-reference.com for player statistics and spotrac.com for salary data. 
We will consider 1696 players in the NFL over a span of ~23 seasons (we plan to start with the 1994 season, which is the season at which the salary cap was implemented).

Most of the data comes in already-formatted CSV files, which are easy to collect and insert into a database. The rest of the data can be scraped from external web sources and cleaned prior to inserting it into a database.

Since most of the data we plan to use comes in CSV files, we don’t expect to have to do too much cleaning. However, since we plan to only analyze the NFL following the implementation of the salary cap - in 1994 - we might have to remove statistics of players who played prior to the 1994 season.

If we decide to expand our project into other sports leagues in the latter half of the semester, according to the availability of datasets we will either choose to selectively scrape and collect raw data or download the appropriate CSV files. Depending on the formatting of scraped, raw data, cleaning and filtering of the data may be necessary depending on the accuracy of our sources.

### Methodology:

Our methodology seeks to answer, how much is a player worth?
This is an important question because building a team is equivalent to maximizing the return of the limited spending budget (salary cap).

Our constraints are as follows:
  * A player’s true value should be roughly proportional to his AV (approximate value)
  * Whatever the salary cap is (168 million per team for 2017)
  * Roster cap of 53 players. 

Under these constraints, a rough way we can calculate a player’s fair salary is as follows:
  * Assumption: The amount practice squad players are paid is negligible, and we will ignore it for now for simplicity
  * There are 1696 players on NFL rosters (32 teams, 53 players per team).
  * Thus we scrape the top 1696 players in Approximate Value for a given year from Pro-Football-Reference.com
  * Let P_player represent the proportion of a player’s AV to the total AV of all 1696 players. P_player does not necessarily have to refer to a player in the top 1696 in AV!
  * We take the total salary cap between all 32 teams (for 2017 that would be 168 million times 32). Let this total value be T.
  Then a player’s fair contract value is P_player*T. 

There are limitations to this method:
  * By the way AV is calculated, talented backup players will be valued less than terrible starting players.
  * For instance, Martellus Bennett is now one of the league’s best tight ends, but years earlier he was sitting behind Jason Witten and barely getting playing time.
  * In terms of AV, he may have been like 28th amongst tight ends, even if he was a top 15 tight end at the time.
  * Another limitation is that fair value should probably be thought of from an opportunity cost standpoint. For instance, if we purged the league of good quarterbacks, except for one average quarterback, that average quarterback would probably end up getting a handsome raise even though their AV might not have changed.

After discovering a player’s fair value, we can analyze it on a positional basis. Which positions have the highest value (highest average AV), and thus are ‘most valuable’? Which positions have the highest variance in AV, and is this reflected in the variance in market values? How does AV per position vary between players who have played 4 years or less versus more than 4 years, and how does that affect which positions we should draft (draft picks are cheap labor for 4 years, usually)? Most of these do not require advanced methodologies (i.e. just analyzing distributions / basic Statistics). We anticipate poking around with some of these questions and perhaps finding opportunities for further analysis which would use more advanced methodologies covered in this course.

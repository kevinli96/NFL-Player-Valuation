# CSCI 1951a - Data Science Final Project

Project website hosted on github pages: https://kevinli96.github.io/cs1951a_project/ 

## Blog Post 1:

Trade and draft data from [http://www.prosportstransactions.com/football/]. 
AV (approximate value) data from pro-football-reference.
Salary data: TBD (for tomorrow's meeting)

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

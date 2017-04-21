setwd("C:/Users/Steven/OneDrive/Documents/Brown/Junior Year/cs1951a_project/data")

# SQL code to create CSV file

#sqlite3 -header -csv nfl_data.db 
#"SELECT m.year, player.id, player.name, m.team_id, 
#m.position_id, m.age, m.av_value, m.year, m.round, 
#m.pick, m.base_salary, m.cap_hit, m.dead_cap 
#FROM player, 
#((av LEFT OUTER JOIN salary 
#ON av.player_id == salary.player_id AND av.year == salary.year) k 
#LEFT OUTER JOIN draft ON k.player_id == draft.player_id) m 
#WHERE av.player_id == player.id 
#ORDER BY m.year ASC, m.av_value DESC" > ..\data\fair_salary.csv

# read in data
av <- read.csv("fair_salary.csv")

# check data to make sure each year has a similar number of players
# i.e. we didn't do anything wrong in the sql
table(av$m.year)

# reset column names
colnames(av) <- c('year', 'id', 'name', 'team_id', 'position_id', 'age', 'av_value', 'draft_year', 'round', 'pick', 'base', 'cap_hit', 'dead_cap')

# new column: roster_size
av$roster_size <- 53

# salary cap for each year
sal_cap <- c(34.608, 37.1, 40.753, 41.454, 52.388, 57.288, 62.172, 67.405, 71.101, 75.007, 80.582, 85.5, 102, 109, 116, 123, 0, 120, 120.6, 123, 133, 143.28, 155.27)
av$salary_cap <- sal_cap[av$year -1993]

# no. teams for each year
av$no_teams <- 28
av$no_teams[av$year >= 1995] <- 30
av$no_teams[av$year >= 1999] <- 31
av$no_teams[av$year >= 2002] <- 32

# total av for that year.
# Note the number of non-zero av's is less than the number of roster spots
table(av$year[av$av_value > 0])

# av$av_total <- 0
for (i in 1994:2016){
  av$av_total[av$year == i] <- sum(av$av_value[av$year == i])
}

av$fair_value <- av$av_value/av$av_total*av$salary_cap*av$no_teams
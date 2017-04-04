#!/usr/bin/env python3
import sqlite3
import csv

def load():

    conn = sqlite3.connect('nfl_valuation_data.db')
    c = conn.cursor()

    # Delete table if already exists
    c.execute('DROP TABLE IF EXISTS "player";')
    c.execute('DROP TABLE IF EXISTS "salary";')
    c.execute('DROP TABLE IF EXISTS "av";')
    c.execute('DROP TABLE IF EXISTS "team";')
    c.execute('DROP TABLE IF EXISTS "position";')
    c.execute('DROP TABLE IF EXISTS "draft";')

    # Create tables
    c.execute('''
            CREATE TABLE player(
                id int not null,
                name text not null,
                PRIMARY KEY(id))
                ''')

    c.execute('''
            CREATE TABLE salary(
                year int,
                team_id text,
                player_id int not null,
                position_id int,
                base_salary int,
                signing_bonus int,
                roster_bonus int,
                option_bonus int,
                workout_bonus int,
                restructured_bonus int,
                dead_cap int,
                cap_hit int,
                cap_percentage real,
                FOREIGN KEY (player_id) REFERENCES player(id),
                FOREIGN KEY (team_id) REFERENCES team(id),
                FOREIGN KEY (position_id) REFERENCES position(id))
                ''')

    c.execute('''
            CREATE TABLE av(
                player_id int not null,
                year int,
                team_id text,
                position_id int,
                age int,
                av_value int,
                games_played int,
                games_Started int,
                pro_bowler int,
                all_pro int,
                FOREIGN KEY (player_id) REFERENCES player(id),
                FOREIGN KEY (team_id) REFERENCES team(id),
                FOREIGN KEY (position_id) REFERENCES position(id))
                ''')

    c.execute('''
            CREATE TABLE team(
                id text not null,
                name text not null,
                PRIMARY KEY(id))
                ''')

    c.execute('''
            CREATE TABLE position(
                id int not null,
                name text not null,
                PRIMARY KEY(id))
                ''')

    c.execute('''
            CREATE TABLE draft(
                year int,
                round int,
                pick int,
                team_id text,
                player_id int not null,
                position_id text,
                age int,
                last_year int, #Equal to last year they played, current year if still playing, blank if never played?
                games_started int,
                career_av int,
                draft_team_av int,
                games_played int,
                FOREIGN KEY (player_id) REFERENCES player(id),
                FOREIGN KEY (team_id) REFERENCES team(id),
                FOREIGN KEY (position_id) REFERENCES position(id))
                ''')

    conn.commit()

    player_data = {}
    player_data_salary = {}
    undrafted_player_data = {}
    undrafted_year = '0000'
    undrafted_pick = 1

    with open('../data/team_data_no_old_teams.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            team_id = row[0]
            team_name = row[1]

            c.execute('''
                INSERT INTO team
                VALUES (?, ?)''',
                (team_id,team_name))

    with open('../data/position_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            position_id = row[0]
            position_name = row[1]

            c.execute('''
                INSERT INTO position
                VALUES (?, ?)''',
                (position_id,position_name))

    with open('../data/draft_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = row[0]
            draft_round = row[1]
            pick = row[2]
            team_id = row[3]
            player_name = row[4]
            position_id = row[5]
            age = row[6]
            last_year = row[7]
            games_started = row[8]
            career_av = row[9]
            draft_team_av =  row[10]
            games_played = row[11]

            player_id = str(year) + str(pick)
            team_id = fix_team_id(team_id)
            position_id = fix_position_id(position_id)

            player_data[(player_name, draft_round, pick)] = player_id
            player_data_salary[(player_name, team_id, year, position_id)] = player_id

            c.execute('''
                INSERT INTO player
                VALUES (?, ?)''',
                (player_id, player_name))

            c.execute('''
                INSERT INTO draft
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (year, draft_round, pick, team_id, player_id, position_id, age, \
                    last_year, games_started, career_av, draft_team_av, games_played))

    with open('../data/av_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            player_name = row[1]
            player_url = row[2]
            year = int(row[3])
            age = int(row[4])
            draft = row[5]
            team_id = row[6]
            games_played = int(row[8])
            games_started = int(row[9])
            pro_bowler = row[11]
            all_pro = row[12]
            av_value = int(row[13])
            position_id = row[14]

            draft_split = draft.split('-')
            player_id = player_data[(player_name,draft_split[0],draft_split[1])]
            team_id = fix_team_id(team_id)
            position_id = fix_position_id(position_id)

            if player_id is None:
                if undrafted_player_data[player_url] is None:
                    player_id = undrafted_year + str(undrafted_pick)
                    undrafted_pick = undrafted_pick + 1
                    undrafted_player_data[player_url] = player_id
                    c.execute('''
                            INSERT INTO player
                            VALUES (?, ?)''',
                            (player_id,player_name))
                else:
                    player_id = undrafted_player_data[player_url]

            player_data_salary[(player_name, team_id, year, position_id)] = player_id

            c.execute('''
                INSERT INTO av
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (player_id, year, team_id, position_id, age, av_value, games_played, games_started, pro_bowler, all_pro))       

    with open('../data/salary_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = row[0]
            team_id = row[1]
            player_name = row[2]
            position_id = row[3]
            base_salary = row[4]
            signing_bonus = row[5]
            roster_bonus = row[6]
            option_bonus = row[7]
            workout_bonus = row[8]
            restructured_bonus = row[9]
            dead_cap =  row[10]
            cap_hit = row[11]
            cap_percentage = row[12]

            team_id = fix_team_id(team_id)
            position_id = fix_position_id(position_id)
            player_id = player_data_salary[(player_name, team_id, year, position_id)]

            c.execute('''
                INSERT INTO salary
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (year, team_id, player_id, position_id, base_salary, \
                signing_bonus, roster_bonus, option_bonus, workout_bonus, \
                restructured_bonus, dead_cap, cap_hit, cap_percentage))     

    conn.commit()
    conn.close()

def fix_team_id(team_id):
    if team_id == 'RAM' or team_id == 'STL':
        team_id = 'LAR'
    elif team_id == 'SDG':
        team_id = 'LAC'
    elif team_id = 'RAI':
        team_id = 'OAK'
    elif team_id = 'HOU' and year < 2000:
        team_id = 'TEN'

    return team_id

def fix_position_id(position_id):
    if position_id == "NT":
        position_id = "DT"
    elif position_id == "LT" or position_id == "RT":
        position_id = "T"
    return position_id

if __name__ == '__main__':
    load()

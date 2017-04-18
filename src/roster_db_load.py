#!/usr/bin/env python3
import sqlite3
import csv

def load():

    conn = sqlite3.connect('roster_data.db')
    c = conn.cursor()

    # Delete table if already exists
    c.execute('DROP TABLE IF EXISTS "player";')
    c.execute('DROP TABLE IF EXISTS "rosters";')
    c.execute('DROP TABLE IF EXISTS "team";')
    c.execute('DROP TABLE IF EXISTS "standings";')

    # Create tables
    c.execute('''
            CREATE TABLE player(
                id int not null,
                name text not null,
                PRIMARY KEY(id))
                ''')

    c.execute('''
            CREATE TABLE rosters(
                year int,
                team_id text,
                player_id int not null,
                age int,
                position text,
                games_played int,
                games_started int,
                weight int,
                height text,
                college text,
                birthdate text,
                experience int,
                av int,
                FOREIGN KEY (player_id) REFERENCES player(id),
                FOREIGN KEY (team_id) REFERENCES team(id))
                ''')

    c.execute('''
            CREATE TABLE team(
                id text not null,
                name text not null,
                PRIMARY KEY(id))
                ''')

    c.execute('''
        CREATE TABLE standings(
            year int,
            team_id text,
            player_id int not null,
            age int,
            position text,
            games_played int,
            games_started int,
            weight int,
            height text,
            college text,
            birthdate text,
            experience int,
            av int,
            FOREIGN KEY (team_id) REFERENCES team(id))
            ''')

    conn.commit()

    player_data = {}
    player_map = {}
    id_count = 0

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

    with open('../data/roster_data_pfr.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = int(row[0])
            team_id = row[1]
            player_name = row[2]
            player_url = row[3]
            age = int(row[4])
            position = row[5]
            games_played = int(row[6])
            games_started = int(row[7])
            weight = int(row[8])
            height = row[9]
            college = row[10]
            birthdate = row[11]
            experience = row[12]
            av_value = int(row[13])

            official_player_name = player_name
            player_name = fix_player_name(player_name)
            team_id = fix_team_id(team_id, year)

            if experience == "Rook":
                experience = 0
            else:
                experience = int(experience)

            if len(height) > 1:
                height = height[1:]
            elif len(height) == 1:
                height = ''

            if player_url not in player_map:
                player_id = id_count
                id_count += 1
                player_map[player_url] = player_id

                c.execute('''
                    INSERT INTO player
                    VALUES (?, ?)''',
                    (player_id, official_player_name))
            else:
                player_id = player_map[player_url]

            player_data[(player_name, year, team_id, birthdate)] = player_id

            c.execute('''
                    INSERT INTO rosters
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (year, team_id, player_id, age, position, games_played, games_started, weight, height, college, birthdate, experience, av_value))       

    with open('../data/roster_data.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = int(row[0])
            team_id = row[1]
            player_name = row[2]
            position = row[3]
            birthdate = row[4]
            college = row[5]

            official_player_name = player_name
            player_name = fix_player_name(player_name)
            team_id = fix_team_id(team_id, year)

            player_id = player_data[(player_name, year, team_id, birthdate)]

            c.execute('''
                UPDATE rosters
                SET position == ?
                WHERE player_id = ? AND year = ? AND team = ?''',
                (position, player_id, year, team_id))

    conn.commit()
    conn.close()

def fix_player_name(name):
    return name.replace("'","").replace(".","").replace(",","").replace("  "," ").replace("-","").replace(" Jr","").lower()

def fix_team_id(team_id, year):
    if team_id == 'RAM' or team_id == 'STL':
        team_id = 'LAR'
    elif team_id == 'SDG':
        team_id = 'LAC'
    elif team_id == 'RAI':
        team_id = 'OAK'
    elif team_id == 'HOU' and int(year) < 2000:
        team_id = 'TEN'
    elif team_id == 'NEW':
        team_id = 'NWE'

    return team_id

if __name__ == '__main__':
    load()

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
                pfr_position text,
                other_position text,
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
                team_id text not null,
                wins int,
                losses int,
                ties int,
                pf int,
                pa int,
                pd int,
                wc int,
                d int,
                c int,
                sl int,
                sw int,
                FOREIGN KEY (team_id) REFERENCES team(id))
                ''')

    conn.commit()

    player_data = {}
    player_data_no_birthdate = {}
    player_map = {}
    team_map = {}
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

    with open('../data/team_data_for_standings.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            team_id = row[0]
            team_name = row[1]

            team_map[team_name] = team_id

    with open('../data/roster_data_pfr.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = int(row[0])
            team_id = row[1]
            player_name = row[2]
            player_url = row[3]

            age = None
            if row[4] != '':
                age = int(row[4])

            position = row[5]
            games_played = int(row[6])

            games_started = None
            if row[7] != '':
                games_started = int(row[7])

            weight = None
            if row[8] != '':
                weight = int(row[8])

            height = row[9]
            college = row[10]
            birthdate = row[11]
            experience = row[12]
            av_value = int(row[13])

            official_player_name = player_name
            pfr_position = position
            other_position = ""
            player_name = fix_player_name(player_name)
            team_id = fix_team_id(team_id, year)
            position = fix_position_id(position)

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
            player_data_no_birthdate[(player_name, year, team_id)] = player_id

            c.execute('''
                    INSERT INTO rosters
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (year, team_id, player_id, age, position, pfr_position, other_position, games_played, games_started, weight, height, college, birthdate, experience, av_value))       

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

            player_id = None
            if (player_name, year, team_id, birthdate) in player_data:
                player_id = player_data[(player_name, year, team_id, birthdate)]
            elif (player_name, year, team_id) in player_data_no_birthdate:
                player_id = player_data_no_birthdate[(player_name, year, team_id)]

            if player_id is not None:
                c.execute('''
                    UPDATE rosters
                    SET position == ?
                    WHERE player_id = ? AND year = ? AND team_id = ?''',
                    (position, player_id, year, team_id))

                c.execute('''
                    UPDATE rosters
                    SET other_position == ?
                    WHERE player_id = ? AND year = ? AND team_id = ?''',
                    (position, player_id, year, team_id))

    with open('../data/NFLStandings.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = int(row[0])
            team_name = row[1]
            wins = int(row[2])
            losses = int(row[3])
            ties = int(row[4])
            pf = int(row[5])
            pa = int(row[6])
            pd = int(row[7])
            wc = int(row[8])
            d = int(row[9])
            con = int(row[10])
            sl = int(row[11])
            sw = int(row[12])

            team_id = team_map[team_name]
            team_id = fix_team_id(team_id, year)

            c.execute('''
                INSERT INTO standings
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (year, team_id, wins, losses, ties, pf, pa, pd, wc, d, con, sl, sw))   

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

def fix_position_id(position_id):
    position_id = position_id.lower()

    if position_id == "nt":
        position_id = "DT"
    elif position_id == "lt" or position_id == "rt" or position_id == "t":
        position_id = "OT"
    elif position_id == "":
        position_id = "UTIL"
    elif position_id == "lcb" or position_id == "rcb" or position_id == "ss" or position_id == "fs" or position_id == "cb" or position_id == "s" or position_id == "rs":
        position_id = "DB"
    elif position_id == "fb" or position_id == "tb" or position_id == "rh" or position_id == "lh":
        position_id = "RB"
    elif position_id == "ilb" or position_id == "olb" or position_id == "rilb" or position_id == "lilb" or position_id == "lolb" \
    or position_id == "rolb" or position_id == "mlb" or position_id == "llb" or position_id == "rlb":
        position_id = "LB"
    elif position_id == "fl" or position_id == "kr" or position_id == "pr" or position_id == "se":
        position_id = "WR"
    elif position_id == "lg" or position_id == "rg" or position_id == "g":
        position_id = "OG"
    elif position_id == "lde" or position_id == "rde":
        position_id = "DE"
    elif position_id == "ldt" or position_id == "rdt":
        position_id = "DT"

    return position_id.upper()

if __name__ == '__main__':
    load()

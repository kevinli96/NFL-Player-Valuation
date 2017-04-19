#!/usr/bin/env python3
import sqlite3
import csv

def load():

    conn = sqlite3.connect('combine_data.db')
    c = conn.cursor()

    # Delete table if already exists
    c.execute('DROP TABLE IF EXISTS "player";')
    c.execute('DROP TABLE IF EXISTS "combine";')
    c.execute('DROP TABLE IF EXISTS "av";')
    c.execute('DROP TABLE IF EXISTS "team";')

    # Create tables
    c.execute('''
            CREATE TABLE player(
                id int not null,
                name text not null,
                PRIMARY KEY(id))
                ''')

    c.execute('''
            CREATE TABLE combine(
                year int,
                player_id int not null, 
                college text, 
                position text, 
                height int, 
                weight int, 
                hand_size real, 
                arm_length real, 
                wonderlic int, 
                dash real, 
                bench int, 
                vert_leap real, 
                broad_jump real, 
                shuttle real, 
                cone real, 
                long_shuttle real,
                FOREIGN KEY (player_id) REFERENCES player(id))
                ''')

    c.execute('''
            CREATE TABLE team(
                id text not null,
                name text not null,
                PRIMARY KEY(id))
                ''')

    c.execute('''
            CREATE TABLE av(
                player_id int not null,
                year int,
                team_id text,
                age int,
                av_value int,
                games_played int,
                games_started int,
                pro_bowler int,
                all_pro int,
                FOREIGN KEY (player_id) REFERENCES player(id),
                FOREIGN KEY (team_id) REFERENCES team(id))
                ''')

    conn.commit()

    player_data_url = {}
    player_data_av = {}
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

    with open('../data/combine_data_pfr.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = int(row[0])
            player_name = row[1]
            url = row[2]
            position = row[3]
            college = row[4]
            weight = int(row[5])

            official_player_name = player_name;
            player_name = fix_player_name(player_name)
            
            if (player_name, year, weight) not in player_map:
                player_id = id_count
                id_count += 1
                player_map[(player_name, year, weight)] = player_id

                c.execute('''
                    INSERT INTO player
                    VALUES (?, ?)''',
                    (player_id, official_player_name))
            else:
                player_id = player_map[(player_name, year, weight)]

            player_data_url[url] = player_id

    with open('../data/combine_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = int(row[0])
            player_name = row[1]
            college = row[2]
            position = row[3]
            height = int(row[4])
            weight = int(row[5])
            hand_size = float(row[6])
            arm_length = float(row[7])
            wonderlic = int(row[8])
            dash = float(row[9])
            bench = int(row[10])
            vert = float(row[11])
            broad = float(row[12])
            shuttle = float(row[13])
            cone = float(row[14])
            long_shuttle = float(row[15])

            official_player_name = player_name;
            player_name = fix_player_name(player_name)

            if (player_name, year, weight) not in player_map:
                player_id = id_count
                id_count += 1
                player_data_av[(player_name, year)] = player_id

                c.execute('''
                    INSERT INTO player
                    VALUES (?, ?)''',
                    (player_id, official_player_name))
            else:
                player_id = player_map[(player_name, year, weight)]

            c.execute('''
                INSERT INTO combine
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (year, player_id, college, position, height, weight, hand_size, arm_length, wonderlic, dash, bench, vert, broad, shuttle, cone, long_shuttle))   

    with open('../data/AVdata1995-2016.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            player_name = row[1]
            player_url = row[2]
            year = int(row[3])
            age = int(row[4])
            team_id = row[6]
            games_played = int(row[8])
            games_started = int(row[9])
            pro_bowler = int(row[11])
            all_pro = int(row[12])
            av_value = int(row[13])

            player_name = fix_player_name(player_name)
            team_id = fix_team_id(team_id, year)

            player_id = None
            if player_url in player_data_url:
                player_id = player_data_url[player_url]
            elif (player_name, year) in player_data_av:
                player_id = player_data_av[(player_name, year)]

            if player_id is not None:
                c.execute('''
                    INSERT INTO av
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (player_id, year, team_id, age, av_value, games_played, games_started, pro_bowler, all_pro))       

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

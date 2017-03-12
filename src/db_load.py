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
                player_id int not null,
                year int,
                cap_hit int,
                team_id text,
                position_id int,
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
                player_id int not null,
                year int,
                team_id text,
                round int,
                pick int,
                position_id text,
                FOREIGN KEY (player_id) REFERENCES player(id),
                FOREIGN KEY (team_id) REFERENCES team(id),
                FOREIGN KEY (position_id) REFERENCES position(id))
                ''')

    conn.commit()

    player_data = {}
    undrafted_player_data = {}
    undrafted_year = '0000'
    undrafted_pick = 1

    with open('../data/team_data.csv', 'r', encoding='utf-8') as csvfile:
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

            player_id = str(year) + str(pick)

            player_data[(player_name,draft_round,pick)] = player_id

            c.execute('''
                INSERT INTO player
                VALUES (?, ?)''',
                (player_id,player_name))

            c.execute('''
                INSERT INTO draft
                VALUES (?, ?, ?, ?, ?)''',
                (player_id, year, team_id, draft_round, pick, position_id))

    with open('../data/av_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            player_name = row[1]
            player_url = row[2]
            year = row[3]
            age = row[4]
            draft = row[5]
            team_id = row[6]
            games_played = row[8]
            games_started = row[9]
            pro_bowler = row[11]
            all_pro = row[12]
            av_value = row[13]
            position_id = row[14]

            draft_split = draft.split('-')
            player_id = player_data[(player_name,draft_split[0],draft_split[1])]

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

            c.execute('''
                INSERT INTO av
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (player_id, year, team_id, position_id, age, av_value, games_played, games_started, pro_bowler, all_pro))       

    # with open('../data/salary_data.csv', 'r', encoding='utf-8') as csvfile:
    #     csv_reader = csv.reader(csvfile)
    #     next(csv_reader, None)
    #     for row in csv_reader:
    #         NEED TO DO THIS

    #         c.execute('''
    #             INSERT INTO salary
    #             VALUES (?, ?, ?, ?, ?)''',
    #             (player_id, year, team_id, position_id, salary))     

    conn.commit()
    conn.close()

if __name__ == '__main__':
    load()

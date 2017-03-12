#!/usr/bin/env python3
import sqlite3
import csv

def load():

    ###################################################
    # TODO:                                           #
    # Fill in this function so that it loads your     #
    # data into a file called playlist_data.db.       #
    ###################################################
    conn = sqlite3.connect('nfl_valuation_data.db')
    c = conn.cursor()

    # Delete table if already exists
    c.execute('DROP TABLE IF EXISTS "player";')
    c.execute('DROP TABLE IF EXISTS "salary";')
    c.execute('DROP TABLE IF EXISTS "av";')
    c.execute('DROP TABLE IF EXISTS "team";')
    c.execute('DROP TABLE IF EXISTS "position";')
    c.execute('DROP TABLE IF EXISTS "plays";')
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
                av_value int,
                team_id text,
                position_id int,
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
            CREATE TABLE plays(
                player_id int not null,
                year int,
                team_id text,
                position_id int,
                FOREIGN KEY (player_id) REFERENCES player(id),
                FOREIGN KEY (team_id) REFERENCES team(id),
                FOREIGN KEY (position_id) REFERENCES position(id))
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

    with open('team_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            team_id = row[0]
            team_name = row[1]

            c.execute('''
                INSERT INTO team
                VALUES (?, ?)''',
                (team_id,team_name))

    with open('position_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            position_id = row[0]
            position_name = row[1]

            c.execute('''
                INSERT INTO position
                VALUES (?, ?)''',
                (position_id,position_name))

    with open('draft_data.csv', 'r', encoding='utf-8') as csvfile:
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

            player_data[player_id] = player_name

            c.execute('''
                INSERT INTO player
                VALUES (?, ?)''',
                (player_id,player_name))

            c.execute('''
                INSERT INTO draft
                VALUES (?, ?, ?, ?, ?)''',
                (player_id, year, team_id, draft_round, pick, position_id))

    with open('av_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            player_id = row[0]
            team_name = row[1]

            c.execute('''
                INSERT INTO av
                VALUES (?, ?)''',
                (team_id,team_name))

    conn.commit()
    conn.close()
    ###################################################
    #               END OF YOUR CODE                  #
    ###################################################


if __name__ == '__main__':
    load()

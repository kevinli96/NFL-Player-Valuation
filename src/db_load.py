#!/usr/bin/env python3
import sqlite3
import csv

def load():

    conn = sqlite3.connect('nfl_data.db')
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

    #last_year is equal to last year they played, current year if still playing, blank if never played?
    c.execute('''
            CREATE TABLE draft(
                year int,
                round int,
                pick int,
                team_id text,
                player_id int not null,
                position_id text,
                age int,
                last_year int, 
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
    player_data_salary_no_year = {}
    player_data_salary_no_team = {}
    player_data_salary_with_position = {}
    player_data_salary_just_name = {}
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
            year = int(row[0])
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
            team_id = fix_team_id(team_id, year)
            position_id = fix_position_id(position_id)
            player_name = fix_player_name(player_name)

            player_data[(player_name, draft_round, pick)] = player_id
            player_data_salary[(player_name, team_id, year)] = player_id
            player_data_salary_no_year[(player_name, team_id)] = player_id
            player_data_salary_no_team[(player_name, year)] = player_id
            player_data_salary_with_position[(player_name, position_id)] = player_id
            player_data_salary_just_name[player_name] = player_id

            c.execute('''
                INSERT INTO player
                VALUES (?, ?)''',
                (player_id, player_name))

            c.execute('''
                INSERT INTO draft
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (year, draft_round, pick, team_id, player_id, position_id, age, \
                    last_year, games_started, career_av, draft_team_av, games_played))

    av_data_repeats = {}

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

            player_id = None
            draft_split = draft.split('-')
            player_name = fix_player_name(player_name)
            if len(draft_split) > 1 and (player_name,draft_split[0],draft_split[1].replace("abc","")) in player_data:
                player_id = player_data[(player_name,draft_split[0],draft_split[1].replace("abc",""))]
            team_id = fix_team_id(team_id, year)
            position_id = fix_position_id(position_id)

            if player_id is None:
                if player_url not in undrafted_player_data:
                    player_id = str(undrafted_year) + str(undrafted_pick)
                    undrafted_pick = undrafted_pick + 1
                    undrafted_player_data[player_url] = player_id
                    c.execute('''
                            INSERT INTO player
                            VALUES (?, ?)''',
                            (player_id,player_name))
                else:
                    player_id = undrafted_player_data[player_url]

            player_data_salary[(player_name, team_id, year)] = player_id
            player_data_salary_no_year[(player_name, team_id)] = player_id
            player_data_salary_no_team[(player_name, year)] = player_id
            player_data_salary_with_position[(player_name, position_id)] = player_id
            player_data_salary_just_name[player_name] = player_id

            if (player_url, team_id, year) not in av_data_repeats:
                av_data_repeats[(player_url, team_id, year)] = position_id
                c.execute('''
                    INSERT INTO av
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (player_id, year, team_id, position_id, age, av_value, games_played, games_started, pro_bowler, all_pro))       
            else:
                curr_position_id = av_data_repeats[(player_url, team_id, year)]
                new_position_id = fix_position_id_repeats(curr_position_id, position_id)
                if new_position_id != curr_position_id:
                    av_data_repeats[(player_url, team_id, year)] = new_position_id
                    c.execute('''
                        UPDATE av
                        SET position_id == ?
                        WHERE player_id = ?''',
                        (new_position_id, player_id))

    with open('../data/salary_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = int(row[0])
            team_id = row[1]
            player_name = row[2]
            position_id = row[3]
            base_salary = int(row[4])
            signing_bonus = int(row[5])
            roster_bonus = int(row[6])
            option_bonus = int(row[7])
            workout_bonus = int(row[8])
            restructured_bonus = int(row[9])
            dead_cap =  int(row[10])
            cap_hit = int(row[11])
            cap_percentage = float(row[12])

            team_id = fix_team_id(team_id, year)
            position_id = fix_position_id(position_id)
            player_name = fix_player_name(player_name)

            if (player_name, team_id, year) in player_data_salary:
                player_id = player_data_salary[(player_name, team_id, year)]
            elif (player_name, "2TM", year) in player_data_salary:
                player_id = player_data_salary[(player_name, "2TM", year)]
            elif year > 2016 and (player_name, team_id, 2016) in player_data_salary:
                player_id = player_data_salary[(player_name, team_id, 2016)]
            elif (player_name, team_id, year - 1) in player_data_salary:
                player_id = player_data_salary[(player_name, team_id, year - 1)]
            elif (player_name, team_id, year + 1) in player_data_salary:
                player_id = player_data_salary[(player_name, team_id, year + 1)]
            elif (player_name, team_id) in player_data_salary_no_year:
                player_id = player_data_salary_no_year[(player_name, team_id)]
            elif (player_name, year) in player_data_salary_no_team:
                player_id = player_data_salary_no_team[(player_name, year)]
            elif (player_name, position_id) in player_data_salary_with_position:
                player_id = player_data_salary_with_position[(player_name, position_id)]
            elif player_name in player_data_salary_just_name:
                player_id = player_data_salary_just_name[player_name]
            else:
                print ((player_name, team_id, year))

            c.execute('''
                INSERT INTO salary
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (year, team_id, player_id, position_id, base_salary, \
                signing_bonus, roster_bonus, option_bonus, workout_bonus, \
                restructured_bonus, dead_cap, cap_hit, cap_percentage))     

    conn.commit()
    conn.close()

def fix_player_name(name):
    return name.replace("'","").replace(".","").replace(",","").replace("  "," ").replace(" Jr","").lower()

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
    if position_id == "NT":
        position_id = "DT"
    elif position_id == "LT" or position_id == "RT":
        position_id = "T"
    return position_id

def fix_position_id_repeats(curr_position_id,position_id):
    if curr_position_id == "OL":
        if position_id == "G" or position_id == "T" or position_id == "C":
            return position_id
    elif curr_position_id == "DL":
        if position_id == "DE" or position_id == "DT":
            return position_id
    elif curr_position_id == "DB":
        if position_id == "CB" or position_id == "S":
            return position_id

    return curr_position_id

if __name__ == '__main__':
    load()

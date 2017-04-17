#!/usr/bin/env python3
import sqlite3
import csv

def load():

    conn = sqlite3.connect('roster_data.db')
    c = conn.cursor()

    # Delete table if already exists
    c.execute('DROP TABLE IF EXISTS "player";')
    c.execute('DROP TABLE IF EXISTS "rosters";')
    c.execute('DROP TABLE IF EXISTS "av";')
    c.execute('DROP TABLE IF EXISTS "team";')
    c.execute('DROP TABLE IF EXISTS "position";')

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
                position int,
                birthdate int,
                college int,
                FOREIGN KEY (player_id) REFERENCES player(id),
                FOREIGN KEY (team_id) REFERENCES team(id))
                ''')

    c.execute('''
            CREATE TABLE av(
                player_id int not null,
                year int,
                team_id text,
                position int,
                age int,
                av_value int,
                games_played int,
                games_started int,
                pro_bowler int,
                all_pro int,
                FOREIGN KEY (player_id) REFERENCES player(id),
                FOREIGN KEY (team_id) REFERENCES team(id))
                ''')

    c.execute('''
            CREATE TABLE team(
                id text not null,
                name text not null,
                PRIMARY KEY(id))
                ''')

    conn.commit()

    player_data = {}
    id_count = 1

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

    with open('../data/roster_data.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            year = int(row[0])
            team_id = row[1]
            player_name = row[2]
            position = row[3]
            birthdate = row[4]
            college = row[5]

            player_id = str(year) + str(pick)
            team_id = fix_team_id(team_id, year)
            position_id = fix_position_id(position_id)
            official_player_name = player_name;

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
                (player_id, official_player_name))

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
            official_player_name = player_name
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
                            (player_id,official_player_name))
                else:
                    player_id = undrafted_player_data[player_url]

            player_data_salary[(player_name, team_id, year)] = player_id
            player_data_salary_no_year[(player_name, team_id)] = player_id
            player_data_salary_no_team[(player_name, year)] = player_id
            player_data_salary_with_position[(player_name, position_id)] = player_id
            player_data_salary_just_name[player_name] = player_id

            if (player_url, team_id, year) not in av_data_repeats:
                av_data_repeats[(player_url, team_id, year)] = position_id
                player_data_salary_position_year[(player_id, year)] = position_id
                c.execute('''
                    INSERT INTO av
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (player_id, year, team_id, position_id, age, av_value, games_played, games_started, pro_bowler, all_pro))       
            else:
                curr_position_id = av_data_repeats[(player_url, team_id, year)]
                new_position_id = fix_position_id_repeats(curr_position_id, position_id)
                if new_position_id != curr_position_id:
                    av_data_repeats[(player_url, team_id, year)] = new_position_id
                    player_data_salary_position_year[(player_id, year)] = new_position_id
                    c.execute('''
                        UPDATE av
                        SET position_id == ?
                        WHERE player_id = ?''',
                        (new_position_id, player_id))

    player_count = {}

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

            player_id = match_salary_data_with_av(player_name, team_id, year, position_id, player_data_salary, player_data_salary_no_year, player_data_salary_no_team, player_data_salary_with_position, player_data_salary_just_name)

            if player_id is None:
                first_name = player_name.split(" ")[0]
                last_name = player_name.split(" ")[1]
                first_name = try_different_first_name(first_name)

                player_name = first_name + " " + last_name
                player_id = match_salary_data_with_av(player_name, team_id, year, position_id, player_data_salary, player_data_salary_no_year, player_data_salary_no_team, player_data_salary_with_position, player_data_salary_just_name)

            if player_id == "200455" and team_id == "JAX" and position_id == "ILB" and year == 2012:
                player_id = "2011185"

            if (player_id, year) in player_data_salary_position_year:
                position_id = fix_position_id_salary_vs_av(position_id, player_data_salary_position_year[(player_id, year)])

            c.execute('''
                UPDATE av
                SET position_id == ?
                WHERE player_id = ? AND year = ?''',
                (position_id, player_id, year))

            if player_id is None:
                if player_name in player_count:
                    player_count[player_name] += 1
                else:
                    player_count[player_name] = 1
                print ((player_name, team_id, year))
            else:
                c.execute('''
                    INSERT INTO salary
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (year, team_id, player_id, position_id, base_salary, \
                    signing_bonus, roster_bonus, option_bonus, workout_bonus, \
                    restructured_bonus, dead_cap, cap_hit, cap_percentage))     

    # for key in player_count:
    #     if player_count[key] > 3:
    #         print (key + ", " + str(player_count[key]))

    conn.commit()
    conn.close()

def match_salary_data_with_av(player_name, team_id, year, position_id, player_data_salary, player_data_salary_no_year, player_data_salary_no_team, player_data_salary_with_position, player_data_salary_just_name):
    player_id = None
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
    return player_id

def try_different_first_name(first_name):
    if first_name == "michael":
        first_name = "mike"
    elif first_name == "mike":
        first_name = "michael"
    elif first_name == "ron":
        first_name = "ronald"
    elif first_name == "ronald":
        first_name = "ron"
    elif first_name == "will":
        first_name = "william"
    elif first_name == "william":
        first_name = "will"
    elif first_name == "nathan":
        first_name = "nate"
    elif first_name == "nate":
        first_name = "nathan"
    elif first_name == "vladimir":
        first_name = "vlad"
    elif first_name == "vlad":
        first_name == "vladimir"
    elif first_name == "stevie":
        first_name = "steve"
    elif first_name == "matthew":
        first_name = "matt"
    elif first_name == "matt":
        first_name = "matthew"
    elif first_name == "chris":
        first_name = "christopher"
    elif first_name == "christopher":
        first_name = "chris"
    elif first_name == "robert":
        first_name = "rob"
    elif first_name == "rob":
        first_name = "robert"
    elif first_name == "joshua":
        first_name = "josh"
    elif first_name == "josh":
        first_name = "joshua"
    elif first_name == "phillip":
        first_name = "phil"
    elif first_name == "phil":
        first_name = "phillip"

    return first_name

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
    if position_id == "NT":
        position_id = "DT"
    elif position_id == "LT" or position_id == "RT":
        position_id = "T"
    elif position_id == "KR":
        position_id = "WR"
    elif position_id == "FS" or position_id == "SS":
        position_id = "S"
    elif position_id == "FB":
        position_id = "RB"
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
    elif curr_position_id == "LB":
        if position_id == "ILB" or position_id == "OLB":
            return position_id

    return curr_position_id

def fix_position_id_salary_vs_av(curr_position_id,position_id):
    if curr_position_id == "OL":
        if position_id == "G" or position_id == "T" or position_id == "C":
            return position_id
    elif curr_position_id == "DL":
        if position_id == "DE" or position_id == "DT":
            return position_id
    elif curr_position_id == "DB":
        if position_id == "CB" or position_id == "S":
            return position_id
    elif curr_position_id == "LB":
        if position_id == "ILB" or position_id == "OLB":
            return position_id
    elif (curr_position_id == "ILB" and (position_id == "OLB" or position_id == "DE")) or \
    (curr_position_id == "OLB" and (position_id == "ILB" or position_id == "DE")):
        return position_id
    elif (curr_position_id == "S" and position_id == "CB") or (curr_position_id == "CB" and position_id == "S"):
        return position_id
    elif (curr_position_id == "G" and (position_id == "T" or position_id == "C")) or \
    (curr_position_id == "T" and (position_id == "G" or position_id == "C")) or \
    (curr_position_id == "C" and (position_id == "T" or position_id == "G")):
        return position_id
    elif (curr_position_id == "DE" and position_id == "DT") or (curr_position_id == "DT" and position_id == "DE"):
        return position_id
    elif (curr_position_id == "RB" and position_id == "WR") or (curr_position_id == "WR" and position_id == "RB"):
        return position_id
    elif (curr_position_id == "K" and position_id == "P") or (curr_position_id == "P" and position_id == "K"):
        return position_id
    elif (curr_position_id == "WR" and position_id == "QB") or (curr_position_id == "QB" and position_id == "WR"):
        return position_id
    elif (curr_position_id == "WR" and position_id == "CB") or (curr_position_id == "CB" and position_id == "WR"):
        return position_id
    elif (curr_position_id == "WR" and position_id == "S") or (curr_position_id == "S" and position_id == "WR"):
        return position_id

    return curr_position_id

if __name__ == '__main__':
    load()

#!/usr/bin/env python3
import sqlite3
import csv

def create_av_salary_viz():

    conn = sqlite3.connect('nfl_data.db')
    c = conn.cursor()

    positions = ["WR", "RB", "S", "CB", "DT", "DE", "T", "G", "TE", "OLB", "ILB", "QB", "LB", "C", "K", "P", "LS"]
    counts_total = [4375,4141,3813,3786,3334,3237,2922,2722,2583,2181,1958,1826,1612,1180,892,808,321]

    data = []
    for year in range(2005,2017):
        for i in range(len(positions)):
            rows = c.execute('''
                    select distinct name, av.av_value, av.position_id, salary.cap_hit, av.year, av.team_id, av.age 
                    from av, player, salary 
                    where av.position_id = ? and av.player_id = player.id and salary.player_id = player.id and av.year = salary.year and av.year = ?
                    order by av.position_id, av_value desc 
                    limit (select count(player_id) from av where position_id = ? and year = ? group by position_id)/10''',
                    (positions[i],year,positions[i],year))
            data.extend(rows)

    with open('..\\blog\\viz\\av_salary_top_av\\av_salary_viz_test.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["name","av_value","position_id","cap_hit","year","team_id","age"])
        for entry in data:
            writer.writerow(
                [entry[0], entry[1], entry[2], entry[3],
                entry[4], entry[5], entry[6]])

if __name__ == '__main__':
    create_av_salary_viz()
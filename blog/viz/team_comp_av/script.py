import csv
import pprint

pp = pprint.PrettyPrinter(indent=4)

def getTeamAVComp(year):
    teamAV = {}
    playerCount = {}
    with open('roster_data_db.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for line in reader:
            if int(line[1]) != year:
                continue
            team = line[2]
            teamAV[team] = teamAV.get(team, {})
            playerCount[team] = playerCount.get(team, {})
            position = line[5]
            AV = float(line[-1])
            teamAV[team][position] = AV + teamAV[team].get(position, 0)
            playerCount[team][position] = 1 + playerCount[team].get(position, 0)
    pp.pprint(teamAV)
    pp.pprint(playerCount)

    return teamAV, playerCount

def write_to_CSV(teamAV, playerCount):
    teamPositions = ["QB","WR","RB","TE","OG","OT","C", "DE","DT","LB","DB","P","K"]
    with open('AV_by_team.csv', 'w', encoding='utf-8') as g:
        writer = csv.writer(g)
        writer.writerow(["Team", "QB", "WR", "RB", "TE","OG", "OT", "C","DE", "DT", "LB","DB","P", "K"])
        allTeams = []
        for team in teamAV:
            perTeam = [team]
            for pos in teamPositions:
                AVCount = [teamAV[team].get(pos, 0)]
                    # AVCount += teamAV[team].get(pos, 0)
                perTeam += AVCount
            allTeams.append(perTeam)

        allTeams.sort(key=lambda item: sum(item[1:14]) )
        for team in allTeams:
            writer.writerow(team)


def main():
    teamAV, playerCount = getTeamAVComp(2016)
    minTeam = ''
    minPos = 100
    # for team in teamAV:
    #     if len(teamAV[team]) < minPos:
    #         minPos = len(teamAV[team])
    #         minTeam = team
    # print("team: " + minTeam)
    # pp.pprint(teamAV[minTeam])
    write_to_CSV(teamAV, playerCount)


if __name__ == '__main__':
    main()

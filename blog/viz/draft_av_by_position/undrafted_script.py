import csv
import pprint

pp = pprint.PrettyPrinter(indent=4)

def get_average_AV():
    AV_by_position = {}
    roundCounts = {}
    for i in range(0, 13):
        roundCounts[i] = {}
    with open('draft_viz_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for line in reader:
            position = line[1]
            AV_by_position[position] = AV_by_position.get(position, {})
            rd = int(line[4]) if line[4] != '' else 0
            if line[2] == '':
                continue
            AV = float(line[2])
            AV_by_position[position][rd] = AV + AV_by_position[position].get(rd, 0)
            roundCounts[rd][position] = 1 + roundCounts[rd].get(position, 0)
    pp.pprint(AV_by_position)
    for pos in AV_by_position:
        counts = AV_by_position[pos]
        for i in range(0, 13):
            if i in counts:
                counts[i] /= roundCounts[i][pos]
                counts[i] = round(counts[i], 3)
    pp.pprint(roundCounts)
    pp.pprint(AV_by_position)

    return AV_by_position

def write_to_CSV(AV_by_position):
    with open('draft_data_clean_with_undrafted.csv', 'w', encoding='utf-8') as g:
        writer = csv.writer(g)
        writer.writerow(["Position", "Round 1", "Round 2", "Round 3",
                         "Round 4", "Round 6-8", "Rounds 9-12", "Undrafted"])
        toWrite = []
        for pos in AV_by_position:
            g1 = AV_by_position[pos].get(1, 0)
            g2 = AV_by_position[pos].get(2, 0)
            g3 = AV_by_position[pos].get(3, 0)
            g4 = AV_by_position[pos].get(4, 0)
            g5 = 0
            for i in range(5, 9):
                g5 += AV_by_position[pos].get(i, 0)
            g9 = 0
            for i in range(9, 13):
                g9 += AV_by_position[pos].get(i, 0)
            g0 = AV_by_position[pos].get(0, 0)
            toWrite.append([pos, g1, g2, g3, g4, g5, g9, g0])

        toWrite.sort(key=lambda item: item[1] + item[2] + item[3] + item[4]
                     + item[5] + item[6] + item[7])
        print(toWrite)
        for row in toWrite:
            writer.writerow(row)


def main():
    counts = get_average_AV()
    write_to_CSV(counts)


if __name__ == '__main__':
    main()

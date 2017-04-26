import csv
import pprint

pp = pprint.PrettyPrinter(indent=4)

def get_average_AV():
    AV_by_position = {}
    roundCounts = {}
    for i in range(0, 12):
        roundCounts[i + 1] = {}
    with open('draft_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for line in reader:
            position = line[5]
            AV_by_position[position] = AV_by_position.get(position, {})
            rd = int(line[1])
            if line[9] == '':
                continue
            endYear = int(line[7]) if line[7] != '' else 2017
            AV = round(float(line[9])/(endYear + 1 - int(line[0])), 3)
            AV_by_position[position][rd] = AV + AV_by_position[position].get(rd, 0)
            roundCounts[rd][position] = 1 + roundCounts[rd].get(position, 0)
    pp.pprint(AV_by_position)
    for pos in AV_by_position:
        counts = AV_by_position[pos]
        for i in range(0, 12):
            if i + 1 in counts:
                counts[i + 1] /= roundCounts[i + 1][pos]
                counts[i + 1] = round(counts[i + 1], 3)
    pp.pprint(roundCounts)
    pp.pprint(AV_by_position)

    return AV_by_position

def write_to_CSV(AV_by_position):
    with open('draft_data_clean.csv', 'w', encoding='utf-8') as g:
        writer = csv.writer(g)
        writer.writerow(["Position", "Round 1", "Round 2", "Rounds 3-6", "Rounds 7-12"])
        toWrite = []
        for pos in AV_by_position:
            g1 = AV_by_position[pos].get(1, 0)
            g2 = AV_by_position[pos].get(2, 0)
            g3 = AV_by_position[pos].get(3, 0)
            for i in range(4, 7):
                g3 += AV_by_position[pos].get(i, 0)
            g4 = AV_by_position[pos].get(7, 0)
            for i in range(8, 13):
                g4 += AV_by_position[pos].get(i, 0)
            if g1 != 0 and g2 != 0 and g3 != 0 and g4 != 0:
                toWrite.append([pos, g1, g2, g3, g4])
                # writer.writerow([pos, g1, g2, g3, g4])

        toWrite.sort(key=lambda item: item[1] + item[2] + item[3] + item[4])
        print(toWrite)
        for row in toWrite:
            writer.writerow(row)


def main():
    counts = get_average_AV()
    write_to_CSV(counts)


if __name__ == '__main__':
    main()

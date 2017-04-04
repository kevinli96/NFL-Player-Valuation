import csv

def main():
    with open('draft_1980_1993.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Year","Rnd","Pick","Tm","Player","Pos","Age","To","St","CarAV","DrAV","G"])
        for year in range(1980, 1994):
            with open('draft_' + str(year) + '.csv', 'r') as g:
                reader = csv.reader(g)
                for line in reader:
                    if (len(line[3].split("\\")) > 1):
                        line[3] = line[3].split("\\")[0]
                    line = [x.replace(' HOF', '') for x in line]
                    writer.writerow([year] + line)

if __name__ == '__main__':
    main()

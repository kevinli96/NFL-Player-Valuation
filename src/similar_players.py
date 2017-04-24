#!/usr/bin/env python3
import csv
import argparse
import numpy as np
from sklearn.preprocessing import scale
from sklearn.neighbors import NearestNeighbors

def parse_args():
    parser = argparse.ArgumentParser(description='Similar player engine')
    parser.add_argument('-train', help='Path to csv file with training data', default='..\\data\\similar_players_data.csv')
    parser.add_argument('-test', help='Path to csv file with test data', default='test_players.csv')
    parser.add_argument('-k', help='Number of neighbors', default=5)
    parser.add_argument('-pos', help='Only return players with the same position', default=False)
    parser.add_argument('-zero', help='Ignore combine values that are zero when finding nearest neighbors', default=False)
    return parser.parse_args()

def similar_players(feature_set, test_set, k, pos, zero, av_list):

    test_keys = []
    test_values = []
    non_zero_index = []
    for key, value in test_set.items():
        test_keys.append(key)
        if zero:
            v = []
            for i in range(len(value)):
                if float(value[i]) != 0:
                    v.append(value[i])
                    non_zero_index.append(i)
            test_values.append(v)
        else:
            test_values.append(value)
    test_num_values = len(test_values[0])
    test_values_array = np.array(test_values)

    position = test_keys[0][1]
    position_set = get_position_set(position)

    feature_keys = []
    feature_values = []
    for key, value in feature_set.items():
        if zero:
            if pos:
                if key[2] in position_set:
                    feature_keys.append(key)
                    v = []
                    for i in non_zero_index:
                        v.append(value[i])
                    feature_values.append(v)
            else:
                feature_keys.append(key)
                v = []
                for i in non_zero_index:
                    v.append(value[i])
                feature_values.append(v)
        else:
            if pos:
                if key[2] in position_set:
                    feature_keys.append(key)
                    feature_values.append(value)
            else:
                feature_keys.append(key)
                feature_values.append(value)
    feature_num_values = len(feature_values[0])
    feature_values_array = np.array(feature_values)

    if feature_num_values != test_num_values:
        print("ERROR: Mismatch between length of feature set and test set.")
        return

    nbrs = NearestNeighbors(n_neighbors=int(k), algorithm='ball_tree').fit(feature_values_array)
    similar_players = nbrs.kneighbors(test_values_array)

    print("Similar players to " + str(test_keys[0]) + ":")
    sum_av = 0
    for index in similar_players[1][0]:
        sum_av += float(feature_keys[index][1])
        print(feature_keys[index])

    average_av = sum_av/float(k)
    print("\nPredicted average seasonal AV:")
    print(str(average_av) + "\n")

    av_list.append((test_keys[0][0], test_keys[0][1], average_av))

def get_position_set(position_id):
    position_set = None

    if position_id == "NT" or position_id == "DT":
        position_set = {"DT", "NT", "DL"}
    elif position_id == "DE" or position_id == "OLB":
        position_set = {"DE", "OLB", "DL", "LB"}
    elif position_id == "S" or position_id == "FS" or position_id == "SS":
        position_set = {"S", "SS", "FS", "DB"}
    elif position_id == "CB":
        position_set = {"CB", "DB"}
    elif position_id == "DB":
        position_set = {"S", "SS", "FS", "DB", "CB"}
    elif position_id == "LB":
        position_set = {"LB","ILB","OLB"}
    elif position_id == "ILB":
        position_set = {"LB","ILB"}
    elif position_id == "OL":
        position_set = {"OG","OT","C","OL"}
    elif position_id == "OG":
        position_set = {"OG", "OL"}
    elif position_id == "OT":
        position_set = {"OT","OL"}
    elif position_id == "C":
        position_set = {"C","OL"}
    elif position_id == "RB" or position_id == "FB":
        position_set = {"RB","FB"}
    elif position_id == "DL":
        position_set = {"DE","DT","DL"}
    else:
        position_set = {position_id}

    return position_set

def main():
    args = parse_args()

    featureSet = {}
    with open(args.train, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            player_name = row[0]
            av = row[1]
            position = row[5]
            featureSet[(player_name, av, position)] = row[6:]

    testSet = {}
    with open(args.test, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            player_name = row[0]
            position = row[4]
            testSet[(player_name, position)] = row[5:]

    av_list = []

    for key, value in testSet.items():
        test_values = {key: value}
        similar_players(featureSet, test_values, args.k, args.pos, args.zero, av_list)

    sorted_list = sorted(av_list, key=lambda player: player[2], reverse=True)

    for item in sorted_list:
        print(item)

if __name__ == '__main__':
    main()

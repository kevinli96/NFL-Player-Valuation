import csv
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from collections import defaultdict
from numpy import mean, var


positions = ['K', 'LB', 'OG', 'P', 'C', 'OT', 'LS', 'TE', 'DE', 'UTIL', 
             'DL', 'DB', 'QB', 'WR', 'DT', 'OL', 'RB']

stat_labels = ['count', 'mean', 'max', 'var', 'sum']
stat_labels = ['count', 'mean', 'max', 'sum']  # NOTE: remove
stat_fxns = [len, mean, max, var, sum]
stat_fxns = [len, mean, max, sum]  # NOTE: remove
feature_labels = [p + '_' + s for p in positions 
                  for s in stat_labels] + ['total']
label_order = None

def load_features(filepath, header=False):

    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        if header is True:
            next(reader)
        result = [row for row in reader]

    return result


def load_labels(filepath):

    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        rosters = []
        wc = []
        d = []
        c = []
        sl = []
        sw = []
        next(reader)
        for row in reader:
            rosters.append((row[0], row[1]))
            wc.append(int(row[8]))
            d.append(int(row[9]))
            c.append(int(row[10]))
            sl.append(int(row[11]))
            sw.append(int(row[12]))


    return rosters, wc, d, c, sl, sw


def transform_features(raw_features, roster_order):

    rosters = defaultdict(lambda: defaultdict(list))

    # Group players by roster
    for player in raw_features:
        roster_id = (player[1], player[2]) 
        pos = player[5]
        av = int(player[15])
        rosters[roster_id][pos].append(av)


    # Calculate roster statistics
    stats = []

    for roster_id in roster_order:
        composition = []
        total = 0
        for pos in positions:
            pos_players = rosters[roster_id][pos]
            num_players = len(pos_players)

            total += num_players
            if num_players > 0:
                for stat, f in zip(stat_labels, stat_fxns):
                    composition.append(f(pos_players))
            else:
                composition.extend([0] * len(stat_labels))

        composition.append(total)
        stats.append(composition)

    return stats

def transform_test_features(raw_features):
    '''
    Compute position-wise roster statistics for a parsed roster csv
    Input: csv.reader() output, formatted as in roster_data.csv
    Output: roster statsitics ordered by 'feature_labels'
    '''
    players = defaultdict(list)

    # Group players by position
    for player in raw_features:
        pos = player[5]
        av = int(player[-1])
        players[pos].append(av)

    # Calculate roster statistics
    composition = []
    total = 0
    for pos in positions:
        pos_players = players[pos]
        num_players = len(pos_players)

        total += num_players
        if num_players > 0:
            for stat, f in zip(stat_labels, stat_fxns):
                composition.append(f(pos_players))
        else:
            composition.extend([0] * len(stat_labels))

    composition.append(total)
    # stats.append(composition)

    return [composition]


if __name__ == '__main__':
    
    # Load data
    rosters, wc, div, conf, sbl, sbw = load_labels('../data/standings.csv')
    raw_features = load_features('../data/roster_data.csv', header=True)
    features = transform_features(raw_features, rosters)

    # Train
    wc_clf = RandomForestClassifier(n_estimators=2500, oob_score=True, 
                                    class_weight='balanced')
    div_clf = RandomForestClassifier(n_estimators=2500, oob_score=True, 
                                     class_weight='balanced')
    conf_clf = RandomForestClassifier(n_estimators=2500, oob_score=True, 
                                      class_weight='balanced')
    sbl_clf = RandomForestClassifier(n_estimators=2500, oob_score=True, 
                                     class_weight='balanced')
    sbw_clf = RandomForestClassifier(n_estimators=2500, oob_score=True, 
                                     class_weight='balanced')
    wc_clf.fit(features, wc)
    div_clf.fit(features, div)
    conf_clf.fit(features, conf)
    sbl_clf.fit(features, sbl)
    sbw_clf.fit(features, sbw)

    classifiers = [wc_clf, div_clf, conf_clf, sbl_clf, sbw_clf]
    label_sets = [wc, div, conf, sbl, sbw]
    playoff_rounds = ['Wildcard', 'Divisional', 'Conference', 
                      'Superbowl', 'Championship']

    
    if len(sys.argv) > 1:
        # Predict playoff sucess
        test_features = transform_test_features(load_features(sys.argv[1]))
        print()
        roster_name = sys.argv[1].split('/')[-1]
        print('{} Standing Predictions:'.format(roster_name))
        print(79 * '-')

        for i in range(len(classifiers)):
            pred = classifiers[i].predict(test_features)[0]
            prob = max(classifiers[i].predict_proba(test_features)[0])
            # TODO: include probabilities
            results = [playoff_rounds[i], bool(pred), prob]
            print('{} Team Prediction: {} (Pr={})'.format(*results))

        if '-stats' in sys.argv:
            print()
            print("Roster Statistics: ")
            print(79 * '-')

            for l, f in zip(feature_labels, test_features[0]): 
                print('{}: {}'.format(l, f))

    else:
        # Validate
        print()
        for i in range(len(label_sets)):
            N = 1
            acc = []
            for trial in range(N):
                clf = RandomForestClassifier(n_estimators=2500, oob_score=True, 
                                             class_weight='balanced')
                acc.extend(cross_val_score(clf, features, label_sets[i], 
                                           scoring='accuracy', cv=10))
            acc = mean(acc)            
            print('{} Team Validation Accuracy: {}'.format(playoff_rounds[i], acc))


        # Get most important features
        for i in range(len(classifiers)):
            print()
            print('Top 10 {} Team Feature Importances: '.format(playoff_rounds[i]))
            print(79 * '-')
            raw_scores = classifiers[i].feature_importances_
            labeled_scores = list(zip(feature_labels, raw_scores))
            labeled_scores.sort(key=lambda x: -x[1])

            for j in range(10):
                print("{}: {}".format(labeled_scores[j][0], labeled_scores[j][1]))

import numpy
import csv
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score


def load_file(file_path, bin_quantiles=None):
    """
    Input: path to the draft data

    Output: training features, training labels for draft and career av, 
            testing set with features for 2016 draft picks and player names

    Arg file_path: path to the draft_data.cvs file formatted like 
                   TODO: where did we get this data?

    Param bin_quantiles: default = None, integer number of bins to apply 
                         to av labels
    """

    # Training set
    dr_av_labels = []
    car_av_labels = []
    training_features = []

    # Testing set
    test_features = []
    test_players = []

    # Set up preprocessing for text labels
    teams = ['CHI', 'BAL', 'WAS', 'TAM', 'CAR', 'SDG', 'OAK', 'CLE', 'ARI', 
             'SFO', 'NYJ', 'DET', 'NWE', 'IND', 'LAR', 'NOR', 'HOU', 
             'RAI', 'RAM', 'NYG', 'JAX', 'SEA', 'STL', 'PHI', 
             'MIN', 'DEN', 'DAL', 'TEN', 'MIA', 'KAN', 'CIN', 'PHO', 
             'GNB', 'BUF', 'PIT', 'ATL', 'LAC']

    positions = ['OLB', 'OL', 'LS', 'DB', 'T', 'DT', 'ILB', 'DE', 
                 'TE', 'WR', 'LB', 'CB', 'P', 'G', 'FS', 'KR', 
                 'SS', 'K', 'S', 'RB', 'QB', 'NT', 'C', 'FB', 'DL']

    team_le = LabelEncoder()
    pos_le = LabelEncoder()

    team_le.fit(teams)
    pos_le.fit(positions)

    # Read draft data file, create training and testing sets
    with open(file_path, 'r', encoding='latin1') as file_reader:
        reader = csv.reader(file_reader, delimiter=',', quotechar='"')
        next(reader)  # Skip the headers
        for row in reader:
            if all(row):  # Exclude data with missing fields
                yr = int(row[0])
                rd = int(row[1])
                pk = int(row[2])
                tm = team_le.transform([row[3]])[0]
                pl = row[4]
                pos = pos_le.transform([row[5]])[0]
                age = int(row[6])
                to = int(row[7])  # TODO: excluded from analysis, remove
                st = int(row[8]) # TODO: excluded from analysis, remove
                cav = int(row[9])
                dav = int(row[10])
                g = int(row[11])

                row_features = [rd, pk, tm, pos, age, g]
                row_features = [rd, pk, tm, pos, age]
                if yr < 2013:
                    training_features.append(row_features)
                    dr_av_labels.append(dav)
                    car_av_labels.append(cav)
                if yr == 2016:
                    test_features.append(row_features)
                    test_players.append(pl)

        if bin_quantiles is not None:
            dr_max = max(dr_av_labels)
            dr_min = min(dr_av_labels)
            dr_av_labels = [bin_quantile(av, dr_min, dr_max, bin_quantiles) 
                            for av in dr_av_labels]

            car_max = max(car_av_labels)
            car_min = min(car_av_labels)
            car_av_labels = [bin_quantile(av, car_min, car_max, bin_quantiles) 
                             for av in car_av_labels]

           
    return (training_features, dr_av_labels, car_av_labels, 
            test_features, test_players, team_le, pos_le)


def bin_quantile(x, low, high, n_bins):

    bin_size = (high - low) / n_bins
    quantile = ((x - low) // bin_size) + 1 

    return quantile


if __name__ == '__main__':

    # Path to the draft data NOTE: may need to be changed
    draft_data = "../data/draft_data.csv"

    # Load data w/ specified number of label bins
    (training_features, dr_av_labels, car_av_labels, 
     test_features, test_players, 
     team_le, pos_le) = load_file(draft_data, bin_quantiles=5)

    # Initialize classifiers
    dr_svm = LinearSVC()
    car_svm = LinearSVC()
    dr_nb = GaussianNB()
    car_nb = GaussianNB()
    dr_rf = RandomForestClassifier()
    car_rf = RandomForestClassifier()

    #Fit classifiers
    dr_svm.fit(training_features, dr_av_labels)
    dr_nb.fit(training_features, dr_av_labels)
    dr_rf.fit(training_features, dr_av_labels)
    car_svm.fit(training_features, car_av_labels)
    car_nb.fit(training_features, car_av_labels)
    car_rf.fit(training_features, car_av_labels)

    # plotting for debugging purposes
    # matplotlib.pyplot.hist(dr_av_labels)
    # matplotlib.pyplot.hist(car_av_labels)
    # matplotlib.pyplot.show()

    # Evaluate classifiers
    dr_svm_score = cross_val_score(dr_svm, training_features, 
                                   dr_av_labels, cv=10, scoring='accuracy')

    dr_nb_score = cross_val_score(dr_svm, training_features, 
                                  dr_av_labels, cv=10, scoring='accuracy')

    dr_rf_score = cross_val_score(dr_svm, training_features, 
                                  dr_av_labels, cv=10, scoring='accuracy')

    car_svm_score = cross_val_score(dr_svm, training_features, 
                                    dr_av_labels, cv=10, scoring='accuracy')

    car_nb_score = cross_val_score(dr_svm, training_features, 
                                   dr_av_labels, cv=10, scoring='accuracy')

    car_rf_score = cross_val_score(dr_svm, training_features, 
                                   dr_av_labels, cv=10, scoring='accuracy')


    print("10-fold cross-validation scores (draft av):")
    print("SVM: {}".format(numpy.average(dr_svm_score)))
    print("NB: {}".format(numpy.average(dr_nb_score)))
    print("RF: {}".format(numpy.average(dr_rf_score)))
    print()
    print("10-fold cross-validation scores (career av):")
    print("SVM: {}".format(numpy.average(car_svm_score)))
    print("NB: {}".format(numpy.average(car_nb_score)))
    print("RF: {}".format(numpy.average(car_rf_score)))

    # Predict draft and career av values for 2016 draft
    # Random Forest:
    
    dr_av_pred = dr_rf.predict(test_features)
    car_av_pred = car_rf.predict(test_features)
    
    #Print results
    col_width = max(max([len(name) for name in test_players]), 
                    len("Pred. CarAV Qtl")) + 2  # Print columns nicely
    
    header = ["Name", "Round", "Pick", "Team", "Position", 
              "Pred. DrAV Qtl", "Pred. CarAV Qtl"]

    print()
    print(''.join(w.ljust(col_width) for w in header))

    for i in range(0, len(test_players)): 
        nm = test_players[i]
        rd = test_features[i][0]
        pk = test_features[i][1]
        tm = team_le.inverse_transform([test_features[i][2]])[0]
        pos = pos_le.inverse_transform([test_features[i][3]])[0]
        dr_pq = dr_av_pred[i]
        car_pq = car_av_pred[i]
        row = [nm, rd, pk, tm, pos, dr_pq, car_pq]

        print(''.join(str(w).ljust(col_width) for w in row))

import csv
import sys
import copy

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
#     if len(sys.argv) != 2:
#         sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(r"shopping.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    file = open(filename)
    type(file)

    data = csv.reader(file)
    header = []
    header = next(data)
    l = len(header) - 1
    data_copy = data
    evidence = []
    labels = []
    for row in data_copy:
        convert_int = [0, 2, 4, 11, 12, 13, 14]
        for i in convert_int:
            row[i] = (int)(row[i])
        
        if row[15] == 'Returning_Visitor':
            row[15] = 1
        else:
            row[15] = 0
        
        if row[16] == 'FALSE':
            row[16] = 0
        else:
            row[16] = 1
        
        convert_float = [1, 3, 5, 6, 7, 8, 9]
        for i in convert_float:
            row[i] = (float)(row[i])
        
        months = {'Jan' : 0,
        'Feb' : 1,
        'Mar' : 2,
        'Apr' : 3,
        'May' : 4,
        'June' : 5,
        'Jul' : 6,
        'Aug' : 7,
        'Sep' : 8,
        'Oct' : 9,
        'Nov' : 10,
        'Dec' : 11
        }
        row[10] = months[row[10]]

        evidence.append(row[0:l])
        
        if row[l] == "FALSE":
            labels.append(0)
        else:
            labels.append(1)

    evidence = list(evidence)
    labels = list(labels)
    
    return(evidence, labels)
    # raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence, labels)
    return neigh
    # raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    tn, fp, fn, tp = confusion_matrix(labels, predictions).ravel()
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)

    return (sensitivity, specificity)
    # raise NotImplementedError


if __name__ == "__main__":
    main()

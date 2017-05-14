# create a decision tree that classifies people into male or female based on body weight

from sklearn import tree, svm
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

def cfl_decision_tree(measurements, labels):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(measurements, labels)
    prediction = clf.predict(measurements)
    accuracy = accuracy_test(labels, prediction)
    return { 'DT' : accuracy}

def cfl_gaussianNB(measurements, labels):
    cfl = GaussianNB()
    cfl = cfl.fit(measurements, labels)
    prediction = cfl.predict(measurements)
    accuracy = accuracy_test(labels, prediction)
    return { 'GNB' : accuracy}

def cfl_svm(measurements, labels):
    # Create an svm model
    cfl = svm.SVC()
    # Train the model
    cfl = cfl.fit(measurements, labels)
    # predict
    prediction = cfl.predict( measurements )
    accuracy = accuracy_test(labels, prediction)
    return { 'svm' : accuracy}


def near_centroid(measurements, labels):
    cfl = NearestCentroid()
    cfl = cfl.fit(measurements,labels)
    prediction = cfl.predict(measurements)
    accuracy = accuracy_test(labels, prediction)
    return { 'nc': accuracy}



def accuracy_test(expected, prediction):
    # Calculate the accuracy of the model
    accurace = accuracy_score(expected, prediction)
    return accurace


def main():

    # lists of lists where each list contains the following items
    # [ height, weight, shoe_size ]

    measurements = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37], [166, 65, 40],
                    [190, 90, 47], [175, 64, 39], [177, 70, 40], [159, 55, 37], [171, 75, 42], [181, 85, 43]]

    # List of labels of each list

    labels = ['male', 'male', 'female', 'female', 'male', 'male', 'female', 'female',
         'female', 'male', 'male']

    accuracy  = cfl_svm(measurements, labels)
    accuracy.update( near_centroid(measurements, labels) )
    accuracy.update( cfl_gaussianNB(measurements, labels) )
    accuracy.update( cfl_decision_tree(measurements, labels) )

    # Print the Dictionary ranked (sorted by value) in reverse
    print sorted(accuracy.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    main()









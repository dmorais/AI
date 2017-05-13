# create a decision tree tha classifies people into male or female based on body weight

from sklearn import tree

# lists of lists where each list contains the following items
# [ height, weight, shoe_size ]

measurements = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37], [166, 65, 40],
     [190, 90, 47], [175, 64, 39], [177, 70, 40], [159, 55, 37], [171, 75, 42], [181, 85, 43]]

# List of labels of each list

labels = ['male', 'male', 'female', 'female', 'male', 'male', 'female', 'female',
     'female', 'male', 'male']

# var store the decision tree model
clf = tree.DecisionTreeClassifier()

# The fit method is reponsible for training the classifier
# It receives the data and the labels as args

clf = clf.fit(measurements, labels)

# The method predict classify (or predicts) the gender of our data

prediction = clf.predict( [[190,70,43]])

# print prediction
print prediction






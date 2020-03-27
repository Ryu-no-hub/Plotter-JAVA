import pandas
from numpy import mean
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import scale

data = pandas.read_csv('C:/Users/Andrew/Desktop/wine.data', names=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
wclass = data[1]
print(wclass.head())
data = data.drop(1, axis=1)
print(data.head())

for i in range(50):
    clf = KNeighborsClassifier(i+1)
    clf.fit(data, wclass)
    kfold = KFold(shuffle=True, random_state=42)
    scores = cross_val_score(clf, data, wclass, cv=kfold, scoring='accuracy')
    print('i =', i+1, mean(scores))

scaled_data = scale(data)
print(type(scaled_data))
print(scaled_data)

for i in range(50):
    clf = KNeighborsClassifier(i+1)
    clf.fit(scaled_data, wclass)
    kfold = KFold(shuffle=True, random_state=42)
    scores = cross_val_score(clf, scaled_data, wclass, cv=kfold, scoring='accuracy')
    print('i =', i+1, mean(scores))

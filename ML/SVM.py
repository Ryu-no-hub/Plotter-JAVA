import pandas as pd
from sklearn.svm import SVC

data = pd.read_csv('C:/Users/Andrew/Desktop/svm-data.csv', header=None, names=[0, 1, 2])
target = data[0]
data = data.drop(0, axis=1)
print(data)

clf = SVC(kernel='linear', C=100000, random_state=241)
clf.fit(data, target)
print(clf.support_)

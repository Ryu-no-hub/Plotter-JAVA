from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas as pd

'''X = np.array([[1, 2], [3, 4], [5, 6]])
y = np.array([-3, 1, 10])
clf = RandomForestRegressor(n_estimators=100)
clf.fit(X, y)
print(clf.predict(X))

print(r2_score(y, clf.predict(X)))'''

data = pd.read_csv('C:/Users/Andrew/Desktop/abalone.csv')
data['Sex'] = data['Sex'].map(lambda x: 1 if x == 'M' else (-1 if x == 'F' else 0))

X = data.iloc[:, :(len(data.columns)-1)]
y = data.iloc[:, -1]

for i in range(49):
    clf = RandomForestRegressor(i+1, random_state=1)
    k = KFold(shuffle=True, random_state=1)
    score = cross_val_score(clf, X, y, scoring='r2', cv=k)
    print('i =', i+1, 'score =', np.mean(score))
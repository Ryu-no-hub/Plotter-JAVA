from sklearn.neighbors import KNeighborsRegressor
import sklearn.datasets
from numpy import mean

data = sklearn.datasets.load_boston()
target = data.target
data = sklearn.preprocessing.scale(data.data)
print(data)
print(target)

for p in range(180):
    clf = KNeighborsRegressor(metric='minkowski', p=(p+20)/20, weights='distance')
    clf.fit(data, target)
    num = sklearn.model_selection.KFold(shuffle=True, random_state=42)
    scores = sklearn.model_selection.cross_val_score(clf, data, target, cv=num, scoring='neg_mean_squared_error')
    print('p =', (p+20)/20, 'Cross validation score =', mean(scores))


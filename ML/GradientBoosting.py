from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
import numpy as np

import matplotlib.pyplot as plt
#%matplotlib inline

data = pd.read_csv('C:/Users/Andrew/Desktop/gbm-data.csv')
X = data.iloc[:, 1:]
y = data.iloc[:, 0]
print(X)
X = X.to_numpy()
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=241)
for i in [1, 0.5, 0.3, 0.2, 0.1]:
    print('learning rate =', i)
    clf = GradientBoostingClassifier(n_estimators=250, verbose=True, random_state=241, learning_rate=i)
    clf.fit(X_train, y_train)

    test_loss = list()
    train_loss = list()
    for i, y_pred in enumerate(clf.staged_decision_function(X_test)):
        y_pred = 1.0 / (1.0 + np.exp(-y_pred))
        test_loss.append([log_loss(y_test, y_pred)])

    for i, y_pred in enumerate(clf.staged_decision_function(X_train)):
        y_pred = 1.0 / (1.0 + np.exp(-y_pred))
        train_loss.append([ log_loss(y_train, y_pred)])

    test_loss = pd.DataFrame(test_loss, columns=['loss'])
    train_loss = pd.DataFrame(train_loss, columns=['loss'])
    print('test_loss =', test_loss)
    print('train_loss =', train_loss)

    print(test_loss[test_loss.loss == test_loss.loss.min()])

    plt.figure()
    plt.plot(test_loss, 'r', linewidth=2)
    plt.plot(train_loss, 'g', linewidth=2)
    plt.legend(['test', 'train'])

plt.show()
clf2 = RandomForestClassifier(n_estimators=36, random_state=241)
clf2.fit(X_train, y_train)
rf_predict = clf2.predict_proba(X_test)
print('rf_predict:\n', rf_predict)
print(log_loss(y_test, rf_predict))

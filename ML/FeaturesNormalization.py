import numpy as np
import pandas as pd
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

train = pd.read_csv('C:/Users/Andrew/Desktop/perceptron-train.csv', header=None)
train.columns = [0, 1, 2]
train_target = train[0]
print(train)
train_data = train.drop(0, axis=1)
test = pd.read_csv('C:/Users/Andrew/Desktop/perceptron-test.csv', header=None, names=[0, 1, 2])
test_target = test[0]
test_data = test.drop(0, axis=1)
print(train.head())
print()
print(test.head())

clf = Perceptron(random_state=241)
clf.fit(train_data, train_target)
predictions = clf.predict(test_data)
#print(predictions)
scores = accuracy_score(test_target, predictions)
print('Scores =', scores)

print('After scaling:')
scaler = StandardScaler()
train_data_Scaled = scaler.fit_transform(train_data)
test_data_Scaled = scaler.transform(test_data)
clf2 = Perceptron()
clf2.fit(train_data_Scaled, train_target)
predictions = clf2.predict(test_data_Scaled)
#print(predictions)
scores2 = accuracy_score(test_target, predictions)
print('Scores =', scores2)
print(scores2 - scores)
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('C:/Users/Andrew/Desktop/titanic.csv', index_col='PassengerId')

data = data[['Pclass', 'Fare', 'Age', 'Sex', 'Survived']]
data = data.dropna(axis=0)

survived = data['Survived']
data = data[['Pclass', 'Fare', 'Age', 'Sex']]

data = data.replace(['male', 'female'], [1, 0])
print(data)
print(survived)

clf = DecisionTreeClassifier(random_state=241)
clf.fit(data, survived)
print(clf.feature_importances_)

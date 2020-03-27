import pandas
from collections import Counter

data = pandas.read_csv('C:/Users/Andrew/Desktop/titanic.csv', index_col='PassengerId')
mean_age, median_age = 0, 0
female_names = []
m = data['Sex'].value_counts()
print(m)
a = data['Survived'].value_counts()
alive = a[1]/(a[1]+a[0])
print(a)

b = data['Pclass'].value_counts()
first_class = b[1]/(b[1]+b[2]+b[3])

for i, j in data.iterrows():
    if j['Name'].find("Miss") != -1:
        name = j['Name']
        for s in name[name.find("Miss")+5:].split():
            female_names.append(s.strip('()"'))

    if j['Name'].find("Mrs") != -1:
        name = j['Name']
        for s in name[name.find("Mrs")+4:].split():
            female_names.append(s.strip('()"'))

print(round(alive*100, 2))
print(round(first_class*100, 2))
print(round(data['Age'].mean(), 2), round(data['Age'].median(), 2))
print(round(data['SibSp'].corr(data['Parch'], method="pearson"), 2))
print(female_names, len(female_names))
c = Counter(female_names)
print(c, len(c))

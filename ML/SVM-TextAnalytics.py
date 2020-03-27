import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn import datasets
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

newsgroup = datasets.fetch_20newsgroups(subset='all',
                                        categories=['alt.atheism', 'sci.space'])
data = newsgroup.data
target = newsgroup.target
print(len(data))
vectoriser = TfidfVectorizer()
data = vectoriser.fit_transform(data)

grid = {'C': np.power(10.0, np.arange(-5, 6))}
cv = KFold(n_splits=5, shuffle=True, random_state=241)
clf = SVC(kernel='linear', random_state=241)
#gs = GridSearchCV(clf, grid, scoring='accuracy', cv=cv)
#gs.fit(data, target)
#C = gs.best_params_['C']
#print('C =', C)

clf2 = SVC(kernel='linear', C=1.0, random_state=241)
clf2.fit(data, target)
result = clf2.coef_
print(result)

#data2 = pd.DataFrame(np.transpose(result.toarray()), index=np.asarray(vectoriser.get_feature_names()), columns=['col1'])
#data3 = abs(data2).sort_values(by=['col1'])
data2 = pd.DataFrame(result.toarray().transpose())
top10 = abs(data2).sort_values([0], ascending=False).head(10)

#top10 = top10.iloc[:, 0]
indices = top10.index
words=[]
feature_mapping = vectoriser.get_feature_names()
for i in indices:
    words.append(feature_mapping[i])

print(sorted(words))
#print('data3 =', top10)
#print(data3[28381])
#keys = top10.keys()
#print(keys, type(keys))
#result = []
#for i in range(10):
#    result.append(keys[-i])
#result.sort()
#print(result)
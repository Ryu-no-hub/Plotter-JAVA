import pandas as pd
import numpy
from sklearn.decomposition import PCA

data = pd.read_csv('C:/Users/Andrew/Desktop/close_prices.csv')
dji = pd.read_csv('C:/Users/Andrew/Desktop/djia_index.csv')
#data.drop('date', axis=1, inplace=True)
data = data.iloc[:, 1:]
dji = dji.iloc[:, 1:]
print(data)
#print(type(dji), len(dji))

pca = PCA(10)
pca.fit(data)

#print('pca.explained_variance_ratio:', pca.explained_variance_ratio_)
#print('pca.components_:', pca.components_)
firstcomp = pd.DataFrame(pca.transform(data)[:, 0])
print(firstcomp)
print(type(firstcomp), len(firstcomp))
print(numpy.corrcoef(firstcomp.T, dji.T))
indx = -1
value = -1
for i in range(len(pca.components_[0])):
    if value < pca.components_[0][i]:
        value = pca.components_[0][i]
        indx = i
print("Company name: '%s' weight: %0.2f" % (data.columns[indx], value))
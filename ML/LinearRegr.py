from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.linear_model import Ridge
from sklearn.feature_extraction import DictVectorizer
import pandas as pd

data = pd.read_csv('C:/Users/Andrew/Desktop/salary-train.csv')
data_test = pd.read_csv('C:/Users/Andrew/Desktop/salary-test-mini.csv')
y = data['SalaryNormalized']


data['FullDescription'].str.lower().replace('[^a-zA-Z0-9]', ' ', regex=True, inplace=True)
data_test['FullDescription'].str.lower().replace('[^a-zA-Z0-9]', ' ', regex=True, inplace=True)
data['LocationNormalized'].fillna('nan', inplace=True)
data_test['LocationNormalized'].fillna('nan', inplace=True)
data['ContractTime'].fillna('nan', inplace=True)
data_test['ContractTime'].fillna('nan', inplace=True)

vectorizer = TfidfVectorizer(min_df=2) #Только слова, встречающиеся хотя бы в 5 объектах
desc_vect = vectorizer.fit_transform(data['FullDescription'])
print(desc_vect)
desc_test_vect = vectorizer.transform(data_test['FullDescription'])

enc = DictVectorizer()
data_categ = enc.fit_transform(data[['LocationNormalized', 'ContractTime']].to_dict('records'))
data_test_categ = enc.transform(data_test[['LocationNormalized', 'ContractTime']].to_dict('records'))
X = hstack([desc_vect, data_categ])

X_test = hstack([desc_test_vect, data_test_categ])

clf = Ridge(alpha=1, random_state=241)
clf.fit(X, y)
print(clf.predict(X_test))

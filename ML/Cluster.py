from skimage.io import imread
from skimage import img_as_float
import pylab
import numpy as np
import pandas as pd
import sklearn.cluster

image = imread('C:/Users/Andrew/Desktop/parrots.jpg')
x, y, z = image.shape
print(image)
print('\n', x, y, z, '\n')
objects_features_matrix = np.reshape(image, (x * y, z))
print(objects_features_matrix, len(objects_features_matrix))

clf = sklearn.cluster.KMeans(init='k-means++', random_state=241)
clf.fit(objects_features_matrix)
df = pd.DataFrame(image)
df['Cluster'] = clf.predict(df)
print(df)
#image = img_as_float(image)
#print(image)
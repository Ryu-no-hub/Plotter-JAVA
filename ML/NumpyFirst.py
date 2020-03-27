import numpy as np

X = np.random.normal(loc=50, scale=10, size=(1000, 50))
m = np.mean(X, axis=0)
std = np.std(X, axis=0)
X_norm = ((X-m)/std)
print(X_norm)
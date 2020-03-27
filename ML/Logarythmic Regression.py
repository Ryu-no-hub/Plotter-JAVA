import math
import numpy as np
from sklearn.metrics import roc_auc_score
import pandas as pd

data = pd.read_csv('C:/Users/Andrew/Desktop/data-logistic.csv', header=None)
y = data[0]
X = data.loc[:, 1:]
x1 = X[1]
x2 = X[2]

def logregr(x1, x2, y, C):
    delta = 1e-5
    k = 0.1
    l = len(y)
    w1, w2, n = 0, 0, 0
    while n < 10000:
        n += 1
        w1old, w2old = w1, w2
        sum_w1 = np.sum(y * x1 * (1 - 1 / (1 + np.exp(-y * (x1 * w1 + x2 * w2)))))
        sum_w2 = np.sum(y * x2 * (1 - 1 / (1 + np.exp(-y * (x1 * w1 + x2 * w2)))))
        w1 = w1 + (k/l)*sum_w1 - k*C*w1
        w2 = w2 + (k/l)*sum_w2 - k*C*w2
        weights_distance = math.sqrt((w1 - w1old)**2 + (w2 - w2old)**2)
        print('n =', n, 'weights_distance =', weights_distance)
        if weights_distance < delta:
            break
    return w1, w2

w1, w2 = logregr(x1, x2, y, 0)
rw1, rw2 = logregr(x1, x2, y, 10.0)
print(w1, w2)
print(rw1, rw2)
score = roc_auc_score(y, 1/(1 + np.exp(-w1*x1 - w2*x2)))
rscore = roc_auc_score(y, 1/(1 + np.exp(-rw1*x1 - rw2*x2)))
print(round(score, 3), round(rscore, 3))

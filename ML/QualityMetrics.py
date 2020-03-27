import pandas
import math
import sklearn.metrics
data = pandas.read_csv('C:/Users/Andrew/Desktop/classification.csv')
scores = pandas.read_csv('C:/Users/Andrew/Desktop/scores.csv')
print(data)
TP, FP, FN, TN = 0, 0, 0, 0
for i in range(len(data)):
    t = data.loc[i]['true']
    p = data.loc[i]['pred']
    if t and p:
        TP+=1
    elif t and not p:
        FN+=1
    elif not t and p:
        FP+=1
    elif not t and not p:
        TN+=1
print(TP, FP, FN, TN)

accuracy = sklearn.metrics.accuracy_score(data['true'], data['pred'])
precision = sklearn.metrics.precision_score(data['true'], data['pred'])
recall = sklearn.metrics.recall_score(data['true'], data['pred'])
f1 = sklearn.metrics.f1_score(data['true'], data['pred'])
print(accuracy, precision, recall, f1)
score_logreg = sklearn.metrics.roc_auc_score(scores['true'], scores['score_logreg'])
scores_svm = sklearn.metrics.roc_auc_score(scores['true'], scores['score_svm'])
score_knn = sklearn.metrics.roc_auc_score(scores['true'], scores['score_knn'])
score_tree = sklearn.metrics.roc_auc_score(scores['true'], scores['score_tree'])
print(score_logreg, scores_svm, score_knn, score_tree)

prc_log = sklearn.metrics.precision_recall_curve(scores['true'], scores['score_logreg'])
prc_svm = sklearn.metrics.precision_recall_curve(scores['true'], scores['score_svm'])
prc_knn = sklearn.metrics.precision_recall_curve(scores['true'], scores['score_knn'])
prc_tree = sklearn.metrics.precision_recall_curve(scores['true'], scores['score_tree'])


for i in range(len(prc_log[1])):
    if prc_log[1][i] < 0.7:
        log_result = max(prc_log[0][:i])
        break

for i in range(len(prc_svm[1])):
    if prc_svm[1][i] < 0.7:
        svm_result = max(prc_svm[0][:i])
        break

for i in range(len(prc_knn[1])):
    if prc_knn[1][i] < 0.7:
        knn_result = max(prc_knn[0][:i])
        break

for i in range(len(prc_tree[1])):
    if prc_tree[1][i] < 0.7:
        tree_result = max(prc_tree[0][:i])
        break

print(log_result, svm_result, knn_result, tree_result)


import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

pd.set_option('display.max_columns', None)
dataframe = pd.read_csv('features.csv', index_col='match_id')
dataframe.head()
dataframe.drop(["duration", "tower_status_radiant", "tower_status_dire", "barracks_status_radiant",
                "barracks_status_dire", ], axis=1, inplace=True)
countna = len(dataframe) - dataframe.count()
print(countna[countna > 0].sort_values(ascending=False))
dataframe.fillna(0, inplace=True)

X_train = dataframe.drop("radiant_win", axis=1)
y_train = dataframe["radiant_win"]

CV = KFold(n_splits=5, shuffle=True, random_state=42)


def score_trees(X: pd.DataFrame, y: pd.Series) -> pd.Series:
    scores = {}

    for n_estimators in [10, 20, 30, 50]:
        print(f"n_estimators={n_estimators}")
        model_trees = GradientBoostingClassifier(n_estimators=n_estimators, random_state=42)

        start_time = datetime.datetime.now()
        score = cross_val_score(model_trees, X, y, cv=CV, scoring="roc_auc", n_jobs=-1).mean()
        print(f"Score: {score:.3f}")
        print(f"Time elapsed: {datetime.datetime.now() - start_time}")

        scores[n_estimators] = score
        print()

    return pd.Series(scores)


scores = score_trees(X_train, y_train)

scaler = StandardScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), index=X_train.index, columns=X_train.columns)


def score_linear(X: pd.DataFrame, y: pd.Series) -> pd.Series:
    scores = {}

    for i in range(-5, 6):
        C = 10.0 ** i

        print(f"C={C}")
        model = LogisticRegression(C=C, random_state=42)

        start_time = datetime.datetime.now()
        score = cross_val_score(model, X, y, cv=CV, scoring="roc_auc", n_jobs=-1).mean()
        print(f"Score: {score:.3f}")
        print(f"Time elapsed: {datetime.datetime.now() - start_time}")

        scores[i] = score
        print()

    return pd.Series(scores)


def best_linear_score(scores: pd.Series):
    best_iter = scores.sort_values(ascending=False).head(1)
    best_C = 10.0 ** best_iter.index[0]
    print(f"best_iter.index[0] = {best_iter.index}")
    best_score = best_iter.values[0]

    print(f"Наилучшее значение AUC-ROC при C = {best_C:.2f} равно {best_score:.2f}.")


best_linear_score(scores)

hero_columns = [f"r{i}_hero" for i in range(1, 6)] + [f"d{i}_hero" for i in range(1, 6)]
cat_columns = ["lobby_type"] + hero_columns
X_train.drop(cat_columns, axis=1, inplace=True)
scores = score_linear(X_train, y_train)
best_linear_score(scores)

unique_heroes = np.unique(dataframe[hero_columns].values.ravel())
N = max(unique_heroes)
print(f"Число уникальных героев в train: {len(unique_heroes)}. Максимальный ID героя: {N}.")


def pick(data: pd.DataFrame) -> pd.DataFrame:
    X_pick = np.zeros((data.shape[0], N))

    for i, match_id in enumerate(data.index):
        for p in range(1, 6):
            X_pick[i, data.loc[match_id, f"r{p}_hero"] - 1] = 1
            X_pick[i, data.loc[match_id, f"d{p}_hero"] - 1] = -1

    return pd.DataFrame(X_pick, index=data.index, columns=[f"hero_{i}" for i in range(N)])


X_pick = pick(dataframe)
X_pick.head()
X_train = pd.concat([X_train, X_pick], axis=1)

scores = score_linear(X_train, y_train)
best_linear_score(scores)
model = LogisticRegression(C=0.1, random_state=42)
model.fit(X_train, y_train)

testframe = pd.read_csv("features_test.csv", index_col="match_id")
testframe.fillna(0, inplace=True)

X_test = pd.DataFrame(scaler.transform(testframe), index=testframe.index, columns=testframe.columns)
X_test.drop(cat_columns, axis=1, inplace=True)
X_test = pd.concat([X_test, pick(testframe)], axis=1)
X_test.head()

predictions = pd.Series(model.predict_proba(X_test)[:, 1])
print(predictions.describe())

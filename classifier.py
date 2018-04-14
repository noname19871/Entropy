from sklearn.model_selection import cross_val_score
from sklearn_deltatfidf import DeltaTfidfVectorizer
from sklearn.svm import LinearSVC

import pandas as pd


def train(train_csv, str_array):
    # считываем подготовленный датасет
    data = pd.read_csv(train_csv, index_col=0).dropna()

    v = DeltaTfidfVectorizer(ngram_range=[1, 2], min_df=2, max_df=0.6)

    X = data['text'].values
    y = data.mark.astype(int).values.tolist()
    new_X = v.fit_transform(X, y)

    new_data = v.transform(str_array)

    delta_clf = LinearSVC(penalty='l2')

    delta_clf.fit(new_X, y)

    return delta_clf.predict(new_data)

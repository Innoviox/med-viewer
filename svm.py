import numpy as np
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
import pickle
import os

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, 'vectorized.pkl'), "rb") as f:
    data = pickle.load(f)

user_svms = {}
TRAINING_LEN = 200
X_train = data['X'][:TRAINING_LEN]
X_test = data['X'][TRAINING_LEN:]

# DOI -> item (title, abstract, index)
train_db = data['doi_db']
# index -> DOI
test_db = data['index_db'][TRAINING_LEN:]


def index2doi(i):
    return test_db[i]

def doi2index(d):
    if d in train_db:
        return train_db[d]['index']
    return None

def doi2Item(lst):
    items = []
    for d in lst:
        if d in train_db:
            item = train_db[d]
            item["doi"] = d
            items.append(item)
    return items

# print(train_db)
# print(test_db)
# Given a set of favorable dois, train the svm classifier to predict other favorites
def train_svm(user, doi, X= X_train, doi2index=doi2index):
    # Create new svm for each user
    # Settings courtesy of arxiv-sanity
    # svm = make_pipeline(StandardScaler(with_mean=False), LinearSVC(class_weight='balanced', verbose=False, max_iter=10000, tol=1e-6, C=0.1))
    svm = make_pipeline(LinearSVC(class_weight='balanced', verbose=False, max_iter=10000, tol=1e-6, C=0.1))
    user_svms[user] = svm

    # set the corresponding index to true
    y = np.zeros(X.shape[0])
    for d in doi:
        if (i := doi2index(d)) is not None:
            y[i] = 1
    svm.fit(X, y)

# Given a set of articles and its tf-idf vectors, evaluate the svm classifier to predict the favorable articles
def eval_svm(user, X = X_test, index2doi = index2doi, top_n = 20):
    svm = user_svms[user]
    y = svm.predict(X)

    top_indexes = (-y).argsort()[:top_n]
    dois = [index2doi(i) for i in top_indexes]
    print(y)
    return dois



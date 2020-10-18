import numpy as np
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

user_svms = {}

X_train = np.zeros(1)
X_test = np.zeros(1)

# DOI -> index of tf-idf
train_db = {}
# index -> DOI
test_db = []

# Given a set of favorable dois, train the svm classifier to predict other favorites
def train_svm(user, doi, X= X_train, doi2index=train_db):
    # Create new svm for each user
    svm = make_pipeline(StandardScaler(), LinearSVC(random_state=0, tol=1e-5))
    user_svms[user] = svm

    # set the corresponding index to true
    y = np.zeros(X.shape[0])
    for d in doi:
        if (i := doi2index[doi]):
            y[i] = 1
    svm.fit(X, y)

# Given a set of articles and its tf-idf vectors, evaluate the svm classifier to predict the favorable articles
def eval_svm(user, X = X_test, index2doi = test_db, top_n = 20):
    svm = user_svms[user]
    y = svm.fit(X)

    top_indexes = (-y).argsort()[:top_n]
    dois = [index2doi[i] for i in top_indexes]
    return dois


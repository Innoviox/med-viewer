from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
import pickle
import numpy as np

pkl_data = None
with open('analyzed.pkl', "rb") as f:
    pkl_data = pickle.load(f)

X = pkl_data['X']
y = np.zeros(X.shape[0])
first_article = X[0]
arb_article = X[10]
liked = [0,1,2,3,4]
y[liked] = 1

clf = make_pipeline(StandardScaler(with_mean=False),
                    LinearSVC(random_state=0, tol=1e-5))
clf.fit(X, y)

for i in range(10):
    print(clf.predict(X[i]))



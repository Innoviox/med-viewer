from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
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
#liked = [0,1,2,3,4]
liked = np.random.randint(0, 200, 50)
y[liked] = 1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = make_pipeline(StandardScaler(with_mean=False),
                    LinearSVC(random_state=0, tol=1e-5))
clf.fit(X_train, y_train)

for i in range(20):
    print(y_test[i], clf.predict(X_test[i]))


from sklearn.svm import LinearSVC
import pandas as import pd

papers_df = pd.read_csv("papers_after_pca.csv")
user_likes_df = pd.read_csv("user_likes.csv")

def train_svm():
    for i in range(user_likes_df.shape[0]):
        papers_df[papers_df["id"] in user_likes_df.iloc[0]]
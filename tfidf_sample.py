from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os

def make_filenames():
    all_files = []
    path = "./txts"
    dirs = os.listdir(path)
    for file in dirs:
        all_files.append(path + "/" + file)
    return all_files

files = make_filenames()
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(files)
df = pd.DataFrame(X.A)
df.to_csv("papers.csv")
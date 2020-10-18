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
vectorizer = TfidfVectorizer(input='filename',
        encoding='utf-8', decode_error='replace', strip_accents='unicode',
        lowercase=True, analyzer='word', stop_words='english',
        token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
        ngram_range=(1, 2), max_features = 5000,
        norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
        max_df=1.0, min_df=1)
X = vectorizer.fit_transform(files)
df = pd.DataFrame(X.A)
df.columns = vectorizer.get_feature_names()
df.to_csv("papers.csv")
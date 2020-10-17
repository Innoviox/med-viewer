from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json

with open("raw_papers.json") as f:
    d = json.load(f)

def get_corpus():
    lst = []
    for key, value in d.items():
        abstract = value["rel_abs"]
        lst.append(abstract)
    return lst

def get_vectors(corpus):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    return X

corpus = get_corpus()
X = get_vectors(corpus)
df = pd.DataFrame(X.A)

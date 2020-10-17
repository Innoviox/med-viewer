from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json

with open("raw_papers.json") as f:
    d = json.load(f)

def get_corpus():
    lst = []
    ids = []
    for key, value in d.items():
        abstract = value["rel_abs"]
        lst.append(abstract)
        ids.append(key)
    return lst, ids

def get_vectors(corpus):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    return X

corpus, ids = get_corpus()
X = get_vectors(corpus)
df = pd.DataFrame(X.A)
ids_df = pd.DataFrame(ids)
final_df = pd.concat([ids_df, df], axis=1)
final_df.to_csv("tfidf_abstracts.csv", index=False, header=False)
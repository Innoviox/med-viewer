from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
import pickle

with open("article_db.json") as json_file:
    raw_papers = json.load(json_file)

ids = []
txt_paths = []
max_features = 5000

for i, key in enumerate(raw_papers):
    ids.append(key)
    raw_papers[key]["id"] = i # paper id -> index corresponds to the position in collection of vectors
    txt_paths.append(raw_papers[key]["path"])

def corpus(paths):
    for p in paths:
        with open(p, "r") as f:
            yield f.read()

# Settings courtesy of arxiv-sanity-preserver
v = TfidfVectorizer(input='content',
        encoding='utf-8', decode_error='replace', strip_accents='unicode',
        lowercase=True, analyzer='word', stop_words='english',
        token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
        ngram_range=(1, 2), max_features = max_features,
        norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
        max_df=1.0, min_df=1)

data = {}
X = v.fit_transform(corpus(txt_paths))

data['X'] = X
data['vectorizer'] = v
data['db'] = raw_papers

with open('analyzed.pkl', 'wb') as f:
    pickle.dump(data, f)
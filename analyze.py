from sklearn.feature_extraction.text import TfidfVectorizer
import json

with open("raw_papers.json") as json_file:
    raw_papers = json.load(json_file)

ids = []
abstracts = []
max_features = 5000

for i, key in enumerate(raw_papers):
    ids.append(key)
    abstracts.append(raw_papers[key]["rel_abs"])

# Settings courtesy of arxiv-sanity-preserver
v = TfidfVectorizer(input='content',
        encoding='utf-8', decode_error='replace', strip_accents='unicode',
        lowercase=True, analyzer='word', stop_words='english',
        token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
        ngram_range=(1, 2), max_features = max_features,
        norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
        max_df=1.0, min_df=1)

X = v.fit_transform(abstracts)
print(v.get_feature_names())

print(X.shape)
print(X.todense())

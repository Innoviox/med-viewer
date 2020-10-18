from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pickle

with open("pdfs.json") as json_file:
    raw_papers = json.load(json_file)

pkl_db = {}
articles = []
max_features = 5000

for i, key in enumerate(raw_papers):
    name = raw_papers["articles"][i]["filename"]
    with open("txts/" + raw_papers["articles"][i]["filename"] + ".txt", "r") as f:
        content = f.read()
        articles.append(content)

# Settings courtesy of arxiv-sanity-preserver
v = TfidfVectorizer(input='content',
        encoding='utf-8', decode_error='replace', strip_accents='unicode',
        lowercase=True, analyzer='word', stop_words='english',
        token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
        ngram_range=(1, 2), max_features = max_features,
        norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
        max_df=1.0, min_df=1)

X = v.fit_transform(articles)
data = {}

data["db"] = raw_papers
data["X"] = X
with open('vectorized.pkl', "wb") as f:
    pickle.dump(data, f)

from sklearn.feature_extraction.text import TfidfVectorizer
import json

with open("raw_papers.json") as json_file:
    data = json.load(json_file)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
print(vectorizer.get_feature_names())

print(X.shape)
print(X.todense())
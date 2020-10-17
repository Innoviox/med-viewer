import requests
import json

r = requests.get('https://api.biorxiv.org/covid19/0')
content_dict = json.loads(r.content)


# Retrieving abstracts is easy - PDFs are hard to obtain
for paper in content_dict["collection"]:
    print(paper["rel_title"])
    print(paper["rel_abs"])

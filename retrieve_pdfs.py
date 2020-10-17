import requests
import json

r = requests.get('https://api.biorxiv.org/covid19/0')
content_dict = json.loads(r.content)

# Retrieving abstracts is easy - PDFs are hard to obtain
papers_db = {}

GET_PDFS = False
for i, paper in enumerate(content_dict["collection"]):
    # First 5 for testing
    # if (i > 5):
    #     break
    print(paper["rel_title"])
    print(paper["rel_abs"])

    # Downloading PDFs are expensive and slow - test with just abstract text first.
    path = None
    if GET_PDFS:
        url = paper["rel_link"] + ".full.pdf"
        r = requests.get(url, stream=True)
        path = "bulk_data/" + url.split("/")[-1]
        with open(path, 'wb') as f:
            f.write(r.content)

    # Store each paper with its doi as the key
    papers_db[paper["rel_doi"]] = {
        "rel_title": paper["rel_title"],
        "rel_abs": paper["rel_abs"],
        "pdf_path": path
    }
    with open("raw_papers.json", 'w') as db_file:
        json.dump(papers_db, db_file)





import requests
import bs4
import tqdm

import json
import os

make_soup = lambda url, site='': bs4.BeautifulSoup(requests.get(site + url).text, features='lxml')


def biorxiv_pdfs():
    # Retrieve abstracts from biorxiv
    r = requests.get('https://api.biorxiv.org/covid19/0')
    content_dict = json.loads(r.content)

    # Retrieving abstracts is easy - PDFs are hard to obtain
    for paper in content_dict["collection"]:
        print(paper["rel_title"])
        print(paper["rel_abs"])


def medrxiv_pdfs(out_dir='pdfs/'):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    url = "https://www.medrxiv.org/content/early/recent?page={}"

    pdf_json = {"articles": []}

    start_page = 0
    max_pages = 40

    for page in range(start_page, max_pages):
        soup = make_soup(url.format(page))

        links = soup.findAll("a", {"class": "highwire-cite-linked-title"})
        for l in tqdm.tqdm(links):
            article = make_soup(l['href'], site='https://www.medrxiv.org')
            file = article.find("a", {"class": "article-dl-pdf-link"})
            title = article.find("h1", {"id": "page-title"}).text
            abstract = article.find("p", {"id": "p-2"}).text
            fname = l['href'].split("/")[-1]
            doi = article.find("span", {"class": "highwire-cite-metadata-doi"}).text

            open(out_dir + fname + ".pdf", "wb").write(requests.get('https://www.medrxiv.org' + file['href']).content)
            pdf_json["articles"].append({"title": title, "abstract": abstract, "filename": fname, "doi": doi})

    with open("pdfs.json", "w") as jsonout:
        json.dump(pdf_json, jsonout)


medrxiv_pdfs()

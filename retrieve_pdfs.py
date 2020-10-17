import requests
import bs4

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

def medrxiv_pdfs(outdir='pdfs/'):
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    url = "https://www.medrxiv.org/content/early/recent?page={}"

    max_pages = 1218

    for page in range(max_pages):
        soup = make_soup(url.format(max_pages))

        links = soup.findAll("a", {"class": "highwire-cite-linked-title"})
        for l in links:
            article = make_soup(l['href'], site='https://www.medrxiv.org')
            file = article.find("a", {"class": "article-dl-pdf-link"})
            title = article.find("h1", {"id": "page-title"}).text

            open("pdfs/" + title + ".pdf", "wb").write(requests.get('https://www.medrxiv.org' + file['href']).content)

medrxiv_pdfs()
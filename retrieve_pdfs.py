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
    papers_db = {}
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    url = "https://www.medrxiv.org/content/early/recent?page={}"

    start_page = 0
    max_pages = 20

    for page in range(start_page, max_pages):
        soup = make_soup(url.format(page))

        links = soup.findAll("a", {"class": "highwire-cite-linked-title"})
        for l in tqdm.tqdm(links):
            article = make_soup(l['href'], site='https://www.medrxiv.org')

            file = article.find("a", {"class": "article-dl-pdf-link"})
            doi = "/".join(article.find("span", {"class": "highwire-cite-metadata-doi"}).text.strip().split('/')[-2:])

            title = l['href'].split("/")[-1]

            name = l.find('span').text
            papers_db[doi] = {"title": name, "path": "txts" + "/" + title + ".txt"}

            open(out_dir + title + ".pdf", "wb").write(requests.get('https://www.medrxiv.org' + file['href']).content)

    with open("article_db.json", "w") as f:
        json.dump(papers_db, f)

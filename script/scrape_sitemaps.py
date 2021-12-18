# simple script to get opengenus article links from its sitemap

import requests, json
from bs4 import BeautifulSoup


SITEMAP_URL = "https://iq.opengenus.org/sitemap-posts.xml"

def get_links():
    xml = requests.get(SITEMAP_URL).text
    bs_object = BeautifulSoup(xml, "xml")


    # "loc is the xml attribute that contains a url"
    # finds all the locs and extract the urls from them
    urls = bs_object.find_all("loc")
    urls = [url.get_text() for url in urls]
    return urls

def dump_to_json(article_links, filepath="../articles.json"):
    articles = {
    "length":len(article_links),
    "links": article_links
    }

    with open(filepath, "w") as file:
        json.dump(articles, file, indent=3)

dump_to_json(get_links())

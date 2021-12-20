# simple script to get opengenus article links from its sitemap
# update populate a html template with the data

import sys, json, re
import requests
from bs4 import BeautifulSoup


SITEMAP_URL = "https://iq.opengenus.org/sitemap-posts.xml"
TEMPLATE_PATH = "./random_template.html"
ACTUAL_FILE_PATH = "../random.html"

def get_links():
    xml = requests.get(SITEMAP_URL).text
    bs_object = BeautifulSoup(xml, "xml")


    # "loc is the xml attribute that contains a url"
    # finds all the locs and extract the urls from them
    urls = bs_object.find_all("loc")
    urls = [url.get_text() for url in urls]
    return urls

def convert_articlelinks_to_json_string(article_links):
    articles = {
    "length":len(article_links),
    "links": article_links
    }
    return json.dumps(articles, indent=2)

def update_html(articles, template_name=TEMPLATE_PATH, file_path=ACTUAL_FILE_PATH):
    """ replaces the article slug in the template with the real json string 
        and updates the actual html
    """
    
    newcontent = ""
    with open(template_name) as file:
        newcontent = file.read()
    
    newcontent = re.sub("{{\s*articles\s*}}", articles, newcontent)
    
    with open(file_path, "w") as file:
        file.write(newcontent)

def main():
    # only 1 extra argument is allowed
    valid_args = ["--update", "--output"]
    if len(sys.argv[1:]) == 1 and sys.argv[1] in valid_args:
        links = get_links()
        articles = convert_articlelinks_to_json_string(links)
        if sys.argv[1] == "--update":
            update_html(articles)
        if sys.argv[1] == "--output":
            print(articles)
    else:
        print(f"invalid usage, accepted commands are {valid_args}")


if __name__ == "__main__":
    main()
    
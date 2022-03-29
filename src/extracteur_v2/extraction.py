import requests
from bs4 import BeautifulSoup

from src.extracteur_v2.surlignage import Surlignage


def get_nombre_pages(url) -> int:
    numero_page = 1

    while requests.get(f"{url}page/{numero_page}/").status_code != 404:
        numero_page += 1

    return numero_page - 1


def get_nombre_articles(page) -> int:
    articles = page.find_all(class_='grid-item')
    return len(articles)


if __name__ == '__main__':
    article = Surlignage()

    print(get_nombre_pages(article.url))
    for page in range(get_nombre_pages(article.url)):
        for article in range(get_nombre_articles(page)):


    pass

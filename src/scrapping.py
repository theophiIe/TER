
import requests
from bs4 import BeautifulSoup

from src.article_court import ArticleCourt
from src.article_long import ArticleLong


def get_nombre_pages(url) -> int:
    page = requests.get(f"{url}page/2/")
    soup = BeautifulSoup(page.content, 'lxml')
    titres = soup.find('title')

    return int(str(titres).split(' ')[5])


def get_nombre_articles(page) -> int:
    articles = page.find_all(class_='container-fluid')[1:]
    return len(articles)


def scrap_article_long():
    articles = ArticleLong()
    pages = get_nombre_pages(articles.url)

    for num in range(1, pages + 1):
        articles.get_url_articles(num)

    num_article = 0

    while num_article < len(articles.url_article):
        page = BeautifulSoup(requests.get(articles.url_article[num_article]).content, 'lxml')

        articles.get_titres_articles(page)
        articles.get_articles_en_liens(page)
        articles.get_auteurs_articles(page)
        articles.get_contenu_articles(page)
        articles.get_liens_citations(page)

        print(get_nombre_articles(page))
        num_article += get_nombre_articles(page)

    return articles


def scrap_article_court():
    articles = ArticleCourt()
    num_article = 0
    pages = get_nombre_pages(articles.url)

    for num in range(1, pages + 1):
        articles.get_url_articles(num)

    while num_article < len(articles.url_article):
        page = BeautifulSoup(requests.get(articles.url_article[num_article]).content, 'lxml')

        articles.get_titres_articles(page)
        articles.get_etiquette_articles(page)
        articles.get_articles_en_liens(page)
        articles.get_auteurs_articles(page)
        articles.get_source_date_citation(page)
        articles.get_contenu_articles(page)
        articles.get_liens_citations(page)

        print(get_nombre_articles(page))
        num_article += get_nombre_articles(page)

    return articles

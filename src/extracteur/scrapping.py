import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from src.extracteur.article_court import ArticleCourt
from src.extracteur.article_long import ArticleLong


def get_nombre_pages(url) -> int:
    page = requests.get(f"{url}page/2/")
    soup = BeautifulSoup(page.content, 'lxml')
    titres = soup.find('title')

    return int(str(titres).split(' ')[5])


def get_nombre_articles(page) -> int:
    articles = page.find_all(class_='container-fluid')[1:]
    return len(articles)


def scrap_article_long(tagger):
    articles = ArticleLong(tagger)
    pages = get_nombre_pages(articles.url)

    for num in range(1, pages + 1):
        articles.get_url_articles(num)

    num_article = 0
    pbar = tqdm(range(len(articles.url_article)), colour='green', desc='Progression')

    while num_article < len(articles.url_article):
        page = BeautifulSoup(requests.get(articles.url_article[num_article]).content, 'lxml')
        articles.article_bs4 = page.find_all(class_='container-fluid')[1:]

        articles.get_titres_articles(page)
        articles.get_articles_en_liens()
        articles.get_auteurs_articles()
        articles.get_profession_auteurs()
        articles.get_contenu_articles(page)
        articles.get_liens_citations()

        num_article += get_nombre_articles(page)
        pbar.update(get_nombre_articles(page))
        pbar.refresh()

    return articles


def scrap_article_court(tagger):
    articles = ArticleCourt(tagger)
    pages = get_nombre_pages(articles.url)

    for num in range(1, pages + 1):
        articles.get_url_articles(num)

    num_article = 0
    pbar = tqdm(range(len(articles.url_article)), colour='green', desc='Progression')

    while num_article < len(articles.url_article):
        page = BeautifulSoup(requests.get(articles.url_article[num_article]).content, 'lxml')
        articles.article_bs4 = page.find_all(class_='container-fluid')[1:]

        articles.get_titres_articles(page)
        articles.get_etiquette_articles(page)
        articles.get_articles_en_liens()
        articles.get_auteurs_articles()
        articles.get_profession_auteurs()
        articles.get_source_date_citation()
        articles.get_contenu_articles(page)
        articles.get_liens_citations()

        num_article += get_nombre_articles(page)
        pbar.update(get_nombre_articles(page))
        pbar.refresh()

    return articles

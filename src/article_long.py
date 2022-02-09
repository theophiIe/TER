import requests
from bs4 import BeautifulSoup

from main import get_nombre_pages
from src.article import Article


class ArticleLong(Article):
    def __init__(self):
        super().__init__()

    def get_url_articles(self, num_page) -> None:
        page = requests.get(f"{self.url}page/{str(num_page)}")
        soup = BeautifulSoup(page.content, 'lxml')
        articles = soup.find_all(class_='article_long')

        for article in articles:
            for lien in article.find_all('a'):
                self.url_article.append(lien.get('href'))

    def get_titres_articles(self, page) -> None:
        articles = page.find_all(class_='col-md-10')

        for article in articles:
            for titre in article.find_all('h1'):
                self.titre_article.append(titre.text)

    def get_auteurs_articles(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            auteurs = []
            auteur = article.find('h2')
            noms = auteur.text.split("//")
            for nom in noms:
                auteurs.append(nom.split(',')[0].replace("Par", "").replace("par", ""))
            self.auteur_article.append(auteurs)


if __name__ == '__main__':
    article = ArticleLong()
    pages = get_nombre_pages(article.url)

    for num in range(1, pages + 1):
        article.get_url_articles(num)

    num_article = 0

    while num_article < len(article.url_article):
        page = BeautifulSoup(requests.get(article.url_article[num_article]).content, 'lxml')

        article.get_titres_articles(page)
        article.get_articles_en_liens(page)
        article.get_auteurs_articles(page)
        article.get_contenu_articles(page)
        article.get_liens_citations(page)

        num_article += 31

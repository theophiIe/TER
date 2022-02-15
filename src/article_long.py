import requests
from bs4 import BeautifulSoup

from src.article import Article


class ArticleLong(Article):
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

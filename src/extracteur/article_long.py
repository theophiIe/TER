import requests

from bs4 import BeautifulSoup

from src.extracteur.article import Article


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

    def get_auteurs_articles(self) -> None:
        for article in self.article_bs4:
            auteur = article.find('h2')
            self.add_date(auteur.text)
            self.add_auteur(auteur.text)

    def get_profession_auteurs(self) -> None:
        for article in self.article_bs4:
            auteur = article.find('h2')
            self.add_profession(auteur.text)

import requests
from bs4 import BeautifulSoup

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

    def get_articles_en_liens(self, page) -> None:
        pass

    def get_contenu_articles(self, page) -> None:
        pass

    def get_liens_citations(self, page) -> None:
        pass

    def get_auteurs_articles(self, page) -> None:
        pass


if __name__ == '__main__':
    pass
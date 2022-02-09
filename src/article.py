import requests
from bs4 import BeautifulSoup
from abc import abstractmethod, ABC


class Article(ABC):
    def __init__(self):
        self.url = 'https://lessurligneurs.eu/lire/'
        self.url_article = []
        self.titre_article = []
        self.auteur_article = []
        self.articles_en_lien = []
        self.contenu_articles = []
        self.liens_citations = []

    def get_nombre_pages(self) -> int:
        page = requests.get(f"{self.url}page/2/")
        soup = BeautifulSoup(page.content, 'lxml')
        titres = soup.find('title')

        return int(str(titres).split(' ')[5])

    @abstractmethod
    def get_url_articles(self, num_page) -> None:
        pass

    @abstractmethod
    def get_titres_articles(self, page) -> None:
        pass

    @abstractmethod
    def get_articles_en_liens(self, page) -> None:
        pass

    @abstractmethod
    def get_contenu_articles(self, page) -> None:
        pass

    @abstractmethod
    def get_liens_citations(self, page) -> None:
        pass

    @abstractmethod
    def get_auteurs_articles(self, page) -> None:
        pass


if __name__ == '__main__':
    pass
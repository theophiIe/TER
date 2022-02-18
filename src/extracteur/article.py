import unicodedata

from abc import abstractmethod, ABC


class Article(ABC):
    def __init__(self):
        self.url = 'https://lessurligneurs.eu/lire/'
        self.url_article = []
        self.titre_article = []
        self.auteur_article = []
        self.profession_auteur = []
        self.articles_en_lien = []
        self.contenu_articles = []
        self.liens_citations = []
        self.date_ecriture = []
        self.lieu_profession = []

    @abstractmethod
    def get_url_articles(self, num_page) -> None:
        pass

    @abstractmethod
    def get_titres_articles(self, page) -> None:
        pass

    @abstractmethod
    def get_auteurs_articles(self, page) -> None:
        pass

    @abstractmethod
    def get_profession_auteurs(self, page) -> None:
        pass

    @abstractmethod
    def get_date_ecriture(self, page) -> None:
        pass

    @abstractmethod
    def get_lieu_profession(self, page) -> None:
        pass

    def get_articles_en_liens(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            lien_article = []
            liens = article.find(class_='related')
            if liens is not None:
                for lien in liens.find_all('a'):
                    lien_article.append(lien.get('href'))
            self.articles_en_lien.append(lien_article)

    def get_contenu_articles(self, page) -> None:
        articles = page.find_all('article')

        for article in articles:
            contenu = ''
            for texte in article.find_all('p'):
                contenu = f"{contenu} {texte.text}"
            self.contenu_articles.append(unicodedata.normalize("NFKD", contenu))

    def get_liens_citations(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            lien_article = []
            for lien in article.find(class_='texte').find_all('a'):
                lien_article.append(lien.get('href'))
            self.liens_citations.append(lien_article)

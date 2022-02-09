import unicodedata
from pprint import pprint

import requests
import re
from bs4 import BeautifulSoup


class Article:
    def __init__(self):
        self.url = 'https://lessurligneurs.eu/lire/'
        self.long = 'article_long'
        self.court = 'article_court'
        self.url_article_court = []
        self.titre_article_court = []
        self.url_article_long = []
        self.titre_article_long = []
        self.etiquette = []
        self.article_en_lien = []
        self.contenu = []
        self.auteur_article_court = []
        self.auteur_article_long = []
        self.source_citation = []
        self.date_citation = []
        self.liens = []

    def get_nombre_pages(self) -> int:
        return int(str(BeautifulSoup(requests.get(f"{self.url}page/2/").content, 'lxml').find('title')).split(' ')[5])

    def url_articles(self, num_page, type_article) -> None:
        page = BeautifulSoup(requests.get(f"{self.url}page/{str(num_page)}").content, 'lxml').find_all(
            class_=type_article)

        for liens in page:
            for link in liens.find_all('a'):
                if type_article == self.court:
                    self.url_article_court.append(link.get('href'))
                else:
                    self.url_article_long.append(link.get('href'))

    def titre_articles_court(self, page) -> None:
        for article in page.find_all(class_='col-md-7'):
            for titre in article.find_all('h1'):
                if titre.text != '':
                    self.titre_article_court.append(titre.text)

    def titre_articles_long(self, page) -> None:
        for article in page.find_all(class_='col-md-10'):
            for titre in article.find_all('h1'):
                self.titre_article_long.append(titre.text)

    def etiquette_article(self, page) -> None:
        for article in page.find_all('article'):
            for etiquettes in article.find_all('button'):
                self.etiquette.append(etiquettes.text)

    def annexe_article(self, page) -> None:
        for article in page.find_all(class_='container-fluid')[1:]:
            lien_article = []
            liens = article.find(class_='related')
            if liens is not None:
                for lien in liens.find_all('a'):
                    lien_article.append(lien.get('href'))
            self.article_en_lien.append(lien_article)

    def contenu_article(self, page) -> None:
        for article in page.find_all('article'):
            content = ''
            for texte in article.find_all('p'):
                content = f"{content} {texte.text}"
            self.contenu.append(unicodedata.normalize("NFKD", content))

    def liens_article(self, page) -> None:
        for article in page.find_all(class_='container-fluid')[1:]:
            lien_article = []
            for lien in article.find(class_='texte').find_all('a'):
                lien_article.append(lien.get('href'))
            self.liens.append(lien_article)

    def auteur_article(self, page) -> None:
        for article in page.find_all(class_='container-fluid')[1:]:
            auteur = []
            for auteurs in article.find(class_='auteur'):
                tmp = auteurs.text.split("//")
                for nom in tmp:
                    auteur.append(nom.split(',')[0])
            self.auteur_article_court.append(auteur)

    def source_date_citation(self, page) -> None:
        for article in page.find_all(class_='container-fluid')[1:]:
            date = []
            source = []
            dates_sources = article.find('h2')
            for date_source in dates_sources:
                date.append(re.findall(r'[0-9]*[0-9] [a-é]+ [0-9]*[0-9]*[0-9]*[0-9]*', date_source.text))
                source.append(date_source.text.split(',')[0])
            self.source_citation.append(source)
            self.date_citation.append(date)


def recup_article() -> None:
    articles = Article()
    num_article = 0
    pages = articles.get_nombre_pages()

    for num in range(1, pages + 1):
        articles.url_articles(num, articles.court)

    while num_article < len(articles.url_article_court):
        page = BeautifulSoup(requests.get(articles.url_article_court[num_article]).content, 'lxml')

        articles.titre_articles_court(page)
        articles.etiquette_article(page)
        articles.annexe_article(page)
        articles.auteur_article(page)
        articles.source_date_citation(page)
        articles.contenu_article(page)
        articles.liens_article(page)

        num_article += 31

    pprint(len(articles.url_article_court))
    pprint(len(articles.titre_article_court))
    pprint(len(articles.etiquette))
    pprint(len(articles.article_en_lien))
    pprint(len(articles.contenu))
    pprint(len(articles.auteur_article_court))
    pprint(len(articles.source_citation))
    pprint(len(articles.date_citation))
    pprint(len(articles.liens))

    # AFFICHAGE POUR LES TESTS

    # for b in range(len(articles.url_article_court)):
    #     print(articles.url_article_court[b])
    #
    # for b in range(len(articles.titre_article_court)):
    #     print(articles.titre_article_court[b])
    #
    # for b in range(len(articles.etiquette)):
    #     print(articles.etiquette[b])
    #
    # for b in range(len(articles.article_en_lien)):
    #     print(articles.article_en_lien[b])
    #
    # for b in range(len(articles.contenu)):
    #     print(articles.contenu[b])
    #
    # for b in range(len(articles.auteur_article_court)):
    #     print(articles.auteur_article_court[b])
    #
    # for b in range(len(articles.source_citation)):
    #     print(articles.source_citation[b])
    #
    # for b in range(len(articles.date_citation)):
    #     print(articles.date_citation[b])
    #
    # for b in range(len(articles.liens)):
    #     print(articles.liens[b])


# Ajout des textes de loi pour chaque article
# Mieux les articles en sous paragraphe avec les sous-titres et l'intro
# Trouver les noms des personnalités de l'article

if __name__ == '__main__':
    recup_article()






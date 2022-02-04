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
        self.liens_article_court = []
        self.titre_article_court = []
        self.liens_article_long = []
        self.titre_article_long = []
        self.etiquette = []
        self.article_en_lien = []
        self.contenu = []
        self.auteur_article_court = []
        self.auteur_article_long = []
        self.source_citation = []
        self.date_citation = []

    def get_nombre_pages(self) -> int:
        return int(str(BeautifulSoup(requests.get(self.url + "page/2/").content, 'lxml').find('title')).split(' ')[5])

    def liens_articles(self, num_page, type_article) -> None:
        page = BeautifulSoup(requests.get(self.url + "page/" + str(num_page)).content, 'lxml').find_all(
            class_=type_article)

        for liens in page:
            for link in liens.find_all('a'):
                if type_article == self.court:
                    self.liens_article_court.append(link.get('href'))
                else:
                    self.liens_article_long.append(link.get('href'))

    def titre_articles(self) -> None:
        for article in self.liens_article_court:
            self.titre_article_court.append(
                article.replace('https://lessurligneurs.eu/', '').replace('-', ' ').replace('/', ''))

        for article in self.liens_article_long:
            self.titre_article_long.append(
                article.replace('https://lessurligneurs.eu/', '').replace('-', ' ').replace('/', ''))

    def etiquette_article(self, page) -> None:
        for article in page.find_all('article'):
            for etiquettes in article.find_all('button'):
                self.etiquette.append(etiquettes.text)

    def annexe_article(self, page) -> None:
        liens = page.find_all(class_='related')
        for lien in liens:
            lien_article = []
            for link in lien.find_all('a'):
                lien_article.append(link.get('href'))
            self.article_en_lien.append(lien_article)

    def contenu_article(self, page) -> None:
        for article in page.find_all('article'):
            content = ''
            for texte in article.find_all('p'):
                content = content + " " + texte.text
            self.contenu.append(unicodedata.normalize("NFKD", content))

    def auteur_article(self, page) -> None:
        for auteurs in page.find_all(class_='auteur'):
            for auteur in auteurs:
                noms = []
                tmp = auteur.text.split("//")
                for nom in tmp:
                    noms.append(nom.split(',')[0])
                self.auteur_article_court.append(noms)

    def source_date_citation(self, page) -> None:
        for dates_sources in page.find_all('h2'):
            for date_source in dates_sources:
                self.source_citation.append(date_source.text.split(',')[0])
                self.date_citation.append(re.findall(r'[0-9]*[0-9] [a-z]+ [0-9]*[0-9]*[0-9]*[0-9]*', date_source.text.replace("é", "e")))

# Ajout des textes de loi pour chaque article
# Mieux les articles en sous paragraphe avec les sous-titres et l'intro
# Trouver les noms des personnalités de l'article


if __name__ == '__main__':
    a = Article()
    # print(a.get_nombre_pages())
    a.liens_articles(1, a.court)
    a.liens_articles(1, a.long)
    a.titre_articles()

    # pprint(a.liens_article_court)
    # print(a.titre_article_court[1])

    content = BeautifulSoup(requests.get("https://lessurligneurs.eu/nicolas-dupont-aignan-veut-lutter-contre-les-decisions-aberrantes-des-cours-europeennes-en-refusant-lapplication-de-leur-jurisprudence/").content, 'lxml')
    a.etiquette_article(content)
    a.annexe_article(content)
    a.auteur_article(content)
    a.source_date_citation(content)

    pprint(a.date_citation)
    pprint(a.source_citation)

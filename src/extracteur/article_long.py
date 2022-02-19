import re
import requests

from abc import ABC
from bs4 import BeautifulSoup
from flair.data import Sentence

from src.extracteur.article import Article


class ArticleLong(Article):
    def __init__(self, tagger):
        super().__init__(tagger)

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

            if auteur.text != '':
                sentence = Sentence(auteur.text)
                self.tagger.predict(sentence)
                for entity in sentence.get_spans('ner'):
                    if entity.tag == 'PER':
                        auteurs.append(entity.to_plain_string())

            self.auteur_article.append(auteurs)

    def get_profession_auteurs(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            metier = []
            auteur = article.find('h2')
            professions = auteur.text.split("//")
            for profession in professions:
                try:
                    metier.append(profession.split(',')[1])
                except Exception:
                    metier.append("Média")
            self.profession_auteur.append(metier)

    def get_date_ecriture(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            date = []
            date_ecriture = article.find('h2')
            date.append(re.findall(r"(\d{1,2}[e]?[r]? (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre"
                                   r"|octobre|novembre|décembre)[ ]*[0-9]{0,4})", date_ecriture.text))
            self.date_ecriture.append(date)

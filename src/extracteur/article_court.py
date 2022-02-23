import re
import requests

from bs4 import BeautifulSoup
from flair.data import Sentence

from src.extracteur.article import Article


class ArticleCourt(Article):
    def __init__(self, tagger):
        super().__init__(tagger)

        self.etiquette = []
        self.source_citation = []
        self.date_citation = []
        self.personnalites = []

    def get_url_articles(self, num_page) -> None:
        page = requests.get(f"{self.url}page/{str(num_page)}")
        soup = BeautifulSoup(page.content, 'lxml')
        articles = soup.find_all(class_='article_court')

        for article in articles:
            for lien in article.find_all('a'):
                self.url_article.append(lien.get('href'))

    def get_titres_articles(self, page) -> None:
        articles = page.find_all(class_='col-md-7')

        for article in articles:
            for titre in article.find_all('h1'):
                if titre.text != '':
                    self.titre_article.append(titre.text)
                    self.get_personnalite(titre.text)

    def get_etiquette_articles(self, page) -> None:
        articles = page.find_all('article')

        for article in articles:
            for etiquette in article.find_all('button'):
                val_etiquette = etiquette.text if etiquette.text != '' else None
                self.etiquette.append(val_etiquette)

    def get_auteurs_articles(self) -> None:
        for article in self.article_bs4:
            auteur = article.find(class_='auteur')
            self.add_date(auteur.text)
            self.add_auteur(auteur.text)

    def get_profession_auteurs(self) -> None:
        for article in self.article_bs4:
            auteur = article.find(class_='auteur')
            self.add_profession(auteur.text)

    def get_source_date_citation(self) -> None:
        for article in self.article_bs4:
            source_date = article.find('h2')
            if re.search(self.regex_date, source_date.text):
                self.date_citation.append(
                    re.findall(self.regex_date, source_date.text))
            else:
                self.date_citation.append(None)

            source = source_date.text.split(',')[0] if source_date.text.split(',')[0] != '' else None
            self.source_citation.append(source)

    def get_personnalite(self, titre: str) -> None:
        personnalite = []
        buffer = titre.replace("TotalEnergies", " ") \
            .replace("procès", " ") \
            .replace("au président de la République", "Emmanuel Macron") \
            .replace("Frexit", " ") \
            .replace("StopCovid", " ")

        sentence = Sentence(buffer)
        self.tagger.predict(sentence)
        for entity in sentence.get_spans('ner'):
            if entity.tag == 'PER':
                nom = entity.to_plain_string()
                if len(nom) > 2:
                    personnalite.append(nom)

        self.personnalites.append(personnalite)

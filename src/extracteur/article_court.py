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
                self.etiquette.append(etiquette.text)

    def get_auteurs_articles(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            auteurs = []
            lieu_buffer = []
            auteur = article.find(class_='auteur')

            if auteur.text != '':
                sentence = Sentence(auteur.text)
                self.tagger.predict(sentence)
                for entity in sentence.get_spans('ner'):
                    if entity.tag == 'PER':
                        auteurs.append(entity.to_plain_string())
                    if entity.tag == 'LOC':
                        lieu_buffer.append(entity.to_plain_string())

            self.auteur_article.append(auteurs)
            self.lieu_profession.append(lieu_buffer)

    def get_profession_auteurs(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            metier = []
            auteur = article.find(class_='auteur')
            professions = auteur.text.split("//")

            for profession in professions:
                try:
                    metier.append(profession.split(',')[1])
                except Exception:
                    metier.append("Média")
            self.profession_auteur.append(metier)

    def get_source_date_citation(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            date = []
            source = []
            date_source = article.find('h2')
            date.append(re.findall(r'[0-9]*[0-9] [a-é]+ [0-9]*[0-9]*[0-9]*[0-9]*', date_source.text))
            source.append(date_source.text.split(',')[0])
            self.source_citation.append(source)
            self.date_citation.append(date)

    def get_date_ecriture(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            date = []
            auteur = article.find(class_='auteur')
            date.append(re.findall(r"(\d{1,2}[e]?[r]? (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre"
                                   r"|octobre|novembre|décembre)[ ]*[0-9]{0,4})", auteur.text))
            self.date_ecriture.append(date)

    def get_personnalite(self, titre: str) -> None:
        personnalite = []
        buffer = titre.replace("TotalEnergies", " ")\
            .replace("procès", " ")\
            .replace("au président de la République", "Emmanuel Macron")\
            .replace("Frexit", " ")\
            .replace("StopCovid", " ")

        sentence = Sentence(buffer)
        self.tagger.predict(sentence)
        for entity in sentence.get_spans('ner'):
            if entity.tag == 'PER':
                tmp = entity.to_plain_string()
                if len(tmp) > 2:
                    personnalite.append(tmp)

        self.personnalites.append(personnalite)

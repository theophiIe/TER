import re

import requests
from bs4 import BeautifulSoup

from src.extracteur.article import Article


class ArticleCourt(Article):
    def __init__(self):
        super().__init__()

        self.etiquette = []
        self.source_citation = []
        self.date_citation = []

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

    def get_etiquette_articles(self, page) -> None:
        articles = page.find_all('article')

        for article in articles:
            for etiquette in article.find_all('button'):
                self.etiquette.append(etiquette.text)

    def get_auteurs_articles(self, page) -> None:
        articles = page.find_all(class_='container-fluid')[1:]

        for article in articles:
            auteurs = []
            auteur = article.find(class_='auteur')
            noms = auteur.text.split("// ")

            for nom in noms:
                if nom[0:1] == " ":
                    # Permet de supprimer les espaces au début
                    nom = nom[1:].split(', ')[0]
                elif nom.startswith("Par ") or nom.startswith("par "):
                    # Permet de supprimer les "par" et "Par"
                    nom = nom[4:].split(', ')[0]
                elif len(nom.split(' ,')) < 0:
                    nom = nom.split(' ,')[0]
                elif re.search(r"(\d{1,2} (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre"
                               r"|novembre|décembre)[ ]*[0-9]{0,4})", nom) and len(noms) > 1:
                    # Permet de supprimer les qui se serait glisse dans les auteur
                    # tout en assurant que les articles ayant un seul auteur soit dans la BDD
                    continue
                else:
                    if len(nom.split(', ')) > 1:
                        nom = nom.split(', ')[0]
                    else:
                        nom = nom.split(' ,')[0]
                if " et " in nom:
                    for i in range(len(nom.split(' et '))):
                        auteurs.append(nom.split(' et ')[i])
                else:
                    auteurs.append(nom)
            self.auteur_article.append(auteurs)

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

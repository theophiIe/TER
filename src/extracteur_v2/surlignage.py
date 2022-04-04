import re
import unicodedata
from pprint import pprint

import requests
from bs4 import BeautifulSoup


def normalize_text(texte: str) -> str:
    return unicodedata.normalize("NFKD", texte)


class Surlignage:
    def __init__(self):
        self.url = 'https://lessurligneurs.eu/surlignage/'
        self.url_surlignage = []
        self.regex_date = r"(\d{1,2}[e]?[r]? (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre" \
                          r"|novembre|décembre)[ ]*[0-9]{4})"
        self.titre = []
        self.etiquette = []
        self.date_creation = []
        self.date_modification = []
        self.auteurs = []
        self.relecteurs = []
        self.redaction = []
        self.url_source = []
        self.nom_source = []
        self.url_references = []
        self.nom_references = []
        self.correction = []
        self.contenu = []
        self.meme_theme = []

    def get_url(self, page) -> None:
        articles = page.find_all(class_='grid-item')

        for article in articles:
            for lien in article.find_all('a'):
                self.url_surlignage.append(lien.get('href'))

    def get_titre_surlignage(self, page) -> None:
        titre = page.find('h1')
        contenu_titre = []

        if titre is not None:
            res = titre.text if titre.text != '' else None
            contenu_titre.append(normalize_text(res))

        self.titre.append(contenu_titre)

    def get_etiquette_surlignage(self, page) -> None:
        etiquette = page.find(class_='etiquette')
        contenu_etiquette = None

        if etiquette is not None:
            contenu_etiquette = etiquette.text if etiquette.text != '' else None
        self.etiquette.append(normalize_text(contenu_etiquette))

    def get_meme_theme_surlignage(self, page) -> None:
        url_meme_theme = []
        meme_theme = page.find_all(class_='grid-item')

        for article in meme_theme:
            for lien in article.find_all('a'):
                url_meme_theme.append(lien.get('href'))

        self.meme_theme.append(url_meme_theme)

    def get_date_surlignage(self, page) -> None:
        dates = page.find(class_='articles-dates')
        date_creation = None
        date_modification = None

        if dates is not None:
            if re.search(self.regex_date, dates.text):
                date_creation = re.findall(self.regex_date, dates.text)[0]
                if len(re.findall(self.regex_date, dates.text)) > 1:
                    date_modification = re.findall(self.regex_date, dates.text)[1]

        self.date_creation.append(date_creation)
        self.date_modification.append(date_modification)

    # Pour la V2
    def __get_contributeur(self, page) -> bool:
        articles_contributeurs = page.find(class_='articles-contributeurs')

        if articles_contributeurs is not None:
            contributeurs = articles_contributeurs.find_all('p')

            if contributeurs:

                auteurs = []
                relecteurs = []
                secretariat = []

                for contributeur in contributeurs:
                    if contributeur.text.startswith('Auteur'):
                        auteurs.append(normalize_text(contributeur.text))
                    elif contributeur.text.startswith('Auteurs'):
                        auteurs.append(normalize_text(contributeur.text))
                    elif contributeur.text.startswith('Autrice'):
                        auteurs.append(normalize_text(contributeur.text))
                    elif contributeur.text.startswith('Autrices'):
                        auteurs.append(normalize_text(contributeur.text))

                    elif contributeur.text.startswith('Relecteurs'):
                        relecteurs.append(normalize_text(contributeur.text))
                    elif contributeur.text.startswith('Relecteur'):
                        relecteurs.append(normalize_text(contributeur.text))
                    elif contributeur.text.startswith('Relectrice'):
                        relecteurs.append(normalize_text(contributeur.text))
                    elif contributeur.text.startswith('Relectrices'):
                        relecteurs.append(normalize_text(contributeur.text))

                    elif contributeur.text.startswith('Secrétariat'):
                        secretariat.append(normalize_text(contributeur.text))

                self.auteurs.append(auteurs)
                self.relecteurs.append(relecteurs)
                self.redaction.append(secretariat)

                return True

            else:
                self.relecteurs.append(None)
                self.redaction.append(None)
                return False
        else:
            self.relecteurs.append(None)
            self.redaction.append(None)
            return False

    # Pour la V1
    def __get_auteurs(self, page) -> None:
        auteurs = page.find(class_='auteur')
        auteur = []

        if auteurs is not None:
            auteur.append(normalize_text(auteurs.text))

        self.auteurs.append(auteur)

    def get_auteurs_surlignage(self, page) -> None:
        if not self.__get_contributeur(page):
            self.__get_auteurs(page)

    def get_source_surlignage(self, page) -> None:
        paragraphe = page.find(class_='col-md-8')
        resultat = None
        nom_source = []

        if paragraphe is not None:
            source = paragraphe.find('h2')
            if source is not None:
                lien = source.find('a')
                if lien is not None:
                    resultat = lien.get('href')
                    liens = lien.text.split(",")
                    for texte in liens:
                        if not re.search(self.regex_date, texte):
                            nom_source.append(normalize_text(texte))

                else:
                    liens = source.text.split(",")
                    for texte in liens:
                        if not re.search(self.regex_date, texte):
                            nom_source.append(normalize_text(texte))

        self.nom_source.append(nom_source)
        self.url_source.append(resultat)

    def get_correction_surlignage(self, page) -> None:
        correction = page.find(class_='correction')
        resultat = None

        if correction is not None:
            resultat = normalize_text(correction.text)
        self.correction.append(resultat)

    def get_contenu_surlignage(self, page) -> None:
        contenu_article = []
        texte = page.find(class_='texte')

        if texte is not None:
            paragraphe = texte.find_all('p')
            for bloc in paragraphe[:-1]:
                contenu_article.append(normalize_text(bloc.text))

        self.contenu.append(contenu_article)

    def get_reference_surlignage(self, page) -> None:
        texte = page.find(class_='texte')
        liens_references = []
        nom_references = []

        if texte is not None:
            paragraphe = texte.find_all('p')
            for bloc in paragraphe[:-1]:
                for lien in bloc.find_all('a'):
                    liens_references.append(lien.get('href'))
                    nom_references.append(normalize_text(lien.text))

        self.url_references.append(liens_references)
        self.nom_references.append(nom_references)

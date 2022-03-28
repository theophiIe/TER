import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup


def get_nombre_pages(url) -> int:
    page = requests.get(f"{url}page/2/")
    soup = BeautifulSoup(page.content, 'lxml')
    titres = soup.find('title')

    return int(str(titres).split(' ')[5])


def get_nombre_articles(page) -> int:
    articles = page.find_all(class_='grid-item')
    return len(articles)


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
        self.references = []
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
        contenu_titre = None

        if titre is not None:
            contenu_titre = titre.text if titre.text != '' else None

        self.titre.append(contenu_titre)

    def get_etiquette_surlignage(self, page) -> None:
        etiquette = page.find(class_='etiquette')
        contenu_etiquette = None

        if etiquette is not None:
            contenu_etiquette = etiquette.text if etiquette.text != '' else None
        self.etiquette.append(contenu_etiquette)

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
    def get_contributeur_surlignage(self, page) -> bool:
        articles_contributeurs = page.find(class_='articles-contributeurs')

        if articles_contributeurs is not None:
            contributeurs = articles_contributeurs.find_all('p')

            if contributeurs:

                auteurs = []
                relecteurs = []
                secretariat = []

                for contributeur in contributeurs:
                    if contributeur.text.startswith('Auteur'):
                        auteurs.append(contributeur.text)
                    elif contributeur.text.startswith('Relecteurs'):
                        relecteurs.append(contributeur.text)
                    elif contributeur.text.startswith('Secrétariat'):
                        secretariat.append(contributeur.text)

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
    def get_auteurs_surlignage(self, page) -> None:
        auteurs = page.find(class_='auteur')
        auteur = None

        if auteurs is not None:
            auteur = auteurs.text

        self.auteurs.append(auteur)

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
                            nom_source.append(texte)

        self.nom_source.append(nom_source)
        self.url_source.append(resultat)

    def get_correction_surlignage(self, page) -> None:
        correction = page.find(class_='correction')
        resultat = None

        if correction is not None:
            resultat = correction.text
        self.correction.append(resultat)

    def get_contenu_surlignage(self, page) -> None:
        contenu_article = []
        texte = page.find(class_='texte')

        if texte is not None:
            paragraphe = texte.find_all('p')
            for bloc in paragraphe[:-1]:
                contenu_article.append(bloc.text)

        self.contenu.append(contenu_article)

    def get_reference_surlignage(self, page) -> None:
        liens_references = []
        texte = page.find(class_='texte')

        if texte is not None:
            paragraphe = texte.find_all('p')
            for bloc in paragraphe[:-1]:
                for lien in bloc.find_all('a'):
                    liens_references.append(lien.get('href'))

        self.references.append(liens_references)


if __name__ == '__main__':
    url_test = "https://www.lessurligneurs.eu/fabien-roussel-sur-les-ecoles-hors-contrat-on-ne-sait-pas-ce-quon-y-enseigne-je-les-ferai-fermer/"
    url_test2 = "https://www.lessurligneurs.eu/surlignage/page/1/"

    page_test = requests.get(url_test)
    soup_test = BeautifulSoup(page_test.content, 'lxml')

    page_test2 = requests.get(url_test2)
    soup_test2 = BeautifulSoup(page_test2.content, 'lxml')

    surlignage = Surlignage()
    surlignage.get_url(soup_test2)
    surlignage.get_etiquette_surlignage(soup_test)
    surlignage.get_titre_surlignage(soup_test)
    surlignage.get_meme_theme_surlignage(soup_test)
    surlignage.get_date_surlignage(soup_test)

    if not surlignage.get_contributeur_surlignage(soup_test):
        surlignage.get_auteurs_surlignage(soup_test)

    surlignage.get_source_surlignage(soup_test)
    surlignage.get_correction_surlignage(soup_test)
    surlignage.get_contenu_surlignage(soup_test)
    surlignage.get_reference_surlignage(soup_test)

    pprint(surlignage.etiquette)
    pprint(surlignage.titre)
    pprint(surlignage.meme_theme)
    pprint(surlignage.date_creation)
    pprint(surlignage.date_modification)
    pprint(surlignage.auteurs)
    pprint(surlignage.relecteurs)
    pprint(surlignage.redaction)
    pprint(surlignage.url_source)
    pprint(surlignage.nom_source)
    pprint(surlignage.references)
    pprint(surlignage.contenu)

    # pprint(surlignage.url_surlignage)
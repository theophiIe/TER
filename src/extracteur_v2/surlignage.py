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
        self.source = []
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
        contenu_titre = titre.text if titre.text != '' else None
        self.titre.append(contenu_titre)

    def get_etiquette_surlignage(self, page) -> None:
        etiquette = page.find(class_='etiquette')
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
        date = page.find(class_='articles-dates')

        # Ajouter une vérification dans le cas où on n'a pas de date ou juste la date de création
        if re.search(self.regex_date, date.text):
            self.date_creation.append(re.findall(self.regex_date, date.text)[0])
            self.date_modification.append(re.findall(self.regex_date, date.text)[1])

    def get_contributeur_surlignage(self, page) -> None:
        contributeurs = page.find(class_='articles-contributeurs').find_all('p')

        # Ajouter des vérifications + implémenter Flair pour reconnaitre les noms
        self.auteurs.append(contributeurs[0].text)
        self.relecteurs.append(contributeurs[1].text)
        self.redaction.append(contributeurs[2].text)

    def get_source_surlignage(self, page) -> None:
        source = page.find(class_='col-md-8').find('h2').find('a')
        self.source.append(source.get('href'))

    def get_correction_surlignage(self, page) -> None:
        correction = page.find(class_='correction')
        self.correction.append(correction.text)

    def get_contenu_surlignage(self, page) -> None:
        contenu_article = []
        texte = page.find(class_='texte').find_all('p')

        for bloc in texte[:-1]:
            contenu_article.append(bloc.text)

        self.contenu.append(contenu_article)


if __name__ == '__main__':
    url_test = "https://www.lessurligneurs.eu/philippe-ballard-conseiller-regional-veut-reinstaurer-la-primaute-du" \
               "-droit-national-tout-en-restant-au-sein-de-lunion-europeenne/ "

    page_test = requests.get(url_test)
    soup_test = BeautifulSoup(page_test.content, 'lxml')

    surlignage = Surlignage()
    surlignage.get_etiquette_surlignage(soup_test)
    surlignage.get_titre_surlignage(soup_test)
    surlignage.get_meme_theme_surlignage(soup_test)
    surlignage.get_date_surlignage(soup_test)
    surlignage.get_contributeur_surlignage(soup_test)
    surlignage.get_source_surlignage(soup_test)
    surlignage.get_correction_surlignage(soup_test)
    surlignage.get_contenu_surlignage(soup_test)

    pprint(surlignage.source)
    # pprint(surlignage.relecteurs)
    # pprint(surlignage.redaction)

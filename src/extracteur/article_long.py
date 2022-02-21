import re
import requests

from bs4 import BeautifulSoup
from flair.data import Sentence

from src.extracteur.article import Article


class ArticleLong(Article):
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

            if re.search(r"(\d{1,2}[e]?[r]? (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre"
                         r"|octobre|novembre|décembre)[ ]*[0-9]{0,4})", auteur.text):
                self.date_ecriture.append(
                    re.findall(r"(\d{1,2}[e]?[r]? (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre"
                               r"|octobre|novembre|décembre)[ ]*[0-9]{0,4})", auteur.text))
            else:
                self.date_ecriture.append(None)

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
            texte = auteur.text
            if str(texte).find("//") != -1:
                professions = texte.split("//")
                for profession in professions:
                    if profession.find(",") != -1:
                        test = profession.split(",")
                        if re.search(r"(\d{1,2}[e]?[r]? (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre"
                                     r"|octobre|novembre|décembre)[ ]*[0-9]{0,4})", test[1]):
                            metier.append(None)
                        else:
                            metier.append(test[1])
            else:
                if str(texte).find(",") != -1:
                    professions = texte.split(",")
                    if re.search(r"(\d{1,2}[e]?[r]? (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre"
                                 r"|octobre|novembre|décembre)[ ]*[0-9]{0,4})", professions[1]):
                        metier.append(None)
                    else:
                        metier.append(professions[1])

            self.profession_auteur.append(metier)

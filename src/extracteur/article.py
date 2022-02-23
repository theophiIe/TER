import re
import unicodedata

from abc import abstractmethod, ABC

from flair.data import Sentence


class Article(ABC):
    def __init__(self, tagger):
        self.url = 'https://lessurligneurs.eu/lire/'
        self.article_bs4 = None
        self.regex_date = r"(\d{1,2}[e]?[r]? (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre" \
                          r"|novembre|décembre)[ ]*[0-9]{0,4})"
        self.url_article = []
        self.titre_article = []
        self.auteur_article = []
        self.profession_auteur = []
        self.articles_en_lien = []
        self.contenu_articles = []
        self.liens_citations = []
        self.titre_citations = []
        self.date_ecriture = []

        self.tagger = tagger

    @abstractmethod
    def get_url_articles(self, num_page) -> None:
        pass

    @abstractmethod
    def get_titres_articles(self, page) -> None:
        pass

    @abstractmethod
    def get_auteurs_articles(self) -> None:
        pass

    @abstractmethod
    def get_profession_auteurs(self) -> None:
        pass

    def get_articles_en_liens(self) -> None:
        for article in self.article_bs4:
            lien_article = []
            liens = article.find(class_='related')
            if liens is not None:
                for lien in liens.find_all('a'):
                    lien_article.append(lien.get('href'))
            self.articles_en_lien.append(lien_article)

    def get_contenu_articles(self, page) -> None:
        articles = page.find_all('article')

        for article in articles:
            contenu = []
            for texte in article.find_all('p'):
                contenu.append(unicodedata.normalize("NFKD", texte.text))
            self.contenu_articles.append(contenu)

    def get_liens_citations(self) -> None:
        for article in self.article_bs4:
            lien_article = []
            titre = []
            for lien in article.find(class_='texte').find_all('a'):
                lien_article.append(lien.get('href'))
                if lien.find('i') is None:
                    title = lien.find('span')
                    if title is not None:
                        titre.append(title.text)
                    else:
                        titre.append(lien.text)
                else:
                    balise = lien.find('i').find('span')
                    if balise is not None:
                        titre.append(balise.text)

            self.liens_citations.append(lien_article)
            self.titre_citations.append(titre)

    def add_date(self, texte):
        if re.search(self.regex_date, texte):
            self.date_ecriture.append(re.findall(self.regex_date, texte))
        else:
            self.date_ecriture.append(None)

    def add_auteur(self, texte):
        auteurs = []
        if texte != '':
            sentence = Sentence(texte)
            self.tagger.predict(sentence)
            for entity in sentence.get_spans('ner'):
                if entity.tag == 'PER':
                    auteurs.append(entity.to_plain_string())

        self.auteur_article.append(auteurs)

    def add_profession(self, texte):
        metier = []
        if texte.find("//") != -1:
            professions = texte.split("//")
            for profession in professions:
                if profession.find(",") != -1:
                    test = profession.split(",")
                    if re.search(self.regex_date, test[1]):
                        metier.append(None)
                    else:
                        metier.append(test[1])
        else:
            if str(texte).find(",") != -1:
                professions = texte.split(",")
                if re.search(self.regex_date, professions[1]):
                    metier.append(None)
                else:
                    metier.append(professions[1])

        self.profession_auteur.append(metier)

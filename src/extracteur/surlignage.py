import re
import unicodedata


def normalize_text(texte: str) -> str:
    """
    Permet le formatage d'une string.
    :param texte : texte à formatter.
    :return : texte formaté.
    """
    return unicodedata.normalize("NFKD", texte)


class Surlignage:
    """
    Classe contenant toutes les informations des articles de type Surlignage.
    """
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

    def get_url(self, page, dico_balise) -> None:
        """
        Permet de remplir la table `url_surlignage` avec les URL des articles de type surlignage.
        :param page : une page parsée par bs4.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        articles = page.find_all(class_=dico_balise['class']['container_article'])

        for article in articles:
            for lien in article.find_all(dico_balise['balise']['lien']):
                self.url_surlignage.append(lien.get(dico_balise['balise']['url']))

    def get_titre_surlignage(self, dom, dico_balise) -> None:
        """
        Permet de remplir la table `titre` avec les titres de chaque article.
        :param dom : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        titre = dom.xpath(dico_balise['xpath']['titre'])
        contenu_titre = []

        if titre is not None:
            res = titre[0] if titre[0] != '' else None
            contenu_titre.append(normalize_text(res))

        self.titre.append(contenu_titre)

    def get_etiquette_surlignage(self, dom, dico_balise) -> None:
        """
        Permet de remplir le tableau 'etiquette' avec les étiquettes de chaque article.
        :param dom : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        xpath = dom.xpath(dico_balise['xpath']['etiquette'])
        if xpath:
            self.etiquette.append(normalize_text(xpath[0]))
        else:
            self.etiquette.append(None)

    def get_meme_theme_surlignage(self, dom, dico_balise) -> None:
        """
        Permet de remplir le tableau 'meme_theme' avec les URL des articles
        dont le thème est identique à l'article courant.
        :param dom : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        url_meme_theme = []

        res1 = dom.xpath(dico_balise['xpath']['meme_theme_1'])
        res2 = dom.xpath(dico_balise['xpath']['meme_theme_2'])
        res3 = dom.xpath(dico_balise['xpath']['meme_theme_3'])

        if res1:
            url_meme_theme.append(res1[0])

        if res2:
            url_meme_theme.append(res2[0])

        if res3:
            url_meme_theme.append(res3[0])

        self.meme_theme.append(url_meme_theme)

    def get_date_surlignage(self, dom, dico_balise) -> None:
        """
        Permet de remplir les tableaux 'date_creation' ainsi que 'date_modification' pour chaque article.
        :param dom : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        date_creation = dom.xpath(dico_balise['xpath']['date_creation'])
        date_modification = dom.xpath(dico_balise['xpath']['date_modification'])

        if date_creation and date_creation[0] is not None and re.search(self.regex_date, date_creation[0]):
            res_date_creation = re.findall(self.regex_date, date_creation[0])[0]
            self.date_creation.append(res_date_creation)
        else:
            self.date_creation.append(None)

        if date_modification and date_modification[0] is not None \
                and re.search(self.regex_date, date_modification[0]):
            res_date_modification = re.findall(self.regex_date, date_modification[0])[0]
            self.date_modification.append(res_date_modification)
        else:
            self.date_modification.append(None)

    # Pour la V2
    def __get_contributeur(self, page, dico_balise) -> bool:
        """
        Permet de remplir les tableaux des 'auteur', 'relecteur' et 'redaction' pour chaque article.
        :param page : une page parsée par bs4.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        :return : True si les auteurs sont trouvés False sinon.
        """
        articles_contributeurs = page.find(class_=dico_balise['class']['contributeur'])

        if articles_contributeurs is not None:
            contributeurs = articles_contributeurs.find_all(dico_balise['balise']['paragraphe'])

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
    def __get_auteurs(self, dom, dico_balise) -> None:
        """
        Permet de remplir le tableau 'auteur' avec l'auteur de chaque article.
        :param dom : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        auteur = dom.xpath(dico_balise['xpath']['auteur'])
        resultat = []

        if auteur[0] != "":
            resultat.append(normalize_text(auteur[0]))

        self.auteurs.append(resultat)

    def get_auteurs_surlignage(self, page, dom, dico_balise) -> None:
        """
        Permet de remplir les tableaux des contributeurs d'un article.
        :param page : une page parsée par bs4.
        :param dom : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        if not self.__get_contributeur(page, dico_balise):
            self.__get_auteurs(dom, dico_balise)

    def get_source_surlignage(self, dom, dico_balise) -> None:
        """
        Permet de remplir les tableaux 'url_source' ainsi que 'nom_source' avec les sources issues de chaque article.
        :param dom : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        url_source = dom.xpath(dico_balise['xpath']['url_source'])
        nom_source = dom.xpath(dico_balise['xpath']['nom_source'])

        url = []
        nom = []

        if url_source:
            url.append(url_source[0])
        else:
            url.append(None)

        if nom_source:
            nom.append(nom_source[0])
        else:
            nom.append(None)

        self.url_source.append(url)
        self.nom_source.append(nom)

    def get_correction_surlignage(self, dom, dico_balise) -> None:
        """
        Permet de remplir le tableau 'correction' avec l'introduction de chaque article.
        :param dom : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        correction = dom.xpath(dico_balise['xpath']['correction'])
        resultat = None

        if correction:
            resultat = normalize_text(correction[0])
        self.correction.append(resultat)

    def get_contenu_surlignage(self, page, dico_balise) -> None:
        """
        Permet de remplir le tableau 'contenu' avec le contenue de chaque article.
        :param page : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        contenu_article = []
        texte = page.find(class_=dico_balise['class']['contenue'])

        if texte is not None:
            paragraphe = texte.find_all(dico_balise['balise']['paragraphe'])
            for bloc in paragraphe[:-1]:
                contenu_article.append(normalize_text(bloc.text))

        self.contenu.append(contenu_article)

    def get_reference_surlignage(self, page, dico_balise) -> None:
        """
        Permet de remplir les tableaux 'url_references' ainsi que 'nom_references' avec les différents
        liens et le nom de chaque citation et references dans chaque article.
        :param page : parsing d'une page HTML.
        :param dico_balise : fichier JSON contenant les balises et les Xpath.
        """
        texte = page.find(class_=dico_balise['class']['contenue'])
        liens_references = []
        nom_references = []

        if texte is not None:
            paragraphe = texte.find_all(dico_balise['balise']['paragraphe'])
            for bloc in paragraphe[:-1]:
                for lien in bloc.find_all(dico_balise['balise']['lien']):
                    liens_references.append(lien.get(dico_balise['balise']['url']))
                    nom_references.append(normalize_text(lien.text))

        self.url_references.append(liens_references)
        self.nom_references.append(nom_references)

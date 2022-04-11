import requests
from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm


def get_nombre_pages(url) -> int:
    """
    Permet d'avoir le nombre de pages sur le site lessurligneurs
    dans la partie article surlignage.
    :param url : url du site les surligneurs.
    :return : le nombre de pages.
    """
    numero_page = 1

    while requests.get(f"{url}page/{numero_page}/").status_code != 404:
        numero_page += 1

    return numero_page - 1


def get_nombre_articles(page, dico_balise) -> int:
    """
    Permet d'avoir le nombre d'articles par page dans la catégorie surlignage.
    :param page : parsing d'une page HTML correspondant à la catégorie surlignage.
    :param dico_balise : fichier JSON contenant les balises et les Xpath.
    :return : le nombre d'articles présent sur la page.
    """
    articles = page.find_all(class_=dico_balise['class']['container_article'])
    return len(articles)


def get_url_all_surlignage(article, dico_balise) -> None:
    """
    Permet de récupérer toutes les URL des articles de type surlignage.
    :param article : instance de la classe 'Surlignage'.
    :param dico_balise : fichier JSON contenant les balises et les Xpath.
    """
    pbar = tqdm(range(1, get_nombre_pages(article.url) + 1), colour='green', desc='Obtention des urls des articles')
    for page in range(1, get_nombre_pages(article.url) + 1):
        page = requests.get(f'{article.url}/page/{page}/')
        soup = BeautifulSoup(page.content, 'lxml')

        article.get_url(soup, dico_balise)
        pbar.update(1)
        pbar.refresh()


def remplir_surlignage(surlignage, balise) -> None:
    """
    Permet de lancer le parsing de la page pour chaque information.
    :param surlignage : une instance de la classe 'Surlignage'.
    :param balise : fichier JSON contenant les balises et les Xpath.
    """
    pbar = tqdm(range(len(surlignage.url_surlignage)), colour='green', desc='Remplissage surlignage')
    for page in surlignage.url_surlignage:
        article = requests.get(page)
        soup = BeautifulSoup(article.content, 'lxml')
        dom = etree.HTML(str(soup))
        surlignage.get_titre_surlignage(dom, balise)
        surlignage.get_etiquette_surlignage(dom, balise)
        surlignage.get_date_surlignage(dom, balise)
        surlignage.get_meme_theme_surlignage(dom, balise)
        surlignage.get_auteurs_surlignage(soup, dom, balise)
        surlignage.get_source_surlignage(dom, balise)
        surlignage.get_contenu_surlignage(soup, balise)
        surlignage.get_reference_surlignage(soup, balise)
        surlignage.get_correction_surlignage(dom, balise)

        pbar.update(1)
        pbar.refresh()

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_nombre_pages(url) -> int:
    numero_page = 1

    while requests.get(f"{url}page/{numero_page}/").status_code != 404:
        numero_page += 1

    return numero_page - 1


def get_nombre_articles(page, dico_balise) -> int:
    articles = page.find_all(class_=dico_balise['class']['container_article'])
    return len(articles)


def get_url_all_surlignage(article, dico_balise) -> None:
    pbar = tqdm(range(1, get_nombre_pages(article.url) + 1), colour='green', desc='Obtention des urls des articles')
    for page in range(1, get_nombre_pages(article.url) + 1):
        page = requests.get(f'{article.url}/page/{page}/')
        soup = BeautifulSoup(page.content, 'lxml')

        article.get_url(soup, dico_balise)
        pbar.update(1)
        pbar.refresh()


def remplir_surlignage(surlignage, balise) -> None:
    pbar = tqdm(range(len(surlignage.url_surlignage)), colour='green', desc='Remplissage surlignage')
    for page in surlignage.url_surlignage:
        article = requests.get(page)
        soup = BeautifulSoup(article.content, 'lxml')
        surlignage.get_titre_surlignage(soup, balise)
        surlignage.get_etiquette_surlignage(soup, balise)
        surlignage.get_date_surlignage(soup, balise)
        surlignage.get_meme_theme_surlignage(soup, balise)
        surlignage.get_auteurs_surlignage(soup, balise)
        surlignage.get_source_surlignage(soup, balise)
        surlignage.get_contenu_surlignage(soup, balise)
        surlignage.get_reference_surlignage(soup, balise)
        surlignage.get_correction_surlignage(soup, balise)

        pbar.update(1)
        pbar.refresh()

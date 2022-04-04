from pprint import pprint

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


from src.extracteur_v2.surlignage import Surlignage


def get_nombre_pages(url) -> int:
    numero_page = 1

    while requests.get(f"{url}page/{numero_page}/").status_code != 404:
        numero_page += 1

    return numero_page - 1


def get_nombre_articles(page) -> int:
    articles = page.find_all(class_='grid-item')
    return len(articles)


def get_url_all_surlignage(article) -> None:
    pbar = tqdm(range(1, get_nombre_pages(article.url) + 1), colour='green', desc='Obtention des urls des articles')
    for page in range(1, get_nombre_pages(article.url) + 1):
        page = requests.get(f'{article.url}/page/{page}/')
        soup = BeautifulSoup(page.content, 'lxml')

        article.get_url(soup)
        pbar.update(1)
        pbar.refresh()


def remplir_surlignage(surlignage) -> None:
    pbar = tqdm(range(len(surlignage.url_surlignage)), colour='green', desc='Remplissage')
    for page in surlignage.url_surlignage:
        article = requests.get(page)
        soup = BeautifulSoup(article.content, 'lxml')
        surlignage.get_titre_surlignage(soup)
        surlignage.get_etiquette_surlignage(soup)
        surlignage.get_date_surlignage(soup)
        surlignage.get_meme_theme_surlignage(soup)
        surlignage.get_auteurs_surlignage(soup)
        surlignage.get_source_surlignage(soup)
        surlignage.get_contenu_surlignage(soup)
        surlignage.get_reference_surlignage(soup)
        surlignage.get_correction_surlignage(soup)

        pbar.update(1)
        pbar.refresh()


def debug(surlignage) -> None:
    print("Début debug")
    pbar = tqdm(range(len(surlignage.url_surlignage)), colour='green', desc='Remplissage')
    for i in range(len(surlignage.titre)):
        print(f"Article num: {i+1}, page: {(i+1)%20}")
        pprint(surlignage.titre[i])
        pprint(surlignage.etiquette[i])
        pprint(surlignage.date_creation[i])
        pprint(surlignage.date_modification[i])
        pprint(surlignage.auteurs[i])
        pprint(surlignage.relecteurs[i])
        pprint(surlignage.redaction[i])
        pprint(surlignage.url_source[i])
        pprint(surlignage.nom_source[i])
        pprint(surlignage.url_references[i])
        pprint(surlignage.nom_references[i])
        pprint(surlignage.correction[i])
        # pprint(surlignage.contenu[i])
        pprint(surlignage.meme_theme[i])

        pbar.update(1)
        pbar.refresh()

    print("Fin debug")



if __name__ == '__main__':
    ar_surlignage = Surlignage()

    get_url_all_surlignage(ar_surlignage)
    remplir_surlignage(ar_surlignage)

    debug(ar_surlignage)

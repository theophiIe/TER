from pprint import pprint

import requests
from bs4 import BeautifulSoup

from src.article_court import ArticleCourt


def recup_article() -> None:
    articles = ArticleCourt()
    num_article = 0
    pages = articles.get_nombre_pages()

    for num in range(1, pages + 1):
        articles.get_url_articles(num)

    while num_article < len(articles.url_article):
        page = BeautifulSoup(requests.get(articles.url_article[num_article]).content, 'lxml')

        articles.get_titres_articles(page)
        articles.get_etiquette_articles(page)
        articles.get_articles_en_liens(page)
        articles.get_auteurs_articles(page)
        articles.get_source_date_citation(page)
        articles.get_contenu_articles(page)
        articles.get_liens_citations(page)

        num_article += 31

    pprint(len(articles.url_article))
    pprint(len(articles.titre_article))
    pprint(len(articles.etiquette))
    pprint(len(articles.articles_en_lien))
    pprint(len(articles.contenu_articles))
    pprint(len(articles.auteur_article))
    pprint(len(articles.source_citation))
    pprint(len(articles.date_citation))
    pprint(len(articles.liens_citations))

    # AFFICHAGE POUR LES TESTS

    # for b in range(len(articles.url_article_court)):
    #     print(articles.url_article_court[b])
    #
    # for b in range(len(articles.titre_article_court)):
    #     print(articles.titre_article_court[b])
    #
    # for b in range(len(articles.etiquette)):
    #     print(articles.etiquette[b])
    #
    # for b in range(len(articles.articles_en_lien)):
    #     print(articles.articles_en_lien[b])
    #
    # for b in range(len(articles.contenu_articles)):
    #     print(articles.contenu_articles[b])
    #
    # for b in range(len(articles.auteur_article)):
    #     print(articles.auteur_article[b])
    #
    # for b in range(len(articles.source_citation)):
    #     print(articles.source_citation[b])
    #
    # for b in range(len(articles.date_citation)):
    #     print(articles.date_citation[b])
    #
    # for b in range(len(articles.liens_citations)):
    #     print(articles.liens_citations[b])


# Ajout des textes de loi pour chaque article
# Mieux les articles en sous paragraphe avec les sous-titres et l'intro
# Trouver les noms des personnalités de l'article

if __name__ == '__main__':
    recup_article()






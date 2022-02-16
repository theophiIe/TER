from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from src.scrapping import scrap_article_court
from table import Base, Auteur, Article, EcritPar, UrlArticleEnLien, EnLien, UrlTexte, Reference


def connexion(user: str, pwd: str, host="localhost", port="5432", name="lessurligneurs"):
    engine = create_engine(f"postgresql://{user}:{pwd}@{host}:{port}/{name}")
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)

    return engine


def insert(session, valeur):
    session.add(valeur)
    session.commit()


def insert_auteur(session, element, articles):
    for auteur in articles.auteur_article[element]:
        q = session.query(Auteur).filter(Auteur.nom == auteur)
        if not session.query(q.exists()).scalar():
            insert(session, Auteur(auteur, "à modifier"))


def insert_article(session, element, articles):
    article = Article(articles.titre_article[element],
                      "court",
                      "à modifier",
                      articles.etiquette[element],
                      articles.auteur_article[element])

    insert(session, article)

    return article


def insert_ecritpar(session, element, article, articles):
    for auteur in articles.auteur_article[element]:
        if articles.date_ecriture[element][0] is None:
            ecrit_par = EcritPar(article.article_id, auteur, None)
        else:
            ecrit_par = EcritPar(article.article_id, auteur, articles.date_ecriture[element][0])
        insert(session, ecrit_par)


def insert_url_lien(session, element, article, articles):
    for url in articles.articles_en_lien[element]:
        q = session.query(UrlArticleEnLien).filter(UrlArticleEnLien.url == url)
        if not session.query(q.exists()).scalar():
            url_enlien = UrlArticleEnLien(url)
            insert(session, url_enlien)

        enlien = EnLien(article.article_id, url)
        insert(session, enlien)


def insert_url_ref(session, element, article, articles):
    for url in articles.liens_citations[element]:
        if url is not None:
            q = session.query(UrlTexte).filter(UrlTexte.url == url)
            if not session.query(q.exists()).scalar():
                url_texte = UrlTexte(url)
                insert(session, url_texte)

            # Permet de vérifier que dans un meme article, un url n'apparait qu'une et une seule fois
            q = session.query(Reference)\
                .filter(Reference.article_texte_url == url).filter(Reference.article_id == article.article_id)
            if not session.query(q.exists()).scalar():
                reference = Reference(article.article_id, url)
                insert(session, reference)


def remplissage(engine, articles):
    with Session(bind=engine) as session:
        for element in range(len(articles.url_article)):
            insert_auteur(session, element, articles)
            article = insert_article(session, element, articles)
            insert_ecritpar(session, element, article, articles)
            insert_url_lien(session, element, article, articles)
            insert_url_ref(session, element, article, articles)


if __name__ == '__main__':
    articles_court = scrap_article_court()
    print("Connexion")
    engines = connexion("theophile", "postgres", "localhost", "5432", "lessurligneurs")
    print("Remplir")
    remplissage(engines, articles_court)
    print("Fin")

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from tqdm import tqdm

from src.extracteur.article_court import ArticleCourt
from src.extracteur.article_long import ArticleLong
from src.database.table import Base, Auteur, Article, EcritPar, UrlArticleEnLien, EnLien, UrlTexte, Reference,\
    Contenu, Personnalite, ParleDe


def connexion(user, pwd, host, port, name):
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
            insert(session, Auteur(auteur, articles.profession_auteur[element][0]))


def insert_personnalite(session, element, articles):
    for personnalite in articles.personnalites[element]:
        q = session.query(Personnalite).filter(Personnalite.nom == personnalite)
        if not session.query(q.exists()).scalar():
            perso = Personnalite(personnalite)
            insert(session, perso)


def insert_article_court(session, element, articles):
    date_citation = articles.date_citation[element][0] if articles.date_citation[element] is not None else None

    article = Article(articles.titre_article[element], "court", articles.etiquette[element],
                      articles.source_citation[element], date_citation)

    insert(session, article)

    return article


def insert_article_long(session, element, articles):
    article = Article(articles.titre_article[element], "long", None, None, None)
    insert(session, article)

    return article


def insert_ecritpar(session, element, article, articles):
    for auteur in articles.auteur_article[element]:
        date = articles.date_ecriture[element][0] if articles.date_ecriture[element] is not None else None
        ecrit_par = EcritPar(article.article_id, auteur, date)

        insert(session, ecrit_par)


def insert_parlede(session, element, article, articles):
    for personnalite in articles.personnalites[element]:
        parle_de = ParleDe(article.article_id, personnalite)
        insert(session, parle_de)


def insert_url_lien(session, element, article, articles):
    for url in articles.articles_en_lien[element]:
        q = session.query(UrlArticleEnLien).filter(UrlArticleEnLien.url == url)
        if not session.query(q.exists()).scalar():
            url_enlien = UrlArticleEnLien(url)
            insert(session, url_enlien)

        enlien = EnLien(article.article_id, url)
        insert(session, enlien)


def insert_url_ref(session, element, article, articles):
    for url, nom in zip(articles.liens_citations[element], articles.titre_citations[element]):
        if url is not None:
            q = session.query(UrlTexte).filter(UrlTexte.url == url)
            if not session.query(q.exists()).scalar():
                url_texte = UrlTexte(url, nom)
                insert(session, url_texte)

            # Permet de vérifier que dans un meme article, un url n'apparait qu'une et une seule fois
            q = session.query(Reference)\
                .filter(Reference.article_texte_url == url).filter(Reference.article_id == article.article_id)
            if not session.query(q.exists()).scalar():
                reference = Reference(article.article_id, url)
                insert(session, reference)


def insert_contenu(session, element, article, articles):
    for contenu_article in articles.contenu_articles[element]:
        if contenu_article is not None and contenu_article != " " and contenu_article != "":
            contenus = Contenu(article.article_id, contenu_article)
            insert(session, contenus)


def remplissage(engine, articles):
    pbar = tqdm(range(len(articles.url_article)), colour='green', desc='Progression')
    with Session(bind=engine) as session:
        for element in range(len(articles.url_article)):
            if isinstance(articles, ArticleCourt):
                article = insert_article_court(session, element, articles)
                insert_personnalite(session, element, articles)
                insert_parlede(session, element, article, articles)
            elif isinstance(articles, ArticleLong):
                article = insert_article_long(session, element, articles)
            insert_auteur(session, element, articles)
            insert_ecritpar(session, element, article, articles)
            insert_url_lien(session, element, article, articles)
            insert_url_ref(session, element, article, articles)
            insert_contenu(session, element, article, articles)

            pbar.update(1)
            pbar.refresh()

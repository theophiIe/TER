import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from tqdm import tqdm

from src.extracteur_v2.extraction import get_url_all_surlignage
from src.extracteur_v2.surlignage import Surlignage
from src.database_V2.table_bdd import Base, Auteur, Personnalite, Article, Source, \
    Contenu, Reference, ParleDe, EcritPar, Contient, Refere
from src.extracteur_v2.traitement import recuperation_nom
from flair.models import SequenceTagger


def connexion(user, pwd, host, port, name):
    """
    Permet la connection à une base de données PostgresQL.

    :param user : nom de l'utilisateur de la base de donnée.
    :param pwd : mot de passe pour se connecter à la base de donnée.
    :param host : hôte de la base de données.
    :param port : port de connexion de la base de donnée.
    :param name : nom de la base de données.
    """
    engine = create_engine(f"postgresql://{user}:{pwd}@{host}:{port}/{name}")
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)

    return engine


def insert(session, valeur) -> None:
    session.add(valeur)
    session.commit()


def setup_date(string: str):
    """
    Prend un date et la retructure en format reconnu par PostgreSQL.

    :param string:
    :return la date restructuré sous format PostgreSQL.
    """
    if string is None:
        return None

    dictmois = {
        "janvier": "-01-",
        "février": "-02-",
        "mars": "-03-",
        "avril": "-04-",
        "mai": "-05-",
        "juin": "-06-",
        "juillet": "-07-",
        "août": "-08-",
        "septembre": "-09-",
        "octobre": "-10-",
        "novembre": "-11-",
        "décembre": "-12-"
    }

    data = string.replace("1er", "1").split(" ")

    if len(data) == 3:
        data.reverse()
        for k, v in dictmois.items():
            data[1] = str(data[1]).replace(k, v)

        date = ""
        for valeur in data:
            date += str(valeur)

        date += ", 00:00:00"
        date = datetime.datetime.strptime(date, '%Y-%m-%d, %H:%M:%S').date()
    else:
        datenow = datetime.datetime.today().strftime('%Y-%m-%d, %H:%M:%S')
        date = datetime.datetime.strptime(datenow, '%Y-%m-%d, %H:%M:%S').date()

    return date


def insert_auteur(session, element, articles) -> None:
    """
    Permet l'insertion des auteurs dans la base de données.

    :param session: élément pour l'interaction avec la base de données.
    :param element: numéro d'article courant.
    :param articles: instance de la classe Article.
    """
    for auteur in articles[element]:
        q = session.query(Auteur).filter(Auteur.nom == auteur)
        if not session.query(q.exists()).scalar():
            insert(session, Auteur(auteur, None))


def insert_personnalite(session, element, personnalite) -> None:
    """
    Permet l'insertion des personnalités (personne sur lequel porte l'article) dans la base de données.

    :param session: élément pour l'interaction avec la base de données
    :param element: numéro d'article courant.
    :param personnalite:
    """
    for perso in personnalite[element]:
        q = session.query(Personnalite).filter(Personnalite.nom == perso)
        if not session.query(q.exists()).scalar():
            insert(session, Personnalite(perso))


def insert_source(session, element, articles) -> None:
    """
    Permet l'insertion des sources dans la base de données.

    :param session: élément pour l'interaction avec la base de données
    :param element: numéro d'article courant.
    :param articles: instance de la classe Article.
    """
    if articles.url_source[element][0] is not None:
        q = session.query(Source).filter(Source.URL == articles.url_source[element][0])
        if not session.query(q.exists()).scalar():
            insert(session, Source(articles.url_source[element][0], articles.nom_source[element][0]))


def insert_contenu(session, element, article, articles) -> None:
    """
    Permet l'insertion du contenu de l'article dans la base de données.

    :param session: élément pour l'interaction avec la base de données.
    :param element: numéro d'article courant.
    :param article: instance de la classe Article représente la table des articles dans la base de données.
    :param articles: instance de la classe ArticleCourt ou ArticleLong.
    """

    for contenu_article in articles.contenu[element]:
        if contenu_article is not None and contenu_article not in ["", " "]:
            q = session.query(Contenu).filter(Contenu.texte == contenu_article)
            if not session.query(q.exists()).scalar():
                insert(session, Contenu(contenu_article))


def insert_article(session, element, articles) -> None:
    """
    Permet l'insertion des articles de type court dans la base de données.

    :param session: élément pour l'interaction avec la base de données
    :param element: numéro d'article courant.
    :param articles: instance de la classe Article.
    """

    date_creation = setup_date(articles.date_creation[element])
    date_modificication = setup_date(articles.date_modification[element])

    article = Article(articles.url_surlignage[element], articles.titre[element][0], date_creation, date_modificication,
                      articles.etiquette[element], articles.correction[element], articles.url_source[element][0])

    q = session.query(Article).filter(Article.URL == article.URL)
    if not session.query(q.exists()).scalar():
        insert(session, article)


def remplissage_article(engine, article) -> None:
    """
    Permet de remplir la base de données.

    :param article:
    :param engine : MockConnection de la base de données.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Progression')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_article(session, element, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_auteur(engine, auteurs) -> None:
    """
    Permet de remplir la base de données.

    :param auteurs:
    :param engine : MockConnection de la base de données.
    """
    pbar = tqdm(range(len(auteurs)), colour='green', desc='Progression')
    with Session(bind=engine) as session:
        for element in range(len(auteurs)):
            insert_auteur(session, element, auteurs)
            pbar.update(1)
            pbar.refresh()


def remplissage_personnalite(engine, personnalite) -> None:
    """
    Permet de remplir la base de données.

    :param personnalite:
    :param engine : MockConnection de la base de données.
    """
    pbar = tqdm(range(len(personnalite)), colour='green', desc='Progression')
    with Session(bind=engine) as session:
        for element in range(len(personnalite)):
            insert_personnalite(session, element, personnalite)
            pbar.update(1)
            pbar.refresh()


def remplissage_source(engine, article) -> None:
    """
    Permet de remplir la base de données.

    :param source:
    :param engine : MockConnection de la base de données.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Progression')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_source(session, element, article)
            pbar.update(1)
            pbar.refresh()

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from tqdm import tqdm

from src.database.table_bdd import Base, Auteur, Personnalite, Article, Source, \
    Contenu, Reference, ParleDe, EcritPar, Contient, Refere, ArticleEnLien, EnLien


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
    """
    Permet d'insérer les tuples dans la base de donnée et de commit l'insertion.
    :param session : instance de connexion à la base de donnée.
    :param valeur : tuple à insérer.
    """
    session.add(valeur)
    session.commit()


def setup_date(string: str):
    """
    Prend une date et la reformate dans un format reconnu par PostgreSQL.

    :param string : la date à formater.
    :return : la date reformatée sous format PostgreSQL.
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

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param articles : instance de la classe Surlignage.
    """
    for auteur in articles[element]:
        q = session.query(Auteur).filter(Auteur.nom == auteur)
        if not session.query(q.exists()).scalar():
            insert(session, Auteur(auteur, None))


def insert_personnalite(session, element, personnalite) -> None:
    """
    Permet l'insertion des personnalités (personne sur lequel porte l'article) dans la base de données.

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param personnalite : nom de la personnalité.
    """
    for perso in personnalite[element]:
        q = session.query(Personnalite).filter(Personnalite.nom == perso)
        if not session.query(q.exists()).scalar():
            insert(session, Personnalite(perso))


def insert_source(session, element, articles) -> None:
    """
    Permet l'insertion des sources dans la base de données.

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param articles : instance de la classe Surlignage.
    """
    if articles.url_source[element][0] is not None:
        q = session.query(Source).filter(Source.URL == articles.url_source[element][0])
        if not session.query(q.exists()).scalar():
            insert(session, Source(articles.url_source[element][0], articles.nom_source[element][0]))


def insert_contenu(session, element, articles) -> None:
    """
    Permet l'insertion du contenu de l'article dans la base de données.

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param articles : instance de la classe Surlignage.
    """

    for contenu_article in articles.contenu[element]:
        if contenu_article is not None and contenu_article not in ["", " "]:
            q = session.query(Contenu).filter(Contenu.texte == contenu_article)
            if not session.query(q.exists()).scalar():
                insert(session, Contenu(contenu_article))


def insert_article(session, element, articles) -> None:
    """
    Permet l'insertion des articles de type court dans la base de données.

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param articles : instance de la classe Surlignage.
    """

    date_creation = setup_date(articles.date_creation[element])
    date_modificication = setup_date(articles.date_modification[element])

    article = Article(articles.url_surlignage[element], articles.titre[element][0], date_creation, date_modificication,
                      articles.correction[element], articles.etiquette[element], articles.url_source[element][0])

    q = session.query(Article).filter(Article.URL == article.URL)
    if not session.query(q.exists()).scalar():
        insert(session, article)


def insert_ecritpar(session, element, auteurs, relecteurs, secretariats, article) -> None:
    """
    Permet l'insertion des articles de type court dans la base de données.

    :param article : instance de la classe Surlignage.
    :param secretariats : tableau contenant les personnes liées au secrétariat.
    :param relecteurs : tableau contenant les personnes liées aux relecteurs.
    :param auteurs : tableau contenant les personnes liées aux auteurs.
    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    """

    for auteur in auteurs[element]:
        q = session.query(EcritPar).filter(EcritPar.nom == auteur).filter(EcritPar.URL == article.url_surlignage[element])
        if not session.query(q.exists()).scalar():
            ecrit_par = EcritPar(article.url_surlignage[element], auteur, "Auteur")
            insert(session, ecrit_par)

    for relecteur in relecteurs[element]:
        q = session.query(EcritPar).filter(EcritPar.nom == relecteur).filter(EcritPar.URL == article.url_surlignage[element])
        if not session.query(q.exists()).scalar():
            ecrit_par = EcritPar(article.url_surlignage[element], relecteur, "Relecteur")
            insert(session, ecrit_par)

    for secretariat in secretariats[element]:
        q = session.query(EcritPar).filter(EcritPar.nom == secretariat).filter(EcritPar.URL == article.url_surlignage[element])
        if not session.query(q.exists()).scalar():
            ecrit_par = EcritPar(article.url_surlignage[element], secretariat, "Secretariat")
            insert(session, ecrit_par)


def insert_parlede(session, element, personnalite, article) -> None:
    """
    Permet l'insertion des articles de type court dans la base de données.

    :param personnalite : nom de la personnalité
    :param article : instance de la classe Surlignage.
    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    """

    for auteur in personnalite[element]:
        q = session.query(ParleDe).filter(ParleDe.nom == auteur).filter(ParleDe.URL == article.url_surlignage[element])
        if not session.query(q.exists()).scalar():
            parle_de = ParleDe(article.url_surlignage[element], auteur)
            insert(session, parle_de)


def insert_reference(session, element, article) -> None:
    """
    Permet l'insertion des références dans la base de données.

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param article : instance de la classe Surlignage.
    """
    for ref in enumerate(article.url_references[element]):
        if article.url_references[element][ref[0]] is not None:
            q = session.query(Reference).filter(Reference.URL == article.url_references[element][ref[0]])
            if not session.query(q.exists()).scalar():
                insert(session, Reference(article.url_references[element][ref[0]],
                                          article.nom_references[element][ref[0]]))


def insert_refere(session, element, article) -> None:
    """
    Permet l'insertion des références en fonction des articles dans la base de données.

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param article : instance de la classe Surlignage.
    """
    for ref in enumerate(article.url_references[element]):
        if article.url_references[element][ref[0]] is not None:
            q = session.query(Refere).filter(Refere.URL_article == article.url_surlignage[element]) \
                .filter(Refere.URL_reference == article.url_references[element][ref[0]])
            if not session.query(q.exists()).scalar():
                insert(session, Refere(article.url_surlignage[element], article.url_references[element][ref[0]]))


def insert_contient(session, element, article) -> None:
    """
    Permet l'insertion des contenus en fonction des articles dans la base de données.

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param article : instance de la classe Surlignage.
    """
    for paragraphe in enumerate(article.contenu[element]):
        if article.contenu[element][paragraphe[0]] not in [None, " ", ""]:
            q = session.query(Contient).filter(Contient.URL == article.url_surlignage[element]) \
                .filter(Contient.ID == article.contenu[element][paragraphe[0]])
            if not session.query(q.exists()).scalar():
                insert(session, Contient(article.url_surlignage[element], article.contenu[element][paragraphe[0]]))


def insert_article_en_lien(session, element, articles) -> None:
    """
    Permet l'insertion des articles en lien dans la base de données.

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param articles : instance de la classe Surlignage.
    """
    for article in enumerate(articles.meme_theme[element]):
        if article[0] is not None:
            q = session.query(ArticleEnLien).filter(ArticleEnLien.URL == articles.meme_theme[element][article[0]])
            if not session.query(q.exists()).scalar():
                insert(session, ArticleEnLien(articles.meme_theme[element][article[0]]))


def insert_en_lien(session, element, articles) -> None:
    """
    Permet l'insertion des articles en lien en fonction de chaque article dans la base de données.

    :param session : instance de connexion à la base de donnée.
    :param element : numéro d'article courant.
    :param articles : instance de la classe Surlignage.
    """
    for article_lien in enumerate(articles.meme_theme[element]):
        if articles.meme_theme[element][article_lien[0]] is not None:
            q = session.query(EnLien).filter(EnLien.URL_article == articles.url_surlignage[element]) \
                .filter(EnLien.URL_article_en_lien == articles.meme_theme[element][article_lien[0]])
            if not session.query(q.exists()).scalar():
                insert(session, EnLien(articles.url_surlignage[element], articles.meme_theme[element][article_lien[0]]))


def remplissage_article(engine, article) -> None:
    """
    Permet de remplir les articles dans la base de données.

    :param article : Instance de la classe Surlignage.
    :param engine : instance de connexion à la base de donnée.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage article')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_article(session, element, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_auteur(engine, auteurs) -> None:
    """
    Permet de remplir les auteurs dans la base de données.

    :param auteurs : tableau contenant les auteurs.
    :param engine : instance de connexion à la base de donnée.
    """
    pbar = tqdm(range(len(auteurs)), colour='green', desc='Remplissage auteur')
    with Session(bind=engine) as session:
        for element in range(len(auteurs)):
            insert_auteur(session, element, auteurs)
            pbar.update(1)
            pbar.refresh()


def remplissage_personnalite(engine, personnalite) -> None:
    """
    Permet de remplir les personnalités dans la base de données.

    :param personnalite : tableau contenant les personnalités.
    :param engine : instance de connexion à la base de donnée.
    """
    pbar = tqdm(range(len(personnalite)), colour='green', desc='Remplissage personnalité')
    with Session(bind=engine) as session:
        for element in range(len(personnalite)):
            insert_personnalite(session, element, personnalite)
            pbar.update(1)
            pbar.refresh()


def remplissage_source(engine, article) -> None:
    """
    Permet de remplir les sources dans la base de données.

    :param article : instance de la classe Surlignage.
    :param engine : instance de connexion à la base de donnée.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage source')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_source(session, element, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_contenu(engine, article) -> None:
    """
    Permet de remplir le texte des articles la base de données.

    :param article : instance de la classe Surlignage.
    :param engine : instance de connexion à la base de donnée.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage contenu')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_contenu(session, element, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_ecrit_par(engine, article, auteurs, relecteurs, secretariat) -> None:
    """
    Permet de mettre en relation les articles ainsi que leurs auteurs dans la base de données.

    :param engine : instance de connexion à la base de données.
    :param article : instance de la classe Surlignage.
    :param auteurs : tableau contenant les auteurs.
    :param relecteurs : tableau contenant les relecteurs.
    :param secretariat : tableau contenant les membres du secretariat.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage ecrit_par')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_ecritpar(session, element, auteurs, relecteurs, secretariat, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_parlede(engine, personnalite, article) -> None:
    """
    Permet de remplir les personnalités en fonctions des articles la base de données.

    :param engine : instance de connexion à la base de donnée.
    :param personnalite : tableau contenant les personnalités.
    :param article : instance de la classe Surlignage.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage parle_de')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_parlede(session, element, personnalite, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_reference(engine, article) -> None:
    """
    Permet de remplir les URLs contenant dans le texte des articles dans la base de données.
    :param engine : instance de connexion à la base de donnée.
    :param article : instance de la classe Surlignage.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage Reference')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_reference(session, element, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_refere(engine, article) -> None:
    """
    Permet de remplir les URLs des références en fonction des articles dans la base de données.
    :param engine : instance de connexion à la base de donnée.
    :param article : instance de la classe Surlignage.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage Refere')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_refere(session, element, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_contient(engine, article) -> None:
    """
    Permet de remplir le texte des articles en fonctions des articles dans la base de données.
    :param engine : instance de connexion à la base de donnée.
    :param article : instance de la classe Surlignage.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage Contient')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_contient(session, element, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_article_en_lien(engine, article) -> None:
    """
    Permet de remplir les URL des articles en liens en fonction des articles insérés dans la base de données.
    :param engine : instance de connexion à la base de donnée.
    :param article : instance de la classe Surlignage.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage ArticleEnLien')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_article_en_lien(session, element, article)
            pbar.update(1)
            pbar.refresh()


def remplissage_en_lien(engine, article) -> None:
    """
    Permet de remplir les articles en lien à chaque article dans la base de données.
    :param engine : instance de connexion à la base de donnée.
    :param article : instance de la classe Surlignage.
    """
    pbar = tqdm(range(len(article.url_surlignage)), colour='green', desc='Remplissage EnLien')
    with Session(bind=engine) as session:
        for element in range(len(article.url_surlignage)):
            insert_en_lien(session, element, article)
            pbar.update(1)
            pbar.refresh()

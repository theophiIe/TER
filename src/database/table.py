import datetime

from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = "T_Article"

    titre = Column(String, primary_key=True)
    type_article = Column(String)
    contenu = Column(String)

    def __init__(self, titre: str, type_article: str, contenu: str):
        self.titre = titre
        self.type_article = type_article
        self.contenu = contenu


class Etiquette(Base):
    __tablename__ = "T_Etiquette"

    nom = Column(String, primary_key=True)

    def __init__(self, nom: str):
        self.nom = nom


class UrlArticle(Base):
    __tablename__ = "T_UrlArticle"

    url = Column(String, primary_key=True)

    def __init__(self, url: str):
        self.url = url


class UrlTexte(Base):
    __tablename__ = "T_UrlTexte"

    url = Column(String, primary_key=True)

    def __init__(self, url: str):
        self.url = url


class Auteur(Base):
    __tablename__ = "T_Auteur"

    nom = Column(String, primary_key=True)
    profession = Column(String)

    def __init__(self, nom: str, profession):
        self.nom = nom
        self.profession = profession


class Personnalite(Base):
    __tablename__ = "T_Personnalite"

    nom = Column(String, primary_key=True)

    def __init__(self, nom: str):
        self.nom = nom


class Reference(Base):
    __tablename__ = "T_Reference"

    article = Column(ForeignKey("T_Article.titre"), primary_key=True)
    url = Column(ForeignKey("T_UrlTexte.url"), primary_key=True)

    def __init__(self, article: str, url: str):
        self.article = article
        self.url = url


class EnLien(Base):
    __tablename__ = "T_EnLien"

    article = Column(ForeignKey("T_Article.titre"), primary_key=True)
    url = Column(ForeignKey("T_UrlArticle.url"), primary_key=True)

    def __init__(self, article: str, url: str):
        self.article = article
        self.url = url


class EcritPar(Base):
    __tablename__ = "T_EcritPar"

    auteur = Column(ForeignKey("T_Auteur.nom"), primary_key=True)
    article = Column(ForeignKey("T_Article.titre"), primary_key=True)
    date_ecrit = Column(Date)

    def __init__(self, auteur: str, article: str, date_ecrit: datetime.date):
        self.auteur = auteur
        self.article = article
        self.date_ecrit = date_ecrit


class ParleDe(Base):
    __tablename__ = "T_ParleDe"

    personnalite = Column(ForeignKey("T_Personnalite.nom"), primary_key=True)
    article = Column(ForeignKey("T_Article.titre"), primary_key=True)
    lieu = Column(String)

    def __init__(self, personnalite: str, article: str, lieu: str):
        self.personnalite = personnalite
        self.article = article
        self.lieu = lieu


class Represente(Base):
    __tablename__ = "T_Represente"

    etiquette = Column(ForeignKey("T_Etiquette.nom"), primary_key=True)
    article = Column(ForeignKey("T_Article.titre"), primary_key=True)

    def __init__(self, etiquette: str, article: str):
        self.etiquette = etiquette
        self.article = article


if __name__ == '__main__':
    pass

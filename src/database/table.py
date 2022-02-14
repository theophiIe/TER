import datetime

from sqlalchemy import Column, String, Date, ForeignKey, Table, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

"""ASSOCIATION TABLE"""


References = Table('T_Reference', Base.metadata,
                   Column('url', ForeignKey('T_UrlArticle.url'), primary_key=True),
                   Column('article', ForeignKey('T_Article.article_id'), primary_key=True)
                   )

En_lien = Table('T_EnLien', Base.metadata,
                Column('url', ForeignKey('T_UrlTexte.url'), primary_key=True),
                Column('article', ForeignKey('T_Article.article_id'), primary_key=True)
                )


class EcritPar(Base):
    __tablename__ = "T_EcritPar"

    auteur_id = Column(ForeignKey("T_Auteur.nom"), primary_key=True)
    article_id = Column(ForeignKey("T_Article.article_id"), primary_key=True)
    date_ecrit = Column(Date)

    auteur = relationship("T_Auteur", back_populates="articles")
    article = relationship("T_Article", back_populates="auteurs")


"""TABLE ENTITEES"""


class Article(Base):
    __tablename__ = "T_Article"

    article_id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(200), nullable=False, unique=True)
    type_article = Column(String(5), nullable=False)
    contenu = Column(String, nullable=False, unique=True)

    etiquette = Column(String(20), nullable=True)

    personnalite = Column(String(50), nullable=True)
    lieu = Column(String(100), nullable=True)

    # Pour les auteurs
    auteurs = relationship("T_EcritPar", back_populates="article")

    # Pour les references dans le texte
    reference = relationship("T_UrlTexte", secondary=References, back_populates="articles")

    # Pour les articles en lien
    articleEnLien = relationship("T_UrlArticle", secondary=En_lien, back_populates="articles")

    def __init__(self, titre: str, type_article: str, contenu: str, etiquette: str, personnalite: str, lieu: str):
        self.titre = titre
        self.type_article = type_article
        self.contenu = contenu
        self.etiquette = etiquette
        self.personnalite = personnalite
        self.lieu = lieu


class UrlArticle(Base):
    __tablename__ = "T_UrlArticle"

    url = Column(String, primary_key=True)

    articles = relationship("T_Article", secondary=En_lien, back_populates="articleEnLien")

    def __init__(self, url: str):
        self.url = url


class UrlTexte(Base):
    __tablename__ = "T_UrlTexte"

    url = Column(String, primary_key=True)

    articles = relationship("T_Article", secondary=References, back_populates="reference")

    def __init__(self, url: str):
        self.url = url


class Auteur(Base):
    __tablename__ = "T_Auteur"

    nom = Column(String, primary_key=True)
    profession = Column(String(200))

    # Relation avec la table d'association EcritPar
    articles = relationship("T_EcritPar", back_populates="auteur")

    def __init__(self, nom: str, profession):
        self.nom = nom
        self.profession = profession

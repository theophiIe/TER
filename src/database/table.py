import datetime

from sqlalchemy import Column, String, Date, ForeignKey, Table, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

"""ASSOCIATION TABLE"""


References = Table('t_reference', Base.metadata,
                   Column('url', ForeignKey('t_urlarticle.url'), primary_key=True),
                   Column('article', ForeignKey('t_article.article_id'), primary_key=True)
                   )

En_lien = Table('T_EnLien', Base.metadata,
                Column('url', ForeignKey('t_urltexte.url'), primary_key=True),
                Column('article', ForeignKey('t_article.article_id'), primary_key=True)
                )


class EcritPar(Base):
    __tablename__ = "t_ecritpar"

    auteur_id = Column(ForeignKey("t_auteur.nom"), primary_key=True)
    article_id = Column(ForeignKey("t_article.article_id"), primary_key=True)
    date_ecrit = Column(Date)

    auteur = relationship("t_auteur", back_populates="articles")
    article = relationship("t_article", back_populates="auteurs")


"""TABLE ENTITEES"""


class Article(Base):
    __tablename__ = "t_article"

    article_id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(200), nullable=False, unique=True)
    type_article = Column(String(5), nullable=False)
    contenu = Column(String, nullable=False, unique=True)

    etiquette = Column(String(20), unique=True, nullable=True)

    personnalite = Column(String(50), nullable=True)
    lieu = Column(String(100), nullable=True)

    # Pour les auteurs
    auteurs = relationship("t_ecritpar", back_populates="article")

    # Pour les references dans le texte
    reference = relationship("t_urltexte", secondary=References, back_populates="articles")

    # Pour les articles en lien
    articleEnLien = relationship("t_urlarticle", secondary=En_lien, back_populates="articles")

    def __init__(self, titre: str, type_article: str, contenu: str, etiquette: str, personnalite: str, lieu: str):
        self.titre = titre
        self.type_article = type_article
        self.contenu = contenu
        self.etiquette = etiquette
        self.personnalite = personnalite
        self.lieu = lieu


class UrlArticle(Base):
    __tablename__ = "t_urlarticle"

    url = Column(String, primary_key=True)

    articles = relationship("t_article", secondary=En_lien, back_populates="articleEnLien")

    def __init__(self, url: str):
        self.url = url


class UrlTexte(Base):
    __tablename__ = "t_urltexte"

    url = Column(String, primary_key=True)

    articles = relationship("t_article", secondary=References, back_populates="reference")

    def __init__(self, url: str):
        self.url = url


class Auteur(Base):
    __tablename__ = "t_auteur"

    nom = Column(String, primary_key=True)
    profession = Column(String(200))

    # Relation avec la table d'association EcritPar
    articles = relationship("t_ecritpar", back_populates="auteur")

    def __init__(self, nom: str, profession):
        self.nom = nom
        self.profession = profession

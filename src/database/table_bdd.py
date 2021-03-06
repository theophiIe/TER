from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Auteur(Base):
    """
    Classe permettant de créer la table Auteur dans la base de donnée.
    """
    __tablename__ = "t_auteur"

    nom = Column(String, primary_key=True)

    def __init__(self, nom):
        self.nom = nom

    # Relationship avec EcritPar
    parent_ecritpar = relationship("EcritPar", back_populates="child_ecritpar")


class Personnalite(Base):
    """
    Classe permettant de créer la table Personnalité dans la base de donnée.
    """
    __tablename__ = "t_personnalite"

    nom = Column(String, primary_key=True)

    def __init__(self, nom):
        self.nom = nom

    # Relationship avec ParleDe
    parent_parlede = relationship("ParleDe", back_populates="child_parlede")


class Article(Base):
    """
    Classe permettant de créer la table Article dans la base de donnée.
    """
    __tablename__ = "t_article"

    url = Column(String, primary_key=True)
    titre = Column(String, nullable=False)
    date_creation = Column(Date, nullable=False)
    date_modification = Column(Date)
    etiquette = Column(String, nullable=True)
    correction = Column(String, nullable=True)

    # Foreign Key de source
    source = Column(String, ForeignKey('t_source.url'))

    def __init__(self, url: str, titre: str, date_creation, date_modification, correction: str, etiquette: str,
                 source: str):
        self.url = url
        self.titre = titre
        self.date_creation = date_creation
        self.date_modification = date_modification
        self.correction = correction
        self.etiquette = etiquette
        self.source = source

    # Relationship avec Source
    child_source = relationship("Source", back_populates="parent_source")

    # Relationship avec ParleDe
    child_parlede = relationship("ParleDe", back_populates="parent_parlede")

    # Relationship avec EcritPar
    child_ecritpar = relationship('EcritPar', back_populates="parent_ecritpar")

    # Relationship avec Contient
    child_contient = relationship('Contient', back_populates="parent_contient")

    # Relationship avec Refere
    child_refere = relationship('Refere', back_populates="parent_refere")

    # Relationship avec Enlien
    child_articleenlien = relationship('EnLien', back_populates="parent_articleenlien")


class Source(Base):
    """
    Classe permettant de créer la table Source dans la base de donnée.
    """
    __tablename__ = "t_source"

    url = Column(String, primary_key=True)
    nom = Column(String, nullable=False)

    def __init__(self, url: str, nom: str):
        self.url = url
        self.nom = nom

    # Relationship avec Article
    parent_source = relationship("Article", back_populates="child_source")


class Contenu(Base):
    """
    Classe permettant de créer la table Contenu dans la base de donnée.
    """
    __tablename__ = "t_contenu"

    texte = Column(String, primary_key=True)

    def __init__(self, texte: str):
        self.texte = texte

    # Relationship avec Contient
    parent_contient = relationship('Contient', back_populates="child_contient")


class Reference(Base):
    """
    Classe permettant de créer la table Reference dans la base de donnée.
    """
    __tablename__ = "t_reference"

    url = Column(String, primary_key=True)
    nom = Column(String, nullable=False)

    def __init__(self, url: str, nom: str):
        self.url = url
        self.nom = nom

    # Relationship avec refere
    parent_refere = relationship('Refere', back_populates="child_refere")


class ParleDe(Base):
    """
    Classe permettant de créer la table ParleDe dans la base de donnée.
    """
    __tablename__ = "t_parlede"

    # Foreign Key de Article
    url = Column(ForeignKey('t_article.url'), primary_key=True)

    # Foreign Key de Personnalite
    nom = Column(ForeignKey('t_personnalite.nom'), primary_key=True)

    # Relationship avec Article
    parent_parlede = relationship("Article", back_populates="child_parlede")

    # Relationship avec Personnalite
    child_parlede = relationship("Personnalite", back_populates="parent_parlede")

    def __init__(self, url: str, nom: str):
        self.url = url
        self.nom = nom


class EcritPar(Base):
    """
    Classe permettant de créer la table Auteur EcritPar la base de donnée.
    """
    __tablename__ = "t_ecritpar"

    # Foreign Key de Article
    url = Column(ForeignKey('t_article.url'), primary_key=True)

    # Foreign Key de Auteur
    nom = Column(ForeignKey('t_auteur.nom'), primary_key=True)

    roles = Column(String, primary_key=True)

    # Relationship avec Article
    parent_ecritpar = relationship('Article', back_populates="child_ecritpar")

    # Relationship avec Auteur
    child_ecritpar = relationship('Auteur', back_populates="parent_ecritpar")

    def __init__(self, url: str, nom: str, role:str):
        self.url = url
        self.nom = nom
        self.roles = role


class Contient(Base):
    """
    Classe permettant de créer la table Contient dans la base de donnée.
    """
    __tablename__ = "t_contient"

    # Foreign Key de Article
    url = Column(ForeignKey('t_article.url'), primary_key=True)

    # Foreign Key de Contenue
    id = Column(ForeignKey('t_contenu.texte'), primary_key=True)

    # Relationship avec Article
    parent_contient = relationship('Article', back_populates="child_contient")

    # Relationship avec Contenue
    child_contient = relationship('Contenu', back_populates="parent_contient")

    def __init__(self, url: str, id: int):
        self.url = url
        self.id = id


class Refere(Base):
    """
    Classe permettant de créer la table Refere la base de donnée.
    """
    __tablename__ = "t_refere"

    # Foreign Key de Article
    url_article = Column(ForeignKey('t_article.url'), primary_key=True)

    # Foreign Key de Reference
    url_reference = Column(ForeignKey('t_reference.url'), primary_key=True)

    # Relationship avec Article
    parent_refere = relationship('Article', back_populates="child_refere")

    # Relationship avec Reference
    child_refere = relationship('Reference', back_populates="parent_refere")

    def __init__(self, url_article: str, url_reference: str):
        self.url_article = url_article
        self.url_reference = url_reference


class ArticleEnLien(Base):
    """
    Classe permettant de créer la table ArticleEnLien la base de donnée.
    """
    __tablename__ = "t_articleenlien"

    url = Column(String, primary_key=True)

    # Relationship avec EnLien
    parent_articleenlien = relationship('EnLien', back_populates="child_articleenlien")

    def __init__(self, url: str):
        self.url = url


class EnLien(Base):
    """
    Classe permettant de créer la table EnLien la base de donnée.
    """
    __tablename__ = "t_enlien"

    # Foreign Key de Article
    url_article = Column(ForeignKey('t_article.url'), primary_key=True)

    # Foreign Key de Article
    url_article_en_lien = Column(ForeignKey('t_articleenlien.url'), primary_key=True)

    # Relationship avec Article 1
    parent_articleenlien = relationship('Article', back_populates="child_articleenlien")

    # Relationship avec Article 2
    child_articleenlien = relationship('ArticleEnLien', back_populates="parent_articleenlien")

    def __init__(self, url1: str, url2: str):
        self.url_article = url1
        self.url_article_en_lien = url2

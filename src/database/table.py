from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Auteur(Base):
    __tablename__ = "t_auteur"

    nom = Column(String, primary_key=True)
    profession = Column(String)

    def __init__(self, nom, profession):
        self.nom = nom
        self.profession = profession

    # Relationship avec EcritPar
    parents_ecritpar = relationship("EcritPar", back_populates="child_ecritpar")


class Article(Base):
    __tablename__ = "t_article"

    article_id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=False, unique=True)
    type_article = Column(String(5), nullable=False)
    contenu = Column(String, nullable=False)
    etiquette = Column(String, nullable=True)
    personnalite = Column(String)
    lieu = Column(String)

    def __init__(self, titre: str, type_article: str, contenu: str, etiquette: str, personnalite: str):
        self.titre = titre
        self.type_article = type_article
        self.contenu = contenu
        self.etiquette = etiquette
        self.personnalite = personnalite

    # Relationship avec EcritPar
    children_ecritpar = relationship("EcritPar", back_populates="parent_ecritpar")

    # Relationship avec EnLien
    children_enlien = relationship("EnLien", back_populates="parent_enlien")

    # Relationship avec Reference
    children_reference = relationship("Reference", back_populates="parent_reference")


class UrlArticleEnLien(Base):
    __tablename__ = "t_articleenlien"

    url = Column(String, primary_key=True)

    def __init__(self, url):
        self.url = url

    # Relationship avec Enlien
    parents_enlien = relationship("EnLien", back_populates="child_enlien")


class UrlTexte(Base):
    __tablename__ = "t_urltexte"

    url = Column(String, primary_key=True)

    def __init__(self, url):
        self.url = url

    # Relationship avec Reference
    parents_reference = relationship("Reference", back_populates="child_reference")


class EcritPar(Base):
    __tablename__ = "t_ecritpar"

    # ForeignKey de Article
    article_id = Column(ForeignKey('t_article.article_id'), primary_key=True)

    # ForeignKey de Auteur
    auteur_nom = Column(ForeignKey('t_auteur.nom'), primary_key=True)

    date_ecriture = Column(String)

    # Relationship de Article
    child_ecritpar = relationship("Auteur", back_populates="parents_ecritpar")

    # Relationship de Auteur
    parent_ecritpar = relationship("Article", back_populates="children_ecritpar")

    def __init__(self, article_id, auteur_nom, date_ecriture):
        self.article_id = article_id
        self.auteur_nom = auteur_nom
        self.date_ecriture = date_ecriture


class EnLien(Base):
    __tablename__ = "t_enlien"

    # ForeignKey de Article
    article_id = Column(ForeignKey('t_article.article_id'), primary_key=True)

    # ForeignKey de UrlArticleEnLien
    article_en_lien_url = Column(ForeignKey('t_articleenlien.url'), primary_key=True)

    def __init__(self, article_id, article_url):
        self.article_id = article_id
        self.article_en_lien_url = article_url

    # Relationship de Article
    child_enlien = relationship("UrlArticleEnLien", back_populates="parents_enlien")

    # Relationship de UrlArticleEnLien
    parent_enlien = relationship("Article", back_populates="children_enlien")


class Reference(Base):
    __tablename__ = "t_reference"

    # ForeignKey de Article
    article_id = Column(ForeignKey('t_article.article_id'), primary_key=True)

    # ForeignKey de UrlTexte
    article_texte_url = Column(ForeignKey('t_urltexte.url'), primary_key=True)

    def __init__(self, article_id, article_url):
        self.article_id = article_id
        self.article_texte_url = article_url

    # Relationship de Article
    child_reference = relationship("UrlTexte", back_populates="parents_reference")

    # Relationship de UrlTexte
    parent_reference = relationship("Article", back_populates="children_reference")

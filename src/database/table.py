import datetime

from sqlalchemy import Column, String, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

References = Table('T_Reference', Base.metadata,
                   Column('url', ForeignKey('T_UrlArticle.url'), primary_key=True),
                   Column('article', ForeignKey('T_Article.reference_id'), primary_key=True)
                   )


class Article(Base):
    __tablename__ = "T_Article"

    titre = Column(String, primary_key=True)
    type_article = Column(String)
    contenu = Column(String)
    reference_id = Column(String)

    # use for relationship between table
    etiquette_id = Column(String)
    personnalite_id = Column(String)

    # ONE-TO-ONE RELATIONSHIP
    # Pour les personnalités
    personnalite = relationship("Personnalite", back_populates="T_Article", uselist=False)
    # Pour les etiquettes
    etiquette = relationship("Etiquette", back_populates="T_Article", uselist=False)
    # Pour les auteurs
    auteur = relationship("T_EcritPar", back_populates="article")

    # MANY-TO-MANY
    # Pour les references dans le texte
    reference = relationship("T_UrlArticle", secondary=References, back_populates="articles")

    def __init__(self, titre: str, type_article: str, contenu: str):
        self.titre = titre
        self.type_article = type_article
        self.contenu = contenu


class Etiquette(Base):
    __tablename__ = "T_Etiquette"

    nom = Column(String, primary_key=True)

    # use for relationship between table
    article_id = Column(String, ForeignKey('T_Article.etiquette'))

    # many-to-one relationship
    article = relationship("Article", back_populates="T_Etiquette")

    def __init__(self, nom: str):
        self.nom = nom


class UrlArticle(Base):
    __tablename__ = "T_UrlArticle"

    url = Column(String, primary_key=True)

    articles = relationship("T_Article", secondary=References, back_populates="reference")

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

    # Relation avec la table d'association EcritPar
    article = relationship("T_EcritPar", back_populates="auteur")

    def __init__(self, nom: str, profession):
        self.nom = nom
        self.profession = profession


class Personnalite(Base):
    __tablename__ = "T_Personnalite"

    nom = Column(String, primary_key=True)
    article_id = Column(String, ForeignKey('T_Article.personnalite_id'))

    # many-to-one relationship
    article = relationship("Article", back_populates="T_Personnalite")

    def __init__(self, nom: str):
        self.nom = nom


if __name__ == '__main__':
    pass

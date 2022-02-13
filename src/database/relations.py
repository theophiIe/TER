import datetime

from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

""" Pas utile car la table d'association n'a pas d'autres attributs """
# class Reference(Base):
#     __tablename__ = "T_Reference"
#
#     article_id = Column(ForeignKey("T_Article.titre"), primary_key=True)
#     url_id = Column(ForeignKey("T_UrlTexte.url"), primary_key=True)
#
#     url = relationship()
#     article = relationship()


class EnLien(Base):
    __tablename__ = "T_EnLien"

    article = Column(ForeignKey("T_Article.titre"), primary_key=True)
    url = Column(ForeignKey("T_UrlArticle.url"), primary_key=True)


class EcritPar(Base):
    __tablename__ = "T_EcritPar"

    auteur_id = Column(ForeignKey("T_Auteur.nom"), primary_key=True)
    article_id = Column(ForeignKey("T_Article.titre"), primary_key=True)
    date_ecrit = Column(Date)

    auteur = relationship("T_Auteur", back_populates="article")
    article = relationship("T_Article", back_populates="auteur")


""" Normalement selon mon schéma c'est inutile """
# class ParleDe(Base):
#     __tablename__ = "T_ParleDe"
#
#     personnalite = Column(ForeignKey("T_Personnalite.nom"), primary_key=True)
#     article = Column(ForeignKey("T_Article.titre"), primary_key=True)
#     lieu = Column(String)
#
#     def __init__(self, personnalite: str, article: str, lieu: str):
#         self.personnalite = personnalite
#         self.article = article
#         self.lieu = lieu
#
#
# class Represente(Base):
#     __tablename__ = "T_Represente"
#
#     etiquette = Column(ForeignKey("T_Etiquette.nom"), primary_key=True)
#     article = Column(ForeignKey("T_Article.titre"), primary_key=True)
#
#     def __init__(self, etiquette: str, article: str):
#         self.etiquette = etiquette
#         self.article = article

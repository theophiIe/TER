from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from table import Base, Auteur, Article, EcritPar, UrlArticleEnLien, EnLien, UrlTexte, Reference

engine = create_engine(f"postgresql://postgres@/lessurligneurs")
print(database_exists(engine.url))
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))

Base.metadata.create_all(engine)
auteur = Auteur("Jojo", "chomeur")
article = Article("blabla", "long", "bonjour mesdames")
article2 = Article("blbl", "long", " mesdames")

with Session(bind=engine) as session:

    session.add(auteur)
    session.add(article)
    session.add(article2)
    session.commit()

    ecritpar = EcritPar(article.article_id, auteur.nom)
    ecritpar2 = EcritPar(article2.article_id, auteur.nom)
    session.add(ecritpar)
    session.add(ecritpar2)
    session.commit()

    articleenlien = UrlArticleEnLien("https://test1/")
    articleenlien2 = UrlArticleEnLien("https://test2")
    session.add(articleenlien)
    session.add(articleenlien2)
    session.commit()

    enlien = EnLien(article.article_id, articleenlien.url)
    enlien2 = EnLien(article2.article_id, articleenlien2.url)
    session.add(enlien)
    session.add(enlien2)
    session.commit()

    urltexte = UrlTexte("https://test3/")
    urltexte2 = UrlTexte("https://test4/")
    session.add(urltexte)
    session.add(urltexte2)
    session.commit()

    reference = Reference(article.article_id, urltexte.url)
    reference2 = Reference(article.article_id, urltexte2.url)
    session.add(reference)
    session.add(reference2)
    session.commit()


if __name__ == '__main__':
    pass

import argparse
import json

from flair.models import SequenceTagger

from src.database.creation_bdd import connexion, remplissage_auteur, remplissage_article, remplissage_personnalite, \
    remplissage_source, remplissage_contenu, remplissage_ecrit_par, remplissage_parlede, remplissage_reference, \
    remplissage_refere, remplissage_contient, remplissage_article_en_lien, remplissage_en_lien
from src.extracteur.extraction import get_url_all_surlignage, remplir_surlignage
from src.extracteur.surlignage import Surlignage
from src.extracteur.traitement import recuperation_nom


def main(user, pwd, host, port, db):
    with open("balise.json") as json_file:
        balise = json.load(json_file)

    article = Surlignage()

    print("Scrapping url article :")
    get_url_all_surlignage(article, balise)

    remplir_surlignage(article, balise)

    print("Chargement de Flair french:")
    tagger = SequenceTagger.load("flair/ner-french")
    noms_auteurs = recuperation_nom(article.auteurs, tagger)
    noms_relecteurs = recuperation_nom(article.relecteurs, tagger)
    noms_redaction = recuperation_nom(article.redaction, tagger)
    noms_politique = recuperation_nom(article.titre, tagger)

    engines = connexion(user, pwd, host, port, db)

    remplissage_source(engines, article)
    remplissage_article(engines, article)
    remplissage_auteur(engines, noms_auteurs)
    remplissage_auteur(engines, noms_relecteurs)
    remplissage_auteur(engines, noms_redaction)
    remplissage_personnalite(engines, noms_politique)
    remplissage_contenu(engines, article)
    remplissage_ecrit_par(engines, article, noms_auteurs, noms_relecteurs, noms_redaction)
    remplissage_parlede(engines, noms_politique, article)
    remplissage_reference(engines, article)
    remplissage_refere(engines, article)
    remplissage_contient(engines, article)
    remplissage_article_en_lien(engines, article)
    remplissage_en_lien(engines, article)

    print("Fin")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pipeline d\'intégration de données du site les surligneurs')
    parser.add_argument("--user", dest="user", help="Pseudonyme utilisateur")
    parser.add_argument("--pwd", dest="pwd", help="Mot de passe utilisateur")
    parser.add_argument("--host", dest="host", help="Adresse de la base de donnée cible")
    parser.add_argument("--port", dest="port", help="Port de la machine cible")
    parser.add_argument("--db", dest="db", help="Base de donnée cible")
    args = parser.parse_args()

    main(args.user, args.pwd, args.host, args.port, args.db)

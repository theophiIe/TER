import json

from tqdm import tqdm
from pprint import pprint

from flair.data import Sentence
from flair.models import SequenceTagger

from src.extracteur_v2.extraction import get_url_all_surlignage, remplir_surlignage
from src.extracteur_v2.surlignage import Surlignage

from unidecode import unidecode


def recuperation_nom(tab_nom, tagger) -> []:
    nom_final = []

    pbar = tqdm(range(len(tab_nom)), colour='green', desc='Flair analyse nom')
    for noms in tab_nom:
        nom_tmp = []
        if noms is not None:
            for nom in noms:
                sentence = Sentence(unidecode(nom))
                tagger.predict(sentence)
                for entity in sentence.get_spans('ner'):
                    if entity.tag == 'PER':
                        clean_nom = entity.to_plain_string()
                        if len(clean_nom) > 2:
                            nom_tmp.append(clean_nom)

        nom_final.append(nom_tmp)
        pbar.update(1)
        pbar.refresh()

    return nom_final


if __name__ == '__main__':
    ar_surlignage = Surlignage()

    with open("../../balise.json") as json_file:
        balise = json.load(json_file)

    get_url_all_surlignage(ar_surlignage, balise)
    remplir_surlignage(ar_surlignage, balise)

    tagger = SequenceTagger.load("flair/ner-french")
    noms_auteurs = recuperation_nom(ar_surlignage.auteurs, tagger)
    noms_relecteurs = recuperation_nom(ar_surlignage.relecteurs, tagger)
    noms_redaction = recuperation_nom(ar_surlignage.redaction, tagger)
    noms_politique = recuperation_nom(ar_surlignage.titre, tagger)

    for i in range(len(ar_surlignage.titre)):
        pprint(ar_surlignage.titre[i])
        # pprint(f'relecteur : {ar_surlignage.relecteurs[i]}')
        # pprint(f'redaction : {ar_surlignage.redaction[i]}')
        pprint(noms_relecteurs[i])
        pprint(noms_redaction[i])
        pprint(noms_politique[i])

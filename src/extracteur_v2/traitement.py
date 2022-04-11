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

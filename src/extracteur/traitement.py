from tqdm import tqdm

from flair.data import Sentence

from unidecode import unidecode


def recuperation_nom(tab_nom, tagger) -> []:
    """
    Permet l'utilisation de la librairie Flair (NLP) pour reconnaitre des noms
    :param tab_nom : tableau contenant les strings à analyser
    :param tagger : dataset utilisé par Flair
    :return : un tableau contenant les noms trouvés
    """
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
                        # Enlève-les stopwords reconnu comme des noms
                        if len(clean_nom) > 2:
                            nom_tmp.append(clean_nom)

        nom_final.append(nom_tmp)
        pbar.update(1)
        pbar.refresh()

    return nom_final

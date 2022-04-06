import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from tqdm import tqdm

from src.extracteur_v2.surlignage import Surlignage
from src.database_V2.table_bdd import Auteur, Personnalite, Article, Source,\
    Contenu, Reference, ParleDe, EcritPar, Contient, Refere, EnLien
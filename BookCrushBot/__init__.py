import logging
import os
import psycopg2
import sys

from .botm_session import BOTMSession
from .functions import *
from .loop import Loop
from .roulette_session import RouletteSession

filename = os.getenv("FILE", None)
if filename:
    logging.basicConfig(
        filename=filename,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
else:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

logger = logging.getLogger()

DATABASE = psycopg2.connect(os.getenv("DATABASE_URL"))  # (user="root", password="root")

botm = os.getenv("BOTM", "True")  # Is BOTM open ?
if botm == "False":
    BOTM = False
else:
    BOTM = True

BOTM_LIMIT = int(os.getenv("BOTM_LIMIT", "1"))  # How many books for BOTM ?

roulette = os.getenv("ROULETTE", "True")  # Is Roulette open ?
if roulette == "False":
    ROULETTE = False
else:
    ROULETTE = True

PORT = int(os.getenv("PORT"))
TOKEN = os.getenv("TOKEN")  # Token

del botm, filename, roulette

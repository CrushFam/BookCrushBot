import logging
import os
import sys
import psycopg2

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO,
)

logger = logging.getLogger()

DATABASE = psycopg2.connect(os.getenv("DATABASE_URL"))  # (user="root", password="root")

botm = os.getenv("BOTM", "True")  # Is BOTM open ?
if botm == "False":
    BOTM = False
else:
    BOTM = True

BOTM_LIMIT = int(os.getenv("BOTM_LIMIT", "1"))  # How many books for BOTM ?

review = os.getenv("REVIEWS", "True")  # Is reviews allowed ?
if review == "False":
    REVIEW = False
else:
    REVIEW = True

roulette = os.getenv("ROULETTE", "True")  # Is Roulette open ?
if roulette == "False":
    ROULETTE = False
else:
    ROULETTE = True

PORT = int(os.getenv("PORT"))
TOKEN = os.getenv("TOKEN")  # Token

del botm, review, roulette

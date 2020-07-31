import os
import psycopg2
import sys

from .botm_session import BOTMSession
from .functions import *
from .loop import Loop
from .roulette_session import RouletteSession

# The mapping of characters that need escaping in Markdown V2
ESCAPE_TABLE = {
    ord(i): f"\{i}"
    for i in [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]
}

DATABASE = psycopg2.connect(os.getenv("DATABASE_URL"))

botm = os.getenv("BOTM", "True")  # Is BOTM open ?
if botm == "False":
    BOTM = False
else:
    BOTM = True

BOTM_LIMIT = int(os.getenv("BOTM_LIMIT", "2"))  # How many books for BOTM ?

filename = os.getenv("FILE", None)
if filename:
    FILE = open(filename, "a")
else:
    FILE = sys.stdout

roulette = os.getenv("ROULETTE", "True")  # Is Roulette open ?
if roulette == "False":
    ROULETTE = False
else:
    ROULETTE = True

URL = f"https://api.telegram.org/bot{os.getenv('TOKEN')}"  # Bot URL

del botm, filename, roulette

import os
import sqlite3
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

DB_CONNECTION = sqlite3.connect(
    os.getenv("database", "data/database.sql"), check_same_thread=False
)
DB_CURSOR = DB_CONNECTION.cursor()

botm = os.getenv("botm", "True")  # Is BOTM open ?
if botm == "False":
    BOTM = False
else:
    BOTM = True

BOTM_LIMIT = int(os.getenv("botm_limit", "2"))  # How many books for BOTM ?

filename = os.getenv("file", None)
if filename:
    FILE = open(filename, "a")
else:
    FILE = sys.stdout

roulette = os.getenv("roulette", "True")  # Is Roulette open ?
if roulette == "False":
    ROULETTE = False
else:
    ROULETTE = True

URL = f"https://api.telegram.org/bot{os.getenv('TOKEN')}"  # Bot URL

del botm, filename, roulette

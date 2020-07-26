import json
import sqlite3
import sys

from .botm_session import BOTMSession
from .functions import *
from .loop import Loop
from .roulette_session import RouletteSession

config = json.load(open("config.json"))

DB_CONNECTION = sqlite3.connect(config["database"])
DB_CURSOR = DB_CONNECTION.cursor()

filename = config.get("file", None)
if filename:
    FILE = open(filename, "a")
else:
    FILE = sys.stdout

BOTM = config["botm"]
BOTM_LIMIT = config["botm_limit"]
ROULETTE = config["roulette"]
URL = f"https://api.telegram.org/bot{config['token']}"
ESCAPE_TABLE = {ord(i): f"\{i}" for i in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+',
                                    '-', '=', '|', '{', '}', '.', '!']}
del config, filename

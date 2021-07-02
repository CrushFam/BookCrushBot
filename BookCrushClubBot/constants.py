from os import getenv


class Constants:

    FICTION_COUNT = int(getenv("FICTION_COUNT", "2"))

    FICTION_GENRE = "Graphic Novel"

    FICTION_SESSION = "FICTION"

    NONFICTION_COUNT = int(getenv("NONFICTION_COUNT", "2"))

    NONFICTION_GENRE = "Graphic Novel"

    NONFICTION_SESSION = "NONFICTION"

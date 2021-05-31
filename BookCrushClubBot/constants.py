from os import getenv


class Constants:

    FICTION_COUNT = int(getenv("FICTION_COUNT", "2"))

    FICTION_GENRE = "Pride Month"

    FICTION_SESSION = "FICTION"

    NONFICTION_COUNT = int(getenv("NONFICTION_COUNT", "2"))

    NONFICTION_GENRE = "Pride Month"

    NONFICTION_SESSION = "NONFICTION"

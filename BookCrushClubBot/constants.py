from os import getenv


class Constants:

    ADMINS_GROUP = -1001407344499

    FICTION_COUNT = int(getenv("FICTION_COUNT", "2"))

    FICTION_GENRE = "Dystopia"

    FICTION_SESSION = "FICTION"

    NONFICTION_COUNT = int(getenv("NONFICTION_COUNT", "2"))

    NONFICTION_GENRE = "No Genre"

    NONFICTION_SESSION = "NONFICTION"

    SHORT_STORY_COUNT = int(getenv("SHORT_STORY_COUNT", "1"))

    SHORT_STORY_GENRE = "Any Genre"

    SHORT_STORY_SESSION = "SHORT_STORY"

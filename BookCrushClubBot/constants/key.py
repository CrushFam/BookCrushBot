"""Keys for values stored in database."""

from enum import Enum


class Key(Enum):
    """Keys for values stored in database."""

    GENRE = "genre{SECTION}"

    MAX_SUGGESTIONS = "maxsuggestions{SECTION}"

    START_TEXT = "starttext"

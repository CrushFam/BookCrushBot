"""BookCrushClubBot is a bot to maintain suggestions in the club."""

import logging

from .server import Server  # noqa

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

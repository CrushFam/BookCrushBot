"""BookCrushClubBot is a bot to maintain suggestions in the club."""

import logging

from .app import App

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

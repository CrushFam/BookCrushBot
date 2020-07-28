# BookCrush Bot

BookCrush Bot is a Telegram bot to manage BOTM and Roulette suggestions. It is designed to make the process of addition and removal, easy and quick.

# Usage

The bot is written using pure Python and the only external dependency is _Requests_ package. After installing it, you
can run start the bot by the following command.

    $ python3 -m BookCrushBot

The required parameters are taken from environment variables.
 1. TOKEN - The Bot's token.
 2. BOTM - (True/False) Whether to allow BOTM sessions. (Default True)
 3. BOTM_LIMIT - The number of books to allow per person for BOTM. (Default 2)
 4. FILE - The path of the file for logging progress. (Default sys.stdout)
 5. DATABASE_URL - The path to PostgreSQL database.
 6. ROULETTE - (True/False) Whether to allow Roulette sessions. (Default True)

# License

The Bot is licensed under GPL v3. Feel free to fork and use it.

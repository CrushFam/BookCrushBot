"""Constant message strings."""


class Message:
    """Constant message strings."""

    BOOK = "• <b>{NAME}</b>\n<i>{AUTHOR}</i>\n"

    BOOK_VERBOSE = "• <code>{NAME}</code>\n<code>{AUTHORS}</code>\n<i>{USERS}</i>\n"

    #BOOK_POST = "<b>{NAME}</b>\n<i>{AUTHORS}</i>\n{STARS}({RATING}/5)\n\n{DESC}\n"

    BROADCAST_COMPLETED = "Broadcast finished with success rate {RATE}%."

    BROADCAST_STARTED = "Broadcast has been started for {TOTAL} users."

    CHOOSE_SECTION = "Please choose the section to proceed."

    CLEARED_SECTION = "<code>{SECTION}</code> cleared successfully."

    CONFIRM_REMOVE = (
        "Choose the book to <b>remove</b>.\n\n"
        "{BOOKS}\n"
        "<b>Remember there won't be any Yes/No prompts!</b>"
    )

    CONFIRM_SUGGEST = (
        "Choose the book to <b>suggest</b>.\n\n"
        "{BOOKS}\n"
        "<b>If the results are wrong, you can try searching again.</b>"
    )

    HELP_ADMINS = (
        "The following commands are available for your usage.\n"
        "• /broadcast\n"
        "Send the quoted message to all users in my database.\n\n"
        "• /clear <i>section</i>\n"
        "Clear the books of <i>section</i>.\n"
        "<u>Example</u> <code>/clear botm</code>\n\n"
        "• /get <i>key</i>\n"
        "Get the value of <i>key</i>.\n"
        "<u>Example</u> <code>/get startText</code>\n\n"
        "• /list <i>section</i>\n"
        "List the books suggested for <i>section</i>.\n"
        "<u>Example</u> <code>/list shortStory</code>\n\n"
        "• /set <i>key</i> <i>value</i>\n"
        "Set the <i>value</i> of <i>key</i>. "
        "The <i>value</i> can be a quoted message.\n"
        "<u>Example</u> <code>/set genreBotm Horror</code>\n\n"
        "<b>Keys</b>\n"
        "• genreSection - Genre for <i>section</i>\n"
        "• maxSuggestionsSection - Maximum suggestions for <i>section</i>\n"
        "• startText - Message sent to users for /start\n\n"
        "<b>Sections</b>\n"
        "• botm - Traditional Book Of The Month\n"
        "• shortStory - Short stories category\n"
    )

    HELP_PRIVATE = (
        "Hello! I'm a bot to manage suggestions of @BookCrushClub 😁. "
        "Let us take a quick look on how to suggest or remove a book.\n\n"
        "1. Send /books to maintain your suggestions.\n"
        "2. Click the section you want to manage.\n"
        "3. Depending on your previous suggestions, you would see your books list.\n"
        "4. To suggest a book, click <b>Suggest</b>. "
        "Use <b>Remove</b> to remove a book.\n"
        "5. Enjoy.\n\n"
        "<b>Suggestions</b>\n"
        "My aim is to make suggesting as easy as possible.\n"
        "After clicking <b>Suggest</b>, you can do the following:\n"
        "1. Enter the book <i>name</i>.\n"
        "2. I will search the world for books matching the name and present to you.\n"
        "<b>OR</b>\n"
        "1. Send me the book <i>name</i> and <i>author</i> in two lines.\n"
        "<u>Example</u>\n"
        "<i>The Story Of My Life\nHelen Keller</i>\n"
        "2. <b>Note the new-line</b> between name and author!\n\n"
        "Irrespective of the method, I will show you the book(s) found.\n"
        "If that's the book in your mind, tap the name else you can try again.\n"
        "Simple isn't it? 😉\n\n"
        "<b>Removal</b>\n"
        "Removal is dead easy, but please keep in mind that there will be "
        "<b>no undo</b> or <b>yes/no prompts</b>! Once decided, nobody can stop you.\n"
        "To remove a book, tap <b>Remove</b> and choose the book.\n"
        "One click and boom! 😉\n\n"
        "Humans make mistakes and so bots. If you face any difficulty or error or "
        "want to improve me, please don't hesitate to tell in @BookCrushClub. 😊\n"
        "Thanks to <a href='https://openlibrary.org'>OpenLibrary</a> for their API!"
    )

    INVALID_KEY = "<code>{KEY}</code> is invalid. Available keys are {KEYS}."

    INVALID_MESSAGE = "The command should be a reply to valid message."

    INVALID_SECTION = (
        "Invalid section <code>{SECTION}</code>.\n" "Available sections are {SECTIONS}."
    )

    INVALID_VALUE = (
        "Invalid value. Either specify it as second argument "
        "or reply the command to a textual message."
    )

    LIST_SECTION = "{BOOKS}\nListing {COUNT} books."

    MONO = "<code>{TERM}</code>"

    NO_RESULTS = (
        "Your search didn't result in <b>anything useful…</b> Why not try again?"
    )

    SET_KEY = "<code>{KEY}</code> has been set to new value."

    START = "Yes, I'm alive."

    SUGGESTED_BOOK = "{NAME} has been suggested."

    SUGGESTIONS_FULL = (
        "You have suggested the following for <b>{GENRE}</b> of <b>{SECTION}</b>.\n\n"
        "{BOOKS}\n"
        "To suggest a new book, you have to remove the existing one."
    )

    SUGGESTIONS_PARTIAL = (
        "You have suggested the following for <b>{GENRE}</b> of <b>{SECTION}</b>.\n\n"
        "{BOOKS}\n"
        "You can suggest {COUNT} more books."
    )

    SUGGESTIONS_ZERO = (
        "You have not made any suggestions for <b>{GENRE}</b> of <b>{SECTION}</b>!\n\n"
        "Why not do it now?"
    )

    SUGGEST_BOOK = (
        "Please suggest the book.\n"
        "You can either send me a name to search or "
        "directly mention its full details.\n"
        "1. Enter the book <i>name</i>.\n"
        "2. I will search the world for books matching the name and present to you.\n"
        "<b>OR</b>\n"
        "1. Send me the book <i>name</i> and <i>author</i> in two lines.\n"
        "<u>Example</u>\n"
        "<i>The Story Of My Life\nHelen Keller</i>\n"
        "2. <b>Note the new-line</b> between name and author!\n\n"
        "Irrespective of the method, I will show you the book(s) found.\n"
        "If that's the book in your mind, tap the name else you can try again.\n\n"
        "Please check /help for more information."
    )

    REMOVED_BOOK = "{NAME} has been removed."

    REPORT = (
        "<b>{ERROR}: {DETAILS}</b>\n"
        "User: <a href='tg://user?={USER_ID}'>{FULL_NAME}</a>\n"
        "Traceback\n<code>{TRACEBACK}</code>"
    )

    UNEXPECTED_MESSAGE = "Okay? So what? 😑 Need some /help?"

    UNKNOWN_ERROR = "Something went wrong, but don't worry, we can always /start fresh."

    ZOMBIE_QUERY = "Oh no no, those messages are old and I forgot their context. Please start new using /books."

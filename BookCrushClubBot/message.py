class Message:

    ADDED_BOOK = "{BOOK_NAME} has been added to your suggestions."

    BOOK = "• <b>{BOOK_NAME}</b>\n <i>{AUTHORS}</i>"

    BOOKS_DISPLAY = "<b>{GENRE}</b>\n{BOOKS}\nTotal: {TOTAL}\nRepeat : {REPEAT}"

    BOOK_FULL = "• <code>{BOOK_NAME}</code>\n <code>{AUTHORS}</code>\n <i>{NAMES}</i>\n"

    CONFIRM_BOOK = (
        "Do you want to add this {ITEM} for suggestion ?\n"
        "{BOOK}\n\n"
        "Wrong {ITEM} ? No worries, try again !"
    )

    EMPTY_SUGGESTIONS = "<b>Whoa there !</b> You haven't suggested anything for <b>{GENRE}</b>, let's get started now !"

    FULL_SUGGESTIONS = (
        "<b>Awesome !</b> You already suggested the maximum number of "
        "{ITEM} for <b>{GENRE}</b>. "
        "You can however remove and add new {ITEM}(s).\n\n"
        "The following {ITEM}(s) are in your list :\n"
        "{BOOKS}"
    )

    HALF_SUGGESTIONS = (
        "<b>Parkour !</b> The following {ITEM}(s) are in your list :\n"
        "{BOOKS}\n\n"
        "You can still suggest {LEFT} book{S} for <b>{GENRE}</b>."
    )

    INVALID_TEXT = "Sorry, I can't understand what's happening ... need some /help ?"

    INVALID_RAW_FORMAT = "Looks like you didn't follow the format. Please try again."

    NO_RESULTS = (
        "Your search got zero "
        "<a href='http://openlibrary.org/search?title={QUERY}'>"
        "results</a>. Please try again."
    )

    REMOVE_BOOKS = (
        "Choose the {ITEM} you want to <b>remove</b>. "
        "Remember, there won't be any <code>Yes/No</code> fancies, once clicked, it's done."
    )

    REMOVED_BOOK = "{BOOK_NAME} has been removed."

    SEARCH_ISBN = "Please send me the ISBN of the {ITEM}."

    SEARCH_NAME = "Please send me the name of the {ITEM}."

    SEARCH_RESULTS = (
        "Here are the {ITEM} matching your search query.\n"
        "{BOOKS}\n\n"
        "Not the one you are looking for ?\n"
        "Please try "
        "<a href='http://openlibrary.org/search?title={QUERY}'>narrowing</a> "
        "your search query.\n"
        "Wrong choice ? Just try out the search again !"
    )

    SUGGEST_RAW = (
        "Please send me the {ITEM} details in the following format. "
        "<code>\n"
        "NAME\n"
        "AUTHOR(S)\n"
        "GENRE(S)\n"
        "</code>\n\n"
        "If there are multiple authors or genres, please separate them by comma."
    )

    SUGGESTIONS_METHOD = "Please choose the suggestion method."

    UNAUTHORIZED_COMMAND = "Haha! No 😠..."

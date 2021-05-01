class Message:

    ADDED_BOOK = "{BOOK_NAME} has been added to your suggestions."

    BOOK = "• <b>{BOOK_NAME}</b>\n <i>{AUTHORS}</i>"

    CONFIRM_BOOK = (
        "Do you want to add this book for suggestion ?\n"
        "{BOOK}\n\n"
        "Wrong book ? No worries, try again !"
    )

    EMPTY_SUGGESTIONS = "<b>Whoa there !</b> You haven't suggested anything for <b>{GENRE}</b>, let's get started now !"

    FULL_SUGGESTIONS = (
        "<b>Awesome !</b> You already suggested the maximum number of "
        "book{S} for <b>{GENRE}</b>. "
        "You can however remove and add new book{S}.\n\n"
        "The following books are in your list :\n"
        "{BOOKS}"
    )

    HALF_SUGGESTIONS = (
        "<b>Parkour !</b> The following books are in your list :\n"
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
        "Choose the book you want to <b>remove</b>. "
        "Remember, there won't be any <code>Yes/No</code> fancies, once clicked, it's done."
    )

    REMOVED_BOOK = "{BOOK_NAME} has been removed."

    SEARCH_ISBN = "Please send me the ISBN of the book."

    SEARCH_NAME = "Please send me the name of the book."

    SEARCH_RESULTS = (
        "Here are the books matching your search query.\n"
        "{BOOKS}\n\n"
        "Not the one you are looking for ?\n"
        "Please try "
        "<a href='http://openlibrary.org/search?title={QUERY}'>narrowing</a> "
        "your search query.\n"
        "Wrong choice ? Just try out the search again !"
    )

    SUGGEST_RAW = (
        "Please send me the book details in the following format. "
        "<code>\n"
        "NAME\n"
        "AUTHOR(S)\n"
        "GENRE(S)\n"
        "</code>\n\n"
        "If there are multiple authors or genres, please separate them by comma."
    )

    SUGGESTIONS_METHOD = "Please choose the suggestion method."

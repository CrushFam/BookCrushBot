import logging
import requests


def get_book_by_isbn(isbn):

    params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}

    try:
        result = requests.get("https://openlibrary.org/api/books", params).json()
    except Exception as e:
        logging.error(str(e))
        return

    if not result:
        return

    details = result[f"ISBN:{isbn}"]
    name = details["title"]
    authors = [author["name"] for author in details.get("authors", ["null"])]
    genres = [
        subject["name"] for subject in details.get("subjects", [{"name": "null"}])[:3]
    ]

    return name, authors, genres


def get_books_by_name(name, limit=3):

    params = {"title": name}

    try:
        result = requests.get("http://openlibrary.org/search.json", params)
        result = result.json()
    except Exception as e:
        logging.error(str(e))
        return []

    books = []

    for book in result["docs"][:limit]:
        name = book["title_suggest"]
        authors = book.get("author_name", ["null"])
        genres = book.get("subject", ["null"])[:3]
        books.append((name, authors, genres))

    return books

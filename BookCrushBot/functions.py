import requests
import BookCrushBot


def add_botm_suggestion(
    user_id, username, display_name, isbn, name, authors, genres, note
):

    cursor = BookCrushBot.DATABASE.cursor()
    cursor.execute(
        "INSERT INTO botm VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
        (user_id, username, display_name, isbn, name, authors, genres, note),
    )
    BookCrushBot.DATABASE.commit()
    cursor.close()


def add_to_roulette(user_id, username, display_name, isbn, name, authors, genres, note):

    cursor = BookCrushBot.DATABASE.cursor()
    cursor.execute(
        "INSERT INTO roulette VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
        (user_id, username, display_name, isbn, name, authors, genres, note),
    )
    BookCrushBot.DATABASE.commit()
    cursor.close()


def get_book_by_isbn(isbn):

    params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}

    result = requests.get("https://openlibrary.org/api/books", params).json()
    if not result:
        return {}

    details = result[f"ISBN:{isbn}"]
    authors = ", ".join((author["name"] for author in details.get("authors", ["null"])))
    genres = ", ".join(
        (subject["name"] for subject in details.get("subjects", [{"name": "null"}])[:3])
    )

    data = {
        "isbn": isbn,
        "name": details["title"],
        "authors": authors,
        "genres": genres,
        "note": "openlibrary-isbn",
    }
    return data


def get_book_by_name(name, limit=3):

    params = {"title": name}
    result = requests.get("http://openlibrary.org/search.json", params)
    result = result.json()
    books = []
    for book in result["docs"][:limit]:
        isbn = book.get("isbn", "0")[0]
        authors = ", ".join(book.get("author_name", ["null"]))
        genres = ", ".join(book.get("subject", ["null"])[:3])
        data = {
            "isbn": isbn,
            "name": book["title_suggest"],
            "authors": authors,
            "genres": genres,
            "note": "openlibrary-name",
        }
        books.append(data)
    return books


def get_book_by_raw(text):

    text = text.splitlines()
    if len(text) == 3:
        text.append("nil")
    elif len(text) != 4:
        return {}
    data = {
        "isbn": 0,
        "name": text[0],
        "authors": text[1],
        "genres": text[2],
        "note": text[3],
    }
    return data


def get_botm_suggestions(user_id):

    cursor = BookCrushBot.DATABASE.cursor()
    cursor.execute("SELECT name, authors FROM botm WHERE user_id=%s;", (user_id,))
    result = cursor.fetchall()
    cursor.close()
    return result


def get_roulette_additions_count(user_id):

    cursor = BookCrushBot.DATABASE.cursor()
    cursor.execute("SELECT COUNT(*) FROM roulette WHERE user_id=%s;", (user_id,))
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]


def get_roulette_additions(user_id):

    cursor = BookCrushBot.DATABASE.cursor()
    cursor.execute("SELECT name, authors FROM roulette WHERE user_id=%s;", (user_id,))
    result = cursor.fetchall()
    cursor.close()
    return result


def remove_botm_suggestion(user_id, name):

    cursor = BookCrushBot.DATABASE.cursor()
    cursor.execute("DELETE FROM botm WHERE user_id=%s AND name=%s", (user_id, name))
    BookCrushBot.DATABASE.commit()
    cursor.close()


def remove_roulette_addition(user_id, name):

    cursor = BookCrushBot.DATABASE.cursor()
    cursor.execute("DELETE FROM roulette WHERE user_id=%s AND name=%s", (user_id, name))
    BookCrushBot.DATABASE.commit()
    cursor.close()


def search_roulette_books(user_id, keyword):

    cursor = BookCrushBot.DATABASE.cursor()
    cursor.execute(
        "SELECT name, authors FROM roulette WHERE user_id=%s AND name ILIKE %s;",
        (user_id, f"%{keyword}%"),
    )
    result = cursor.fetchall()
    cursor.close()
    return result

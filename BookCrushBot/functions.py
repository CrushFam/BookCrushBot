import json
import time
import threading
import requests
import BookCrushBot

def add_botm_suggestion(user, isbn, name, author, genre_a, genre_b, note):

    BookCrushBot.DB_CURSOR.execute("INSERT INTO botm VALUES(?, ?, ?, ?, ?, ?, ?);",
                            (user, isbn, name, author, genre_a, genre_b, note))

def add_to_roulette(user, isbn, name, author, genre_a, genre_b, note):

    BookCrushBot.DB_CURSOR.execute("INSERT INTO roulette VALUES(?, ?, ?, ?, ?, ?, ?);",
                            (user, isbn, name, author, genre_a, genre_b, note))

def escape(string):

    return string.translate(BookCrushBot.ESCAPE_TABLE)

def get_book_by_isbn(isbn):

    try:
        isbn = int(isbn)
    except ValueError:
        return {}

    params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}

    result = requests.get("https://openlibrary.org/api/books", params).json()
    if not result:
        return {}

    details = result[f"ISBN:{isbn}"]
    genres = [subject["name"] for subject in result.get("subjects", [{"name": "null"}, {"name": "null"}])[:2]]
    ln = len(genres)
    if ln == 0:
        genres = ["null", "null"]
    elif ln == 1:
        genres.append("null")

    data = {"isbn": isbn,
            "name": details["title"],
            "author": details["authors"][0]["name"],
            "genre_a": genres[0],
            "genre_b": genres[1]
            }
    return data

def get_book_by_name(name, limit=3):

    params = {"title": name}
    result = requests.get("http://openlibrary.org/search.json", params)
    result = result.json()
    books = []
    for book in result["docs"][:limit]:
        genres = [subject for subject in book.get("subject", ["null", "null"])[:2]]
        ln = len(genres)
        if ln == 0:
            genres = ["null", "null"]
        elif ln == 1:
            genres.append("null")
        try:
            isbn = int(book.get("isbn", ["0"])[0])
            note = "isbn"
        except ValueError:
            isbn = 0
            note = "invalid isbn"
        data = {"isbn": isbn,
                "name": book["title_suggest"],
                "author": book["author_name"][0],
                "genre_a": genres[0],
                "genre_b": genres[1],
                "note": note
                }
        books.append(data)
    return books

def get_book_by_raw(text):

    text = text.splitlines()
    if len(text) != 5:
        return {}
    data = {"isbn": 0,
            "name": text[0],
            "author": text[1],
            "genre_a": text[2],
            "genre_b": text[3],
            "note": text[4]}
    return data

def get_botm_suggestions(user):

    result = BookCrushBot.DB_CURSOR.execute("SELECT name FROM botm WHERE user=?;", (user,))
    return [res[0] for res in result]

def get_buttons_markup(rows):

    button_rows = [[{"text": label, "callback_data": cb} for label, cb in row] for row in rows]
    markup = {"inline_keyboard": button_rows}
    return json.dumps(markup)

def get_roulette_additions_count(user):

    result = BookCrushBot.DB_CURSOR.execute("SELECT 1 FROM roulette WHERE user=?;", (user,))
    return len(tuple(result))

def get_roulette_additions(user):

    result = BookCrushBot.DB_CURSOR.execute("SELECT name FROM roulette WHERE user=?;", (user,))
    return [res[0] for res in result]

def log(*messages):

    print(time.ctime(), "::", *messages, file=BookCrushBot.FILE)

def remove_botm_suggestion(user, name):

    BookCrushBot.DB_CURSOR.execute("DELETE FROM botm WHERE user=? AND name=?", (user, name))

def remove_roulette_addition(user, name):

    BookCrushBot.DB_CURSOR.execute("DELETE FROM roulette WHERE user=? AND name=?", (user, name))

def request(url, data=None):

    response = requests.get(url, data)
    response_json = response.json()
    if response_json["ok"]:
        return response_json["result"]
    raise AssertionError(response_json["description"])

def request_async(url, data=None):

    thread = threading.Thread(target=request, args=(url, data))
    thread.start()

def search_roulette_books(user, keyword, limit=10):

    result = BookCrushBot.DB_CURSOR.execute("SELECT name, author FROM roulette WHERE user=?;", (user,))
    matches = []
    count = 0
    for name, author in result:
        if keyword in name.lower():
            matches.append({"name": name, "author": author})
        if count == 9:
            break
        count += 1
    return matches


import datetime
import getpass
import gspread
import psycopg2

default_user = getpass.getuser()
username = input(f"Enter database username [{default_user}] :")
password = getpass.getpass()
database = input("Enter database name :")

if not username.strip():
    username = default_user

connection = psycopg2.connect(username=username, password=password, database=database)
cursor = connection.cursor()
cursor.execute("SELECT display_name, name, authors, genre FROM roulette;")

gc = gspread.service_account()
sheets = gc.open("Book_Roulette")
sheet = sheets.get_worksheet(0)

rows = [
    [
        "",  # Read By Date
        row[1],  # Title
        row[2],  # Authors
        row[3],  # Genre
        "",  # BCC Rating
        "",  # GR Rating
        "",  # Page Count
        "",  # Year Published
        datetime.datetime.today(),  # Date Added
        "",  # Additional Authors
        row[0],  # Added by
    ]
    for row in cursor
]

sheet.append_rows(rows, value_input_option="USER_ENTERED")
cursor.close()
connection.close()
print("Done")

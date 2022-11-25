import sqlite3

# def create_database():
#     conn = None

#     try:
#         conn = sqlite3.connect('quotes')
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()

# start = create_database()

# def create_table():
#     conn = sqlite3.connect('quotes')
#     cur = conn.cursor()

#     cur.execute('''CREATE TABLE IF NOT EXISTS  quotes (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name VARCHAR, quote VARCHAR NOT NULL) ''');

# create_table = create_table()

# def insert_into():
#     conn = sqlite3.connect('quotes')
#     cur = conn.cursor()
    
#     cur.execute('INSERT INTO quotes (user_name, quote) VALUES ("SitLetto", "Kobiety sa gorace")')
#     conn.commit()
#     conn.close()

# first_execute = insert_into()

def get_all():
    conn = sqlite3.connect('quotes')
    cur = conn.cursor()

    cur.execute('SELECT * FROM quotes')
    asd = cur.fetchall()
    for data in asd:
        print(data)
    conn.close()

get_all = get_all()
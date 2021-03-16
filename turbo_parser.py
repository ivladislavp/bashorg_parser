from bs4 import BeautifulSoup
import requests, sqlite3


# page 3282
# https://bash.im/index/1

def db_quotes_create():
    conn = sqlite3.connect("bash_base.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE quotes
                     (bash_id text, rating text, date text, text text)
                  """)
    conn.commit()
    print('quotes creates')

    db_state_create()


def db_state_create():
    conn = sqlite3.connect("bash_base.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE status
                     (current_quote int)
                  """)
    conn.commit()
    print('status created')


def db_add_state():
    conn = sqlite3.connect("bash_base.db")
    cursor = conn.cursor()
    state = ('0')
    cursor.execute("INSERT INTO status VALUES (?)", state)
    conn.commit()
    print('state set')


def db_add_comix():
    conn = sqlite3.connect("bash_base.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE comixes
                     (comix_id int)
                  """)
    conn.commit()


def get_status():
    conn = sqlite3.connect("bash_base.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * from status """)
    return cursor.fetchall()[0][0]


def set_status(current_quote):
    conn = sqlite3.connect("bash_base.db")
    cursor = conn.cursor()
    state = (str(current_quote),)
    cursor.execute("UPDATE status SET current_quote =(?) WHERE rowid ='1'", state)
    conn.commit()


def set_status(current_quote):
    conn = sqlite3.connect("bash_base.db")
    cursor = conn.cursor()
    state = (str(current_quote),)
    cursor.execute("UPDATE status SET current_quote =(?) WHERE rowid ='1'", state)
    conn.commit()


def write_quote(value):
    # bash_id text, rating text, date text, text text
    conn = sqlite3.connect("bash_base.db")  # или :memory: чтобы сохранить в RAM
    conn.text_factory = str
    cursor = conn.cursor()
    values = (value[0], value[1], value[2], value[3])
    cursor.execute("INSERT INTO quotes VALUES (?,?,?,?)", values)
    conn.commit()
    print('save done #', value[0])


def quote_saver(pageid):
    resp = requests.get(f"https://bash.im/index/{pageid}")
    soup = BeautifulSoup(resp.text, features="html.parser")
    all_quotes = soup.findAll("article", class_="quote")
    all_texts = soup.findAll("div", class_="quote__body")
    quote_rating = soup.findAll("div", class_="quote__total")
    quote_date = soup.findAll("div", class_="quote__header_date")
    quote_id = soup.findAll("a", class_="quote__header_permalink")

    for i in range(0,len(all_quotes)):
       #print('len all_quotes=', len(all_quotes))
       quote_object = [quote_id[i].text, quote_rating[i].text, quote_date[i].text, all_texts[i].text]
       write_quote(quote_object)

def db_print():
    conn = sqlite3.connect("bash_base.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    print("BD Request")
    cursor.execute("SELECT rowid, * FROM quotes")
    return cursor.fetchall()


# quote_saver(1)

#db_quotes_create()
#db_add_state()
#print(get_status())

for i in range(0, 3282):
    current_quote = get_status() + 1
    quote_saver(current_quote)
    set_status(current_quote)
    print(f"{i}/3282")

# print(db_print())

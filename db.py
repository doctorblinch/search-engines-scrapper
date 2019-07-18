import urllib.parse as up
import psycopg2
import pickle

up.uses_netloc.append("postgres")
url = up.urlparse('postgres://zkynsogs:Mtak9HA6-oV5shMzPjZzd-4ZjiYAsVnv@balarama.db.elephantsql.com:5432/zkynsogs')
connection = psycopg2.connect(database=url.path[1:],
                              user=url.username,
                              password=url.password,
                              host=url.hostname,
                              port=url.port)

'''
from sqlalchemy import create_engine
engine = create_engine(, echo=True)
engine.execute('SELECT * FROM users')
'''


def write_to_db(result, engine):
    if len(result) == 0:
        return

    cursor = connection.cursor()
    for res in result:
        for element in res:
            query = """INSERT INTO scrapes(index, query, link, title, description, time, search_engine) VALUES \
                           (%s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(query, (element['index'], element['query'],
                                   element['link'], element['title'],
                                   element['description'], element['time'],
                                   element['engine']))
            # cursor.execute(query)
    connection.commit()
    print("-Elements of %s parsing successfully inserted in PostgreSQL\n" % engine)


def read_from_db(quantity='all'):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM scrapes;")
    record = cursor.fetchall()
    if quantity == 'all':
        return record
    return record[-quantity:]


def write_user_to_db(user):
    cursor = connection.cursor()
    query = """INSERT INTO users(name, user_agent,cookies) VALUES \
                (%s, %s, %s);"""
    # for i in user.cookies._cookies:
    #     print(i)
    cursor.execute(query, (user.name, user.agent['User-Agent'], pickle.dumps(user.cookies)))
    connection.commit()

    print("-Cookies successfully inserted in PostgreSQL\n")

def write_cookies_to_file(user, file_name=None):
    if file_name == None:
        file_name = user.name + '.cookies'
    with open(file_name, 'wb') as f:
        pickle.dump(user.cookies, f)

def read_cookies_from_file(file_name):
    with open(file_name, 'rb') as f:
        cookies_data = pickle.load(f)
    return cookies_data

'''
def read_user_from_db(quantity='all')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    if quantity == 'all':
        return 0
'''

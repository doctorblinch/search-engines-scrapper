import urllib.parse as up
import psycopg2

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


def write_to_db(result, engine='default'):
    cursor = connection.cursor()
    for res in result:
        for element in res:
            cursor.execute("""INSERT INTO scrapes(index, query, link, title, description, time, search_engine) VALUES \
                           (%s, %s, %s, %s, %s, %s, %s);""", (element['index'], element['query'],
                                                              element['link'], element['title'],
                                                              element['description'], element['time'],
                                                              engine))
            # cursor.execute(query)
    connection.commit()
    print("Elements of %s parsing successfully inserted in PostgreSQL " % engine)


def read_from_db():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM scrapes;")
    record = cursor.fetchall()
    return record
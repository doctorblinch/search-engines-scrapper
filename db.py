import os
import urllib.parse as up
import psycopg2

up.uses_netloc.append("postgres")
url = up.urlparse()
connection = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)

'''
from sqlalchemy import create_engine
engine = create_engine(, echo=True)
engine.execute('SELECT * FROM users')
'''
def write_to_db(result):
    cursor = connection.cursor()
    for res in result:
        for element in res:
            query = "INSERT INTO scrapes(index,query,link,title,description,time) VALUES \
                           ({},'{}','{}','{}','{}','{}');".format(element['index'],element['query'],element['link'], element['title'],
                                                        element['description'], element['time'])
            cursor.execute(query)
    connection.commit()
    print("Elements successfully inserted in PostgreSQL ")


def read_from_db():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM scrapes;")
    record = cursor.fetchall()
    return record
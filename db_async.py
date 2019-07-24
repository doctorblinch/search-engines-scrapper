import urllib.parse as up
import psycopg2
import pickle

# import asyncio
# import aiopg

up.uses_netloc.append("postgres")
url = up.urlparse('postgres://zkynsogs:Mtak9HA6-oV5shMzPjZzd-4ZjiYAsVnv@balarama.db.elephantsql.com:5432/zkynsogs')
# dsn = 'dbname={database} user={user} password={password} host={host} port={port}'.format(database=url.path[1:],
#                                                                                          user=url.username,
#                                                                                          password=url.password,
#                                                                                          host=url.hostname,
#                                                                                          port=url.port)
connection = psycopg2.connect(database=url.path[1:],
                              user=url.username,
                              password=url.password,
                              host=url.hostname,
                              port=url.port)


def write_to_db(result, engine=''):
    # async with aiopg.create_pool(dsn) as pool:
    #     async with pool.acquire() as conn:
    #         async with conn.cursor() as cur:
    #             for element in result:
    #                 query = """INSERT INTO scrapes(index, query,\
    #                 link, title, description, time, search_engine) VALUES \
    #                               (%s, %s, %s, %s, %s, %s, %s);"""
    #                 await cur.execute(query, (element['index'], element['query'],
    #                                           element['link'], element['title'],
    #                                           element['description'], element['time'],
    #                                           engine))

    if len(result) == 0:
        return

    cursor = connection.cursor()
    for res in result:
        for element in res:
            # print(len(element['description']))
            # print(len(element['link']))
            # print(len(element['title']))
            # print()
            query = """INSERT INTO scrapes(index, query, link, title, description, time, search_engine) VALUES \
                           (%s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(query, (element['index'], element['query'],
                                   element['link'], element['title'],
                                   element['description'],
                                   element['time'],
                                   element['engine']))
    connection.commit()
    print("-Elements successfully inserted in PostgreSQL\n")


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
    cursor.execute(query, (user.name, user.agent['User-Agent'], pickle.dumps(user.cookies)))
    connection.commit()

    print("-Cookies successfully inserted in PostgreSQL\n")


def write_cookies_to_file(user, file_name=None):
    if file_name is None:
        file_name = user.name + '.cookies'
    with open(file_name, 'wb') as f:
        pickle.dump(user.cookies, f)


def read_cookies_from_file(file_name):
    with open(file_name, 'rb') as f:
        cookies_data = pickle.load(f)
    return cookies_data

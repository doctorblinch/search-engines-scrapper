import urllib.parse as up
import psycopg2
import pickle
import aiohttp
import asyncio
import os.path

from user_async import UserAsync


# import asyncio
# import aiopg
db_key = ''

with open('.env', 'r') as f:
    db_key = f.readline()
    db_key = db_key[:-1]

up.uses_netloc.append("postgres")
url = up.urlparse(db_key)
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


def write_to_db(result, engine='', user=None):
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

    if user is not None:
        id = user.id_in_db
    else:
        id = 1

        print(type(id), id)

    cursor = connection.cursor()
    #for res in result:
    for element in result:
            # print(len(element['description']))
            # print(len(element['link']))
            # print(len(element['title']))
            # print()
            if len(element['description']) >= 8192:
                element['description'] = element['description'][:8191]
            query = """INSERT INTO scrapes(index, query, link, title, description, time, search_engine, user_id) VALUES \
                           (%s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(query, (element['index'], element['query'],
                                   element['link'], element['title'],
                                   element['description'],
                                   element['time'],
                                   element['engine'],
                                   id))
    connection.commit()
    print("-Elements successfully inserted in PostgreSQL\n")


def read_from_db(quantity='all'):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM scrapes;")
    record = cursor.fetchall()
    if quantity == 'all':
        return record
    return record[-quantity:]

def get_last_user_id():
    cursor = connection.cursor()
    query = f"SELECT * FROM users ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    record = cursor.fetchone()
    return int(record[0])


def read_user_from_db(id=None, name=None, create_if_not_exists=False, requests=None):
    cursor = connection.cursor()

    if id is not None:
        query = f"SELECT * FROM users WHERE (id = \'{id}\') ORDER BY id DESC LIMIT 1"
        cursor.execute(query)

    elif name is not None:
        query = f"SELECT * FROM users WHERE (name LIKE \'{name}\') ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
    else:
        return 'User with such parrametrs not found!'

    record = cursor.fetchone()

    if create_if_not_exists and name is not None and record is None:
        user = UserAsync(name=name)
        id = get_last_user_id() + 1
        user.id_in_db = id
        if requests is not None:
            user.requests = requests
        write_user_to_db(user)
        return user

    user = UserAsync(record[1])
    user.id_in_db = record[0]
    if requests is not None:
        user.requests = requests
    user.agent = {'User-Agent': record[2]}
    user.cookies = read_cookies_from_file('data/' + record[3])

    return user


def write_user_to_db(user):
    cursor = connection.cursor()
    query = """INSERT INTO users(name, user_agent, cookies) VALUES \
                (%s, %s, %s);"""
    cursor.execute(query, (user.name, user.agent['User-Agent'], user.file_name))
    connection.commit()

    print("-User successfully inserted in PostgreSQL\n")


def write_cookies_to_file(user, file_name=None):
    if file_name is None:
        file_name = 'data/' + user.name + '.cookies'
    with open(file_name, 'wb') as f:
        pickle.dump(user.cookies, f)


def read_cookies_from_file_pickle(file_name):
    if not os.path.exists('data/' + file_name):
        return 'not exists'
    file_name = 'data/' + file_name
    with open(file_name, 'rb') as f:
        cookies_data = pickle.load(f)
    return cookies_data

async def __async_read_cookies_from_file(file_name=None, user=None):
    if user is not None:
        if os.path.exists('data/' + user.file_name):
            async with aiohttp.ClientSession() as session:
                session._cookie_jar.load('data/' + file_name)
                cookies = session._cookie_jar._cookies
                return cookies

    if file_name is not None:
        if os.path.exists('data/' + file_name):
            async with aiohttp.ClientSession() as session:
                session._cookie_jar.load('data/' + file_name)
                cookies = session._cookie_jar._cookies
                return cookies

def read_cookies_from_file(file_name=None, user=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(__async_read_cookies_from_file(file_name=file_name, user=user))
    return result

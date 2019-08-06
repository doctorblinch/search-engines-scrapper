import urllib.parse as up
import psycopg2
import pickle
import aiohttp
import os.path

from user_async import UserAsync

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
            if len(element['description']) >= 8192:
                element['description'] = element['description'][:8191]
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


def read_user_from_db(id=None, name=None, create_if_not_exists=False, requests=None):
    cursor = connection.cursor()

    if id is not None:
        query = f"SELECT * FROM users WHERE (id = \'{id}\') ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
    elif name is not None:
        query = f"SELECT * FROM users WHERE (name LIKE \'{name}\') ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
    else:
        return

    record = cursor.fetchone()

    if create_if_not_exists and name is not None:
        bot = UserAsync(name=name)
        if requests is not None:
            bot.requests = requests


    user = UserAsync(record[1])
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
        file_name = user.name + '.cookies'
    with open(file_name, 'wb') as f:
        pickle.dump(user.cookies, f)


def read_cookies_from_file_pickle(file_name):
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


import asyncio
if __name__=='__main__':
    print(read_cookies_from_file('Bot Kid.cookies'))

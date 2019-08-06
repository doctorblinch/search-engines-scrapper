from engine_parser_async import EngineParserAsync
from time import time
import asyncio
import aiohttp
import os.path

from db_async import write_to_db, write_user_to_db, write_cookies_to_file, read_user_from_db

from user_async import UserAsync


all_results = []
s = None

#bot = UserAsync(name='Bot Kid')

bot = read_user_from_db(name='Nolan Diagram v1 bot #1', create_if_not_exists=True)



async def main():
    tasks = []

    engines = ['Google', 'Bing', 'Youtube']
    # engines = ['Google', 'Bing', 'Yahoo']

    async with aiohttp.ClientSession() as session:
        if os.path.exists('data/' + bot.file_name):
            session._cookie_jar.load('data/' + bot.file_name)
        for engine in engines:
            task = asyncio.create_task(sub_task(engine, session))
            tasks.append(task)
        global s
        s = session
        await asyncio.gather(*tasks)


async def sub_task(engine, session):
    engine_parser = EngineParserAsync()
    num_of_links = 10

    #requests = ["Мультики", "Игрушки" , "Лунтик", "Лего", "Игры для детей", "Магазин игрушек",
     #"Сказка", "Хот вилс", "Игрушки машинки", "История Игрушек", "Машинка на радиоуправлении", "купить машинку на радиоуправлении"]

    if bot.requests is None
        requests = ['Машинка', 'магазин']
    else:
        requests = bot.requests

    for request in requests:
        await engine_parser.start_engine_scrapping(request, number=num_of_links, user=bot,
                                                   language_code='ru', engine=engine,
                                                   use_proxy=False, timeout_range=(3, 6),
                                                   print_output=True, session=session,
                                                   all_results=all_results)



if __name__ == '__main__':
    # print(s._cookie_jar)
    start = time()

    asyncio.run(main())

    write_to_db(all_results)
    write_user_to_db(bot)
    # write_cookies_to_file(bot,  + bot.file_name)
    print('\n\nTIME:', time() - start)

    s._cookie_jar.save('data/' + bot.file_name)

    # print(all_results)

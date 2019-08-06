from engine_parser_async import EngineParserAsync
from time import time
import asyncio
import aiohttp
import os.path

from db_async import write_to_db, write_user_to_db, write_cookies_to_file, read_user_from_db

from user_async import UserAsync


all_results = []
s = None


bot = read_user_from_db(name='Nolan Diagram v1 bot #1', create_if_not_exists=True, requests=['анархизм', 'митинги', 'нацболы', 'лимонов', 'революция', 'народная самооборона', 'путин вор',  'азат мифтахов', 'русский марш', 'антифашисты'])

#bot = read_user_from_db(name='Nolan Diagram v1 bot #2', create_if_not_exists=True, requests=['голунов', 'выборы москва 2019', 'аннексия крым', 'телеканал дождь', 'медуза', 'митинги москва', 'навальный', 'эхо москвы', 'протестные акции', 'собчак'])

#bot = read_user_from_db(name='Nolan Diagram v1 bot #3', create_if_not_exists=True, requests=['коммунисты', 'зюганов', 'советский союз', 'кпрф', 'армия', 'оборона страны', 'возвращение крыма', 'пенсии', 'сталин', 'шойгу'])

#bot = read_user_from_db(name='Nolan Diagram v1 bot #4', create_if_not_exists=True, requests=['прямая линия с путиным', 'налоги', 'присоединение крыма', 'единая россия', 'russia today', 'первый канал', 'дмитрий киселев', 'владимир соловьев', 'программа время', 'пенсии'])


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

    if bot.requests is None:
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

    write_to_db(all_results, user=bot)
    write_user_to_db(bot)
    # write_cookies_to_file(bot,  + bot.file_name)
    print('\n\nTIME:', time() - start)

    s._cookie_jar.save('data/' + bot.file_name)

    # print(all_results)

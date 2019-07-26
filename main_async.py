from engine_parser_async import EngineParserAsync
from time import time
import asyncio
import aiohttp

from db_async import write_to_db, write_user_to_db, write_cookies_to_file, read_user_from_db

from user_async import UserAsync


all_results = []
s = None

bot = read_user_from_db(name='Adult auto bot')
# bot = UserAsync(name='Adult auto bot')


async def main():
    tasks = []

    engines = ['Google', 'Bing', 'Youtube']
    # engines = ['Google']

    async with aiohttp.ClientSession() as session:
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

    # requests = ["Путин", "Единая Россия" , "Выборы в России", "Новости Соловьев", "Раша тудей"]
    # requests = ["Зеленский", "Слуга народа", "Выборы в Украине", "Мажоритарка", "Зе команда"]
    requests = ["Audi RS", "авто запчасти", "машины украина", "авто риа", "машины с америки", "купить машину",
                "как выбрать машину", "политика", "гордон", "рыбалка", "поехать на море", "работа"]
    # requests = ['Mexican wall', "Audi RS"]

    for request in requests:
        await engine_parser.start_engine_scrapping(request, number=num_of_links, user=bot,
                                                   language_code='ru', engine=engine,
                                                   use_proxy=False, timeout_range=(3, 6),
                                                   print_output=False, session=session,
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

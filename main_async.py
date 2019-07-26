from engine_parser_async import EngineParserAsync
from time import time
import asyncio
import aiohttp
from user_async import UserAsync

from db_async import write_to_db, write_user_to_db, write_cookies_to_file, read_cookies_from_file


all_results = []
bot = UserAsync(name='Bot with going to other links Zelenskyi')
#bot.cookies = read_cookies_from_file('')


async def main():
    tasks = []

    engines = ['Google', 'Bing', 'Youtube']
    # engines = ['Google', 'Bing', 'Yahoo']

    async with aiohttp.ClientSession() as session:
        for engine in engines:
            task = asyncio.create_task(sub_task(engine, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def sub_task(engine, session):
    engine_parser = EngineParserAsync()
    num_of_links = 10

    # requests = ["Путин", "Единая Россия" , "Выборы в России", "Новости Соловьев", "Раша тудей"]
    requests = ["Зеленский", "Слуга народа", "Выборы в Украине", "Мажоритарка", "Зе команда"]
    # requests = ["Зеленский"]
    # requests = ['Mexican wall']

    for request in requests:
        await engine_parser.start_engine_scrapping(request, number=num_of_links, user=bot,
                                                 language_code='ru', engine=engine,
                                                 use_proxy=False, timeout_range=(3, 6),
                                                 print_output=False, session=session,
                                                 all_results=all_results)



if __name__ == '__main__':
    start = time()

    asyncio.run(main())

    write_to_db(all_results)
    write_user_to_db(bot)
    write_cookies_to_file(bot, 'data/Russian.cookies')
    print('\n\nTIME:', time() - start)

    # print(all_results)

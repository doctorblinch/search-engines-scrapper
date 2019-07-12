from engine_parser_async import EngineParserAsync
from time import time
import asyncio
import aiohttp
from user_async import UserAsync

from db_async import write_to_db, write_user_to_db


all_results = []
bot = UserAsync(name='TestBot')


async def main():
    tasks = []
    num_of_links = 10

    engine_parser = EngineParserAsync()

    requests = ['Автосалон', 'Салон красоты', 'Новости']
    engines = ['Google', 'Bing']
    # engines = ['Google', 'Bing', 'Yahoo']

    async with aiohttp.ClientSession() as session:
        for engine in engines:
            for request in requests:
                task = asyncio.create_task(engine_parser.start_engine_scrapping(request, number=num_of_links, user=bot,
                                                                                language_code='ru', engine=engine,
                                                                                use_proxy=False, timeout_range=(3, 6),
                                                                                print_output=False, session=session,
                                                                                all_results=all_results))
                tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start = time()

    asyncio.run(main())

    write_to_db(all_results)
    write_user_to_db(bot)

    print('\n\nTIME:', time() - start)

    # print(all_results)

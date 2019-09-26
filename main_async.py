from engine_parser_async import EngineParserAsync
from time import time, sleep
import asyncio
import aiohttp
import os.path

from db_async import write_to_db, write_user_to_db, write_cookies_to_file, read_user_from_db
from user_async import UserAsync


all_results = []
s = None


bot = read_user_from_db(name='Nolan Diagram v2 bot #3', create_if_not_exists=True, requests=['прямая линия с путиным', 'налоги', 'присоединение крыма', 'единая россия', 'russia today', 'первый канал', 'дмитрий киселев', 'владимир соловьев', 'программа время', 'пенсии'])

#bot = read_user_from_db(name='Nolan Diagram v2 bot #1', create_if_not_exists=True, requests=['анархизм', 'митинги', 'нацболы', 'лимонов', 'революция', 'народная самооборона', 'путин вор',  'азат мифтахов', 'русский марш', 'антифашисты'])

#bot = read_user_from_db(name='Nolan Diagram v2 bot #2', create_if_not_exists=True, requests=['голунов', 'выборы москва 2019', 'аннексия крым', 'телеканал дождь', 'медуза', 'митинги москва', 'навальный', 'эхо москвы', 'протестные акции', 'собчак'])

#bot = read_user_from_db(name='Nolan Diagram v2 bot #3', create_if_not_exists=True, requests=['коммунисты', 'зюганов', 'советский союз', 'кпрф', 'армия', 'оборона страны', 'возвращение крыма', 'пенсии', 'сталин', 'шойгу'])

#bot = read_user_from_db(name='Nolan Diagram v2 bot #4', create_if_not_exists=True, requests=['прямая линия с путиным', 'налоги', 'присоединение крыма', 'единая россия', 'russia today', 'первый канал', 'дмитрий киселев', 'владимир соловьев', 'программа время', 'пенсии'])


async def main(engines_export=None, browser=False, b=None):
    tasks = []

    engines = ['Google'] if engines_export is None else engines_export
    if b is not None:
        global bot
        bot = b

    async with aiohttp.ClientSession() as session:
        if os.path.exists('data/' + bot.file_name):
            session._cookie_jar.load('data/' + bot.file_name)
        for engine in engines:
            task = asyncio.create_task(sub_task(engine, session, browser))
            tasks.append(task)
        global s
        s = session
        await asyncio.gather(*tasks)


async def sub_task(engine, session, browser=False):
    engine_parser = EngineParserAsync()
    num_of_links = 10

    #requests = ["Мультики", "Игрушки" , "Лунтик", "Лего", "Игры для детей", "Магазин игрушек",
     #"Сказка", "Хот вилс", "Игрушки машинки", "История Игрушек", "Машинка на радиоуправлении", "купить машинку на радиоуправлении"]

    if bot.requests is None:
        requests = ['Машинка', 'магазин']
    else:
        requests = bot.requests

    if browser:
        await engine_parser.start_engine_scrapping(requests, number=num_of_links, user=bot, language_code='ru',
                                                   print_output=True, all_results=all_results, engine=engine, browser=True)
        return

    for request in requests:
        await engine_parser.start_engine_scrapping(request, number=num_of_links, user=bot,
                                                   language_code='ru', engine=engine,
                                                   use_proxy=False, timeout_range=(3, 6),
                                                   print_output=True, session=session,
                                                   all_results=all_results, browser=True)

import yaml
import os.path
from datetime import datetime


def program(file_name='program.yaml'):
    if os.path.exists('program.yaml'):
        with open('program.yaml', 'r') as f:
            plan = yaml.load(f)
            print(plan)

        schedule = {}
        for b in plan['bots']:
            bot = read_user_from_db(name=b['name'], requests=b['queries'], create_if_not_exists=True)
            sch = b['visit_schedule']
            engines = sch['engine_types']
            for i in range(sch['num_cycles']):
                hours, minutes = sch['start_time'].split(':')
                days = 0
                hours = int(hours)
                minutes = float(minutes)
                minutes += i * sch['every_minutes']
                if minutes >= 60:
                    hours += int(minutes // 60)
                    minutes = minutes % 60
                if hours >= 24:
                    days += hours // 24
                    hours = hours % 24
                start_time = datetime.strptime(str(hours) + ':' + str(minutes).split('.')[0], '%H:%M')
                start_time = start_time.replace(year=datetime.now().year, month=datetime.now().month,
                                                day=datetime.now().day + days)
                schedule.update({start_time: bot})
            #print('Engine: {}\nStart time: {}\nEvery minutes: {}\nNumber of cycles: {}\nFL: {}\n'.format(
             #   sch['engine_types'],sch['start_time'],sch['every_minutes'],sch['num_cycles'],sch['follow_links']))

        keys = list(schedule.keys())
        keys.sort()
        for key in keys:
            print(schedule[key])
            print((key - datetime.now()).total_seconds())
            if (key - datetime.now()).total_seconds() > 0:
                sleep((key - datetime.now()).total_seconds())
            start = time()

            asyncio.run(main(engines_export=engines, b=schedule[key], browser=True))
            global all_results
            write_user_to_db(bot)
            write_to_db(all_results, user=bot)
            all_results = []
            print('\n\nTIME:', time() - start)



        print('THIS IS THE END!')


if __name__ == '__main__':
    file_name = 'program.yaml'
    if os.path.exists(file_name):
        program(file_name)
    else:
        start = time()

        asyncio.run(main(browser=True))

#        write_user_to_db(bot)
        write_to_db(all_results, user=bot)

        print('\n\nTIME:', time() - start)

        #s._cookie_jar.save('data/' + bot.file_name)

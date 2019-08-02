from engine_parser import EngineParser
from user import User
from db import write_to_db, read_from_db, write_user_to_db

from time import time

requests = ['Автосалон', 'Салон красоты', 'Новости']
engine_parser = EngineParser()
engines = ['Google', 'Bing', 'Youtube']

num_of_links = 10

bot = User(name='TestBot')
start = time()

for engine in engines:
    results = []
    for request in requests:
        results.append(engine_parser.start_engine_scrapping(request, number=num_of_links, user=bot,
                                                            language_code='ru', engine=engine,
                                                            use_proxy=False, timeout_range=(3, 6),
                                                            print_output=False))
    write_to_db(results, engine)

print('\n\nTIME:', time() - start)

write_user_to_db(bot)

# with open('output.json', 'w', encoding='utf-8') as outfile:
#    json.dump(results, outfile,indent=4,sort_keys=True,ensure_ascii=False)

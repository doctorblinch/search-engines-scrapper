from engine_parser import EngineParser
from db import write_to_db, read_from_db

from time import time

requests = ['Автосалон', 'Салон красоты', 'Новости']
engine_parser = EngineParser()
engines = ['Google', 'Bing', 'Yahoo']
# engines = ['Google', 'Bing']

num_of_links = 10

start = time()
for engine in engines:
    results = []
    for request in requests:
        results.append(engine_parser.start_engine_scrapping(request, number=num_of_links,
                                                            language_code='ru', engine=engine,
                                                            use_proxy=True, timeout_range=(3, 6),
                                                            print_output=False))
    write_to_db(results, engine)

print('\n\nTIME:', time() - start)

# with open('output.json', 'w', encoding='utf-8') as outfile:
#    json.dump(results, outfile,indent=4,sort_keys=True,ensure_ascii=False)

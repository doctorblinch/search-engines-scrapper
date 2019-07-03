from engine_parser import EngineParser
from db import write_to_db, read_from_db

requests = ['Автосалон', 'Салон красоты', 'Новости']
engine_parser = EngineParser()
engines = ['Google', 'Bing', 'Yahoo']

num_of_links = 10

for engine in engines:
    results = []
    for request in requests:
        results.append(engine_parser.start_engine_scrapping(request, num_of_links, 'ru', engine=engine, use_proxy=True))
    write_to_db(results, engine)


# with open('output.json', 'w', encoding='utf-8') as outfile:
#    json.dump(results, outfile,indent=4,sort_keys=True,ensure_ascii=False)

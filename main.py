# import json
# from google_parser import google_parser
# from bing_parser import bing_parser
from engine_parser import EngineParser
from db import write_to_db, read_from_db

requests = ['Автосалон', 'Салон красоты', 'Новости']
# engines = {'google': google_parser, 'bing': bing_parser}
engine_parser = EngineParser()
engines = ['Google', 'Bing']
num_of_links = 10

# for key, engine in engines.items():
#     results = []
#     for request in requests:
#         results.append(engine(request, num_of_links, 'ru'))
#     write_to_db(results, key)

for engine in engines:
    results = []
    for request in requests:
        engine_parser.ENGINE = engine
        results.append(engine_parser.start_engine_scrapping(request, num_of_links, 'ru'))
    write_to_db(results, engine)

read_from_db()

# with open('output.json', 'w', encoding='utf-8') as outfile:
#    json.dump(results, outfile,indent=4,sort_keys=True,ensure_ascii=False)
#
# json.dump(output, twitter_data_file, indent=4, sort_keys=True)


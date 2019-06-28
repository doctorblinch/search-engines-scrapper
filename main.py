import json
from google_parser import google_parser
from db import write_to_db,read_from_db

requests = ['Автосалон','Салон красоты', 'Новости']
num_of_links = 10
results  = []

for request in requests:
    results.append(google_parser(request,10,'ru'))

write_to_db(results)
read_from_db()

#with open('output.json', 'w', encoding='utf-8') as outfile:
#    json.dump(results, outfile,indent=4,sort_keys=True,ensure_ascii=False)

#json.dump(output, twitter_data_file, indent=4, sort_keys=True)


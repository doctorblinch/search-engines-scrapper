import json
from google_parser import main

requests = ['Автосалон','Салон красоты', 'Новости']
num_of_links = 10
results  = []

for request in requests:
    results.append(main(request,10,'ru'))

with open('output.json', 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile,indent=4,sort_keys=True,ensure_ascii=False)

#json.dump(output, twitter_data_file, indent=4, sort_keys=True)


import requests
from bs4 import BeautifulSoup
from datetime import datetime

import sys

# Headers for imitation user activity
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def fetch_results(query, number):
    # preparation of request link
    bing_url = 'https://www.bing.com/search?q={}&count={}'.format(query, number)

    # get page with timeout = 5sec (for imitation user activity)
    response = requests.get(bing_url, headers=HEADERS, timeout=5)

    # error checking
    response.raise_for_status()

    # return HTML code of page
    return response.text


def parse_html(html, query):
    soup = BeautifulSoup(html, 'lxml')

    found_results = []
    index = 1
    result_block = soup.find_all('li', attrs={'class': 'b_algo'})
    for result in result_block:

        link = result.find('a', href=True)
        title = result.find('h2')
        description = result.find('p')
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#' and description is not None:
                found_results.append({'index': index, 'query': query,
                                      'link': link, 'title': title,
                                      'description': description,
                                      'time': datetime.now()})
                index += 1
    return found_results


def scrape_bing(query, number, language_code):
    try:
        html = fetch_results(query, number)
        return parse_html(html=html, query=query)
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")


def bing_parser(query, number, language_code):
    results = scrape_bing(query=query, number=number, language_code=language_code)

    for i in results:
        print(i)

    return results


if '__main__' == __name__:
    """
    query                   <--->       your search query
    number                  <--->       how many links you want to see
    language_code           <--->       code of language of your query

    How to run this script? (example):
        python main.py "право постійного користування земельною ділянкою" 3 ru
    """
    bing_parser(query=sys.argv[1], number=int(sys.argv[2]), language_code=sys.argv[3])

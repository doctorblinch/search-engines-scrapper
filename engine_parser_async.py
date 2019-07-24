import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime

from user_async import UserAsync

from time import time
import asyncio
import aiohttp

from random import choice, uniform

import sys

import re


def timer(func):
    async def wrapper(self, *args, **kwargs):
        start = time()
        res = await func(self, *args, **kwargs)
        print('({}) Function {} ---> {} sec'.format(kwargs['engine'], func.__name__, time() - start))
        if func.__name__ == '__fetch_results':
            print('Timeout:', kwargs['timeout'])
        print()
        return res

    return wrapper


class EngineParserAsync:
    def __init__(self):
        pass

    # @timer
    async def __fetch_results(self, query, number, language_code, user_agent=None, user: UserAsync = None,
                              proxy=None, timeout=5.0, session: aiohttp.client.ClientSession = None, engine='google'):
        url = ''

        # preparation of request link
        if engine == 'bing':
            url = 'https://www.bing.com/search?q={}&count={}'.format(query, number)
        elif engine == 'google':
            url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(query, number, language_code)
        elif engine == 'yahoo':
            url = 'https://search.yahoo.com/search?p={}&n={}&ei=UTF-8'.format(query, number)
        elif engine == 'youtube':
            url = 'https://www.youtube.com/results?search_query={}'.format(query)

        # get page with timeout (for imitation user activity)
        async with session.get(url, headers=user.agent, timeout=timeout, proxy=proxy) as response:
            # error checking
            if response.status != 200:
                response.raise_for_status()

            # get HTML code of page
            data = await response.text()

            # get cookies
            user.cookies = session._cookie_jar._cookies

            # delay between requests
            # await asyncio.sleep(timeout)

            # return HTML code of page
            return data

    def __parse_bing_html(self, html, query, engine):
        # print('---------------' + self.ENGINE)
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
                title = title.get_text().strip()
                split = link.split('/url?q=')
                if split[0] == '':
                    link = 'http://www.bing.com/url?q=' + split[1]
                # print(link)
                if description:
                    description = description.get_text().strip()
                if link != '#' and description is not None:
                    found_results.append({'index': index, 'query': query,
                                          'link': link, 'title': title,
                                          'description': description,
                                          'time': datetime.now(),
                                          'engine': engine})
                    index += 1
        return found_results

    def __parse_youtube_html(self, html, query, engine):
        soup = BeautifulSoup(html, 'lxml')

        found_results = []
        index = 1
        result_block = soup.findAll('div', attrs={'class': 'yt-lockup-content'})
        # print('Url= ', result_block)
        # input()

        for result in result_block:

            link = result.find('a', href=True)
            title = link['title']
            description = result.find('div', attrs={'class': 'yt-lockup-description'})
            # print('Link = ',link, '\ntitle = ', title, '\ndescription=', description)
            if link and title:
                link = link['href']
                title = title.strip()
                if 'https://www.youtube.com' not in link:
                    link = 'https://www.youtube.com' + link
                if description:
                    description = description.get_text().strip()
                if link != '#' and description is not None:
                    found_results.append({'index': index, 'query': query,
                                          'link': link, 'title': title,
                                          'description': description,
                                          'time': datetime.now(),
                                          'engine': engine})

            index += 1
        # print(found_results)
        return found_results

    def __parse_google_html(self, html, query, engine):
        # print('---------------' + self.ENGINE)
        soup = BeautifulSoup(html, 'lxml')

        found_results = []
        index = 1
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:

            link = result.find('a', href=True)
            title = result.find('h3')
            description = result.find('span', attrs={'class': 'st'})
            if link and title:
                link = link['href']
                title = title.get_text().strip()
                split = link.split('/url?url=')
                if split[0] == '':
                    link = 'http://www.google.com/url?url=' + split[1]
                # print(link)
                if description:
                    description = description.get_text().strip()
                if link != '#' and description is not None:
                    found_results.append({'index': index, 'query': query,
                                          'link': link, 'title': title,
                                          'description': description,
                                          'time': datetime.now(),
                                          'engine': engine})
                    index += 1
        return found_results

    def __parse_yahoo_html(self, html, query, engine):
        soup = BeautifulSoup(html, 'lxml')

        found_results = []
        index = 1
        result_block = soup.findAll('div', attrs={'class': 'dd algo algo-sr Sr'})
        # print('Url= ', result_block)
        # input()

        for result in result_block:

            link = result.find('a', href=True)
            title = result.find('h3')
            description = result.find('p', attrs={'class': 'lh-16'})
            # print('Link = ',link, '\ntitle = ', title, '\ndescription=', description)
            if link and title:
                link = link['href']
                title = title.get_text().strip()
                # split = link.split('')
                if description:
                    description = description.get_text().strip()
                if link != '#' and description is not None:
                    found_results.append({'index': index, 'query': query,
                                          'link': link, 'title': title,
                                          'description': description,
                                          'time': datetime.now(),
                                          'engine': engine})

            index += 1
        # print(found_results)
        return found_results

    async def __scrape(self, query, number, language_code, use_proxy, timeout_range, session, user, engine):
        # set User-Agent header
        ua = UserAgent()
        user_agent = {"User-Agent": ua.random}

        # set proxy
        if use_proxy:
            with open('proxies.txt') as file:
                proxies = file.read().split('\n')
                proxy = 'http://' + choice(proxies)
        else:
            proxy = None

        # set timeout value
        timeout = uniform(*timeout_range)

        try:
            # get HTML code of some page
            html = await self.__fetch_results(query=query, number=number, language_code=language_code, engine=engine,
                                              user_agent=user_agent, proxy=proxy, timeout=timeout, session=session,
                                              user=user)

            # parse results
            if engine == 'bing':
                return self.__parse_bing_html(html=html, query=query, engine=engine)
            elif engine == 'google':
                return self.__parse_google_html(html=html, query=query, engine=engine)
            elif engine == 'yahoo':
                return self.__parse_yahoo_html(html=html, query=query, engine=engine)
            elif engine == 'youtube':
                return self.__parse_youtube_html(html=html, query=query, engine=engine)

        except AssertionError:
            raise Exception("Incorrect arguments parsed to function")
        except requests.HTTPError:
            raise Exception("You appear to have been blocked by {}".format(engine))
        except requests.RequestException:
            raise Exception("Appears to be an issue with your connection")

    async def start_engine_scrapping(self, query, number=10, language_code='ru', user=None,
                                     print_output=False, engine='google', use_proxy=False,
                                     timeout_range=(3, 5), session=None, all_results=[]):
        # set search engine
        engine = engine.lower()

        # get results
        results = await self.__scrape(query=query, number=number,
                                      language_code=language_code,
                                      use_proxy=use_proxy, user=user,
                                      timeout_range=timeout_range,
                                      session=session, engine=engine)

        all_results.append(results)
        # await write_to_db(results, engine)

        if print_output:
            print('---------------{}(len={})---------------'.format(engine, len(results)))
            for res in results:
                for key in res.keys():
                    if key == 'index':
                        print(key + ': ' + str(res[key]))
                    else:
                        print('\t' + key + ': ' + str(res[key]))
                print()
            print('---------------END---------------\n')


if '__main__' == __name__:
    """
    query                   <--->       your search query
    number                  <--->       how many links you want to see
    language_code           <--->       code of language of your query
    print_output            <--->       print output flag
    use_proxy               <--->       use proxy flag

    How to run this script? (example):
        python main.py "право постійного користування земельною ділянкою" 3 ru
    """
    engine_parser = EngineParserAsync()
    engine_parser.start_engine_scrapping(query=sys.argv[1], number=int(sys.argv[2]),
                                         language_code=sys.argv[3], print_output=True,
                                         use_proxy=True, engine='google',
                                         timeout_range=(3, 5))

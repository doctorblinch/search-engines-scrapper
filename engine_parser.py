import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
from user import User

from random import choice, uniform

import sys


class EngineParser:
    def __init__(self, engine='google'):
        # Set engine
        self.ENGINE = engine.lower()

    def __fetch_results(self, query, number, language_code, user_agent=None, proxy=None, timeout=5, user=None):

        url = ''

        # preparation of request link
        if self.ENGINE == 'bing':
            url = 'https://www.bing.com/search?q={}&count={}'.format(query, number)
        elif self.ENGINE == 'google':
            url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(query, number, language_code)
        elif self.ENGINE == 'yahoo':
            url = 'https://search.yahoo.com/search?p={}&n={}&ei=UTF-8'.format(query,number)

        if not user:
            # get page with timeout = 5sec (for imitation user activity)
            response = requests.get(url, headers=user_agent, proxies=proxy)#, timeout=timeout)
        else:
            session = requests.Session()
            session.cookies = user.cookies
            response = session.get(url, headers=user.agent, proxies=proxy)
            user.cookies = session.cookies
            #print('User.name = {}\nUser.user_agent = {}\nUser.cookies={}'.format(user.name,user.user_agent,user.cookies))
            #input()

        # error checking
        response.raise_for_status()

        # return HTML code of page
        return response.text

    def __parse_bing_html(self, html, query):
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
                                          'time': datetime.now()})
                    index += 1
        return found_results

    def __parse_google_html(self, html, query):
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
                                          'time': datetime.now()})
                    index += 1
        return found_results

    def __parse_yahoo_html(self, html, query):
        soup = BeautifulSoup(html, 'lxml')

        found_results = []
        index = 1
        result_block = soup.findAll('div', attrs={'class': 'dd algo algo-sr Sr'})
        #print('Url= ', result_block)
        #input()

        for result in result_block:

            link = result.find('a',href=True)
            title = result.find('h3')
            description = result.find('p', attrs={'class': 'lh-16'})
            #print('Link = ',link, '\ntitle = ', title, '\ndescription=', description)
            if link and title:
                link = link['href']
                title = title.get_text().strip()
                #split = link.split('')
                if description:
                    description = description.get_text().strip()
                if link != '#' and description is not None:
                    found_results.append({'index': index,'query': query,
                                          'link': link,'title': title,
                                          'description': description,
                                          'time': datetime.now()})

            index += 1
        #print(found_results)
        return found_results

    def __scrape(self, query, number, language_code, use_proxy, user=None):

        # set User-Agent header
        ua = UserAgent()
        user_agent = {"User-Agent": ua.random}

        # set proxy
        if use_proxy:
            with open('proxies.txt') as file:
                proxies = file.read().split('\n')
                proxy = {'http': 'http://' + choice(proxies)}
        else:
            proxy = None

        # set timeout value
        timeout = uniform(3, 6)

        try:
            # get HTML code of some page
            html = self.__fetch_results(query=query, number=number, language_code=language_code,
                                        user_agent=user_agent, proxy=proxy, timeout=timeout, user=user)

            # parse results
            if self.ENGINE == 'bing':
                return self.__parse_bing_html(html=html, query=query)
            elif self.ENGINE == 'google':
                return self.__parse_google_html(html=html, query=query)
            elif self.ENGINE == 'yahoo':
                return self.__parse_yahoo_html(html=html, query=query)

        except AssertionError:
            raise Exception("Incorrect arguments parsed to function")
        except requests.HTTPError:
            raise Exception("You appear to have been blocked by {}".format(self.ENGINE))
        except requests.RequestException:
            raise Exception("Appears to be an issue with your connection")

    def start_engine_scrapping(self, query, number, language_code,
                               print_output=False, engine='google', use_proxy=False, user=None):
        # set search engine
        #if engine == None:
            #self.ENGINE = 'google'
        self.ENGINE = engine.lower()

        # get results
        results = self.__scrape(query=query, number=number, language_code=language_code, use_proxy=use_proxy, user=user)

        if print_output:
            for i in results:
                print(i)

        return results


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
    engine_parser = EngineParser('Google')
    engine_parser.start_engine_scrapping(query=sys.argv[1], number=int(sys.argv[2]),
                                         language_code=sys.argv[3], print_output=True,
                                         use_proxy=True, engine=engine_parser.ENGINE)

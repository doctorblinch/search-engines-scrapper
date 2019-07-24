import requests
from fake_useragent import UserAgent


class User:
    def __init__(self, name):
        self.name = name
        self.user_agent = UserAgent()
        self.agent = {'User-Agent': self.user_agent.random}
        self.cookies = requests.cookies.RequestsCookieJar()

    def change_data(self, name=None, user_agent=None, cookies=None):
        if name is not None:
            self.name = name

        if user_agent is not None:
            self.user_agent = user_agent

        if cookies is not None:
            self.cookies = cookies

    def __repr__(self):
        return 'User: {}, using: {}'.format(self.name, self.agent)

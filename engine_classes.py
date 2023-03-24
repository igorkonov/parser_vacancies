import os
import requests
from abc import ABC, abstractmethod
from connector import Connector


class Engine(ABC):
    @abstractmethod
    def get_request(self, url: str, params: dict, headers: dict):
        resp = requests.get(url=url, params=params, headers=headers)
        return resp.json()

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        connector = Connector()
        connector.data_file = file_name
        return connector


class HH(Engine):
    def __init__(self, text: str):
        self.text = text
        self.params = {'text': self.text, 'per_page': 100, 'page': 0, 'area': 113}
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    def get_request(self, **kwargs):
        return super().get_request(self.url, self.params, self.headers)


class SuperJob(Engine):

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                                      'X-Api-App-Id': os.environ['SUPERJOB_API_KEY']}
        self.params = {'keyword': self.keyword, 'page': 0, 'count': 100}
        self.url = 'https://api.superjob.ru/2.0/vacancies/search'

    def get_request(self, **kwargs):
        return super().get_request(self.url, self.params, self.headers)

import os
from abc import ABC, abstractmethod
from pprint import pprint
from jobs_classes import *
import requests
from utils import *

from connector import Connector


class Engine(ABC):
    @abstractmethod
    def get_request(self, url: str, params: dict, headers: dict):
        resp = requests.get(url=url, params=params, headers=headers)
        return resp.json()

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        return Connector(file_name)


class HH(Engine):
    def __init__(self, text: str):
        self.text = text
        self.params = {'text': self.text, 'per_page': 20, 'page': 0, 'area': 113}
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    def get_request(self, **kwargs):
        return super().get_request(self.url, self.params, self.headers)

    def get_vacancies_hh(self, count=1000):
        vacancies = []
        page = 0
        while self.params['per_page'] * page < count:
            data = self.get_request()
            if data:
                vacancies += data.get('items')
                page += 1
            else:
                break
        return vacancies


class SuperJob(Engine):

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                                      'X-Api-App-Id': os.environ['SUPERJOB_API_KEY']}
        self.params = {'keyword': self.keyword, 'per_page': 20, 'count': '100'}
        self.url = 'https://api.superjob.ru/2.0/vacancies/search'

    def get_request(self, **kwargs):
        return super().get_request(self.url, self.params, self.headers)

    def get_vacancies_sj(self, pages=1000):
        vacancies = []
        for i in range(1, pages + 1):
            self.params['page'] = i
            data = self.get_request()
            for item in data['objects']:
                vacancies.append(item)
            if len(vacancies) >= 500:
                break
        return vacancies

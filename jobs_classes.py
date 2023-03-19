from engine_classes import *
from utils import *
from connector import *
import requests


class Vacancy:

    __slots__ = ['name', 'link', 'description', 'salary']

    def __init__(self, name, link, description, salary):
        self.name = name
        self.link = link
        self.description = description
        self.salary = salary


    def __gt__(self, other):
        if not self.salary:
            self.salary = 0
        if not other.salary:
            other.salary = 0
        return self.salary > other.salary

    def __lt__(self, other):
        if not self.salary:
            self.salary = 0
        if not other.salary:
            other.salary = 0
        return self.salary < other.salary

    def __iter__(self):
        self.index = 0
        return

    def __next__(self):
        if self.index < len(HHVacancy.hh_vacancies):
            x = HHVacancy.hh_vacancies[self.index]
            self.index += 1
            return x
        else:
            raise StopIteration


class CountMixin:
    counter = 0
    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        return CountMixin.counter

    @get_count_of_vacancy.setter
    def get_count_of_vacancy(self, value):
        CountMixin.counter = value
class HHVacancy(Vacancy, CountMixin):  # add counter mixin
    """ HeadHunter Vacancy """
    hh_vacancies: list = []
    data_file = 'hh_vacancy.json'

    def __init__(self, name, link, description, salary):
        super().__init__(name, link, description, salary)
        self.data_file = HHVacancy.data_file

    @classmethod
    def get_file(cls, data_file):
        with open(data_file, encoding='utf-8') as f:
            data = json.load(f)
            for obj in data:
                for item in obj:
                    name = item.get('name')
                    link = item.get('url')
                    description = get_description_hh(item)
                    try:
                        if item.get('salary').get('currency') == 'USD':
                            salary = round(item.get('salary').get('from') * 76.96), \
                                    round(item.get('salary').get('to') * 76.96)
                        elif item.get('salary').get('currency') == 'EUR':
                            salary = round(item.get('salary').get('from') * 81.11),  \
                                    round(item.get('salary').get('to') * 81.11)
                        else:
                            salary = item.get('salary').get('from'), item.get('salary').get('to')
                    except (AttributeError, TypeError):
                        salary = 0
                dict_vacancies = {
                    'name': name,
                    'link': link,
                    'description': description,
                    'salary': salary
                    }
                cls.hh_vacancies.append(HHVacancy(**dict_vacancies))

    def __str__(self):
        return f"\n************\nСервис -----HeadHunter-----\nВакансия: {self.name} - ({self.link})" \
               f"\n--------------------\n{self.description}\nЗаработная плата {self.salary} руб/мес"


class SJVacancy(Vacancy):  # add counter mixin
    """ SuperJob Vacancy """
    sj_vacancies: list = []
    data_file = 'sj_vacancy.json'

    def __init__(self, name, link, description, salary):
        super().__init__(name, link, description, salary)
        self.data_file = SJVacancy.data_file

    @classmethod
    def get_file(cls, data_file):
        with open(data_file) as f:
            data = json.load(f)
            for obj in data:
                for item in obj:
                    name = item.get('profession')
                    link = item.get('link')
                    description = get_description_sj(item)
                    try:
                        salary = item.get('payment_from')
                    except (AttributeError, TypeError):
                        salary = 0

                    cls.sj_vacancies.append(HHVacancy(name, link, description, salary))

    def __str__(self):
        return f'SJ: {self.name}, зарплата: {self.salary} руб/мес'


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    sorted_by_salary = sorted(vacancies, reverse=True)
    return sorted_by_salary


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    try:
        for i in range(top_count):
            print(vacancies[i])
    except IndexError:
        print(f'Нет {top_count} записей вакансий')


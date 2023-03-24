import json
from engine_classes import HH, SuperJob
from utils import get_description_hh, get_description_sj, get_salary


class Vacancy:

    __slots__ = ['source', 'name', 'link', 'description', 'salary', 'city']

    def __init__(self, source, name, link, description, salary, city):
        self.name = name
        self.link = link
        self.description = description
        self.salary = salary
        self.city = city
        self.source = source

    def __str__(self):
        return f"\n************\nСервис -----{self.source}-----\nВакансия: {self.name} - ({self.link})" \
               f"\n--------------------\n{self.description}\nЗаработная плата {self.salary} руб/мес\nГород {self.city}"

    def __repr__(self):
        return f"\n************\nСервис -----{self.source}-----\nВакансия: {self.name} - ({self.link})" \
               f"\n--------------------\n{self.description}\nЗаработная плата {self.salary} руб/мес\nГород {self.city}"

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
        return self

    def __next__(self):
        if self.index < len(HHVacancy.hh_vacancies):
            x = HHVacancy.hh_vacancies[self.index]
            self.index += 1
            return x
        else:
            raise StopIteration


class CountMixin:

    def __init__(self):
        self.data_file_json = None

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        with open(self.data_file_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len(data)


class HHVacancy(Vacancy, CountMixin):
    """ HeadHunter Vacancy """
    hh_vacancies: list = []

    def __init__(self, source, name, link, description, salary, city):
        super().__init__(source, name, link, description, salary, city)
        self.data_file_json = 'hh_vacancy.json'
        self.source = 'HeadHunter'

    def get_vacancies_hh(self, text, count_pages=5):
        hh = HH(text)
        for i in range(1, count_pages + 1):
            hh.params['page'] = i
            data = hh.get_request()
            for item in data.get('items'):
                self.name = item.get('name')
                self.link = item.get('alternate_url')
                self.description = get_description_hh(item)
                try:
                    if item.get('salary').get('currency') == 'USD':
                        self.salary = [round(item.get('salary').get('from') * 76.96),
                                       round(item.get('salary').get('to') * 76.96)]
                    elif item.get('salary').get('currency') == 'EUR':
                        self.salary = [round(item.get('salary').get('from') * 81.11),
                                       round(item.get('salary').get('to') * 81.11)]
                    else:
                        self.salary = [item.get('salary').get('from'), item.get('salary').get('to')]
                except (AttributeError, TypeError):
                    self.salary = 0
                self.city = item.get('area').get('name')

                HHVacancy.hh_vacancies.append({'source': self.source, 'name': self.name,
                                               'link': self.link, 'description': self.description,
                                               'salary': get_salary(self.salary), 'city': self.city})

                if len(HHVacancy.hh_vacancies) >= 500:
                    break

        connector = HH.get_connector(self.data_file_json)
        connector.insert(HHVacancy.hh_vacancies)
        return connector.data_file

    def __str__(self):
        return f"\n************\nСервис -----{self.source}-----\nВакансия: {self.name} - ({self.link})" \
               f"\n--------------------\n{self.description}\nЗаработная плата {self.salary} руб/мес\nГород {self.city}"

    def __repr__(self):
        return f"\n************\nСервис -----{self.source}-----\nВакансия: {self.name} - ({self.link})" \
               f"\n--------------------\n{self.description}\nЗаработная плата {self.salary} руб/мес\nГород {self.city}"


class SJVacancy(Vacancy, CountMixin):
    """ SuperJob Vacancy """
    sj_vacancies: list = []

    def __init__(self, source, name, link, description, salary, city):
        super().__init__(source, name, link, description, salary, city)
        self.data_file_json = 'sj_vacancy.json'
        self.source = 'Superjob'

    def get_vacancies_sj(self, text, count_pages=5):
        sj = SuperJob(text)
        for i in range(1, count_pages + 1):
            sj.params['page'] = i
            data = sj.get_request()
            for item in data.get('objects'):
                self.name = item.get('profession')
                self.link = item.get('link')
                self.description = get_description_sj(item)
                try:
                    self.salary = [item.get("payment_from"), item.get("payment_to")]
                except (AttributeError, TypeError):
                    self.salary = 0
                self.city = item.get('town').get('title')

                SJVacancy.sj_vacancies.append(
                    {'source': self.source, 'name': self.name, 'link': self.link, 'description': self.description,
                     'salary': get_salary(self.salary), 'city': self.city})

                if len(SJVacancy.sj_vacancies) >= 500:
                    break

        connector = SuperJob.get_connector(self.data_file_json)
        connector.insert(SJVacancy.sj_vacancies)
        return connector.data_file

    def __str__(self):
        return f"\n************\nСервис -----{self.source}-----\nВакансия: {self.name} - ({self.link})" \
               f"\n--------------------\n{self.description}\nЗаработная плата {self.salary} руб/мес\nГород {self.city}"

    def __repr__(self):
        return f"\n************\nСервис -----{self.source}-----\nВакансия: {self.name} - ({self.link})" \
               f"\n--------------------\n{self.description}\nЗаработная плата {self.salary} руб/мес\nГород {self.city}"

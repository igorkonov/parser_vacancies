import os
from pprint import pprint
from engine_classes import HH, SuperJob
from jobs_classes import *
import pandas as pd
import requests

def main():
    input_word = 'python'#input('Введите поисковый запрос:')
    user_input = "HH"#input("Введите сервис подбора вакансий [HH, SuperJob]:")
    input_count = 10#input("Сколько вывести вакансий?")
    input_sorting = 'yes'#input("Вы хотите отсортировать вакансии по зп? yes/no")
    while True:
        if user_input == 'HH':
            engine = HH(user_input)
            hh_res = engine.get_vacancies_hh()
            hh_data = HH.get_connector('hh_vacancy.json')
            hh_data.insert(hh_res)
            HHVacancy.get_file('hh_vacancy.json')
            if input_sorting.lower() == 'Yes' or 'yes':
                get_top(sorting(HHVacancy.hh_vacancies), input_count)
                print(f'{HHVacancy.get_count_of_vacancy} - количество вакансий от HH')




if __name__ == '__main__':
    main()

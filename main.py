from jobs_classes import HHVacancy, SJVacancy
from utils import sorting, get_top, collect_jobs


def main():
    input_word = input('Введите название вакансии для поиcка: ')
    print('================================================================')
    user_input = input("Введите желаемый сервис на выбор для подбора вакансий (HH/SuperJob): ")
    print('================================================================')
    input_count = int(input("Сколько желаете вывести вакансий?\n"))
    print('================================================================')
    input_sorting = input("Вы хотите отсортировать вакансии по зп? yes/no\n")

    if user_input.lower() == "hh":
        vac_1 = collect_jobs(HHVacancy)
        connector = vac_1.get_vacancies_hh(input_word)
        vacancy = vac_1.get_vacancies_hh_from_file(connector)
        if input_sorting.lower() == "yes":
            get_top(sorting(vacancy), input_count)
            print(f'{vac_1.get_count_of_vacancy} - количество вакансий от HH')
        if input_sorting.lower() == "no":
            get_top(vacancy, input_count)
            print(f'{vac_1.get_count_of_vacancy} - количество вакансий от HH')

    if user_input.lower() == "superjob":
        vac_2 = collect_jobs(SJVacancy)
        connector = vac_2.get_vacancies_sj(input_word)
        vacancy = vac_2.get_vacancies_sj_from_file(connector)

        if input_sorting.lower() == "yes":
            get_top(sorting(vacancy), input_count)
            print(f'{vac_2.get_count_of_vacancy} - количество вакансий от SuperJob')
        if input_sorting.lower() == "no":
            get_top(vacancy, input_count)
            print(f'{vac_2.get_count_of_vacancy} - количество вакансий от SuperJob')


if __name__ == '__main__':
    main()

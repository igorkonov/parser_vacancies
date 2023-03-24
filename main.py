from jobs_classes import HHVacancy, SJVacancy
from utils import sorting, get_top, collect_jobs


def main():
    input_word = 'python'#input('Введите поисковый запрос:')
    user_input = "SuperJob"#input("Введите сервис подбора вакансий [HH, SuperJob]:")
    input_count = 2#input("Сколько вывести вакансий?")
    input_sorting = 'No'#input("Вы хотите отсортировать вакансии по зп? yes/no")

    if user_input.lower() == "hh":
        vac_1 = collect_jobs(HHVacancy)
        vac_1.get_vacancies_hh(input_word)

        if input_sorting.lower() == "yes":
            get_top(sorting(HHVacancy.hh_vacancies), input_count)
            print(f'{vac_1.get_count_of_vacancy} - количество вакансий от HH')
        if input_sorting.lower() == "no":
            get_top(HHVacancy.hh_vacancies, input_count)
            print(f'{vac_1.get_count_of_vacancy} - количество вакансий от HH')

    if user_input.lower() == "superjob":
        vac_2 = collect_jobs(SJVacancy)
        vac_2.get_vacancies_sj(input_word)

        if input_sorting.lower() == "yes":
            get_top(sorting(SJVacancy.sj_vacancies), input_count)
            print(f'{vac_2.get_count_of_vacancy} - количество вакансий от SuperJob')
        if input_sorting.lower() == "no":
            get_top(SJVacancy.sj_vacancies, input_count)
            print(f'{vac_2.get_count_of_vacancy} - количество вакансий от SuperJob')


if __name__ == '__main__':
    main()

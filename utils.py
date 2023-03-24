def get_description_hh(data: dict) -> str:
    """
    Возвращает отформантированное описание вакансии из HH
    """
    description = ''
    if data['snippet']['requirement'] is not None:
        description += data['snippet']['requirement']
    if data['snippet']['responsibility'] is not None:
        description += '\n' + data['snippet']['responsibility']
    return description.replace('<highlighttext>', '').replace('</highlighttext>', '')


def get_description_sj(data: dict) -> str:
    """
    Возвращает отформантированное описание вакансии из SJ
    """

    description = ''
    if data['candidat'] is not None:
        description += data['candidat']
    else:
        description += 'Не указано'
    return description


def get_salary(salary):
    """
    Возвращает отформантированную заработную плату
    """
    if salary:
        if salary[0] and salary[1]:
            return f"{salary[0]}-{salary[1]}руб"
        elif salary[0]:
            return f"от {salary[0]}руб"
        elif salary[1]:
            return f"до {salary[1]}руб"
    return 0


def collect_jobs(class_source):
    vacancy = class_source(source=None, name=None, link=None, description=None, salary=None, city=None)
    return vacancy


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    def extract_salary(vacancy):
        salary_range = str(vacancy['salary'])
        if '-' in salary_range:
            salary_range = salary_range.split('-')
            salary_num = max((int(salary_range[0].replace('руб', '').replace(' ', '')),
                              int(salary_range[1].replace('руб', '').replace(' ', ''))))
        elif 'от' in salary_range:
            salary_num = int(salary_range.replace('от ', '').replace('руб', '').replace(' ', ''))
        else:
            salary_num = int(salary_range.replace('до ', '').replace('руб', '').replace(' ', ''))
        return salary_num

    sorted_vacancies = sorted(vacancies, key=extract_salary, reverse=True)
    return sorted_vacancies


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    try:
        for i in range(top_count):
            print(vacancies[i])
    except IndexError:
        print(f'Нет {top_count} записей вакансий')



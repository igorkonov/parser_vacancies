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


def get_salary_hh(salary: dict) -> int | str:
    """
    Возвращает отформантированную заработную плату вакансии из HH
    """
    if salary["salary"] is None or salary["salary"]["from"] is None:
        return 'не указана'
    else:
        salary_from = f'от {salary["salary"]["from"]}'
    if salary["salary"] is None or salary["salary"]["to"] is None:
        return 'не указана'
    else:
        salary_to = f' до {salary["salary"]["to"]}'
    return f'{salary_from}{salary_to}({salary["salary"]["currency"]})'


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


def get_salary_sj(salary: dict) -> int | str:
    """
    Возвращает отформантированную заработную плату вакансии из SJ
    """
    if salary["payment_from"] is None:
        return 'не указана'
    else:
        salary_from = f'от {salary["payment_from"]}'
    if salary["payment_to"] is None:
        return 'не указана'
    else:
        salary_to = f' до {salary["payment_to"]}'
    return f'{salary_from}{salary_to}({salary["currency"]})'

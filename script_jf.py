import requests
from salary_counter import get_average_salary

SUPERJOB_TOWN = 4
SUPERJOB_CATALOGUES = 48
SUPERJOB_COUNT = 100


def get_vacancies(language, token, page=0):
    headers = {'X-Api-App-Id': token}
    params = {'town': SUPERJOB_TOWN, 'catalogues': SUPERJOB_CATALOGUES,
              'page': page,
              'keyword': '{}'.format(language), 'count': SUPERJOB_COUNT}
    response = requests.get(
        'https://api.superjob.ru/2.0/vacancies/',
        headers=headers,
        params=params).json()
    vacancies = {'objects': response['objects'], 'total': response['total']}
    return vacancies


def get_all_vacancies(languages, token):
    all_vacancies = {}
    vacancies_objects = []
    page_number = 0
    for language in languages:
        while True:
            vacancies = get_vacancies(language, token, page_number)
            if not vacancies['objects']:
                break
            for vacancy in vacancies['objects']:
                vacancies_objects.append(vacancy)
            page_number += 1
        all_vacancies[language] = (vacancies_objects, vacancies['total'])
    return all_vacancies


def get_avarage_salary(vacancies):
    nonempty_salary = 0
    salary_count = 0
    for vacancie in vacancies:
        avarage_salary = get_average_salary(
            vacancie['payment_from'],
            vacancie['payment_to'])
        if avarage_salary:
            nonempty_salary += avarage_salary
            salary_count += 1
    return (nonempty_salary, salary_count)


def calculation_jf_statistic_salary(all_vacancies):
    avarage_stattistic = {}
    for language, language_vacancies in all_vacancies.items():
        vacancies = language_vacancies[0]
        salaries = get_avarage_salary(vacancies)
        if salaries[1]:
            avarage_salary = int(salaries[0]/salaries[1])
        else:
            avarage_salary = 0
        count = salaries[1]
        amount = language_vacancies[1]
        avarage_stattistic[language] = {
            "vacancies_found": amount,
            "vacancies_processed": count,
            "average_salary": avarage_salary,
        }
    return avarage_stattistic


def get_jf_statistic_salary(token):
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    all_vacancies = get_all_vacancies(languages, token)
    avarage_stattistic = calculation_jf_statistic_salary(all_vacancies)
    return avarage_stattistic

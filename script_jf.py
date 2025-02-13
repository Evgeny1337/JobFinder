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
    api_response = requests.get(
        'https://api.superjob.ru/2.0/vacancies/',
        headers=headers,
        params=params)
    api_response.raise_for_status()
    response = api_response.json()
    vacancies = {'objects': response['objects'], 'total': response['total']}
    return vacancies


def get_all_vacancies(languages, token):
    all_vacancies = {}
    page_number = 0
    for language in languages:
        vacancies_list = []
        while True:
            vacancies = get_vacancies(language, token, page_number)
            if not vacancies['objects']:
                break
            vacancies_list.extend(vacancies['objects'])
            page_number += 1
        all_vacancies[language] = (vacancies_list, vacancies['total'])
    return all_vacancies


def get_avarage_salary(vacancies):
    nonempty_salary = []
    for vacancie in vacancies:
        avarage_salary = get_average_salary(
            vacancie['payment_from'],
            vacancie['payment_to'])
        if avarage_salary:
            nonempty_salary.append(avarage_salary)
    return nonempty_salary


def get_jf_statistic_salary(token):
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    all_vacancies = get_all_vacancies(languages, token)
    avarage_stattistic = {}
    for language, (vacancies, total) in all_vacancies.items():
        salaries = get_avarage_salary(vacancies)
        count = len(salaries)
        average_salary = int(sum(salaries) / count) if count else 0
        avarage_stattistic[language] = {
            "found": total,
            "processed": count,
            "salary": average_salary,
        }
    return avarage_stattistic

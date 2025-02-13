import requests
import time
from salary_counter import get_average_salary

HH_AREA = 113
HH_PROFESSIONAL_ROLE = 96
HH_PURE_PAGE = 100


def get_vacancies(language, page=0):
    params = {'text': 'Программист {}'.format(language),
              'area': HH_AREA,
              'professional_role': HH_PROFESSIONAL_ROLE,
              'currency': 'RUR', 'page': page, 'per_page': HH_PURE_PAGE}
    api_response = requests.get('https://api.hh.ru/vacancies', params=params)
    api_response.raise_for_status()
    response = api_response.json()
    vacancies = {'items': response['items'],
                 'pages': response['pages'],
                 'found': response['found']}
    return vacancies


def get_all_vacancies(languages):
    all_vacancies = {}
    for language in languages:
        page = 0
        vacancies = []
        while True:
            language_vacancies = get_vacancies(language, page)
            vacancies.extend(language_vacancies['items'])
            if page >= language_vacancies['pages'] - 1:
                all_vacancies[language] = (vacancies, language_vacancies['found'])
                break
            page += 1
            time.sleep(2)
    return all_vacancies


def predict_rub_salaries(vacancy):
    salary = vacancy['salary']
    if salary:
        salary = get_average_salary(salary['from'], salary['to'])
        return salary
    return None


def get_hh_statistic_salary():
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    all_vacancies = get_all_vacancies(languages)
    avarage_salary = {}
    for language, (vacancies, count) in all_vacancies.items():
        salaries_sum = 0
        nonempty_count = 0
        for vacancy in vacancies:
            salary = predict_rub_salaries(vacancy)
            if salary:
                salaries_sum += salary
                nonempty_count += 1 
        average_salary = int(salaries_sum / max(1, len(vacancies)))
        avarage_salary[language] = {"found": count,
                                    "processed": nonempty_count,
                                    "salary": average_salary}
    return avarage_salary




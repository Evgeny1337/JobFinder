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
    json_response = requests.get('https://api.hh.ru/vacancies', params=params)
    response = json_response.json()
    vacancies = {'items': response['items'],
                 'pages': response['pages'],
                 'found': response['found']}
    return vacancies


def get_all_vacancies(languages):
    all_vacancies = {}
    vacancies = []
    for language in languages:
        page = 0
        while True:
            language_vacancies = get_vacancies(language, page)
            for vacancy in language_vacancies['items']:
                vacancies.append(vacancy)
            if page >= language_vacancies['pages'] - 1 or page > 5:
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


def calculation_hh_statistic_salary(all_vacancies):
    avarage_salary = {}
    for language, language_vacancies in all_vacancies.items():
        count = language_vacancies[1]
        salaries = 0
        nonempty_count = 0
        for vacancy in language_vacancies[0]:
            predict_salary = predict_rub_salaries(vacancy)
            if predict_salary:
                salaries += predict_salary
                nonempty_count += 1 
        average_salary = 0 if nonempty_count <= 0 else int(salaries / len(language_vacancies[0]))
        avarage_salary[language] = {"vacancies_found": count,
                                    "vacancies_processed": nonempty_count,
                                    "average_salary": average_salary}
    return avarage_salary


def get_hh_statistic_salary():
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    all_vacancies = get_all_vacancies(languages)
    avarage_salary = calculation_hh_statistic_salary(all_vacancies)
    return avarage_salary

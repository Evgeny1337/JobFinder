import requests
import time
from salary_counter import get_average_salary
from requests.adapters import HTTPAdapter, Retry


def get_vacancies(area, professional_role, language, page=0):
    params = {'text': 'Программист {}'.format(language),
              'area': area,
              'professional_role': professional_role,
              'currency': 'RUR', 'page': page, 'per_page': 100}
    json_response = requests.get('https://api.hh.ru/vacancies', params=params)
    response = json_response.json()
    return {'items': response['items'],
            'pages': response['pages'],
            'found': response['found']}


def get_all_vacancies(languages, area, professional_role):
    all_vacancies = {}
    for language in languages:
        page = 0
        all_vacancies[language] = []
        while True:
            # print(page)
            language_vacancies = get_vacancies(
                area, professional_role, language, page)
            try:
                k = language_vacancies['pages']
            except:
                print(language_vacancies)
            all_vacancies[language].append(language_vacancies)
            if page >= language_vacancies['pages'] - 1:
                break
            page += 1
            print(f'{page}/{language_vacancies["pages"]}')
            time.sleep(2)
    return all_vacancies


def predict_rub_salaries(vacancies):
    predict_salaries_result = []
    language_vacancies = vacancies['items']
    for vacancy in language_vacancies:
        salary = vacancy['salary']
        if salary:
            salary = get_average_salary(salary['from'], salary['to'])
        predict_salaries_result.append(salary)
    return predict_salaries_result


def get_hh_statistic_salary(area=113, professional_role=96):
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    avarage_salary_result = {}
    all_vacancies = get_all_vacancies(
        languages,
        area,
        professional_role
    )
    for language, language_vacancies in all_vacancies.items():
        count = language_vacancies[0]['found']
        nonempty_salaries = []
        for vacancies in language_vacancies:
            salaries = [salary for salary in predict_rub_salaries(
                vacancies) if salary]
            nonempty_salaries += salaries
        nonempty_count = len(nonempty_salaries)
        average_salary = 0 if nonempty_count <= 0 else int(
            sum(nonempty_salaries) /
            len(nonempty_salaries)
        )
        avarage_salary_result[language] = {"vacancies_found": count,
                                           "vacancies_processed": nonempty_count,
                                           "average_salary": average_salary}
    return avarage_salary_result


def main():
    avarage_salarys = get_hh_statistic_salary()
    print(avarage_salarys)


if __name__ == '__main__':
    main()

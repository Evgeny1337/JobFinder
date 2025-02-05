import requests
import time
from salary_counter import counte_salary


def get_vacancies(area, professional_role, language, page=0):
    params = {'text': 'Программист {}'.format(language),
              'area': area,
              'professional_role': professional_role,
              'currency': 'RUR', 'page': page}
    json_response = requests.get('https://api.hh.ru/vacancies', params=params)
    response = json_response.json()
    return response


def get_pagecount(json):
    return json['pages']


def get_all_vacancies(languages, pages_number, area, professional_role):
    all_vacancies = {}
    for language in languages:
        page = 0
        all_vacancies[language] = []
        language_vacancies = get_vacancies(
            area, professional_role, language, page)
        page_count = get_pagecount(language_vacancies)
        if page_count > 10:
            page_count = 10
        while page < page_count:
            all_vacancies[language].append(get_vacancies(
                area, professional_role, language, page))
            time.sleep(2)
            page += 1
    return all_vacancies


def predict_rub_salary(vacancies):
    predict_salary_result = []
    language_vacancies = vacancies['items']
    for json_item in language_vacancies:
        salary = json_item['salary']
        if salary:
            salary = counte_salary(salary['from'], salary['to'])
        predict_salary_result.append(salary)
    return predict_salary_result


def get_hh_statistic_salary(area=113, professional_role=96, pages_number=5):
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    avarage_salary_result = {}
    all_vacancies = get_all_vacancies(
        languages,
        pages_number,
        area,
        professional_role
    )
    for language, language_vacancies in all_vacancies.items():
        count = language_vacancies[0]['found']
        nonempty_salaries = []
        for vacancies in language_vacancies:
            salaries = [salary for salary in predict_rub_salary(
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

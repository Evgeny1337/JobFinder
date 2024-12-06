import requests
import json


def salary_counter(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to)/2
    elif salary_from and not salary_to:
        return salary_from * 1.2
    return salary_to * 0.8


def get_vacancies(area, professional_role, language, page=0):
    params = {'text': 'Программист {}'.format(
        language), 'area': area, 'professional_role': professional_role,  'currency': 'RUR', 'page': page}
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    json_response = response.json()
    return json_response


def get_all_vacancies(languages, pages_number, area, professional_role):
    all_vacancies = {}
    for language in languages:
        page = 0
        all_vacancies[language] = []
        while page < pages_number:
            all_vacancies[language].append(get_vacancies(
                area, professional_role, language, page))
            page += 1
    return all_vacancies


def predict_rub_salary(vacancies):
    score_result = []
    for json_item in vacancies['items']:
        salary = json_item['salary']
        if salary:
            salary = salary_counter(salary['from'], salary['to'])
        score_result.append(salary)
    return score_result


def get_average_salary(area, professional_role, languages, pages_number):
    avarage_result = {}
    all_vacancies = get_all_vacancies(
        languages, pages_number, area, professional_role)
    for language in languages:
        language_vacancies = all_vacancies[language]
        count = language_vacancies[0]['found']
        nonempty_salarys = []
        for vacancies in language_vacancies:
            salarys = [salary for salary in predict_rub_salary(
                vacancies) if salary != None]
            nonempty_salarys += salarys
        nonempty_count = len(nonempty_salarys)
        avarage_result[language] = {"vacancies_found": count, "vacancies_processed": nonempty_count, "average_salary": int(
            sum(nonempty_salarys)/len(nonempty_salarys))}
    return avarage_result


def main():
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    avarage_salarys = get_average_salary(113, 96, languages, 5)
    print(avarage_salarys)


if __name__ == '__main__':
    main()

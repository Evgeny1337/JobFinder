import requests
import time


def salary_counter(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to)/2
    elif salary_from and not salary_to:
        return salary_from * 1.2
    return salary_to * 0.8


def get_vacancies(area, professional_role, language, page=0):
    params = {'text': 'Программист {}'.format(language),
              'area': area,
              'professional_role': professional_role,
              'currency': 'RUR', 'page': page}
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    json_response = response.json()
    return json_response


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
            time.sleep(10)
            page += 1
            print('Язык {} {}/{}'.format(language, page, page_count))
    return all_vacancies


def predict_rub_salary(vacancies):
    score_result = []
    language_vacancies = vacancies['items']
    for json_item in language_vacancies:
        salary = json_item['salary']
        if salary:
            salary = salary_counter(salary['from'], salary['to'])
        score_result.append(salary)
    return score_result


def get_statistic_salary(area=113, professional_role=96, pages_number=5):
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    avarage_result = {}
    all_vacancies = get_all_vacancies(
        languages,
        pages_number,
        area,
        professional_role
    )
    for language in languages:
        language_vacancies = all_vacancies[language]
        count = language_vacancies[0]['found']
        nonempty_salaries = []
        for vacancies in language_vacancies:
            salaries = [salary for salary in predict_rub_salary(
                vacancies) if salary]
            nonempty_salaries += salaries
        nonempty_count = len(nonempty_salaries)
        avarage_result[language] = {"vacancies_found": count,
                                    "vacancies_processed": nonempty_count,
                                    "average_salary": int(sum(nonempty_salaries)/len(nonempty_salaries))}
    return avarage_result


def main():
    avarage_salarys = get_statistic_salary()
    print(avarage_salarys)


if __name__ == '__main__':
    main()

import requests
from dotenv import load_dotenv
from os import environ
from salary_counter import counte_salary

SUPERJOB_TOWN = 4
SUPERJOB_CATALOGUES = 48


def get_vacancies(language, token):
    headers = {'X-Api-App-Id': token}
    params = {'town': SUPERJOB_TOWN, 'catalogues': SUPERJOB_CATALOGUES,
              'keyword': '{}'.format(language), 'count': 100}
    response = requests.get(
        'https://api.superjob.ru/2.0/vacancies/',
        headers=headers,
        params=params)
    return response


def get_all_vacancies(languages, token):
    all_vacancies = {}
    for language in languages:
        response = get_vacancies(language, token)
        all_vacancies[language] = response.json()
    return all_vacancies


def get_avarage_salary(vacancies):
    avarage_salaries = []
    for vacancie in vacancies:
        avarage_salaries.append(counte_salary(
            vacancie['payment_from'],
            vacancie['payment_to']))
    nonempty_salary = [salary for salary in avarage_salaries if salary]
    return nonempty_salary


def get_jf_statistic_salary(token):
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    avarage_stattistic = {}
    all_vacancies = get_all_vacancies(languages, token)
    for language, language_vacancies in all_vacancies.items():
        vacancies = language_vacancies['objects']
        salaries = get_avarage_salary(vacancies)
        if sum(salaries) > 0:
            avarage_salary = int(sum(salaries)/len(salaries))
        else:
            avarage_salary = 0
        count = len(salaries)
        amount = language_vacancies['total']
        avarage_stattistic[language] = {
            "vacancies_found": amount,
            "vacancies_processed": count,
            "average_salary": avarage_salary}
    return avarage_stattistic


def main():
    load_dotenv()
    token = environ['SUPERJOB_TOKEN']
    print(get_jf_statistic_salary(token))


if __name__ == '__main__':
    main()

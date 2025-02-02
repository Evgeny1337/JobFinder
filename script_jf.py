import requests
from dotenv import load_dotenv
from os import environ

SUPERJOB_TOWN = 4
SUPERJOB_CATALOGUES = 48


def predict_rub_salary_for_superJob(vacancie):
    if vacancie['payment_from'] and vacancie['payment_to']:
        return (vacancie['payment_from'] + vacancie['payment_to'])/2
    elif vacancie['payment_from'] and not vacancie['payment_to']:
        return vacancie['payment_from'] * 1.2
    elif not vacancie['payment_from'] and vacancie['payment_to']:
        return vacancie['payment_to'] * 0.8
    return None


def get_vacancies(language, token):
    headers = {'X-Api-App-Id': token}
    params = {'town': SUPERJOB_TOWN, 'catalogues': SUPERJOB_CATALOGUES,
              'keyword': '{}'.format(language), 'count': 100}
    response = requests.get(
        'https://api.superjob.ru/2.0/vacancies/',
        headers=headers,
        params=params)
    return response


def get_all_vacancies(languages):
    token = environ['SUPERJOB_TOKEN']
    all_vacancies = {}
    for language in languages:
        response = get_vacancies(language, token)
        all_vacancies[language] = response.json()
    return all_vacancies


def get_avarage_salary(vacancies):
    avarage_salary = []
    for vacancie in vacancies:
        avarage_salary.append(predict_rub_salary_for_superJob(vacancie))
    nonempty_salary = [salary for salary in avarage_salary if salary]
    return nonempty_salary


def get_statistic_salary():
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    avarage_stattistic = {}
    all_vacancies = get_all_vacancies(languages)
    for language in languages:
        vacancies = all_vacancies[language]['objects']
        salaries = get_avarage_salary(vacancies)
        if sum(salaries) > 0:
            avarage_salary = int(sum(salaries)/len(salaries))
        else:
            avarage_salary = 0
        # avarage_salary = int(sum(salaries)/len(salaries)
        #                      ) if sum(salaries) > 0 else 0
        count = len(salaries)
        amount = all_vacancies[language]['total']
        avarage_stattistic[language] = {
            "vacancies_found": amount,
            "vacancies_processed": count,
            "average_salary": avarage_salary}
    return avarage_stattistic


def main():
    load_dotenv()
    print(get_statistic_salary())


if __name__ == '__main__':
    main()

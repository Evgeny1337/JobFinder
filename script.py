import requests


# def get_vacancies_count(area, professional_role, period, languages):
#     score_result = {}
#     for language in languages:
#         params = {'text': 'Программист {}'.format(
#             language), 'area': area, 'professional_role': professional_role, 'period': period}
#         response = requests.get('https://api.hh.ru/vacancies', params=params)
#         json_response = response.json()
#         score_result[language] = json_response['found']
#     return score_result


# def get_salary(area, professional_role, period, language):
#     params = {'text': 'Программист {}'.format(
#         language), 'area': area, 'professional_role': professional_role, 'period': period, 'clasters': True}
#     response = requests.get('https://api.hh.ru/vacancies', params=params)
#     json_response = response.json()
#     return [salary['salary'] for salary in json_response['items']]


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


def predict_rub_salary(area, professional_role, language, page):
    json_response = get_vacancies(area, professional_role, language, page)
    score_result = []
    for json_item in json_response['items']:
        salary = json_item['salary']
        if salary:
            salary = salary_counter(salary['from'], salary['to'])
        score_result.append(salary)
    return score_result


def get_average_salary(area, professional_role, languages):
    avarage_result = {}
    for language in languages:
        pages_number = 5
        page = 0
        vacancies_count = 0
        nonempty_salary = []
        nonempty_count = 0
        while page < pages_number:
            vacancies_count += get_vacancies(
                area, professional_role, language, page)['found']
            all_salary = predict_rub_salary(area, professional_role, language)
            nonempty_salary += [salary for salary in all_salary if salary != None]
            page += 1
        nonempty_count += len(nonempty_salary)
        avarage_salary = int(sum(nonempty_salary)/len(nonempty_salary))
        avarage_result[language] = {"vacancies_found": vacancies_count,
                                    "vacancies_processed": nonempty_count, "average_salary": avarage_salary}
    return avarage_result
    # empty_salary_count = all_salary.count(None)


def main():
    languages = ['JavaScript', 'Java', 'Python', 'Ruby',
                 'PHP', 'C++', 'C#', 'C', 'Go', 'Objective-C']
    # print(get_vacancies_count(113,96,30))
    print(get_average_salary(113, 96, languages))
    # print(predict_rub_salary(113, 96, languages[3]))


if __name__ == '__main__':
    main()

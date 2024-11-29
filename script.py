import requests

def get_vacancies_count(area,professional_role,period):
    languages=['JavaScript','Java','Python','Ruby','PHP','C++','C#','C','Go','Objective-C']
    score_result = {}
    for language in languages:
        params={'text':'Программист {}'.format(language),'area':area,'professional_role':professional_role,'period':period}
        response = requests.get('https://api.hh.ru/vacancies',params=params)
        json_response = response.json()
        score_result[language] = json_response['found']
    return score_result

def get_salary(area,professional_role,period,language):
    params = {'text':'Программист {}'.format(language),'area':area,'professional_role':professional_role,'period':period,'clasters':True}
    response = requests.get('https://api.hh.ru/vacancies',params=params)
    json_response = response.json()
    return [salary['salary'] for salary in json_response['items']]

def salary_counter(salary_from,salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to)/2
    elif salary_from and not salary_to:
        return salary_from * 1.2
    return salary_to * 0.8

def predict_rub_salary(area,professional_role,language):
    params = {'text':'Программист {}'.format(language),'area':area,'professional_role':professional_role,'clasters':True,'currency':'RUR'}
    response = requests.get('https://api.hh.ru/vacancies',params=params)
    json_response = response.json()
    score_result = []
    for json_item in json_response['items']:
        salary = json_item['salary']
        if salary:
            salary = salary_counter(salary['from'],salary['to'])
        score_result.append(salary)
    return score_result

def get_average_salary():



def main():
    # print(get_vacancies_count(113,96,30))
    print(predict_rub_salary(113,96,'Python'))

if __name__ == '__main__':
    main()
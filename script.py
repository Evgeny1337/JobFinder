from dotenv import load_dotenv
from script_hh import get_hh_statistic_salary
from script_jf import get_jf_statistic_salary
from terminaltables import AsciiTable
from os import environ


def main():
    load_dotenv()
    token = environ['SUPERJOB_TOKEN']
    header = [[' Язык программирования ', 'Вакансий найдено',
              'Вакансий обработано', 'Средняя зарплата']]
    hh_avarage_salary = get_hh_statistic_salary().items()
    superjob_avarage_salary = get_jf_statistic_salary(token).items()
    hh_salaries = header + [[key] + list(value.values())
                            for key, value in hh_avarage_salary]
    jf_salaries = header + [[key] + list(value.values())
                            for key, value in superjob_avarage_salary]

    table_hh = AsciiTable(hh_salaries, 'HeadHunter Moscow')
    table_hh.justify_columns[2] = 'right'

    table_jf = AsciiTable(jf_salaries, 'SuperJob Moscow')
    table_jf.justify_columns[2] = 'right'

    print(table_hh.table)
    print(table_jf.table)


if __name__ == '__main__':
    main()

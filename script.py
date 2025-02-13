from dotenv import load_dotenv
from script_hh import get_hh_statistic_salary
from script_jf import get_jf_statistic_salary
from terminaltables import AsciiTable
from os import environ

def create_table(salaries_statistic, title):
    header = [[' Язык программирования ', 'Вакансий найдено',
              'Вакансий обработано', 'Средняя зарплата']]
    table_data = header + [[language] + list(statistic.values())
                            for language, statistic in salaries_statistic]
    table = AsciiTable(table_data,title)
    table.justify_columns[2] = 'right'
    return table

def main():
    load_dotenv()
    token = environ['SUPERJOB_TOKEN']
    hh_salaries_statistic = get_hh_statistic_salary().items()
    superjob_salaries_statistic = get_jf_statistic_salary(token).items()
    table_hh = create_table(hh_salaries_statistic, 'HeadHunter Moscow')
    table_jf = create_table(superjob_salaries_statistic, 'SuperJob Moscow')
    print(table_hh.table)
    print(table_jf.table)


if __name__ == '__main__':
    main()

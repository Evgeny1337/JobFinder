from dotenv import load_dotenv
from script_hh import get_statistic_salary as hh_statistic
from script_jf import get_statistic_salary as jf_statistic
from terminaltables import AsciiTable


def main():
    load_dotenv()

    header = [[' Язык программирования ', 'Вакансий найдено',
              'Вакансий обработано', 'Средняя зарплата']]
    hh_avarage_salary = hh_statistic().items()
    superjob_avarage_salary = jf_statistic().items()
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

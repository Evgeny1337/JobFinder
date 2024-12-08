from dotenv import load_dotenv
from script_hh import get_statistic_salary as hh_statistic
from script_jf import get_statistic_salary as jf_statistic
from terminaltables import AsciiTable, DoubleTable, SingleTable


def main():
    load_dotenv()

    header = [[' Язык программирования ', 'Вакансий найдено',
              'Вакансий обработано', 'Средняя зарплата']]

    hh_salarys = header + [[key] + list(value.values())
                           for key, value in hh_statistic(113, 96, 5).items()]
    jf_salarys = header + [[key] + list(value.values())
                           for key, value in jf_statistic().items()]

    table_hh = AsciiTable(hh_salarys, 'HeadHunter Moscow')
    table_hh.justify_columns[2] = 'right'

    table_jf = AsciiTable(jf_salarys, 'SuperJob Moscow')
    table_jf.justify_columns[2] = 'right'

    print(table_hh.table)
    print(table_jf.table)


if __name__ == '__main__':
    main()

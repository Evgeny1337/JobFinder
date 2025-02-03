def counte_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to)/2
    elif salary_from and not salary_to:
        return salary_from * 1.2
    return salary_to * 0.8

import calendar


def get_weekdays_per_month (day, month):
    year = 2024
    month = 3
    day_to_count = day - 1

    matrix = calendar.monthcalendar(year,month)
    print (matrix)
    num_days = sum(1 for x in matrix if x[day_to_count] != 0)
    return 1, 1
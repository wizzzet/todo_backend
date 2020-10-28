import datetime

from django.conf import settings

from xlrd import xldate_as_tuple


def get_month_name(month):
    months = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь'
    }
    return months.get(month, '')


def get_month_num(month):
    months = {
        'Январь': 1,
        'Февраль': 2,
        'Март': 3,
        'Апрель': 4,
        'Май': 5,
        'Июнь': 6,
        'Июль': 7,
        'Август': 8,
        'Сентябрь': 9,
        'Октябрь': 10,
        'Ноябрь': 11,
        'Декабрь': 12
    }
    return months.get(month, '')


_days_of_week = (
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
)


def monthrange(start_date, end_date):
    data = []
    start_year = start_date.year
    end_year = end_date.year

    for month in range(
        start_date.month,
        end_date.month + 1 if start_year == end_year else 13
    ):
        data.append((month, start_year))

    for year in range(start_year + 1, end_year):
        for month in range(1, 13):
            data.append((month, year))

    if start_year < end_year:
        for month in range(1, end_date.month + 1):
            data.append((month, end_year))

    return data


def parse_excel_date(value):
    if not value:
        return None

    if isinstance(value, (int, float)):
        try:
            return datetime.date(*xldate_as_tuple(value, 0)[0:3])
        except ValueError:
            pass

    formats = settings.DATE_INPUT_FORMATS if settings.DATE_INPUT_FORMATS else ('%Y-%m-%d',)
    for _format in formats:
        try:
            return datetime.datetime.strptime(value, _format).date()
        except (ValueError, TypeError):
            continue

    return None


def first_day_of_week(day):
    return day - datetime.timedelta(days=day.weekday())


def last_day_of_week(day):
    return day + datetime.timedelta(days=6 - day.weekday())

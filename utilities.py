"""Различные полезные функции."""

import hashlib
from datetime import datetime #  ,  date

import datetime as dt

COMMON_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
COMMON_DATE_FORMAT = "%Y-%m-%d"
RUSSIAN_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"
RUSSIAN_DATE_FORMAT = "%d.%m.%Y"


def create_md5(ps_line, ps_salt):
    """Возвращает хэш заданной строки.
    >>> create_md5("1234567890", None)
    'e807f1fcf82d132f9bb018ca6738a19f'
    >>> create_md5("1234567890", "0987654321")
    '4a8a2b374f463b7aedbb44a066363b81'
    """
    assert ps_line is not None, ("Assert: [utilities:create_md5]: No <ps_line> parameter specified!")

    if ps_salt is not None:

        return hashlib.md5(bytes(ps_line + ps_salt, "ANSI")).hexdigest()
    return hashlib.md5(bytes(ps_line, "ANSI")).hexdigest()


def date2datestring(pdate, pformat=COMMON_DATETIME_FORMAT):
    """Преобразовывает дату в строковое представление даты.
    >>> date2datestring(datetime(2020, 12, 31, 23, 59, 59), COMMON_DATETIME_FORMAT)
    '2020-12-31 23:59:59'
    """
    return pdate.strftime(pformat)


def datestring2date(pdatestring, pformat=COMMON_DATETIME_FORMAT):
    """Преобразовывает дату в строке в дату.
    >>> datestring2date('31.12.2020', RUSSIAN_DATE_FORMAT)
    datetime.datetime(2020, 12, 31, 0, 0)
    >>> datestring2date('2020-12-31 23:59:59', COMMON_DATETIME_FORMAT)
    datetime.datetime(2020, 12, 31, 23, 59, 59)
    >>> datestring2date('2020-20-31 23:59:59', COMMON_DATETIME_FORMAT) is None
    True
    """
    try:

        return datetime.strptime(pdatestring, pformat)
    except ValueError:

        return None


def datetime2date(pdatetime):
    """Конвертит дату со временем в дату.
    >>> datetime2date(datetime(2020, 12, 31, 23, 59, 59))
    datetime.date(2020, 12, 31)
    >>> datetime2date(datetime(2020, 12, 31))
    datetime.date(2020, 12, 31)
    """

    if is_datetime(pdatetime):

        return pdatetime.date()
    return pdatetime


def is_datetime(pdate):
    """Определяет, является ли параметр датой со временем.
    >>> is_datetime(datetime(2020, 12, 31, 23, 59, 59))
    True
    >>> is_datetime(datetime(2020, 12, 31).date())
    False
    """
    return type(pdate) is datetime


def is_string_empty(ps_line):
    """Возвращает True, если строка содержит None либо пустую строку.
    >>> is_string_empty("")
    True
    >>> is_string_empty(None)
    True
    >>> is_string_empty("Однажды, в студёную зимнюю пору")
    False
    """
    return (ps_line is None) or not bool(str(ps_line)) or not bool(str(ps_line.strip()))


def is_date_in_range(pdatefrom, pdateto, ptestingdate):
    """Производит валидацию даты в заданном диапазоне.
    >>> is_date_in_range( datetime(2020, 12, 1, 0, 0), datetime(2020, 12, 31, 0, 0), datetime(2019, 12, 31, 0, 0))  # doctest: +ELLIPSIS
    (False, ...)
    >>> is_date_in_range( datetime(2020, 12, 1, 0, 0), datetime(2020, 12, 31, 0, 0), datetime(2020, 12, 1, 0, 0))  # doctest: +ELLIPSIS
    (True, '')
    >>> is_date_in_range( datetime(2020, 12, 1, 0, 0), datetime(2020, 12, 31, 0, 0), datetime(2021, 1, 1, 0, 0))  # doctest: +ELLIPSIS
    (False, ...)
    """
    assert pdatefrom is not None, ("Assert: [tpylib:utilities:is_date_in_range]: No <plowlimitdate> parameter specified!")
    assert pdateto is not None, ("Assert: [tpylib:utilities:is_date_in_range]: No <pdateto> parameter specified!")
    assert ptestingdate is not None, ("Assert: [tpylib:utilities:is_date_in_range]: No <pdt_date> parameter specified!")

    if datetime2date(ptestingdate) < datetime2date(pdatefrom):

        return False, "Ошибка: дата должна быть больше или равна " + date2datestring(pdatefrom, RUSSIAN_DATE_FORMAT)

    if datetime2date(ptestingdate) > datetime2date(pdateto):

        return False, "Ошибка: дата должна быть меньше или равна " + date2datestring(pdateto, RUSSIAN_DATE_FORMAT)
    return True, ""


def shift_date(pdate, pdays):
    """Смещает дату на заданный интервал.
    >>> shift_date(dt.date(2021, 1, 1), 31)
    datetime.date(2021, 2, 1)"""
    time_delta = dt.timedelta(days=pdays)
    return pdate+time_delta


def split_line_ex(ps_input_line, po_lengths):
    """Разбивает строку по заданным длинам.
           >>> split_line_ex("Однажды в студёную зимнюю пору сижу за решеткой в темнице сырой", (8, 2, 9, 7, 5))  # doctest: +ELLIPSIS
           ['Однажды ', 'в ', 'студёную ', 'зимнюю ', 'пору ', ...]
          """
    lo_result = list()
    li_shift = 0
    for flen in po_lengths:

        lo_result.append(ps_input_line[li_shift:li_shift + flen])
        li_shift += flen
    lo_result.append(ps_input_line[li_shift:])
    return lo_result

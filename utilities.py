"""Различные полезные функции."""

import hashlib
from datetime import datetime #  ,  date

RUSSIAN_DATETIME_FORMAT  = "%d.%m.%Y %H:%M:%S"
RUSSIAN_DATE_FORMAT  = "%d.%m.%Y"
COMMON_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
COMMON_DATE_FORMAT = "%Y-%m-%d"


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
    else:

        return hashlib.md5(bytes(ps_line, "ANSI")).hexdigest()


def date2datestring(pdate,  pformat = COMMON_DATETIME_FORMAT):
    """Преобразовывает дату в строковое представление даты.
    >>> date2datestring(datetime(2020, 12, 31, 23, 59, 59), COMMON_DATETIME_FORMAT)
    '2020-12-31 23:59:59'
    """
    return pdate.strftime(pformat)


def datestring2date(pdatestring,  pformat = COMMON_DATETIME_FORMAT):
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




def date_check_and_convert(ps_date):
    """Проверяет корректность строковой даты и конвертит собственно в тип date.
    >>> date_check_and_convert("2020-12-31")
    (datetime.datetime(2020, 12, 31, 0, 0), '')
    >>> date_check_and_convert("2020-12-") # doctest: +ELLIPSIS
    (None, ...)
    """
    assert ps_date is not None, ("Assert: [utilities:date_check_and_convert]: No <ps_date> parameter specified!")

    try:

        return datetime.strptime(ps_date, '%Y-%m-%d'), ""  # noqa
    except ValueError:

        return None, "Ошибка: Дата введена неверно, перепроверьте дату."


def is_date_between_limits(plowlimitdate, phighlimitdate, ptestingdate):
    """Производит валидацию даты в заданном диапазоне.
    >>> is_date_between_limits( datetime(2020, 12, 1, 0, 0), datetime(2020, 12, 31, 0, 0), datetime(2019, 12, 31, 0, 0))  # doctest: +ELLIPSIS
    (False, ...)
    >>> is_date_between_limits( datetime(2020, 12, 1, 0, 0), datetime(2020, 12, 31, 0, 0), datetime(2020, 12, 1, 0, 0))  # doctest: +ELLIPSIS
    (True, '')
    >>> is_date_between_limits( datetime(2020, 12, 1, 0, 0), datetime(2020, 12, 31, 0, 0), datetime(2021, 1, 1, 0, 0))  # doctest: +ELLIPSIS
    (False, ...)
    """
    assert plowlimitdate is not None, ("Assert: [tpylib:utilities:is_date_between_limits]: No <plowlimitdate> parameter specified!")
    assert phighlimitdate is not None, ("Assert: [tpylib:utilities:is_date_between_limits]: No <phighlimitdate> parameter specified!")
    assert ptestingdate is not None, ("Assert: [tpylib:utilities:is_date_between_limits]: No <pdt_date> parameter specified!")
   

    #if is_datetime(plowlimitdate) and is_datetime(phighlimitdate) and is_datetime(ptestingdate):
    if datetime2date(ptestingdate) < datetime2date(plowlimitdate):

        return False, "Ошибка: дата должна быть больше, чем " + date2datestring(plowlimitdate,RUSSIAN_DATE_FORMAT)

    elif datetime2date(ptestingdate) > datetime2date(phighlimitdate):

        return False, "Ошибка: дата должна быть меньше или равна " + date2datestring(phighlimitdate,RUSSIAN_DATE_FORMAT)
    return True, ""


def is_date_valid(pdt_date, pdt_date_begin):
    """Проверяет дату на валидность.
    >> is_date_valid( datetime(2020, 12, 31, 0, 0), datetime(2020, 1, 1, 0, 0))  # doctest: +ELLIPSIS
    (False, ...)
    >> is_date_valid( datetime(2020, 12, 1, 0, 0), datetime(2020, 1, 1, 0, 0))  # doctest: +ELLIPSIS
    (False, ...)
    """
    assert pdt_date is not None, ("Assert: [is_date_valid]:"
                                  "No <pdt_date> parameter specified!")

    ldt_date, ls_message = date_check_and_convert(pdt_date)
    if ldt_date is not None:
        
        return is_date_between_limits(pdt_date_begin, datetime.now().date(), ldt_date)
    return False, ls_message


def split_line_ex(ps_input_line, po_lengths):
    """Разбивает строку по заданным длинам."""
    lo_result = list()
    li_shift = 0
    for flen in po_lengths:

        lo_result.append(ps_input_line[li_shift:li_shift + flen])
        li_shift += flen
    lo_result.append(ps_input_line[li_shift:])
    return lo_result

#if __name__ == "__main__":
    #print(datestring2date('31.12.2020', RUSSIAN_DATE_FORMAT))
    #print(datestring2date('2020-20-31 23:59:59', COMMON_DATETIME_FORMAT))
    #print(is_date_between_limits(datetime(2020, 12, 1, 0, 0), datetime(2020, 12, 31, 0, 0), datetime(2020, 12, 31, 0, 0)))
    #d = datestring2date('2020-20-31 23:59:59', COMMON_DATETIME_FORMAT)
#    d = datetime(2020, 12, 31, 23, 59, 59)
#    print(d)
#    print(type(d))
#    if type(d) is datetime:
#        print("************************")
#    if is_date(d):
#        print("++++++++++++++++++++++++++")
#    d = d.date()
#    print(d)
#    print(type(d))
#    if is_date(d):
#        print("++++++++++++++++++++++++++")#

"""Различные полезные функции."""
import hashlib
from datetime import datetime


def create_md5(ps_line, ps_salt):
    """Возвращает хэш заданной строки."""
    assert ps_line is not None, ("Assert: [create_md5]: No <ps_line> parameter specified!")

    if ps_salt is not None:

        return hashlib.md5(bytes(ps_line + ps_salt, "ANSI")).hexdigest()
    else:

        return hashlib.md5(bytes(ps_line, "ANSI")).hexdigest()


def is_string_empty(ps_line):
    """Возвращает True, если строка содержит None либо пустую строку."""
    assert ps_line is not None, ("Assert: [is_empty]: No <ps_line> parameter specified!")

    return (ps_line is None) or not bool(str(ps_line)) or not bool(str(ps_line.strip()))


def date_check_and_convert(ps_date):
    """Проверяет корректность строковой даты и конвертит собственно в тип date."""
    assert ps_date is not None, ("Assert: [date_check_and_convert]: No <ps_date> parameter specified!")

    try:

        return datetime.strptime(ps_date, '%Y-%m-%d'), ""  # noqa
    except ValueError:

        return None, "Ошибка: Дата введена неверно, перепроверьте дату."


def is_date_between_limits(pdt_low_limit, pdt_high_limit, pdt_date):
    """Производит валидацию даты в заданном диапазоне."""
    assert pdt_low_limit is not None, ("Assert: [is_date_between_limits]: No <pdt_low_limit> parameter specified!")
    assert pdt_high_limit is not None, ("Assert: [is_date_between_limits]: No <pdt_high_limit> parameter specified!")
    assert pdt_date is not None, ("Assert: [is_date_between_limits]: No <pdt_date> parameter specified!")

    if pdt_date.date() < pdt_low_limit:

        return False, f"Ошибка: дата должна быть больше, чем {pdt_low_limit:%d.%m.%Y}"

    elif pdt_date.date() > pdt_high_limit:

        return False, f"Ошибка: дата должна быть меньше или равна {pdt_high_limit:%d.%m.%Y}"
    return True, ""


def is_date_valid(pdt_date, pdt_date_begin):
    """Проверяет дату на валидность."""
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

# -*- coding: utf-8 -*-
""" Модуль пагинатора"""

SESSION_CURRENT_FRAME_KEY = "current_frame"
SESSION_CURRENT_PAGE_KEY = "current_page"
FIRST_FRAME_CONTROL = "first_frame"
PREV_FRAME_CONTROL = "prev_frame"
NEXT_FRAME_CONTROL = "next_frame"
LAST_FRAME_CONTROL = "last_frame"
FULL_FRAME_SIZE = 10
FULL_PAGE_SIZE = 25
RECORDS_IN_FULL_FRAME = FULL_FRAME_SIZE * FULL_PAGE_SIZE

def recalc(precords_count):
    """Процедура производит расчёт параметров пагинатора."""
    assert precords_count is not None, ("Assert: [paginator:pager_recalc]: No "
                                        "<precords_count> parameter specified!")

    partial_frame_flag = False
    records_in_partial_frame = 0
    pages_in_partial_frame = 0
    partial_page_flag = False
    records_in_partial_page = 0

    # *** Найдём к-во полных фреймов
    full_frames_total = int(precords_count // RECORDS_IN_FULL_FRAME)
    # li_full_frames_records = (full_frames_total * RECORDS_IN_FULL_FRAME)
    # *** Если к-во записей не делится нацело на к-во записей во фрейме
    if precords_count % RECORDS_IN_FULL_FRAME > 0:
        # *** Добавим неполный фрейм
        partial_frame_flag = True
        # *** Посчитаем, сколько записей будет в последнем, неполном фрейме
        records_in_partial_frame = precords_count - (full_frames_total * RECORDS_IN_FULL_FRAME)  # li_full_frames_records
        # *** Рассчитаем к-во страниц в последнем фрейме
        pages_in_partial_frame = int(records_in_partial_frame / FULL_PAGE_SIZE)
    # *** Если к-во зап. в выборке не делится нацело на к-во зап. на странице
    if precords_count % FULL_PAGE_SIZE > 0:

        # *** Выставляем флаг неполной страницы
        partial_page_flag = True
        # *** Рассчитаем к-во записей на последней странице ???
        records_in_partial_page = (records_in_partial_frame - pages_in_partial_frame * FULL_PAGE_SIZE)
    return full_frames_total, partial_frame_flag, pages_in_partial_frame, partial_page_flag, records_in_partial_page


def route(prequest, precords_count):
    """Процедура обрабатывает нажатия кнопок пейджера."""
    assert precords_count is not None, ("Assert: [paginator:route]: No "
                                        "<precords_count> parameter specified!")
    full_frames_total= (precords_count // RECORDS_IN_FULL_FRAME)
    if prequest.form.get(FIRST_FRAME_CONTROL):

        # *** Переходим на первый фрейм
        session[SESSION_CURRENT_FRAME_KEY] = 0
        session[SESSION_CURRENT_PAGE_KEY] = 0
    elif prequest.form.get(PREV_FRAME_CONTROL):

        # *** Переходим на предыдущий фрейм
        session[SESSION_CURRENT_FRAME_KEY] -= 1
        session[SESSION_CURRENT_PAGE_KEY] = 0
    elif prequest.form.get(NEXT_FRAME_CONTROL):

        # *** Переходим на следующий фрейм
        session[SESSION_CURRENT_FRAME_KEY] += 1
        session[SESSION_CURRENT_PAGE_KEY] = 0
    elif prequest.form.get(LAST_FRAME_CONTROL):

        # *** Переходим на последний фрейм
        session[SESSION_CURRENT_FRAME_KEY] = full_frames_total
        session[SESSION_CURRENT_PAGE_KEY] = 0
    else:

        page_offset = 0
        # *** Перебираем страницы
        for page in range(0, FULL_FRAME_SIZE):

            # *** Ищем нажатую
            if prequest.form.get(f"page{page}"):

                # *** Нашли. Обрабатываем.
                page_offset = int(prequest.form.get(f"page{page}")) - 1
                session[SESSION_CURRENT_PAGE_KEY] = page
                break
        return page_offset
    return (session[SESSION_CURRENT_FRAME_KEY] * RECORDS_IN_FULL_FRAME)

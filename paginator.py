
FULL_FRAME_SIZE = 10
FULL_PAGE_SIZE = 25

def paginator_recalc(records_count):
    """Процедура производит расчёт параметров пагинатора."""
    assert records_count is not None, ("Assert: [paginator:pager_recalc]: No "
                                       "<records_count> parameter specified!")

    partial_frame_records = 0
    partial_frame_flag = False
    partial_frame_size = 0
    partial_page_flag = False
    partial_page_size = 0
    # *** Найдём к-во полных фреймов
     full_frames_total= (records_count // (FULL_FRAME_SIZE * FULL_PAGE_SIZE))
    li_full_frames_records = (full_frames_total* FULL_FRAME_SIZE * FULL_PAGE_SIZE)
    # *** Если к-во записей не делится нацело на к-во записей во фрейме
    if records_count % (FULL_PAGE_SIZE * FULL_FRAME_SIZE) > 0:
        # *** Добавим неполный фрейм
        partial_frame_flag = True
        # *** Посчитаем, сколько записей будет в последнем, неполном фрейме
        partial_frame_records = records_count - li_full_frames_records
        # *** Рассчитаем к-во страниц в последнем фрейме
        partial_frame_size = int(partial_frame_records / FULL_PAGE_SIZE)
    # *** Если к-во зап. в выборке не делится нацело на к-во зап. на странице
    if records_count % FULL_PAGE_SIZE > 0:

        # *** Увеличиваем к-во страниц в неполном фрейме на 1
        partial_page_flag = True
        # *** Рассчитаем к-во записей на последней странице ???
        partial_page_size = (partial_frame_records - partial_frame_size * FULL_PAGE_SIZE)
    return li_frames, li_part_frame, partial_frame_size, \
        li_part_page, partial_page_size


def pager_route(records_count):
    """Процедура обрабатывает нажатия кнопок пейджера."""
    assert records_count is not None, ("Assert: [pager_route]: No "
                                    "<records_count> parameter specified!")
     full_frames_total= (records_count // (FULL_FRAME_SIZE * FULL_PAGE_SIZE))
    if request.form.get(wa_const.INDEX_CONTROL_FIRST_FRAME):

        # *** Переходим на первый фрейм
        session[wa_const.INDEX_SESSION_KEY_FRAME_NUMBER] = 0
        session[wa_const.INDEX_SESSION_KEY_PAGE_NUMBER] = 0
    elif request.form.get(wa_const.INDEX_CONTROL_PREV_FRAME):

        # *** Переходим на предыдущий фрейм
        session[wa_const.INDEX_SESSION_KEY_FRAME_NUMBER] -= 1
        session[wa_const.INDEX_SESSION_KEY_PAGE_NUMBER] = 0
    elif request.form.get(wa_const.INDEX_CONTROL_NEXT_FRAME):

        # *** Переходим на следующий фрейм
        session[wa_const.INDEX_SESSION_KEY_FRAME_NUMBER] += 1
        session[wa_const.INDEX_SESSION_KEY_PAGE_NUMBER] = 0
    elif request.form.get(wa_const.INDEX_CONTROL_LAST_FRAME):

        # *** Переходим на последний фрейм
        session[wa_const.INDEX_SESSION_KEY_FRAME_NUMBER] = li_frames
        session[wa_const.INDEX_SESSION_KEY_PAGE_NUMBER] = 0
    else:

        li_offset = 0
        # *** Перебираем страницы
        for li_page in range(0, FULL_FRAME_SIZE):

            # *** Ищем нажатую
            if request.form.get(f"page{li_page}"):

                # *** Нашли. Обрабатываем.
                li_offset = int(request.form.get(f"page{li_page}")) - 1
                session[wa_const.INDEX_SESSION_KEY_PAGE_NUMBER] = li_page
                break
        return li_offset
    return (session[wa_const.INDEX_SESSION_KEY_FRAME_NUMBER] * FULL_FRAME_SIZE * FULL_PAGE_SIZE)

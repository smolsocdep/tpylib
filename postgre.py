"""Модуль содержит всякие процедуры для работы с postgresql."""

import psycopg2


def read_fields_max_lengths(po_connection, ps_table_name):
    """Получает данные о полях заданной таблицы."""
    assert po_connection is not None, ("Assert: "
                                       "[get_field_max_length_from_db]:"
                                       "No <po_connection> parameter "
                                       "specified!")
    assert ps_table_name is not None, ("Assert: "
                                       "[get_field_max_length_from_db]:"
                                       "No <ps_table_name> parameter "
                                       "specified!")
    try:
        # *** Получим курсор
        lo_meta_cursor = po_connection.cursor()
        # *** Получим выборку
        ldc_parameters = dict()
        ldc_parameters["p_table_name"] = ps_table_name
        ls_sql = """select column_name, character_maximum_length
                      from information_schema.columns
                      where     (table_schema = 'public')
                            and (table_name=%(p_table_name)s)"""
        ldc_result = dict()
        lo_meta_cursor.execute(ls_sql, ldc_parameters)
        # *** Получим длину поля
        lo_meta_data = lo_meta_cursor.fetchall()
        if lo_meta_data is not None:

            for row in lo_meta_data:

                ldc_result[row[0]] = row[1]
            return ldc_result, ""
        return None, f"Ошибка - таблица {ps_table_name} не существует!"
    except psycopg2.Error as ex:  # noqa

        return None, (f"!!! При обращении к базе данных возникла "
                      "исключительная ситуация !!! : {ex}:{ex.pgerror}")

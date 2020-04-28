"""Модуль содержит класс CWTFGuard."""

# Класс получает из БД размеры
# полей и соответственно выставляет максимальную длину поля
# в qLineEdit, чтобы исключить ввод данных, которые не будут сохранены.

# CONTRACT_NUMBER_FIELD_NUMBER = 0
# SUBJECT_FIELD_NUMBER = 1
# NOTICE_FIELD_NUMBER = 2
# REGISTRATION_DATE_FIELD_NUMBER = 3
# RECORD_DATE_FIELD_NUMBER = 4
# CONTRACT_TYPE_FIELD_NUMBER = 5
# ORGANIZATION_FIELD_NUMBER = 6
# DETAIL_FIELDS = ("fnumber", "fsubject", "fnotice",
#                  "fregistration_date", "frecord_date", "fcontract_type",
#                  "forganization")

# c_table_guard = tgrd.CTableGuard(connection, "tbl_details")
# c_table_guard.set_query_for_insert("select {} \
#                                          from public.tbl_details \
#                                          limit 1")
# c_table_guard.set_field_list(DETAIL_FIELDS)
# if c_table_guard.prepare():
#   c_table_guard.init_line_edit(self.qSubjectLineEdit, SUBJECT_FIELD_NUMBER)
#   c_table_guard.init_date_edit(self.qRegistrationDateEdit)
#   c_table_guard.init_line_edit(self.qNoticeLineEdit, NOTICE_FIELD_NUMBER)
#   c_table_guard.init_date_edit(self.qRecordDateEdit)


# c_table_guard = tgrd.CTableGuard(connection, "tbl_details")
# c_table_guard.set_query_for_update("select {} \
#                                         from public.tbl_details \
#                                         where id = %(p_id)s;",
#                                         p_record_id)
# c_table_guard.set_field_list(DETAIL_FIELDS)
# if c_table_guard.prepare():
#   c_table_guard.load_line_edit(self.qSubjectLineEdit, SUBJECT_FIELD_NUMBER)
#   c_table_guard.load_line_edit(self.qNoticeLineEdit, NOTICE_FIELD_NUMBER)
#   c_table_guard.load_date_edit(self.qRegistrationDateEdit,
#                                   REGISTRATION_DATE_FIELD_NUMBER)
#  c_table_guard.load_date_edit(self.qRecordDateEdit, RECORD_DATE_FIELD_NUMBER)

import datetime

import psycopg2

from tpylib import ttableguard as tguard
#from wtforms import StringField, DateField
#from wtforms.validators import DataRequired, Length


FIELD_IS_REQUIRED = "Поле должно быть заполнено"
# FIELD_IS_TOO_LONG = """Длина текста не может быть более %(max)s знаков!"""
# %(min)d and %(max)d
FIELD_IS_TOO_LONG = ("Строка не может быть короче %(min)d "
                     "и длиннее %(max)d знаков!")


#  pylint: disable=too-many-instance-attributes
class CWTFGuard(tguard.CTableGuard):
    """Класс реализует защиту БД для WTForm."""

    def __init__(self, ps_table_name):
        """Конструктор."""
        self.s_table_name = ps_table_name
        # self.dc_flags_list = list()
        # self.pi_minimal_lengths = list()
        lbl_successfull, ls_message = self.prepare()
        # self.query_metadata()
        if not lbl_successfull:
            raise ValueError(ls_message)

    # def set_minimal_length(pi_minimal_length):
    #     """Задает минимальную длину вводимого текста."""
    #     self.i_minimal_length = pi_minimal_length
    #
    # def set_additional_flag(self, ps_key, ps_value):
    #     """Задает дополнительные флаги для контролов."""
    #     self.dc_flags[ps_key] = ps_value

    def init_string_field(self, ps_label, pi_field_idx,
                          ps_default="", pi_minimal_length=0,
                          pbl_autofocus=False):
        """Создает поле типа String WTForm с нужными параметрами."""
        assert ps_label is not None, ("Assert: [CWTFGuard.__init__]:"
                                      "No <ps_label> parameter "
                                      "specified!")
        assert pi_field_idx is not None, ("Assert: [CWTFGuard.__init__]:"
                                          "No <pi_field_idx> parameter "
                                          "specified!")
        # *** Получим максимальную длину поля из параметров таблицы
        li_length = self.get_string_field_max_length(pi_field_idx)
        lo_validators = []
        # *** Проверим, что нам вернули
        if li_length > 0:

            # *** Ага, есть макс. длина, порядок. А минимальную длину задали?
            if pi_minimal_length > 0:

                # *** Отлично, есть и макс. и мин. длина
                lo_validators.append(Length(min=pi_minimal_length,
                                            max=li_length,
                                            message=FIELD_IS_TOO_LONG))

            else:

                # *** Нет, ограничиваем только максимальную длину
                lo_validators.append(Length(max=li_length,
                                            message=FIELD_IS_TOO_LONG))
            # Автофокус нужен на этом контроле?
            if pbl_autofocus:

                # *** Добавляем автофокус
                lo_field = StringField(ps_label,
                                       default=ps_default,
                                       validators=lo_validators,
                                       render_kw={'autofocus': True})
            else:

                # *** Обходимся без автофокуса
                lo_field = StringField(ps_label,
                                       default=ps_default,
                                       validators=lo_validators)
            # *** Возвращаем то, что у нас получилось
            return lo_field
        # *** Хьюстон, у нас проблемы!
        raise TypeError(f"Поле N{pi_field_idx} не текстовое!")
        return None

    def init_date_field(self, ps_label, pi_field_idx,
                        pdt_default=datetime.datetime.now(),
                        pbl_required=False):
        """Создает поле типа DateField WTForm с нужными параметрами."""
        if pbl_required:

            return DateField(ps_label,
                             default=pdt_default,
                             validators=[DataRequired(FIELD_IS_REQUIRED)])
        return DateField(ps_label, default=pdt_default)

    # Нет смысла передавать в процедуру поле, так как мы
    # не сможем задать ему параметры!
    def load_string_field(self, po_field, pi_field_idx, ps_label,
                          pbl_minimal_length, pbl_autofocus=False,
                          ps_style=None):
        """Загружает данные в строку ввода и задает макс. длину."""
        assert po_field is not None, ("Assert: [CWTFGuard.load_string_field]:"
                                      "No <po_field> parameter "
                                      "specified!")
        assert pi_field_idx is not None, ("Assert: [CWTFGuard.load_line_edit]:"
                                          "No <pi_field_idx> parameter "
                                          "specified!")

        # *** Получим максимальную длину поля из параметров таблицы
        li_length = self.get_string_field_max_length(pi_field_idx)
        ldc_validators = []
        ldc_parameters = []
        # # *** Проверим, что нам вернули
        if li_length > 0:

            # *** Ага, есть макс. длина, порядок. А минимальную длину задали?
            if self.i_minimal_length > 0:

                # *** Отлично, есть и макс. и мин. длина
                ldc_validators.append(Length(min=self.i_minimal_length,
                                             max=li_length,
                                             message=FIELD_IS_TOO_LONG))

            else:

                # *** Нет, ограничиваем только максимальную длину
                ldc_validators.append(Length(max=li_length,
                                             message=FIELD_IS_TOO_LONG))
            if pbl_autofocus is True:

                ldc_parameters["autofocus"] = True

            if ps_style is not None:

                ldc_parameters["id"] = ps_style

            # lo_field = StringField(ps_label,
            #                        validators=lo_validators,
            #                        render_kw={'autofocus': True})
            #
            # *** Заносим данные из базы
            # lo_field.data = self.get_field_value(pi_field_idx)
            # *** Возвращаем то, что у нас получилось
            # return lo_field
        # *** Хьюстон, у нас проблемы!
        raise TypeError(f"Поле N{pi_field_idx} не текстовое!")
        return None

    def load_date_edit(self, p_date_edit, p_field_idx):
        """Загружает дату в редактор дат."""
        assert p_date_edit is not None, ("Assert: [CTableGuard."
                                         "load_date_edit]:"
                                         "No <p_date_edit> parameter "
                                         "specified!")
        assert p_field_idx is not None, ("Assert: [CTableGuard."
                                         "load_date_edit]:"
                                         "No <p_field_idx> parameter "
                                         "specified!")

        l_field_name = self.c_field_list[p_field_idx]
        if self.c_field_types[l_field_name] == "date":

            p_date_edit.setDate(self.c_source_data[0][p_field_idx])


def get_field_max_len(po_connection, ps_table_name, ps_field_name):
    """Получает данные о полях заданной таблицы."""
    assert po_connection is not None, ("Assert: "
                                       "[get_field_max_length_from_db]:"
                                       "No <po_connection> parameter "
                                       "specified!")
    assert ps_table_name is not None, ("Assert: "
                                       "[get_field_max_length_from_db]:"
                                       "No <ps_table_name> parameter "
                                       "specified!")
    assert ps_field_name is not None, ("Assert: "
                                       "[get_field_max_length_from_db]:"
                                       "No <ps_field_name> parameter "
                                       "specified!")
    try:
        # *** Получим курсор
        lo_meta_cursor = po_connection.cursor()
        # *** Получим выборку
        ldc_parameters = dict()
        ldc_parameters["p_table_name"] = ps_table_name
        ldc_parameters["p_field_name"] = ps_field_name
        ls_sql = """select character_maximum_length
                      from information_schema.columns
                      where     (table_schema = 'public')
                            and (table_name=%(p_table_name)s)
                            and (column_name=%(p_field_name)s)"""
        lo_meta_cursor.execute(ls_sql, ldc_parameters)
        # *** Получим длину поля
        lo_meta_data = lo_meta_cursor.fetchall()
        if lo_meta_data is not None:
            return lo_meta_data[0][0], ""
    except psycopg2.Error as ex:  # noqa

        return None, (f"!!! При обращении к базе данных возникла "
                      "исключительная ситуация !!! : {ex}:{ex.pgerror}")


def read_values_from_table(po_connection, ps_sql, po_field_list, pi_id=None):
    lo_data = None
    try:

        lo_cursor = po_connection.cursor()
        lo_fields = ", ".join(po_field_list)
        # *** Получим выборку
        l_query = ps_sql.format(lo_fields)
        if pi_id is not None:
            lo_param = dict(p_id=pi_id)
            lo_cursor.execute(l_query, lo_param)
        else:
            lo_cursor.execute(l_query)
        lo_data = lo_cursor.fetchall()
        return lo_data, ""

    except psycopg2.Error as ex:

        # tmsg.error_occured()
        return None, ("При обращении к базе данных возникла "
                      "исключительная ситуация: ") + str(ex.pgerror)


# def load_data_into_line_edit(po_field, pi_id):
#     """Процедура загружает редактируемые данные в StringField."""
#     lo_connection, ls_message = wa_db.db_connect()
#     if lo_connection is not None:
#
#         # *** Создадим объект хранителя
#         try:
#
#             lo_guard = grd.CWTFGuard(lo_connection, REFERENCE_TABLE)
#             ls_field_list = "{}"
#             ls_sql = f"""select {ls_field_list}
#                          from {REFERENCE_TABLE}
#                          where id=%(p_id)s"""
#             lo_guard.set_query_for_update(ls_sql, pi_id)
#             lo_guard.set_field_list(REF_FIELDS)
#             # *** вызываем подготовительную процедуру
#             # lbl_successfull, ls_message = lo_guard.prepare()
#             lbl_successfull, ls_message = lo_guard.__reopen_source_query()
#             if lbl_successfull:
#
#                 lo_guard.load_string_field(po_form.name_field,
#                                            NAME_FIELD_NUMBER)
#         except psycopg2.Error as ex:
#
#             ls_message = wa_db.DB_REQUEST_FAILED_EXCEPTION.format(
#                 ex.pgerror)
#             flash(ls_message)
#             session[wa_msg.RETURN_ADDRESS] = wa_ref.REFERENCE_URL
#             return redirect(url_for(wa_msg.MESSAGE_URL))
#         except TypeError:
#             flash(ls_message)
#             redirect(url_for('message'))  # no RETURN!!!
#         except ValueError:
#             flash(ls_message)
#             redirect(url_for('message'))  # no RETURN!!!
#             pass
#         #  validate(form, extra_validators=())
#         # login = StringField('Имя пользователя:',
#         #                     validators=[DataRequired("Введите логин!")])
#     else:
#         flash(ls_message)
#         redirect(url_for('message'))  # no RETURN!!!

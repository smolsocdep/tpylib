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

# import datetime
# import psycopg2

import ttableguard as tguard
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length

FIELD_IS_REQUIRED = "Поле должно быть заполнено"


#  pylint: disable=too-many-instance-attributes
class CWTFGuard(tguard.CTableGuard):
    """Класс реализует защиту БД для WTForm."""

    # def __init__(self, po_connection, ps_table_name):
    #     """Конструктор."""
    #     super().__init__(po_connection, ps_table_name)
    #     assert po_connection is not None, ("Assert: [CWTFGuard.__init__]:"
    #                                        "No <po_connection> parameter "
    #                                        "specified!")
    #     assert ps_table_name is not None, ("Assert: [CTableGuard.__init__]:"
    #                                        "No <ps_table_name> parameter "
    #                                        "specified!")

    def init_string_field(self, ps_label, po_field, pi_field_idx,
                          ps_default="", pbl_required=False):
        """Производит настройку строкового компонента WTForm."""
        lo_validators = []
        if pbl_required:

            lo_validators.append(DataRequired(FIELD_IS_REQUIRED))
        li_length = self.get_string_field_max_length(pi_field_idx)
        if li_length > 0:

            lo_validators.append(Length(max=li_length))

        return StringField(ps_label, ps_default,
                           validators=lo_validators)

    def load_line_edit(self, p_line_edit, p_field_idx):
        """Загружает данные в строку ввода и задает макс. длину."""
        assert p_line_edit is not None, ("Assert: [CTableGuard."
                                         "load_line_edit]:"
                                         "No <p_line_edit> "
                                         "parameter specified!")
        assert p_field_idx is not None, ("Assert: [CTableGuard."
                                         "load_line_edit]:"
                                         "No <p_field_idx> parameter "
                                         "specified!")

        l_field_name = self.c_field_list[p_field_idx]
        if self.c_field_types[l_field_name] == "character varying":

            p_line_edit.setText(self.c_source_data[0][p_field_idx])
            p_line_edit.setMaxLength(self.c_field_widthes[l_field_name])

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

    def init_line_edit(self, p_field_idx):
        """Очищает контрол и задает макс. длину."""
        assert p_field_idx is not None, ("Assert: [CTableGuard."
                                         "init_line_edit]:"
                                         "No <p_field_idx> parameter "
                                         "specified!")
        # print("===============================")
        # print("Field list:")
        # print(self.c_field_list)
        l_field_name = self.c_field_list[p_field_idx]
        l_length = -1
        # print("===============================")
        # print("Field types:")
        # print(self.c_field_types)

        if self.c_field_types[l_field_name] == "character varying":

            l_length = self.c_field_widthes[l_field_name]
        return l_length

"""Модуль содержит класс CTableGuard."""

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

FIELD_NAME_ORDER = 0
FIELD_TYPE_ORDER = 1
FIELD_WIDTH_ORDER = 2

CONTROL_INSTANCE = "control"
CONTROL_FIELDNAME = "fieldname"
CONTROL_FIELDNUMBER = "fieldnumber"

TG_FIELD_NOT_FOUND = -1

FIELD_TYPE_VARCHAR = "character varying"
FIELD_TYPE_INTEGER = "integer"
FIELD_TYPE_DATE = "date"

DB_MODE_INSERT = 0
DB_MODE_UPDATE = 1


#  pylint: disable=too-many-instance-attributes
class CTableGuard():
    """Класс реализует защиту БД."""

    def __init__(self, p_connection, p_table_name):
        """Конструктор."""
        self.c_field_count = 0
        # *** Эти списки заполняются из выборки
        self.c_field_types = {}
        self.c_field_widthes = {}
        self.c_connection = None
        self.c_table_name = ""
        self.c_source_query = ""
        self.c_source_data = None
        self.c_source_cursor = None
        self.c_field_list = None
        self.c_id_value = None
        self.c_parameters = None

        assert p_connection is not None, ("Assert: [CTableGuard.__init__]:"
                                          "No <p_connection> parameter "
                                          "specified!")
        assert p_table_name is not None, ("Assert: [CTableGuard.__init__]:"
                                          "No <p_table_name> parameter "
                                          "specified!")

        self.c_connection = p_connection
        self.c_table_name = p_table_name

    def __reopen_source_query(self):  # +**
        """Производит выборку данных для редактирования/добавления."""
        try:

            self.c_source_cursor = self.c_connection.cursor()
            # *** Получим выборку
            l_fields = ", ".join(self.c_field_list)
            l_query = self.c_source_query.format(l_fields)
            l_param = dict(p_id=self.c_id_value)
            self.c_source_cursor.execute(l_query, l_param)
            self.c_source_data = self.c_source_cursor.fetchall()
            return True, ""

        except psycopg2.Error as ex:

            # tmsg.error_occured()
            return False, ("При обращении к базе данных возникла "
                           "исключительная ситуация: ")+str(ex.pgerror)

    def __query_metadata(self):
        """Получает данные о полях заданной таблицы."""
        assert self.c_field_list is not None, ("Assert: [CTableGuard."
                                               "__query_metadata]:"
                                               "No field list was defined in "
                                               "CTableGuard!")
        # print("****** __query_metadata")
        try:

            # print("*** 0.1 ", self.c_connection)
            # *** Получим курсор
            l_meta_cursor = self.c_connection.cursor()
            # *** Получим выборку
            # print("*** 0.2 ", l_meta_cursor)
            l_param = dict(p_table_name=self.c_table_name)
            l_query = """select column_name, data_type,
                                character_maximum_length
                           from information_schema.columns
                           where     (table_schema = 'public')
                                 and (table_name=%(p_table_name)s)"""
            l_meta_cursor.execute(l_query, l_param)
            # *** Вытащим все данные из выборки
            l_meta_data = l_meta_cursor.fetchall()
            # *** Получим кол-во строк
            l_rows = len(l_meta_data)
            # *** если выборка не пустая...
            # print("*** 1 ")
            if l_rows > 0:

                # print("*** 2 ")
                for l_meta_row in l_meta_data:

                    if self.c_field_list.count(l_meta_row[0]):

                        # print("*** 3 ")
                        self.c_field_types[l_meta_row[0]] = l_meta_row[1]
                        self.c_field_widthes[l_meta_row[0]] = l_meta_row[2]
            return True, ""

        except psycopg2.Error as ex:  # noqa

            # print("**** Exception!")
            # print("ex:", ex)
            # print("ex.pgerror:", ex.pgerror)
            return False, (f"!!! При обращении к базе данных возникла "
                           "исключительная ситуация !!! : {ex}:{ex.pgerror}")

    def set_query_for_update(self, p_query, p_id):  # +++
        """Задает запрос для загрузки данных в компоненты."""
        assert p_query is not None, ("Assert: [CTableGuard."
                                     "set_query_for_update]:"
                                     "No <p_query> parameter specified!")
        assert p_id is not None, ("Assert: [CTableGuard.set_query_for_update]:"
                                  "No <p_id> parameter specified!")

        self.c_source_query = p_query
        self.c_id_value = p_id

    def set_query_for_insert(self, p_query):
        """Задает запрос для инициализации компонентов без загрузки данных."""
        assert p_query is not None, ("Assert: [CTableGuard."
                                     "set_query_for_insert]: "
                                     "No <p_query> parameter specified!")

        self.c_source_query = p_query

    def set_field_list(self, p_field_list):
        """Задает список полей для выборки."""
        assert p_field_list is not None, ("Assert: [CTableGuard."
                                          "set_field_list]: "
                                          "No <p_field_list> "
                                          "parameter specified!")

        self.c_field_list = p_field_list
        self.c_field_count = len(p_field_list)

    def prepare(self):
        """Получает данные из БД."""
        # *** Получим метаданные выбранной таблицы
        if self.__query_metadata():
            # print("!!!! prepare")
            # *** Откроем выборку для загрузки в контролы
            return self.__reopen_source_query()
        return False

    def get_field_value(self, p_field_idx):
        """Возвращает значение поля с указанным индексом."""
        assert p_field_idx is not None, ("Assert: [CTableGuard."
                                         "get_field_value]:"
                                         "No <p_field_idx> "
                                         "parameter specified!")

        return self.c_source_data[0][p_field_idx]

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

    # pylint: disable=no-self-use
    def init_date_edit(self, p_date_edit):
        """Задает текущую дату редактору дат."""
        assert p_date_edit is not None, ("Assert: [CTableGuard."
                                         "init_date_edit]:"
                                         "No <p_date_edit> parameter "
                                         "specified!")

        p_date_edit.setDate(datetime.datetime.now())

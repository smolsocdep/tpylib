""" Модуль содержит класс CTableGuard, который получает из БД размеры\
    полей и соответственно выставляет максимальную длину поля \
    в qLineEdit, чтобы исключить ввод данных, которые не будут сохранены"""


import datetime
import psycopg2
from tpylib import tdebug as deb

SQL_QUERY_COLUMNS_INFO = "select column_name, data_type, character_maximum_length \
                          from information_schema.columns \
                          where table_schema = 'public' and table_name=%(p_table_name)s"
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

class CTableGuard():
    """ Класс реализует защиту БД """

    # pylint: disable=too-many-instance-attributes
    #*** Эти списки заполняются из выборки
    c_field_count = 0 #+
    c_field_types = {}
    c_field_widthes = {}

    c_kernel = None
    c_table_name = ""
    c_source_query = ""
    c_source_data = None
    c_source_cursor = None
    c_field_list = None
    c_id_value = None
    c_parameters = None

    def __init__(self, p_kernel, p_table_name): #+++
        """ Конструктор """

        assert p_kernel is not None, "Assert: [table_guard.__init__]: \
            No <p_kernel> parameter specified!"
        assert p_table_name is not None, "Assert: [table_guard.__init__]: \
            No <p_table_name> parameter specified!"

        self.c_kernel = p_kernel
        self.c_table_name = p_table_name


    def __reopen_source_query(self): #+**
        """ Производит выборку данных для редактирования/добавления """

        # deb.dout("CTableGuard", "__reopen_source_query")
        try:

            self.c_source_cursor = self.c_kernel.get_connection().cursor()
            #*** Получим выборку
            l_fields = ", ".join(self.c_field_list)
            l_query = self.c_source_query.format(l_fields)
            l_param = dict(p_id=self.c_id_value)
            #deb.dout("CTableGuard", "__reopen_source_query", l_query)
            #deb.dout("CTableGuard", "__reopen_source_query", l_param)
            self.c_source_cursor.execute(l_query, l_param)
            self.c_source_data = self.c_source_cursor.fetchall()
            #deb.dout("CTableGuard", "__reopen_source_query", self.c_source_data)
            return True

        except psycopg2.Error:

            # deb.dout("CTableGuard", "__reopen_source_query", "Query failed")
            return False


    def __query_metadata(self): #+**
        """ Получает данные о полях заданной таблицы """

        assert self.c_field_list is not None, "Assert: [table_guard.__query_metadata]: \
            No field list was defined in CTableGuard!"

        # print("CTableGuard:__query_metadata")

        #*** Получим курсор
        l_meta_cursor = self.c_kernel.get_connection().cursor()
        #*** Получим выборку
        l_param = dict(p_table_name=self.c_table_name)
        l_meta_cursor.execute(SQL_QUERY_COLUMNS_INFO, l_param)
        #*** Вытащим все данные из выборки
        l_meta_data = l_meta_cursor.fetchall()
        #*** Получим кол-во строк
        l_rows = len(l_meta_data)
        #*** если выборка не пустая...
        if l_rows > 0:

            for l_meta_data_row in l_meta_data:

                if self.c_field_list.count(l_meta_data_row[0]):

                    self.c_field_types[l_meta_data_row[0]] = l_meta_data_row[1]
                    self.c_field_widthes[l_meta_data_row[0]] = l_meta_data_row[2]


    def set_query_for_update(self, p_query, p_id): #+++
        """ Задает запрос для загрузки данных в компоненты """

        assert p_query is not None, "Assert: [table_guard.set_query_for_update]: \
            No <p_query> parameter specified!"
        assert p_id is not None, "Assert: [table_guard.set_query_for_update]: \
            No <p_id> parameter specified!"

        self.c_source_query = p_query
        self.c_id_value = p_id


    def set_query_for_insert(self, p_query):
        """ Задает запрос для инициализации компонентов без загрузки данных """

        assert p_query is not None, "Assert: [table_guard.set_query_for_insert]: \
            No <p_query> parameter specified!"

        self.c_source_query = p_query


    def set_field_list(self, p_field_list): #++
        """ Задает список полей для выборки """

        assert p_field_list is not None, "Assert: [table_guard.set_field_list]: \
            No <p_field_list> parameter specified!"

        self.c_field_list = p_field_list
        self.c_field_count = len(p_field_list)


    def prepare(self): #+++
        """ Получает данные из БД"""

        #*** Получим метаданные выбранной таблицы
        self.__query_metadata()

        #*** Откроем выборку для загрузки в контролы
        self.__reopen_source_query()


    def get_field_value(self, p_field_idx):
        """ Возвращает значение поля с указанным индексом """

        assert p_field_idx is not None, "Assert: [table_guard.get_field_value]: \
            No <p_field_idx> parameter specified!"

        return self.c_source_data[0][p_field_idx]


    def load_line_edit(self, p_line_edit, p_field_idx): #+++
        """ Загружает данные в строку ввода и задает макс. длину """

        assert p_line_edit is not None, "Assert: [table_guard.load_line_edit]: \
            No <p_line_edit> parameter specified!"
        assert p_field_idx is not None, "Assert: [table_guard.load_line_edit]: \
            No <p_field_idx> parameter specified!"

        #ToDo: Сделать обработку Integer'а и Float'а
        l_field_name = self.c_field_list[p_field_idx]
        if self.c_field_types[l_field_name] == "character varying":

            p_line_edit.setText(self.c_source_data[0][p_field_idx])
            p_line_edit.setMaxLength(self.c_field_widthes[l_field_name])


    def load_date_edit(self, p_date_edit, p_field_idx): #+++
        """ Загружает дату в редактор дат """

        assert p_date_edit is not None, "Assert: [table_guard.load_date_edit]: \
            No <p_date_edit> parameter specified!"
        assert p_field_idx is not None, "Assert: [table_guard.load_date_edit]: \
            No <p_field_idx> parameter specified!"

        l_field_name = self.c_field_list[p_field_idx]
        if self.c_field_types[l_field_name] == "date":

            p_date_edit.setDate(self.c_source_data[0][p_field_idx])


    def init_line_edit(self, p_line_edit, p_field_idx):
        """ Очищает контрол и задает макс. длину """

        assert p_line_edit is not None, "Assert: [table_guard.init_line_edit]: \
            No <p_line_edit> parameter specified!"
        assert p_field_idx is not None, "Assert: [table_guard.init_line_edit]: \
            No <p_field_idx> parameter specified!"

        l_field_name = self.c_field_list[p_field_idx]
        if self.c_field_types[l_field_name] == "character varying":

            p_line_edit.setText("")
            p_line_edit.setMaxLength(self.c_field_widthes[l_field_name])

    #pylint: disable=no-self-use
    def init_date_edit(self, p_date_edit): #+++
        """ Задает текущую дату редактору дат """

        assert p_date_edit is not None, "Assert: [table_guard.init_date_edit]: \
            No <p_date_edit> parameter specified!"

        p_date_edit.setDate(datetime.datetime.now())

""" Модуль содержит класс CTableGuard, который получает из БД размеры\
    полей и соответственно выставляет максимальную длину поля \
    в qLineEdit, чтобы исключить ввод данных, которые не будут сохранены"""


#import collections
from PyQt5 import QtWidgets, QtCore
import psycopg2

# from pip._vendor.pyparsing import line
# from pylint.test.functional.undefined_variable import Self
#, QtGui QtCore,


SQL_QUERY_COLUMNS_INFO = "select column_name, data_type, character_maximum_length \
                          from information_schema.columns \
                          where table_schema = 'public' and table_name='%s'"

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

class CTableGuard():
    """ Класс реализует защиту БД """

    #*** Эти списки заполняются из выборки
    c_field_count = 0
    c_field_names = []
    c_field_types = []
    c_field_widthes = []

    c_controls = []
    c_kernel = None
    c_table_name = ""
    c_source_query = ""
    c_source_data = None
    c_source_cursor = None


    def __init__(self, p_kernel, p_table_name):
        """ Конструктор """

        assert p_kernel is not None, "Assert: [table_guard.__init__]: \
            No <p_kernel> parameter specified!"
        self.c_kernel = p_kernel
        assert p_table_name is not None, "Assert: [table_guard.__init__]: \
            No <p_table_name> parameter specified!"
        self.c_table_name = p_table_name

        #*** Читаем описания полей
        self.__query_metadata()


    def __reopen_source_query(self):
        """ Производит выборку данных для редактирования/добавления """

        try:

            self.c_source_cursor = self.c_kernel.get_connection().cursor()
            #*** Получим выборку
            self.c_source_cursor.execute(self.c_source_query)
            self.c_source_data = self.c_source_cursor.fetchall()
            print("Data: ", self.c_source_data)
            return True

        except psycopg2.Error:

            return False


    def __query_metadata(self):
        """ Получает данные о полях заданной таблицы """

        #*** Получим курсор
        l_meta_cursor = self.c_kernel.get_connection().cursor()
        #*** Получим выборку
        l_sql = SQL_QUERY_COLUMNS_INFO % self.c_table_name
        l_meta_cursor.execute(l_sql)
        #*** Вытащим все данные из выборки
        l_meta_data = l_meta_cursor.fetchall()
        #*** Получим кол-во строк
        l_rows = len(l_meta_data)
        #*** если выборка не пустая...
        if l_rows > 0:

            self.c_field_count = l_rows
            for l_row in range(l_rows):

                self.c_field_names.append(l_meta_data[l_row][FIELD_NAME_ORDER])
                self.c_field_types.append(l_meta_data[l_row][FIELD_TYPE_ORDER])
                self.c_field_widthes.append(l_meta_data[l_row][FIELD_WIDTH_ORDER])


    def get_field_index(self, p_field_name):
        """ Ищет заданное поле в списке имён """

        assert p_field_name is not None, "Assert: [table_guard.get_field_index]: \
            No <p_field_name> parameter specified!"
        print("Name: ",p_field_name)
        try:

            return self.c_field_names.index(p_field_name)
        except ValueError:

            return TG_FIELD_NOT_FOUND


    def get_field_length_by_index(self, p_field_index):
        """ Возвращает длину заданного поля по его индексу """
        
        assert p_field_index is not None, "Assert: [table_guard.get_field_length_by_index]: \
            No <p_field_index> parameter specified!"
        return self.c_field_widthes[p_field_index]


#     def get_field_length_by_name(self, p_field_name):
#         """ Возвращает длину заданного поля """
# 
#         assert p_field_name is not None, "Assert: [table_guard.get_field_length]: \
#             No <p_field_name> parameter specified!"
#         l_field_idx = self.get_field_index(p_field_name)
#         if l_field_idx == TG_FIELD_NOT_FOUND:
# 
#             return None
#         return self.c_field_widthes[l_field_idx]

    def get_field_content_by_index(self, p_field_index):
        """ Возвращает длину заданного поля по его индексу """
        
        assert p_field_index is not None, "Assert: [table_guard.get_field_length_by_index]: \
            No <p_field_index> parameter specified!"
        print("Idx: ",p_field_index)
        return self.c_source_data[0][p_field_index]


#     def get_field_data_by_number(self, p_field_number):
#         """ Возвращает значение заданного поля """
# 
#         assert p_field_number is not None, "Assert: [table_guard.get_field_data_by_name]: \
#             No <p_field_number> parameter specified!"
#         if len(self.c_source_data)-1 > p_field_number:
# 
#             return self.c_source_data[p_field_number]
#         return None


    def set_source_query(self, p_query):
        """ Задает запрос для загрузки данных в компоненты """

        assert p_query is not None, "Assert: [table_guard.set_source_query]: \
            No <p_query> parameter specified!"
        self.c_source_query = p_query




    # Балбес, сначала нужно из выборки взять имена полей, типы и длину!


    def prepare(self):
        """ Получает данные из БД"""

        #*** Получим метаданные выбранной таблицы
        self.__query_metadata()

        #*** Откроем выборку для загрузки в контролы
        self.__reopen_source_query()



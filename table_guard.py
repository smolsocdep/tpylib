""" Модуль содержит класс CTableGuard, который получает из БД размеры\
    полей и соответственно выставляет максимальную длину поля \
    в qLineEdit, чтобы исключить ввод данных, которые не будут сохранены"""


#import collections
#from PyQt5 import QtCore #QtWidgets, 
import psycopg2
#from os.path import join

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

        try:

            #c_parameters = dict()
            self.c_source_cursor = self.c_kernel.get_connection().cursor()
            #*** Получим выборку
            l_fields = ", ".join(self.c_field_list)
            l_query = self.c_source_query % l_fields
            l_param = dict(p_id=self.c_id_value)
            self.c_source_cursor.execute(l_query, l_param)
            self.c_source_data = self.c_source_cursor.fetchall()
            #print("Data: ", self.c_source_data)
            #c_parameters = None
            return True

        except psycopg2.Error:

            return False


    def __query_metadata(self): #+**
        """ Получает данные о полях заданной таблицы """

        assert self.c_field_list is not None, "Assert: [table_guard.__query_metadata]: \
            No field list was defined in CTableGuard!"

        #*** Получим курсор
        l_meta_cursor = self.c_kernel.get_connection().cursor()
        #*** Получим выборку
        l_sql = SQL_QUERY_COLUMNS_INFO % self.c_table_name
        l_meta_cursor.execute(l_sql)
        #*** Вытащим все данные из выборки
        l_meta_data = l_meta_cursor.fetchall()
        #*** Получим кол-во строк
        l_rows = len(l_meta_data)
#         print("Meta: ", l_meta_data)
        #*** если выборка не пустая...
        if l_rows > 0:
            
            for l_meta_data_row in l_meta_data:

                if self.c_field_list.count(l_meta_data_row[0]):
                    
                    self.c_field_types[l_meta_data_row[0]] = l_meta_data_row[1]
                    self.c_field_widthes[l_meta_data_row[0]] = l_meta_data_row[2]

    
    def set_source_query(self, p_query, p_id): #+++
        """ Задает запрос для загрузки данных в компоненты """

        assert p_query is not None, "Assert: [table_guard.set_source_query]: \
            No <p_query> parameter specified!"
        assert p_id is not None, "Assert: [table_guard.set_source_query]: \
            No <p_id> parameter specified!"
        
        self.c_source_query = p_query
        self.c_id_value = p_id
    
    def set_field_list(self, p_field_list): #++
        """ Задает список полей для выборки """

        assert p_field_list is not None, "Assert: [table_guard.set_field_list]: \
            No <p_field_list> parameter specified!"

        self.c_field_list = p_field_list
        self.c_field_count = len(p_field_list)
#         print(self.c_field_count)


    def prepare(self): #+++
        """ Получает данные из БД"""

        #*** Получим метаданные выбранной таблицы
        self.__query_metadata()

        #*** Откроем выборку для загрузки в контролы
        self.__reopen_source_query()
    
#     def get_field_index(self, p_field_name):
#         """ Ищет заданное поле в списке имён """
# 
#         assert p_field_name is not None, "Assert: [table_guard.get_field_index]: \
#             No <p_field_name> parameter specified!"
#         print("Name: ",p_field_name)
#         try:
# 
#             return self.c_field_names.index(p_field_name)
#         except ValueError:
# 
#             return TG_FIELD_NOT_FOUND
# 
# 
#     def get_field_length_by_index(self, p_field_index):
#         """ Возвращает длину заданного поля по его индексу """
#         
#         assert p_field_index is not None, "Assert: [table_guard.get_field_length_by_index]: \
#             No <p_field_index> parameter specified!"
#         return self.c_field_widthes[p_field_index]


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

#     def get_field_content_by_index(self, p_field_index):
#         """ Возвращает длину заданного поля по его индексу """
#         
#         assert p_field_index is not None, "Assert: [table_guard.get_field_length_by_index]: \
#             No <p_field_index> parameter specified!"
#         print("Idx: ",p_field_index)
#         return self.c_source_data[0][p_field_index]


#     def get_field_data_by_number(self, p_field_number):
#         """ Возвращает значение заданного поля """
# 
#         assert p_field_number is not None, "Assert: [table_guard.get_field_data_by_name]: \
#             No <p_field_number> parameter specified!"
#         if len(self.c_source_data)-1 > p_field_number:
# 
#             return self.c_source_data[p_field_number]
#         return None

    
    def get_field_value(self, p_field_idx):
        """ Возвращает значение поля с указанным индексом """

        assert p_field_idx is not None, "Assert: [table_guard.get_field_value]: \
            No <p_field_idx> parameter specified!"
        
#         print("Field: ", p_field_idx)
#         print("Data: ",self.c_source_data)
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

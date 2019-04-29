""" Модуль содержит класс CTableGuard, который получает из БД размеры\
    полей и соответственно выставляет максимальную длину поля \
    в qLineEdit, чтобы исключить ввод данных, которые не будут сохранены"""


#import collections
#from PyQt5 import QtCore, QtWidgets, QtGui
#import constants as cns


SQL_QUERY_COLUMNS_INFO = "select column_name, data_type, character_maximum_length \
                          from information_schema.columns \
                          where table_schema = 'public' and table_name='%s'"

FIELD_NAME_ORDER = 0
FIELD_TYPE_ORDER = 1
FIELD_WIDTH_ORDER = 2

CONTROL_INSTANCE = "control"
CONTROL_FIELDNAME = "fieldname"

TG_FIELD_NOT_FOUND = -1


class CTableGuard():
    """ Класс реализует защиту БД """

    c_field_count = 0
    c_field_names = []
    c_field_types = []
    c_field_widthes = []
    c_controls = []
    c_kernel = None
    c_table_name = ""
    c_source_query = ""

    def __init__(self, p_kernel, p_table_name):
        """ Конструктор """

        assert p_kernel is not None, "Assert: [table_guard.__init__]: \
            No <p_kernel> parameter specified!"
        self.c_kernel = p_kernel
        assert p_table_name is not None, "Assert: [table_guard.__init__]: \
            No <p_table_name> parameter specified!"
        self.c_table_name = p_table_name

        #*** Читаем описания полей
        l_cursor = self.c_kernel.get_connection().cursor()
        l_sql = SQL_QUERY_COLUMNS_INFO % self.c_table_name
        l_cursor.execute(l_sql)
        l_data = l_cursor.fetchall()
        self.c_field_count = len(l_data)
        if self.c_field_count:
            for l_row in l_data:

                self.c_field_names.append(l_row[FIELD_NAME_ORDER])
                self.c_field_types.append(l_row[FIELD_TYPE_ORDER])
                self.c_field_widthes.append(l_row[FIELD_WIDTH_ORDER])
            # print(self.c_field_names)
            # print(self.c_field_types)
            # print(self.c_field_widthes)


    def __find_field_in_list(self, p_field_name):
        """ Ищет заданное поле в списке имён """

        assert p_field_name is not None, "Assert: [table_guard.find_field_in_list]: \
            No <p_field_name> parameter specified!"
        try:

            return self.c_field_names.index(p_field_name)
        except ValueError:

            return TG_FIELD_NOT_FOUND


    def __reopen_query(self):
        """ Производит выборку данных для редактирования/добавления """

        try:

            self.c_source_cursor = self.c_kernel.get_connection().cursor()
            #*** Получим выборку
            self.c_source_cursor.execute(self.c_source_query)
            
            return True

        except:
            
            return False


    def __query_metadata(self):
        """ Получает данные о полях заданной таблицы """
        
        #*** Получим курсор
        l_meta_cursor = self.c_kernel.get_connection().cursor()
        #*** Получим выборку
        l_meta_cursor.execute(SQL_QUERY_COLUMNS_INFO % self.c_table_name)
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


    def add_control(self, p_control, p_field_name):
        """ Добавляет очередной элемент в список """

        assert p_control is not None, "Assert: [table_guard.add_control]: \
            No <p_control> parameter specified!"
        assert p_field_name is not None, "Assert: [table_guard.add_control]: \
            No <p_field_name> parameter specified!"
        if self.__find_field_in_list(p_field_name) == TG_FIELD_NOT_FOUND:

            return None # ????
        l_control = {}
        l_control[CONTROL_INSTANCE] = p_control
        l_control[CONTROL_FIELDNAME] = p_field_name
        self.c_controls.append(l_control)
        return l_control


    def get_field_length(self, p_field_name):
        """ Возвращает длину заданного поля """

        assert p_field_name is not None, "Assert: [table_guard.get_field_length]: \
            No <p_field_name> parameter specified!"
        l_field_idx = self.__find_field_in_list(p_field_name)
        if l_field_idx == TG_FIELD_NOT_FOUND:

            return None
        return self.c_field_widthes[l_field_idx]


    def set_source_query(self, p_query):
        """ Задает запрос для загрузки данных в компоненты """

        assert p_query is not None, "Assert: [table_guard.set_source_query]: \
            No <p_query> parameter specified!"
        self.c_source_query = p_query




    # Балбес, сначала нужно из выборки взять имена полей, типы и длину!
    
    
    def load_data(self):
        """ Загружает данные в соответствующие элементы и задает макс. длину
            строк для эдитов """

        print(self.c_field_names)
        #*** Перебираем сохраненные контролы
        for l_control in self.c_controls:

            #*** Каждый l_control - это словарь!
            l_field_name = l_control[CONTROL_FIELDNAME]
            l_field_idx = self.__find_field_in_list(l_field_name)
            if l_field_idx != TG_FIELD_NOT_FOUND:

                l_field_type = self.c_field_types[l_field_idx]
                l_field_width = self.c_field_widthes[l_field_idx]
                if l_field_type == 
                l_control[CONTROL_INSTANCE]
                print("T: ", l_field_type)
                print("W: ", l_field_width)

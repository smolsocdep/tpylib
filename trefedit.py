""" Диалог редактирования элемента справочника """

from PyQt5 import QtWidgets #, QtGui, QtCore
import psycopg2
from tpylib import form_ref_edit
from tpylib import tmsgboxes as tmsg, \
    tforms as frm, \
    table_guard as guard, \
    tdebug as deb

SINGLE_FIELD_NAME_IDX = 0
SINGLE_FIELD_NAME = "fname"

class CRefItemEdit(QtWidgets.QDialog, form_ref_edit.Ui_qRefItemEditDialog):
    """ Класс окна редактирования  таблицы tbl_master """

    # pylint: disable=too-many-instance-attributes
    c_kernel = None
    c_table_guard = None
    c_record_id = None
    c_db_mode = None
    c_parameters = None
    c_table_name = ""
    c_insert_sql = ""
    c_update_sql = ""

    def __init__(self, p_kernel):
        """ Конструктор """

        assert p_kernel is not None, "Assert: [CRefItemEdit.__init__]: \
            No <p_kernel> parameter specified!"

        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.c_kernel = p_kernel
        self.qModeCheckBox.stateChanged.connect(self.__state_changed)
        # self.accept.connect(self.__accepted)
        # self.qOkToolButton.clicked.connect(self.__ok_button_pressed)


    def accept(self):
        """ Обработчик вызывается при вызове accept() или done() """

        #ToDo: не отрабатывает эта функа!
        # deb.dout("** 1 **")
        if self.__validate_data():
            if self.c_db_mode == guard.DB_MODE_INSERT:

                l_query = self.c_insert_sql
            else:

                l_query = self.c_update_sql

            # deb.dout("** 2 **")
            ## To Do: тут try впихнуть
            try:

                self.__store_data()
                l_cursor = self.__get_cursor()
                deb.dout("*", l_query)
                l_cursor.execute(l_query, self.c_parameters)
                self.c_kernel.get_connection().commit()
                self.c_parameters = None
            except psycopg2.Error as ex:

                tmsg.error_occured("При обращении к базе данных возникла " + \
                                  "исключительная ситуация, возможно, " + \
                                  "сервер " + \
                                  self.c_kernel.c_settings[self.c_kernel.DB_HOST_KEY] + \
                                  " недоступен!", str(ex.pgerror))
            self.close()


    def __form_management(self):
        """ Разрешает/запрещает работу с компонентами формы """

        self.qRefItemLineEdit.setEnabled(self.qModeCheckBox.isChecked())


    def __get_cursor(self):
        """ Возвращает курсор """

        return self.c_kernel.get_connection().cursor()


    def __init_data(self):
        """ Процедура очистки и инициализации контролов """

        self.c_table_guard.init_line_edit(self.qRefItemLineEdit, SINGLE_FIELD_NAME_IDX)


    def __load_data(self):
        """ Процедура загрузки данных из БД в контролы """

        self.c_table_guard.load_line_edit(self.qRefItemLineEdit, SINGLE_FIELD_NAME_IDX)


    def __prepare_form(self):
        """ Выполняет предварительные работы перед выводом окна"""

        if self.c_db_mode == guard.DB_MODE_INSERT:

            self.qModeCheckBox.setCheckState(True)
            self.qModeCheckBox.setEnabled(False)
            self.qOkToolButton.setEnabled(True)
        else:

            self.qModeCheckBox.setCheckState(False)
            self.qModeCheckBox.setEnabled(True)
            self.qOkToolButton.setEnabled(False)
        self.__form_management()


    def __state_changed(self):
        """ Обработчик флажка режима БД """

        self.__form_management()


    def __store_data(self):
        """ Сохраняет данные из контролов в словаре параметров """

        self.c_parameters = dict()
        self.c_parameters["pname"] = self.qRefItemLineEdit.text()
        if self.c_db_mode == guard.DB_MODE_UPDATE:

            self.c_parameters["pid"] = self.c_record_id


    #pylint: disable=no-self-use
    def __validate_data(self):
        """ Функция, осуществляющая проверку введенных данных """

        return len(self.qRefItemLineEdit.text()) > 0
    #pylint: enable=no-self-use


    def append_record(self, p_kernel, p_table_name):
        """ Открывает форму в режиме добавления записи """

        assert p_kernel is not None, "Assert: [CRefItemEdit.append_record]:  \
            No <p_kernel> parameter specified!"
        assert p_table_name is not None, "Assert: [CRefItemEdit.append_record]:  \
            No <p_table_name> parameter specified!"

        self.c_kernel = p_kernel
        self.c_db_mode = guard.DB_MODE_INSERT
        self.c_table_name = p_table_name
        self.c_table_guard = guard.CTableGuard(self.c_kernel, self.c_table_name)
        self.c_table_guard.set_query_for_insert("select {fields[0]} \
                                                 from {table_name[0]} \
                                                 limit 1".format( \
                                                     table_name=[self.c_table_name], \
                                                     fields=["{}"]))
        self.c_table_guard.set_field_list([SINGLE_FIELD_NAME])
        self.c_table_guard.prepare()
        self.__init_data()
        ##ToDo: Обработать возможную ошибку!
        self.__prepare_form()


    def closeEvent(self, p_event):
        """ Обработчик события закрытия формы """

        frm.save_form_pos_and_size(self.c_kernel, self)
        p_event.accept()


    def set_insert_sql(self, p_sql):
        """ Задает запрос для добавления элемента в справочник """

        assert p_sql is not None, "Assert: [CRefItemEdit.set_insert_sql]: \
            No <p_sql> parameter specified!"

        self.c_insert_sql = p_sql


    def set_update_sql(self, p_sql):
        """ Задает запрос для изменения элемента справочника """

        assert p_sql is not None, "Assert: [CRefItemEdit.set_update_sql]: \
            No <p_sql> parameter specified!"

        self.c_update_sql = p_sql


    def view_record(self, p_kernel, p_table_name, p_record_id):
        """ Открывает форму в режиме просмотра записи """

        assert p_kernel is not None, "Assert: [CRefItemEdit.view_record]:  \
            No <p_kernel> parameter specified!"
        assert p_table_name is not None, "Assert: [CRefItemEdit.view_record]:  \
            No <p_table_name> parameter specified!"
        assert p_record_id is not None, "Assert: [CRefItemEdit.view_record]: \
            No <p_record_id> parameter specified!"

        self.c_kernel = p_kernel
        self.c_table_name = p_table_name
        self.c_record_id = p_record_id
        self.c_db_mode = guard.DB_MODE_UPDATE
        self.c_table_guard = guard.CTableGuard(self.c_kernel, self.c_table_name)
        self.c_table_guard.set_query_for_update("select {fields[0]} \
                                                from {table_name[0]} \
                                                where id = %(p_id)s;".format( \
                                                table_name=[self.c_table_name],
                                                fields=["{}"]),
                                                p_record_id)
        self.c_table_guard.set_field_list([SINGLE_FIELD_NAME])
        self.c_table_guard.prepare()
        frm.load_form_pos_and_size(self.c_kernel, self)
        self.__load_data()
        self.__prepare_form()

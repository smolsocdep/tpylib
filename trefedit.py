from PyQt5 import QtWidgets, QtGui, QtCore
import psycopg2
from tpylib import form_ref_edit
from tpylib import tmsgboxes as tmsg, tdebug as deb, tforms as frm


class CRefItemEdit(QtWidgets.QDialog, detailedit.Ui_qRefItemEditDialog):
    """ Класс окна редактирования  таблицы tbl_master """

    # pylint: disable=too-many-instance-attributes
    c_kernel = None
    c_table_guard = None
    c_record_id = None
    c_db_mode = None
    c_parameters = None

    def __init__(self):
        """ Конструктор """

        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        # self.qTable.viewport().installEventFilter(self)
        self.qModeCheckBox.stateChanged.connect(self.__state_changed)
        self.qOkToolButton.clicked.connect(self.__ok_button_pressed)


    def __form_management(self):
        """ Разрешает/запрещает работу с компонентами формы """

        # self.qSubjectLineEdit.setEnabled(self.qModeCheckBox.isChecked())
        pass


    def __get_cursor(self):
        """ Возвращает курсор """

        return self.c_kernel.get_connection().cursor()


    def __init_data(self):
        """ Процедура очистки и инициализации контролов """

        # self.c_table_guard.init_line_edit(self.qSubjectLineEdit, SUBJECT_FIELD_NUMBER)
        pass


    def __load_data(self):
        """ Процедура загрузки данных из БД в контролы """

        # self.c_table_guard.load_line_edit(self.qSubjectLineEdit, SUBJECT_FIELD_NUMBER)
        pass


    def __ok_button_pressed(self):
        """ Обработчик кнопки 'Принять' """

        if self.__validate_data():
            self.accept()


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
        self.c_parameters["pname"] = self.Ui_qRefItemLineEdit.text()
        if self.c_db_mode == guard.DB_MODE_UPDATE:

            self.c_parameters["pid"] = self.c_record_id


    #pylint: disable=no-self-use
    def __validate_data(self):
        """ Функция, осуществляющая проверку введенных данных """

        return True
    #pylint: enable=no-self-use


    def accepted(self):
        """ Обработчик вызывается при вызове accept() или done() """

            #*** Получим номер нового субконтракта
            if self.c_db_mode == guard.DB_MODE_INSERT:

                # l_query = "insert into public.tbl_details ( \
                #                fsubject, fnotice, fregistration_date, \
                #                frecord_date, fnumber, fstatus, \
                #                fcontract, fcontract_type, forganization \
                #                ) VALUES ( \
                #                %(psubject)s, %(pnotice)s, %(pregistration_date)s, \
                #                %(precord_date)s, %(pnumber)s, 1, \
                #                %(pcontract)s, %(pcontract_type)s, %(porganization)s \
                #             );"

            else:

                # l_query = "update public.tbl_details \
                #              set fsubject=%(psubject)s, \
                #                  fnotice=%(pnotice)s, \
                #                  fregistration_date=%(pregistration_date)s, \
                #                  frecord_date=%(precord_date)s, \
                #                  fcontract_type=%(pcontract_type)s, \
                #                  forganization=%(porganization)s \
                #              where id=%(pid)s;"

            ## ToDo: тут try впихнуть
            self.__store_data()
            l_cursor = self.__get_cursor()
            # l_cursor.execute(l_query, self.c_parameters)
            # self.c_kernel.get_connection().commit()
            self.c_parameters = None


    def append_record(self, p_kernel, p_super_contract_id):
        """ Открывает форму в режиме добавления записи """

        assert p_kernel is not None, "Assert: [detail_edit.append_record]:  \
                                     No <p_kernel> parameter specified!"
        assert p_super_contract_id is not None, "Assert: [detail_edit.append_record]: \
                                      No <p_super_contract_id> parameter specified!"

        self.c_kernel = p_kernel
        # self.c_super_contract_id = p_super_contract_id
        self.c_db_mode = guard.DB_MODE_INSERT
        # self.c_contracttypes_combo = combolook.CComboLookup(self.c_kernel,
        #                                                     CONTRACT_TYPE_QUERY)
        # self.c_organizations_combo = combolook.CComboLookup(self.c_kernel,
        #                                                     ORGANIZATIONS_QUERY)
        # self.c_table_guard = guard.CTableGuard(self.c_kernel, "tbl_details")
        # self.c_table_guard.set_query_for_insert("select {} \
        #                                          from public.tbl_details \
        #                                          limit 1")
        # self.c_table_guard.set_field_list(DETAIL_FIELDS)
        self.c_table_guard.prepare()
        self.__init_data()
        self.__prepare_form()


    def closeEvent(self, p_event):
        """ Обработчик события закрытия формы """
        #deb.dout("details: ", self.objectName())

        frm.save_form_pos_and_size(self.c_kernel, self)
        p_event.accept()


        def view_record(self, p_kernel, p_record_id):
            """ Открывает форму в режиме просмотра записи """

            assert p_kernel is not None, "Assert: [detail_edit.view_record]:  \
                                          No <p_kernel> parameter specified!"
            assert p_record_id is not None, "Assert: [detail_edit.view_record]: \
                                             No <p_record_id> parameter specified!"
            self.c_kernel = p_kernel
            self.c_record_id = p_record_id
            self.c_db_mode = guard.DB_MODE_UPDATE
            # self.c_table_guard = guard.CTableGuard(self.c_kernel, "tbl_details")
            # self.c_table_guard.set_query_for_update("select {} \
            #                                         from public.tbl_details \
            #                                         where id = %(p_id)s;",
            #                                         p_record_id)
            # self.c_table_guard.set_field_list(DETAIL_FIELDS)
            self.c_table_guard.prepare()
            frm.load_form_pos_and_size(self.c_kernel, self)
            self.__load_data()
            self.__prepare_form()

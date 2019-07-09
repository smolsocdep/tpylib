""" Класс универсального справочника """

from PyQt5 import QtWidgets, QtGui, QtCore
import psycopg2
from tpylib import form_reference
from tpylib import tmsgboxes as tmsg, tforms as frm #, tdebug as deb
import trefedit as trefed
#pylint: disable=invalid-name
#_grid = [[_background_char for column in range(_max_columns)] for row in range(_max_rows)]
ID_COL_NUMBER = 0
NAME_COL_NUMBER = 1
TABLE_HEADERS = [" ID", "Наименование"]
TABLE_ALIGNS = [QtCore.Qt.AlignLeft, QtCore.Qt.AlignLeft]

class CReference(QtWidgets.QWidget, form_reference.Ui_qReferenceWidget):
    """ Класс реализует универсальный справочник """

    # pylint: disable=too-many-instance-attributes
    c_kernel = None
    c_select_sql = ""
    c_insert_sql = ""
    c_update_sql = ""
    c_delete_sql = ""
    c_check_sql = ""
    c_count_sql = ""
    c_table_name = None
    c_trash_state = 0
    c_filter_state = 0
    c_parameters = None
    c_count_label = None
    c_id_label = None
    c_ref_item_edit = None

    def __init__(self, p_kernel):
        """ Constructor """

        assert p_kernel is not None, "Assert: [CReference.__init__]: \
            No <p_kernel> parameter specified!"

        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.c_kernel = p_kernel
        self.c_ref_item_edit = trefed.CRefItemEdit()
        # deb.dout("treference", "__init__", self)


    def __accept_toolbutton_clicked(self):
        """ Обработчик кнопки qAcceptToolButton """
        pass


    def __add_toolbutton_clicked(self):
        """ Обработчик кнопки qAddToolButton """
        #ToDo: вот тут вставить код для передачи запросов на апдейт/инсерт
        # и вызов CRefItemEdit.append_record

        self.c_ref_item_edit.set_insert_sql(self.c_insert_sql)
        self.c_ref_item_edit.append_record(self.c_kernel, self.c_table_name)


    def __build_sql(self):
        """ Функция возвращает SQL готовый к исполнению"""

        l_sql = self.c_select_sql
        self.c_parameters = dict()
        if self.c_trash_state == 0:

            self.c_parameters["pstatus"] = 1
        else:

            self.c_parameters["pstatus"] = 0

        if self.c_filter_state == 1:
            l_sql += " and (fname like %(pname)s)"
            self.c_parameters["pname"] = "%"+self.qFilterLineEdit.text()+"%"
        #deb.dout("treference", "__build_sql", l_sql)
        return l_sql


    def __get_cursor(self):
        """ Возвращает курсор """

        return  self.c_kernel.get_connection().cursor()


    def __delete_toolbutton_clicked(self):
        """ Обработчик кнопки qDeleteToolButton """
        pass


    def __edit_toolbutton_clicked(self):
        """ Обработчик кнопки qEditToolButton """
        #ToDo: вот тут вставить код для передачи запросов на апдейт/инсерт
        # и вызов CRefItemEdit.view_record
        l_id = frm.get_current_data_column(self.qReferenceTableWidge, ID_COL_NUMBER)
        self.c_ref_item_edit.set_update_sql(self.c_update_sql)
        self.c_ref_item_edit.view_record(self.c_kernel, self.c_table_name, l_id)


    def __filter_toolbutton_clicked(self):
        """ Обработчик кнопки qFilterToolButton """

        #*** В зависимости от состояния фильтра загружаем нужную иконку:
        if self.qFilterLineEdit.text().strip():

            l_icon = QtGui.QIcon()
            if self.c_filter_state == 0:

                #*** Иконка "Отключить фильтр"
                l_icon.addPixmap(QtGui.QPixmap(":/pixmaps/icons/view-filter_off.png"),
                                 QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.c_filter_state = 1
                self.qFilterLineEdit.setReadOnly(True)
                self.qTrashToolButton.setEnabled(False)
            else:

                #*** Иконка "Включить фильтр"
                l_icon.addPixmap(QtGui.QPixmap(":/pixmaps/icons/view-filter_on.png"),
                                 QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.c_filter_state = 0
                self.qFilterLineEdit.setReadOnly(False)
                self.qTrashToolButton.setEnabled(True)

            #*** Выводим иконку и рестартуем выборку
            self.qFilterToolButton.setIcon(l_icon)
            self.__reopen_query(self.__build_sql())


    def __reject_toolbutton_clicked(self):
        """ Обработчик кнопки qRejectToolButton """
        pass


    def __reopen_query(self, p_query_text):
        """ Заполняет таблицу результатами выполнения запроса """

        assert p_query_text is not None, "Assert: [CReference.treference.__reopen_query]: \
            No <p_query_text> parameter specified!"

        try:

            #*** Получим курсор
            l_cursor = self.__get_cursor()
            #*** Получим выборку
            l_cursor.execute(p_query_text, self.c_parameters)
            #*** Параметры больше не нужны
            self.c_parameters = None
            #*** Вытащим все данные из выборки
            l_data = l_cursor.fetchall()
            #*** Получим кол-во строк
            l_rows = len(l_data)
            #*** если выборка не пустая...
            if l_rows > 0:

                #*** Получим к-во столбцов
                l_columns = len(l_data[0])
                #*** Преднастройка таблицы
                frm.pre_tweak_table(self.qReferenceTableWidget, l_rows, l_columns, \
                    [ID_COL_NUMBER], TABLE_HEADERS)
                #*** Заполняем таблицу данными
                frm.fill_table_with_data(self.qReferenceTableWidget, l_data, \
                    TABLE_ALIGNS, None, None)
                #frm.load_table_widget(self.c_kernel, self.qReferenceTableWidget)
                #*** Выводим данные в строку статуса
                self.c_count_label.setText("Всего договоров: "+str(l_rows))
                #*** Пост-настройка таблицы
                self.qReferenceTableWidget.setSortingEnabled(True)
                self.qEditToolButton.setEnabled(True)
                self.qDeleteToolButton.setEnabled(True)
                # deb.dout("treference", "__reopen_query", "filled")
            else:

                #*** Пустая выборка
                self.qReferenceTableWidget.setRowCount(l_rows)
                self.qReferenceTableWidget.clearContents()
                self.qEditToolButton.setEnabled(False)
                self.qDeleteToolButton.setEnabled(False)
                self.c_count_label.setText("Всего договоров: "+str(l_rows))
                # deb.dout("treference", "__reopen_query", "empty")
        except psycopg2.Error as ex:

            tmsg.error_occured("При обращении к базе данных возникла \
                исключительная ситуация!", str(ex.pgerror))


    def __trash_toolbutton_clicked(self):
        """ Обработчик кнопки qTrashToolButton """

        #*** В зависимости от состояния корзины загружаем нужную иконку:
        l_icon = QtGui.QIcon()
        if self.c_trash_state == 0:

            #*** Иконка "Закрыть корзину"
            l_icon.addPixmap(QtGui.QPixmap(":/pixmaps/icons/user-trash-exit.png"),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.c_trash_state = 1
            self.qFilterLineEdit.setEnabled(False)
            self.qFilterToolButton.setEnabled(False)
        else:

            #*** Иконка "Открыть корзину"
            l_icon.addPixmap(QtGui.QPixmap(":/pixmaps/icons/user-trash.png"),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.c_trash_state = 0
            self.qFilterLineEdit.setEnabled(True)
            self.qFilterToolButton.setEnabled(True)
        #*** Выводим иконку и рестартуем выборку
        self.qTrashToolButton.setIcon(l_icon)
        self.__reopen_query(self.__build_sql())


    def closeEvent(self, p_event):
        """ Обработчик события закрытия формы """

        assert p_event is not None, "Assert: [CReference.closeEvent]: \
            No <p_event> parameter specified!"

        frm.save_form_pos_and_size(self.c_kernel, self)
        #frm.save_table_widget(self.c_kernel, self.qReferenceTableWidget)
        p_event.accept()


    def initialization(self):
        """ Выполняет подготовительные действия для формы """

        self.qAddToolButton.clicked.connect(self.__add_toolbutton_clicked)
        self.qEditToolButton.clicked.connect(self.__edit_toolbutton_clicked)
        self.qDeleteToolButton.clicked.connect(self.__delete_toolbutton_clicked)
        self.qTrashToolButton.clicked.connect(self.__trash_toolbutton_clicked)
        self.qFilterToolButton.clicked.connect(self.__filter_toolbutton_clicked)
        self.qAcceptToolButton.clicked.connect(self.__accept_toolbutton_clicked)
        self.qRejectToolButton.clicked.connect(self.__reject_toolbutton_clicked)
        #*** Строка статуса
        self.c_count_label = QtWidgets.QLabel("Всего договоров: ")
        self.qStatusBar.addWidget(self.c_count_label)
        self.c_id_label = QtWidgets.QLabel("ID: ")
        self.qStatusBar.addWidget(self.c_id_label)
        # l_width = self.qReferenceTableWidget.width()
        # deb.dout("treference", "initialization", l_width)
        frm.load_form_pos_and_size(self.c_kernel, self)
        # #***** Выполняем запрос
        self.__reopen_query(self.__build_sql())
        self.qReferenceTableWidget.horizontalHeader().resizeSections( \
            QtWidgets.QHeaderView.ResizeToContents)


    def keyPressEvent(self, p_event):
        """ Обработчик событий от клавиатуры """

        assert p_event is not None, "Assert: [CReference.keyPressEvent]: \
            No <p_event> parameter specified!"
        #*** Если это событие от клавиатуры...
        if isinstance(p_event, QtGui.QKeyEvent):

            #*** Если нажали Escape - закрываем программу
            if p_event.key() == QtCore.Qt.Key_Escape:

                #self.__exit_action_triggered()
                self.close()
                p_event.accept()

                #*** Если нажаты Ctrl-F12 и фокус в поле фильтра - включаем фильтр
            elif (p_event.key() == QtCore.Qt.Key_F12) and \
                   (self.qFilterLineEdit.hasFocus()):

                self.__filter_toolbutton_clicked()

            else:
                p_event.ignore()


    def set_check_sql(self, p_sql):
        """ Задает запрос для проверки того, что элемент справочника используется """

        assert p_sql is not None, "Assert: [CReference.set_check_sql]: \
            No <p_sql> parameter specified!"

        self.c_check_sql = p_sql


    def set_count_sql(self, p_sql):
        """ Задает запрос для подсчёта элементов справочника """

        assert p_sql is not None, "Assert: [CReference.set_count_sql]: \
            No <p_sql> parameter specified!"
        assert self.c_table_name is not None, "Assert: [CReference.set_count_sql]: \
            Function <set_table_name> must be called before that function!"

        self.c_count_sql = p_sql.format(table_name=[self.c_table_name])


    def set_delete_sql(self, p_sql):
        """ Задает запрос для удаления элемента справочника """

        assert p_sql is not None, "Assert: [CReference.set_delete_sql]: \
            No <p_sql> parameter specified!"
        assert self.c_table_name is not None, "Assert: [CReference.set_delete_sql]: \
            Function <set_table_name> must be called before that function!"

        self.c_delete_sql = p_sql.format(table_name=[self.c_table_name])


    def set_insert_sql(self, p_sql):
        """ Задает запрос для добавления элемента в справочник """

        assert p_sql is not None, "Assert: [CReference.set_insert_sql]: \
            No <p_sql> parameter specified!"
        assert self.c_table_name is not None, "Assert: [CReference.set_insert_sql]: \
            Function <set_table_name> must be called before that function!"

        self.c_insert_sql = p_sql.format(table_name=[self.c_table_name])


    def set_select_sql(self, p_sql):
        """ Задает запрос для выборки для просмотра справочника """

        assert p_sql is not None, "Assert: [CReference.set_select_sql]: \
            No <p_sql> parameter specified!"
        assert self.c_table_name is not None, "Assert: [CReference.set_select_sql]: \
            Function <set_table_name> must be called before that function!"

        self.c_select_sql = p_sql.format(table_name=[self.c_table_name])


    def set_table_name(self, p_table_name):
        """ Задает имя таблицы справочника """

        assert p_table_name is not None, "Assert: [CReference.set_table_name]: \
            No <p_table_name> parameter specified!"

        self.c_table_name = p_table_name


    def set_update_sql(self, p_sql):
        """ Задает запрос для изменения элемента справочника """

        assert p_sql is not None, "Assert: [CReference.set_update_sql]: \
            No <p_sql> parameter specified!"
        assert self.c_table_name is not None, "Assert: [CReference.set_update_sql]: \
            Function <set_table_name> must be called before that function!"

        self.c_update_sql = p_sql.format(table_name=[self.c_table_name])

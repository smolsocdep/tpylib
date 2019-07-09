""" Данный модуль содержит процедуры, необходимые для создания окон с таблицами """

import os
import os.path
import configparser
from PyQt5 import QtWidgets, QtCore, QtGui
import constants as cns
#from tpylib import tdebug as deb

def calculate_summary_width_of_content(p_widthes, p_columns, p_hidden_columns):
    """ Вычисляет суммарную длину списка """

    assert p_widthes is not None, "Assert: [tforms.calculate_summary_width_of_content]: \
        No <p_widthes> parameter specified!"
    assert p_columns is not None, "Assert: [tforms.calculate_summary_width_of_content]: \
        No <p_columns> parameter specified!"
    assert p_hidden_columns is not None, "Assert: [tforms.calculate_summary_width_of_content]: \
        No <p_hidden_columns> parameter specified!"

    l_sum_width = 0
    for l_column in range(p_columns):

        if l_column not in p_hidden_columns:
            l_sum_width += p_widthes[l_column]
    return l_sum_width


def calculate_table_columns_width(p_widget, p_hidden_columns):
    """ Устанавливает ширину столбцов таблицы в зависимости от содержимого """

    assert p_widget is not None, "Assert: [tforms.calculate_table_columns_width]: \
        No <p_widget> parameter specified!"
    assert p_hidden_columns is not None, "Assert: [tforms.calculate_table_columns_width]: \
        No <p_hidden_columns> parameter specified!"

    #*** Получим длины содержимого столбцов
    l_widthes = get_table_cells_value_lengths(p_widget)

    #*** Рассчитаем процент ширины таблицы
    l_table_width = p_widget.width()# так надо!
    l_table_width -= (l_table_width/100)*6
    l_table_width_percent = (l_table_width) / 100

    #*** Получим общую длину содержимого столбцов и рассчит. процент
    ## To do: Вынести расчет суммарной ширины содержимого в отдельную процедуру
    l_sum_width = calculate_summary_width_of_content(l_widthes, p_widget.columnCount(), \
        p_hidden_columns)
    l_sum_width_percent = l_sum_width / 100

    #*** Нет ли у нас столбцов, которые будут короче 32 пикселей?
    #columnwidth=(32/(tabwidth/100))*(summwidth/100)
    l_minimal_width = int((32/l_table_width_percent)*l_sum_width_percent) + 1
    l_recalc_flag = False
    for l_column in range(p_widget.columnCount()):

        if l_column not in p_hidden_columns:

            if l_widthes[l_column] < l_minimal_width:

                l_widthes[l_column] = l_minimal_width
                l_recalc_flag = True

    #*** Пересчет нужен?
    if l_recalc_flag:
        l_sum_width = calculate_summary_width_of_content(l_widthes, \
            p_widget.columnCount(), p_hidden_columns)
        l_sum_width_percent = l_sum_width / 100

    #*** Рассчитаем коэффициенты для каждого столбца
    l_coefficients = dict()
    for l_column in range(p_widget.columnCount()):

        if l_column not in p_hidden_columns:

            l_coefficients[l_column] = l_widthes[l_column] / l_sum_width_percent

    #*** Рассчитываем и выставляем ширины столбцов
    for l_column in range(p_widget.columnCount()):

        if l_column not in p_hidden_columns:

            l_column_width = int(l_table_width_percent * l_coefficients[l_column])
            p_widget.setColumnWidth(l_column, l_column_width)


def colorize_item(p_colors, p_data, p_row, p_color_column, p_item):
    """ Раскрашивает элемент таблицы """

    assert p_colors is not None, "Assert: [tforms.colorize_item]: \
        No <p_colors> parameter specified!"
    assert p_data is not None, "Assert: [tforms.colorize_item]: \
        No <p_data> parameter specified!"
    assert p_row is not None, "Assert: [tforms.colorize_item]: \
        No <p_row> parameter specified!"
    assert p_color_column is not None, "Assert: [tforms.colorize_item]: \
        No <p_color_column> parameter specified!"
    assert p_item is not None, "Assert: [tforms.colorize_item]: \
        No <p_item> parameter specified!"

    l_color_index = p_data[p_row][p_color_column]
    l_color = p_colors[l_color_index-1]
    p_item.setBackground(QtGui.QBrush(l_color))


def fill_table_with_data(p_widget, p_data, p_aligns, p_color_column, p_colors):
    """ Заполняет таблицу данными """

    assert p_widget is not None, "Assert: [tforms.fill_table_with_data]: \
        No <p_widget> parameter specified!"
    assert p_data is not None, "Assert: [tforms.fill_table_with_data]: \
        No <p_data> parameter specified!"
    assert p_aligns is not None, "Assert: [tforms.fill_table_with_data]: \
        No <p_aligns> parameter specified!"
    # assert p_color_column is not None, "Assert: [tforms.fill_table_with_data]: \
    #     No <p_color_column parameter specified!"
    # assert p_colors is not None, "Assert: [tforms.fill_table_with_data]: \
    #     No <p_colors> parameter specified!"

    ## To Do: получть из табль p_rows, p_cols
    #*** перебираем строки
    for l_row in range(p_widget.rowCount()):

        #*** перебираем столбцы
        for l_column in range(p_widget.columnCount()):

            #*** создаем элемент таблицы и инициализируем его данными
            l_text = str(p_data[l_row][l_column])
            l_item = QtWidgets.QTableWidgetItem(l_text)
            l_item.setTextAlignment(p_aligns[l_column] | QtCore.Qt.AlignVCenter)
            #*** Добавляем новый элемент в таблицу
            p_widget.setItem(l_row, l_column, l_item)

            #*** Раскрашиваем строку
            if p_color_column is not None and p_colors is not None:
                colorize_item(p_colors, p_data, l_row, p_color_column, l_item)
    p_widget.setCurrentCell(0, 0)


def get_current_data_column(p_widget, p_column):
    """ Возвращает содержимое запрошенного столбца в выбранной строке """

    assert p_widget is not None, "Assert: [tforms.get_current_data_column]: \
        No <p_widget> parameter specified!"
    assert p_column is not None, "Assert: [tforms.get_current_data_column]: \
        No <p_column> parameter specified!"

    l_row = p_widget.currentRow()
    l_item = p_widget.item(l_row, p_column)
    return str(l_item.text())


def get_table_cells_value_lengths(p_widget):
    """ Возвращает список длин содержимого ячеек текущей строки """

    assert p_widget is not None, "Assert: [tforms.get_table_cells_value_lengths]: \
        No <p_widget> parameter specified!"

    l_row = p_widget.currentRow()
    l_widthes = dict()
    for l_column in range(p_widget.columnCount()):
        l_len = len(str(p_widget.item(l_row, l_column).text()))
        l_widthes[l_column] = l_len
    return l_widthes


def get_etc_folder(p_kernel):
    """ Возвращает строку с путём к каталогу etc """

    assert p_kernel is not None, "Assert: [tforms.get_etc_folder]: \
        No <p_kernel> parameter specified!"

    l_folder = p_kernel.get_settings()[cns.PRG_PROGRAM_FOLDER_KEY]
    l_folder += cns.ETC_FOLDER
    if not os.path.exists(l_folder):
        os.mkdir(l_folder)
    return l_folder


def load_form_pos_and_size(p_kernel, p_form):
    """ Читает положение и размеры формы из ini-файла """

    assert p_kernel is not None, "Assert: [tforms.load_form_pos_and_size]: \
        No <p_kernel> parameter specified!"
    assert p_form is not None, "Assert: [tforms.load_form_pos_and_size]: \
        No <p_form> parameter specified!"

    l_folder = get_etc_folder(p_kernel)
    if l_folder:

        #*** Прочитаем словарь из ini-шки
        l_folder += p_form.objectName() + ".ini"
        l_config = configparser.ConfigParser()
        l_config.read(l_folder)
        #*** Прочитаем параметры формы из словаря
        try:

            #*** Выставим положение формы
            l_top = l_config[cns.FORM_SECTION]["top"]
            l_left = l_config[cns.FORM_SECTION]["left"]
            p_form.move(int(l_left), int(l_top))
            #*** Выставим размеры формы
            l_height = l_config[cns.FORM_SECTION]["height"]
            l_width = l_config[cns.FORM_SECTION]["width"]
            p_form.resize(int(l_width), int(l_height))
            #*** Прочитаем и установим размер шрифта таблицы
        except KeyError:

            #*** В инишке нет каких-то данных, ничего не делаем
            pass


def load_table_widget(p_kernel, p_widget):
    """ Восстанавливает настройки QtTableWidget """

    assert p_kernel is not None, "Assert: [tforms.save_table_widget]: \
        No <p_kernel> parameter specified!"
    assert p_widget is not None, "Assert: [tforms.save_table_widget]: \
        No <p_widget> parameter specified!"

    l_folder = get_etc_folder(p_kernel) + p_widget.objectName() + ".ini"
    # deb.dout("load_table_widget", l_folder)
    if os.path.exists(l_folder):
        #*** Заполним словарь
        l_config = configparser.ConfigParser()
        l_config.read(l_folder)
        #for l_item in l_config:
        # deb.dout("load_table_widget", l_config[cns.TABLE_SECTION])
        for l_col_number in range(p_widget.columnCount()):

            if l_config[cns.TABLE_SECTION][str(l_col_number)]:

                l_width = l_config[cns.TABLE_SECTION][str(l_col_number)]
                p_widget.setColumnWidth(l_col_number, int(l_width))


def pre_tweak_table(p_widget, p_rows, p_columns, p_hide_columns, p_headers):
    """ Производит настройки таблицы """

    assert p_widget is not None, "Assert: [tforms.pre_tweak_table]: \
        No <p_widget> parameter specified!"
    assert p_columns is not None, "Assert: [tforms.pre_tweak_table]: \
        No <p_columns> parameter specified!"
    assert p_rows is not None, "Assert: [tforms.pre_tweak_table]: \
        No <p_rows> parameter specified!"
    assert p_hide_columns is not None, "Assert: [tforms.pre_tweak_table]: \
        No <p_hide_columns> parameter specified!"
    assert p_headers is not None, "Assert: [tforms.pre_tweak_table]: \
        No <p_headers> parameter specified!"

    #*** Чистим таблицу
    p_widget.clear()
    #*** К-во столбцов
    p_widget.setColumnCount(p_columns)
    #*** К-во строк
    p_widget.setRowCount(p_rows)
    #*** прячем столбцы
    for l_column in p_hide_columns:
        p_widget.hideColumn(l_column)
    #*** Задаем наименования столбцов
    p_widget.setHorizontalHeaderLabels(p_headers)
    #*** Запретим прямое редактирование таблицы
    p_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    #*** Запрещаем сортировку для избежания глюков
    p_widget.setSortingEnabled(False)


def save_form_pos_and_size(p_kernel, p_form):
    """ Сохраняет положение и размеры формы в ini-файл """

    assert p_kernel is not None, "Assert: [tforms.save_form_pos_and_size]: \
        No <p_kernel> parameter specified!"
    assert p_form is not None, "Assert: [tforms.save_form_pos_and_size]: \
        No <p_form> parameter specified!"

    l_folder = get_etc_folder(p_kernel)
    #*** Заполним словарь
    l_config = configparser.ConfigParser()
    l_config[cns.FORM_SECTION] = {}
    l_config[cns.FORM_SECTION]["top"] = str(p_form.y())
    l_config[cns.FORM_SECTION]["left"] = str(p_form.x())
    l_config[cns.FORM_SECTION]["height"] = str(p_form.height())
    l_config[cns.FORM_SECTION]["width"] = str(p_form.width())
    #*** и сохраним его.
    # deb.dout("save_form_pos_and_size", l_folder+p_form.objectName()+".ini")
    with open(l_folder+p_form.objectName()+".ini", "w") as l_ini_file:

        l_config.write(l_ini_file)


def save_table_widget(p_kernel, p_widget):
    """ Сохраняет настройки QtTableWidget """

    assert p_kernel is not None, "Assert: [tforms.save_table_widget]: \
        No <p_kernel> parameter specified!"
    assert p_widget is not None, "Assert: [tforms.save_table_widget]: \
        No <p_widget> parameter specified!"

    l_folder = get_etc_folder(p_kernel)

    #*** Заполним словарь
    l_config = configparser.ConfigParser()
    l_config[cns.TABLE_SECTION] = {}
    l_config[cns.TABLE_SECTION]["count"] = str(p_widget.columnCount())
    for l_col_number in range(p_widget.columnCount()):
        l_config[cns.TABLE_SECTION][str(l_col_number)] = str(p_widget.columnWidth(l_col_number))
    l_config[cns.TABLE_SECTION]["fontsize"] = str(p_widget.font().pointSize())
    with open(l_folder+p_widget.objectName()+".ini", "w") as l_ini_file:

        l_config.write(l_ini_file)

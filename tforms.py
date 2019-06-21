""" Данный модуль содержит процедуры, необходимые для создания окон с таблицами """

#from PyQt5 import QtGui #QtCore, QtWidgets,
import os
import configparser
import constants as cns
from tpylib import tdebug as deb


def calculate_table_columns_width(p_widget):
    """ Устанавливает ширину столбцов таблицы в зависимости от содержимого """

    assert p_widget is not None, "Assert: [tforms.calculate_table_columns_width]: \
        No <p_widget> parameter specified!"
    l_widthes = get_table_cells_value_lengths(p_widget)


def get_table_cells_value_lengths(p_widget):
    """ Возвращает список длин содержимого ячеек текущей строки """

    assert p_widget is not None, "Assert: [tforms.get_table_cells_value_lengths]: \
        No <p_widget> parameter specified!"

    l_row = p_widget.currentRow()
    l_widthes = dict()
    for l_column in range(p_widget.columnCount()):
        # l_item = p_widget.item(l_row, l_column)
        # l_data = str(l_item.text())
        # l_widthes[l_column] = len(l_data)
        l_widthes[l_column] = len(str(p_widget.item(l_row, l_column)))
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

    l_folder = get_etc_folder(p_kernel)
    #*** Заполним словарь
    l_config = configparser.ConfigParser()
    l_config.read(l_folder)
    #deb.dout(p_widget.columnCount())

    for l_col_number in range(p_widget.columnCount()):

        #deb.dout(l_col_number, l_config[cns.TABLE_SECTION][l_col_number])
        if l_config[cns.TABLE_SECTION][str(l_col_number)]:

            l_width = l_config[cns.TABLE_SECTION][str(l_col_number)]
            p_widget.setColumnWidth(l_col_number, int(l_width))
            deb.dout(l_col_number, l_width)


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

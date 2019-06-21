""" Данный модуль содержит процедуры, необходимые для создания окон с таблицами """

from PyQt5 import QtCore, QtWidgets, QtGui
import configparser
import constants as cns
import os


def load_form_pos_and_size(p_kernel, p_form):
        """ Читает положение и размеры формы из ini-файла """

        assert p_kernel is not None, "Assert: [tforms.load_form_pos_and_size]: \
            No <p_kernel> parameter specified!"
        assert p_form is not None, "Assert: [tforms.load_form_pos_and_size]: \
            No <p_form> parameter specified!"

        #*** Определим, где лежит Ini-шка с параметрами формы
        l_folder = p_kernel.get_settings()[cns.PRG_PROGRAM_FOLDER_KEY]
        l_folder += cns.ETC_FOLDER
        if os.path.exists(l_folder):

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


def save_form_pos_and_size(p_kernel, p_form):
        """ Сохраняет положение и размеры формы в ini-файл """

        assert p_kernel is not None, "Assert: [tforms.save_form_pos_and_size]: \
            No <p_kernel> parameter specified!"
        assert p_form is not None, "Assert: [tforms.save_form_pos_and_size]: \
            No <p_form> parameter specified!"

        #*** Определим, куда нужно сохранять Ini-шку
        l_folder = p_kernel.get_settings()[cns.PRG_PROGRAM_FOLDER_KEY]
        l_folder += cns.ETC_FOLDER
        if not os.path.exists(l_folder):
            os.mkdir(l_folder)
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

    #*** Определим, куда нужно сохранять Ini-шку
    l_folder = p_kernel.get_settings()[cns.PRG_PROGRAM_FOLDER_KEY]
    l_folder += cns.ETC_FOLDER
    if not os.path.exists(l_folder):
        os.mkdir(l_folder)
    #*** Заполним словарь
    l_config = configparser.ConfigParser()
    l_config[cns.TABLE_SECTION] = {}
    l_config[cns.TABLE_SECTION]["count"] = str(p_widget.columnCount())
    for l_col_number in range p_widget.columnCount():
        l_config[cns.TABLE_SECTION][l_col_number] = str(p_widget.columnWidth(l_col_number))
    l_config[cns.TABLE_SECTION]["fontsize"] = str(p_widget.font().pointSize())
    with open(l_folder+p_widget.objectName()+".ini", "w") as l_ini_file:

            l_config.write(l_ini_file)

def load_table_widget(p_kernel, p_widget):
    """ Восстанавливает настройки QtTableWidget """

    assert p_kernel is not None, "Assert: [tforms.save_table_widget]: \
        No <p_kernel> parameter specified!"
    assert p_widget is not None, "Assert: [tforms.save_table_widget]: \
        No <p_widget> parameter specified!"

    #*** Определим, куда нужно сохранять Ini-шку
    l_folder = p_kernel.get_settings()[cns.PRG_PROGRAM_FOLDER_KEY]
    l_folder += cns.ETC_FOLDER
    if os.path.exists(l_folder):
        l_folder += p_widget.objectName() + ".ini"
    #*** Заполним словарь
    l_config = configparser.ConfigParser()
    l_config.read(l_folder)

    for l_col_number in range p_widget.columnCount():

        if l_config[cns.TABLE_SECTION][l_col_number]:

            l_width = l_config[cns.TABLE_SECTION][l_col_number]
            p_widget.setColumnWidth(l_width)

    if l_config[cns.TABLE_SECTION]["fontsize"]:

        l_font = p_widget.font()
        l_font.setPointSize(int(l_config[cns.TABLE_SECTION]["fontsize"]))
        p_widget.setFont(l_font)

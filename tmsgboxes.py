""" Модуль содержит процедуры вызова стандартных диалоговых окон """

from PyQt5.QtWidgets import *

def askYesOrNo(p_text):
    """ Процедура вызывает стандартное окно выбора одной \
        из двух альтернатив и возвращает True в случае нажатия \
        кнопки <Yes> и False - если была нажата <No> """

    l_msgbox = QMessageBox()
    l_msgbox.setWindowTitle("Внимание!")
    l_msgbox.setInformativeText(p_text)
    l_msgbox.setIcon(QMessageBox.Question)
    l_msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    l_msgbox.setDefaultButton(QMessageBox.No)
    l_msgbox.setEscapeButton(QMessageBox.Close)
    return (l_msgbox.exec() == QMessageBox.Yes)


def errorOccured(p_text,p_inform_text=""):
    """ Процедура выводит стандартное сообщение об ошибке """

    l_msgbox = QMessageBox()
    l_msgbox.setWindowTitle("Ошибка!!")
    l_msgbox.setText(p_text)
    l_msgbox.setInformativeText(p_inform_text)
    l_msgbox.setIcon(QMessageBox.Critical)
    l_msgbox.setStandardButtons(QMessageBox.Ok)
    l_msgbox.setDefaultButton(QMessageBox.Ok)
    l_msgbox.setEscapeButton(QMessageBox.Ok)
    l_msgbox.exec()

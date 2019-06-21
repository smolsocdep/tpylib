""" Модуль отладочных процедур """


import constants as const

def dout(*params):
    """ Процедура вывода отладочной информации """

    if const.__DEBUG__:
        print(params)

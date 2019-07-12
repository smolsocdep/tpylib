""" Модуль отладочных процедур """

__DEBUG__ = True

def dout(*params):
    """ Процедура вывода отладочной информации """

    if __DEBUG__:
        print(params)

""" Класс универсального справочника """

class CComboLookup():
    """ Класс реализует универсальный справочник """

    c_kernel = None
    c_select_sql = ""
    c_insert_sql = ""
    c_update_sql = ""
    c_delete_sql = ""
    c_check_sql = ""
    с_count_sql = ""

    def __init__(self, p_kernel):
        """ Constructor """

        assert p_kernel is not None, "Assert: [combo_lookup.__init__]:
            No <p_kernel> parameter specified!"

        # assert p_query is not None, "Assert: [combo_lookup.__init__]: \
        #     No <p_query> parameter specified!"
        self.c_kernel = p_kernel


    def set_select_sql(self, p_sql):
        """ Задает запрос для выборки для просмотра справочника """

        assert p_sql is not None, "Assert: [combo_lookup.set_select_sql]:
            No <p_sql> parameter specified!"

        self.c_select_sql = p_sql


    def set_insert_sql(self, p_sql):
        """ Задает запрос для добавления элемента в справочник """

        assert p_sql is not None, "Assert: [combo_lookup.set_insert_sql]:
            No <p_sql> parameter specified!"

        self.c_insert_sql = p_sql


    def set_update_sql(self, p_sql):
        """ Задает запрос для изменения элемента справочника """

        assert p_sql is not None, "Assert: [combo_lookup.set_update_sql]:
            No <p_sql> parameter specified!"

        self.c_update_sql = p_sql


    def set_delete_sql(self, p_sql):
        """ Задает запрос для удаления элемента справочника """

        assert p_sql is not None, "Assert: [combo_lookup.set_delete_sql]:
            No <p_sql> parameter specified!"

        self.c_delete_sql = p_sql


    def set_check_sql(self, p_sql):
        """ Задает запрос для проверки того, что элемент справочника используется """

        assert p_sql is not None, "Assert: [combo_lookup.set_check_sql]:
            No <p_sql> parameter specified!"

        self.c_check_sql = p_sql


    def set_count_sql(self, p_sql):
        """ Задает запрос для подсчёта элементов справочника """

        assert p_sql is not None, "Assert: [combo_lookup.set_count_sql]:
            No <p_sql> parameter specified!"

        self.c_count_sql = p_sql

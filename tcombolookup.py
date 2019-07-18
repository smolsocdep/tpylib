""" Модуль реализует класс CComboLookup """
import psycopg2
from tpylib import tmsgboxes as tmsg
from tpylib import tdebug as deb
class CComboLookup():
    """ Класс реализует Lookup Combobox """

    def __init__(self, p_kernel, p_query):
        """ Constructor """
        self.c_id_dict = {}
        self.c_kernel = None
        self.c_query = None

        assert p_kernel is not None, "Assert: [CComboLookup.__init__]: \
            No <p_kernel> parameter specified!"
        assert p_query is not None, "Assert: [CComboLookup.__init__]: \
            No <p_query> parameter specified!"

        self.c_kernel = p_kernel
        #*** В запросе должно быть только два поля - идентификатор и текст,
        #*** идентификатор должен быть первым
        self.c_query = p_query


    def load(self, p_combobox):
        """ Загружает данные в комбобокс """

        assert p_combobox is not None, "Assert: [CComboLookup.load]: \
            No <p_combobox> parameter specified!"
        self.c_id_dict.clear()
        l_source_cursor = self.c_kernel.get_connection().cursor()
        try:

            #*** Получим выборку
            l_source_cursor.execute(self.c_query)
            l_source_data = l_source_cursor.fetchall()
            l_row_num = 0
            #*** Обходим выборку
            if l_source_data:

                for l_row in l_source_data:

                    p_combobox.addItem(l_row[1])
                    self.c_id_dict[l_row_num] = l_row[0]
                    l_row_num += 1
                p_combobox.setCurrentIndex(0)
            return True
        except psycopg2.Error as ex:

            tmsg.error_occured("При обращении к базе данных возникла " + \
                  "исключительная ситуация, возможно, " + \
                  "сервер " + \
                  self.c_kernel.c_settings[self.c_kernel.DB_HOST_KEY] + \
                  " недоступен!", str(ex.pgerror))
            return False


    def find_index_by_id(self, p_id):
        """ Производит поиск в словаре по заданному ID """

        assert p_id is not None, "Assert: [CComboLookup.find_index_by_id]: \
            No <p_id> parameter specified!"

        #print("## find.id:",p_id)
        for l_key in self.c_id_dict:

            if self.c_id_dict[l_key] == p_id:

                return l_key
        return None


    def find_id_by_index(self, p_index):
        """ Возвращает ID по заданному индексу """

        assert p_index is not None, "Assert: [CComboLookup.find_id_by_index]: \
            No <p_index> parameter specified!"

        return self.c_id_dict[p_index]


    def load_and_select(self, p_combobox, p_id):
        """Загружает данные в комбо и выбирает строку с заданным ID """

        assert p_combobox is not None, "Assert: [CComboLookup.load_and_select]: \
            No <p_combobox> parameter specified!"
        assert p_id is not None, "Assert: [CComboLookup.load_and_select]: \
            No <p_id> parameter specified!"

        if self.load(p_combobox):

            self.select_item(p_combobox, p_id)
            return True
        return False


    def select_item(self, p_combobox, p_id):
        """ Находит индекс заданного ID и выбирает этот пункт в комбо """

        assert p_combobox is not None, "Assert: [CComboLookup.load_and_select]: \
            No <p_combobox> parameter specified!"
        assert p_id is not None, "Assert: [CComboLookup.load_and_select]: \
            No <p_id> parameter specified!"

        l_index = self.find_index_by_id(p_id)
        if l_index is not None:

            p_combobox.setCurrentIndex(l_index)


    def print_dict(self, p_count):
        """ Выводит содержимое словаря """

        l_idx = 0
        l_count = p_count if p_count is not None else 10
        for l_key in self.c_id_dict:

            print("Key:", l_key, "Value:", self.c_id_dict[l_key])
            l_idx += 1
            if l_idx == l_count:
                break

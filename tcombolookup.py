""" Модуль реализует класс CComboLookup """
import psycopg2
from tpylib import tmsgboxes as tmsg
# from tpylib import tdebug as deb
class CComboLookup():
    """ Класс реализует Lookup Combobox """

    def __init__(self, p_combobox, p_kernel, p_query):
        """ Constructor """

        self.c_id_dict = {}
        self.c_kernel = None
        self.c_query = None
        self.c_combobox = None

        assert p_combobox is not None, "Assert: [CComboLookup.__init__]: \
            No <p_combobox> parameter specified!"
        assert p_kernel is not None, "Assert: [CComboLookup.__init__]: \
            No <p_kernel> parameter specified!"
        assert p_query is not None, "Assert: [CComboLookup.__init__]: \
            No <p_query> parameter specified!"

        self.c_combobox = p_combobox
        self.c_kernel = p_kernel
        #*** В запросе должно быть только два поля - идентификатор и текст,
        #*** идентификатор должен быть первым
        self.c_query = p_query

    def __load(self):
        """ Загружает данные в комбобокс """

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

                    self.c_combobox.addItem(l_row[1])
                    self.c_id_dict[l_row_num] = l_row[0]
                    l_row_num += 1
                self.c_combobox.setCurrentIndex(0)
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


    def find_id_by_index(self):
        """ Возвращает ID по заданному индексу """

        return(self.c_id_dict[self.c_combobox.currentIndex()])


    def load_and_select(self, p_id):
        """Загружает данные в комбо и выбирает строку с заданным ID """

        assert p_id is not None, "Assert: [CComboLookup.load_and_select]: \
            No <p_id> parameter specified!"

        if self.__load():

            self.select_item(self.c_combobox, p_id)
            return True
        return False


    def select_item(self, p_id):
        """ Находит индекс заданного ID и выбирает этот пункт в комбо """

        assert p_id is not None, "Assert: [CComboLookup.load_and_select]: \
            No <p_id> parameter specified!"

        l_index = self.find_index_by_id(p_id)
        if l_index is not None:

            self.c_combobox.setCurrentIndex(l_index)


    def print_dict(self, p_count):
        """ Выводит содержимое словаря """

        l_idx = 0
        l_count = p_count if p_count is not None else 10
        for l_key in self.c_id_dict:

            print("Key:", l_key, "Value:", self.c_id_dict[l_key])
            l_idx += 1
            if l_idx == l_count:
                break

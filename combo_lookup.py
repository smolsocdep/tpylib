'''
Created on 28 мая 2019 г.

@author: pakhomenkov
'''

class CComboLookup():
    """ Класс реализует Lookup Combobox """

    c_kernel = None
    c_query = None
    c_id_dict = {}

    def __init__(self, p_kernel, p_query):
        """ Constructor """

        assert p_kernel is not None, "Assert: [combo_lookup.__init__]: \
            No <p_kernel> parameter specified!"
        assert p_query is not None, "Assert: [combo_lookup.__init__]: \
            No <p_query> parameter specified!"

        self.c_kernel = p_kernel
        #*** В запросе должно быть только два поля - идентификатор и текст,
        #*** идентификатор должен быть первым
        self.c_query = p_query


    def load(self, p_combobox):
        """ Загружает данные в комбобокс """

        assert p_combobox is not None, "Assert: [combo_lookup.load]: \
            No <p_combobox> parameter specified!"

        l_source_cursor = self.c_kernel.get_connection().cursor()
        #*** Получим выборку
        l_source_cursor.execute(self.c_query)
        l_source_data = l_source_cursor.fetchall()
        #*** Обходим выборку
        if l_source_data:

            for l_row in l_source_data:

                p_combobox.addItem(l_row[1])
                self.c_id_dict[p_combobox.count()-1] = l_row[0]


    def find_index_by_id(self, p_id):
        """ Производит поиск в словаре по заданному ID """

        assert p_id is not None, "Assert: [combo_lookup.find_index_by_id]: \
            No <p_id> parameter specified!"

        # print()
        for l_key in self.c_id_dict:

            if self.c_id_dict[l_key] == p_id:

                return l_key
        return None


    def find_id_by_index(self, p_index):
        """ Возвращает ID по заданному индексу """

        assert p_index is not None, "Assert: [combo_lookup.find_id_by_index]: \
            No <p_index> parameter specified!"

        return self.c_id_dict[p_index]


    def load_and_select(self, p_combobox, p_id):
        """Загружает данные в комбо и выбирает строку с заданным ID """

        assert p_combobox is not None, "Assert: [combo_lookup.load_and_select]: \
            No <p_combobox> parameter specified!"
        assert p_id is not None, "Assert: [combo_lookup.load]: \
            No <p_id> parameter specified!"

        self.load(p_combobox)
        # print("ID: ", p_id)
        l_index = self.find_index_by_id(p_id)
        # print("Index: ", l_index)
        if l_index:
            p_combobox.setCurrentIndex(l_index)

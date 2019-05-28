'''
Created on 28 мая 2019 г.

@author: pakhomenkov
'''

class CComboLookup(object):
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
            #print(self.c_id_dict)
        
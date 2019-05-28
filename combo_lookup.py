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
        self.c_query = p_query
        
        
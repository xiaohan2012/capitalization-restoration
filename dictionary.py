import codecs


class ItemListDictionary(set):
    def __init__(self, line_dictionary_path):
        with codecs.open(line_dictionary_path, 'r', 'utf8') as f:
            item_list = [l.strip() for l in f]
        super(ItemListDictionary, self).__init__(item_list)
    
    def check(self, obj):
        return obj in self

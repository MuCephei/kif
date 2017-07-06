class Autovivifier:
    def __init__(self, fct):
        self.fct = fct
        self.items = dict()

    def __getitem__(self, item):
        if item not in self.items:
            self.items[item] = self.fct(item)
        return self.items[item]

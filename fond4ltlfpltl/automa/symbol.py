class Symbol:
    def __init__(self, name, objects_list=[]):
        self.name = name
        self.objects = objects_list

    def __str__(self):
        return "{0} - {1}".format(self.name, ",".join(self.objects))

    def __hash__(self):
        if self.objects:
            return hash(self.name + str("_".join(self.objects)))
        else:
            return hash(self.name)

    def __eq__(self, other):
        if self.name == other.name and self.objects == other.objects:
            return True
        else:
            return False

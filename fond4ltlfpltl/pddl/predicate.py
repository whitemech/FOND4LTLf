class Predicate:
    def __init__(self, name, args=[]):
        self._name = name
        self._args = args

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args[:]

    @property
    def arity(self):
        return len(self._args)

    def __str__(self):
        if self.name == "=":
            return "(= {0} {1})".format(str(self._args[0]), str(self._args[1]))
        elif self.arity == 0:
            return "(" + self.name + ")"
        else:
            return "({0} {1})".format(self.name, " ".join(map(str, self._args)))

    def __eq__(self, other):
        return self._name == other._name

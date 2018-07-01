class Predicate: #atormic formula on(?x,?y) oppure x=y

    def __init__(self, name, variables=[]):
        self.name = name
        self.variables = variables

    def arity(self):
        return len(self.variables)

    def __str__(self):
        if self.name == '=':
            return '{0} = {1}'.format(str(self.variables[0]), str(self.variables[1]))
        elif self.arity == 0:
            return self.name
        else:
            return '{0}({1})'.format(self.name, ', '.join(map(str, self.variables)))


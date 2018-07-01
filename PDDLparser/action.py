class Action:

    def __init__(self, name, parameters, preconditions, effects):
        self.name = name #string
        self.parameters = parameters #list
        self.preconditions = preconditions #formula.Formula
        self.effects = effects #formula.Formula

        # for x in self.preconditions:
        #     print(type(x))

    def __str__(self):
        operator_str = '{0} ({1})\n'.format(self.name, ', '.join(map(str, self.parameters)))
        operator_str += '>> precond: {0}\n'.format(str(self.preconditions))
        operator_str += '>> effects: {0}\n'.format(str(self.effects))
        return operator_str

    # def __str__(self):
    #     operator_str  = '{0}({1})\n'.format(self.name, ', '.join(map(str, self.parameters)))
    #     operator_str += '>> precond: {0}\n'.format(', '.join(map(str, self.preconditions)))
    #     operator_str += '>> effects: {0}\n'.format(', '.join(map(str, self.effects)))
    #     return operator_str

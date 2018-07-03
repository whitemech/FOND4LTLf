class Action:

    def __init__(self, name, parameters, preconditions, effects):
        self.name = name #string
        self.parameters = parameters #list
        self.preconditions = preconditions #formula.FormulaXXX
        self.effects = effects #formula.FormulaXXX

    def __str__(self):
        operator_str = '{0}\n'.format(self.name)
        operator_str += '\t:parameters ({0})\n'.format(' '.join(map(str, self.parameters)))
        operator_str += '\t:precondition {0}\n'.format(self.preconditions)
        operator_str += '\t:effect {0}\n'.format(self.effects)
        return operator_str

    # def __str__(self):
    #     operator_str  = '{0}({1})\n'.format(self.name, ', '.join(map(str, self.parameters)))
    #     operator_str += '>> precond: {0}\n'.format(', '.join(map(str, self.preconditions)))
    #     operator_str += '>> effects: {0}\n'.format(', '.join(map(str, self.effects)))
    #     return operator_str

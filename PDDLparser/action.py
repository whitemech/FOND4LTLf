class Action:

    def __init__(self, name, parameters, preconditions, effects):
        self.name = name
        self.parameters = parameters
        self.preconditions = preconditions
        self.effects = effects

    def __str__(self):
        operator_str  = '{0}({1})\n'.format(self.name, ', '.join(map(str, self.parameters)))
        operator_str += '>> precond: {0}\n'.format(', '.join(map(str, self.preconditions)))
        operator_str += '>> effects: {0}\n'.format(', '.join(map(str, self.effects)))
        return operator_str

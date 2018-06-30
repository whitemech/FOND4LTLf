class Domain:

    def __init__(self, name, requirements, types, predicates, operators):
        self.name = name
        self.requirements = requirements
        self.types = types
        self.predicates = predicates
        self.operators = operators

    def __str__(self):
        domain_str = '@ Domain: {0}\n'.format(self.name)
        domain_str += '>> requirements: {0}\n'.format(', '.join(self.requirements))
        domain_str += '>> types: {0}\n'.format(', '.join(self.types))
        domain_str += '>> predicates: {0}\n'.format(', '.join(map(str, self.predicates)))
        domain_str += '>> operators:\n\t{0}\n'.format(
            '\n\t'.join(str(op).replace('\n', '\n\t') for op in self.operators))
        domain_str += 'ciao caro'
        return domain_str
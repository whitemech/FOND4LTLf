class Domain:

    def __init__(self, name, requirements, types, predicates, operators):
        self.name = name #string
        self.requirements = requirements #list
        self.types = types #list
        self.predicates = predicates #list
        self.operators = operators #list

    def __str__(self):
        domain_str = '(define (domain {0})\n'.format(self.name)
        domain_str += '\t(:requirements {0})\n'.format(' '.join(self.requirements))
        domain_str += '\t(:types {0})\n'.format(' '.join(self.types))
        domain_str += '\t(:predicates {0})\n'.format(' '.join(map(str, self.predicates)))

        for op in self.operators:
            domain_str += '\t(:action {0})\n'.format(str(op).replace('\n', '\n\t'))

        domain_str += ')'
        return domain_str
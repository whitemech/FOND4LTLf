class Domain:

    def __init__(self, name, requirements, types, constants, predicates, operators):
        self.name = name #string
        self.requirements = requirements #list
        self.types = types #list
        self.constants = constants #list
        self.predicates = predicates #list
        self.operators = operators #list

    def __str__(self):
        self.requirements.remove(':non-deterministic')
        domain_str = '(define (domain {0})\n'.format(self.name)
        domain_str += '\t(:requirements {0})\n'.format(' '.join(self.requirements))
        domain_str += '\t(:types {0})\n'.format(' '.join(self.types))
        domain_str += '\t(:constants {0})\n'.format(' '.join(map(str, self.constants)))
        domain_str += '\t(:predicates {0})\n'.format(' '.join(map(str, self.predicates)))

        for op in self.operators:
            domain_str += '\t(:action {0})\n'.format(str(op).replace('\n', '\n\t'))

        domain_str += ')'
        return domain_str

    def add_operator_trans(self, transition_operator):
        self.operators.append(transition_operator)

    def add_predicates(self, fluents, states):
        self.predicates.append('(turnDomain)')
        for state in states:
            self.predicates.append('(q{0})'.format(str(state)))
        for fluent in fluents:
            self.predicates.append('({0})'.format(fluent))

    def add_constants(self, states):
        for state in states:
            self.constants.append('{0}'.format(str(state)))

    def add_precond_effect(self):
        for op in self.operators:
            if isinstance(op, str):
                pass
            else:
                if op.isOneOf():
                    oneof_fluent = str(op.effects)
                    self.predicates.append(oneof_fluent)
                else:
                    pass
            op.add_turn_domain()

    def get_new_domain(self, fluents, states, transition_operator):
        #self.add_constants(states)
        self.add_predicates(fluents, states)
        self.add_precond_effect()
        self.add_operator_trans(transition_operator)
        return self.__str__()
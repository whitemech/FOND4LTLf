from fond4ltlfpltl.PDDLparser.formula import FormulaAnd, FormulaOneOf
from fond4ltlfpltl.PDDLparser.literal import Literal
from fond4ltlfpltl.PDDLparser.predicate import Predicate

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

    def add_to_precond(self):
        if isinstance(self.preconditions, FormulaAnd):
            self.preconditions.complete_domain_turn(True)
        else:
            old_formula = self.preconditions
            precond_to_be_added = Literal.positive(Predicate('turnDomain'))
            self.preconditions = FormulaAnd([old_formula,precond_to_be_added])

    def add_to_effect(self):
        if isinstance(self.effects, FormulaAnd):
            self.effects.complete_domain_turn(False)
        else:
            old_formula = self.effects
            effect_to_be_added = Literal.negative(Predicate('turnDomain'))
            self.effects = FormulaAnd([old_formula,effect_to_be_added])

    def add_turn_domain(self):
        self.add_to_precond()
        self.add_to_effect()

    def isOneOf(self):
        if isinstance(self.effects, FormulaOneOf):
            return True
        else:
            return False

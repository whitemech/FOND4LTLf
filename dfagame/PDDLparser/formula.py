from dfagame.PDDLparser.literal import Literal
from dfagame.PDDLparser.predicate import Predicate

class FormulaAnd:

    def __init__(self, andList):
        self.andList = andList

    def __str__(self):
        return '(and {0})'.format(' '.join(map(str, self.andList)))

    def complete_domain_turn(self, flag):
        if flag:
            self.andList.append(Literal.positive(Predicate('turnDomain')))
        else:
            self.andList.append(Literal.negative(Predicate('turnDomain')))

class FormulaOr:

    def __init__(self, orList):
        self.orList = orList

    def __str__(self):
        return '(or {0})'.format(' '.join(map(str, self.orList)))

class FormulaNot:

    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return '(not {0})'.format(self.formula)

class FormulaImply:

    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        return '(imply {0} {1})'.format(self.formula1, self.formula2)

class FormulaExists:

    def __init__(self, variables, formula):
        self.variables = variables
        self.formula = formula

    def __str__(self):
        return '(exists ({0}) {1})'.format(' '.join(map(str, self.variables)), self.formula)

class FormulaForall:

    def __init__(self, variables, formula):
        self.variables = variables
        self.formula = formula

    def __str__(self):
        return '(forall ({0}) {1})'.format(' '.join(map(str, self.variables)), self.formula)

class FormulaWhen:

    def __init__(self, condition, formula):
        self.condition = condition
        self.formula = formula

    def __str__(self):
        return '(when {0} {1})'.format(self.condition, self.formula)

class FormulaOneOf:

    def __init__(self, oneofList):
        self.oneofList = oneofList

    def __str__(self):
        intermediate_str = '(A (oneof {0}))'.format(' '.join(map(str, self.oneofList)))
        final_str = intermediate_str.replace(' ', '_')
        return final_str

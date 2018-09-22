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

    def get_variables(self):
        vars = []
        for literal in self.andList:
            vars += literal.get_vars()
            # vars.append(literal.get_vars())
        return vars

    def inside_when(self):
        for item in self.andList:
            if isinstance(item, FormulaWhen):
                return True
        return False

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

    def get_variables(self):
        # it works only for literals for the moment
        vars = []
        vars += self.condition.get_vars()
        print(vars)
        vars += self.formula.get_vars()
        print(vars)
        return vars

    def inside_when(self):
        for item in self.formula:
            if isinstance(item, FormulaWhen):
                return True
        return False

class FormulaOneOf:

    def __init__(self, oneofList, flag=True):
        #self.id = id
        self.oneofList = oneofList
        self.variables = []
        self.variables_order = []
        self.vars_set = self.get_set_variables()
        self.flag = flag

    def __str__(self):
        # return '(oneof {0})'.format(' '.join(map(str, self.oneofList)))
        # if self.flag:
        #     return '(oneof-{0} {1})'.format(self.id, ' '.join(map(str, self.vars_set)))
        # else:
        return '(oneof {0})'.format(' '.join(map(str, self.oneofList)))
        # str_1= 'A (oneof {0})'.format(' '.join(map(str, self.oneofList)))
        # str_2 = str_1.replace(' ', '_') # A_(oneof_(tizio)_(caio)_(sempronio))
        # str_3 = str_2.replace('(','-l-') # A_-l-oneof_-l-tizio)_-l-caio)_-l-sempronio))
        # str_4 = str_3.replace(')', '-r-') # A_-l-oneof_-l-tizio-r-_-l-caio-r-_-l-sempronio-r--r-
        # return '({0})'.format(str_4) # (A_-l-oneof_-l-tizio-r-_-l-caio-r-_-l-sempronio-r--r-)

    def get_set_variables(self):
        variables = set()
        for formula in self.oneofList:
            self.variables += formula.get_variables()
            variables.update(self.variables)
        self.variables_order = list(variables)
        return variables

    def inside_when(self):
        for item in self.oneofList:
            if isinstance(item, FormulaWhen):
                return True
        return False
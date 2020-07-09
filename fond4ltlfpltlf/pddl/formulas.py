# -*- coding: utf-8 -*-

"""This module contains the implementations of PDDL formulas."""

from fond4ltlfpltlf.pddl.literal import Literal
from fond4ltlfpltlf.pddl.predicate import Predicate


class FormulaAnd:
    """A class for the And formula."""

    def __init__(self, andList=None):
        """Initialize the formula."""
        if andList is None:
            andList = []
        self.andList = andList

    def __str__(self):
        """Represent the formula."""
        if self.andList:
            return "(and {0})".format(" ".join(map(str, self.andList)))
        else:
            return "(and)"

    def complete_domain_turn(self, flag):
        """Add domain turn predicate."""
        if flag:
            self.andList.append(Literal.positive(Predicate("turnDomain")))
        else:
            self.andList.append(Literal.negative(Predicate("turnDomain")))

    def get_variables(self):
        """Get variables."""
        vars = []
        for literal in self.andList:
            vars += literal.get_vars()
            # vars.append(literal.get_vars())
        return vars

    def count_whens(self):
        """Count the number of When formulas."""
        count = 0
        for item in self.andList:
            if isinstance(item, FormulaWhen):
                count += 1
        return count

    def inside_when(self):
        """Check the presence of When formulas inside the And formula."""
        for item in self.andList:
            if isinstance(item, FormulaWhen):
                return True
        return False


class FormulaOr:
    """A class for the Or formula."""

    def __init__(self, orList):
        """Initialize the formula."""
        self.orList = orList

    def __str__(self):
        """Represent the formula."""
        return "(or {0})".format(" ".join(map(str, self.orList)))


class FormulaNot:
    """A class for the Not formula."""

    def __init__(self, formula):
        """Initialize the formula."""
        self.formula = formula

    def __str__(self):
        """Represent the formula."""
        return "(not {0})".format(self.formula)


class FormulaImply:
    """A class for the Imply formula."""

    def __init__(self, formula1, formula2):
        """Initialize the formula."""
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        """Represent the formula."""
        return "(imply {0} {1})".format(self.formula1, self.formula2)


class FormulaExists:
    """A class for the Exists formula."""

    def __init__(self, variables, formula):
        """Initialize the formula."""
        self.variables = variables
        self.formula = formula

    def __str__(self):
        """Represent the formula."""
        return "(exists ({0}) {1})".format(
            " ".join(map(str, self.variables)), self.formula
        )


class FormulaForall:
    """A class for the Forall formula."""

    def __init__(self, variables, formula):
        """Initialize the formula."""
        self.variables = variables
        self.formula = formula

    def __str__(self):
        """Represent the formula."""
        return "(forall ({0}) {1})".format(
            " ".join(map(str, self.variables)), self.formula
        )


class FormulaWhen:
    """A class for the When formula."""

    def __init__(self, condition, formula):
        """Initialize the formula."""
        self.condition = condition
        self.formula = formula

    def __str__(self):
        """Represent the formula."""
        return "(when {0} {1})".format(self.condition, self.formula)

    def get_variables(self):
        """Get variables."""
        # it works only for literals for the moment
        vars = []
        vars += self.condition.get_vars()
        print(vars)
        vars += self.formula.get_vars()
        print(vars)
        return vars


class FormulaOneOf:
    """A class for the Oneof formula."""

    def __init__(self, oneofList, flag=True):
        """Initialize the formula."""
        # self.id = id
        self.oneofList = oneofList
        self.variables = []
        self.variables_order = []
        self.vars_set = self.get_set_variables()
        self.flag = flag

    def __str__(self):
        """Represent the formula."""
        # return '(oneof {0})'.format(' '.join(map(str, self.oneofList)))
        # if self.flag:
        #     return '(oneof-{0} {1})'.format(self.id, ' '.join(map(str, self.vars_set)))
        # else:
        return "(oneof {0})".format(" ".join(map(str, self.oneofList)))
        # str_1= 'A (oneof {0})'.format(' '.join(map(str, self.oneofList)))
        # str_2 = str_1.replace(' ', '_') # A_(oneof_(tizio)_(caio)_(sempronio))
        # str_3 = str_2.replace('(','-l-') # A_-l-oneof_-l-tizio)_-l-caio)_-l-sempronio))
        # str_4 = str_3.replace(')', '-r-') # A_-l-oneof_-l-tizio-r-_-l-caio-r-_-l-sempronio-r--r-
        # return '({0})'.format(str_4) # (A_-l-oneof_-l-tizio-r-_-l-caio-r-_-l-sempronio-r--r-)

    def get_set_variables(self):
        """Get variables as set."""
        variables = set()
        for formula in self.oneofList:
            self.variables += formula.get_variables()
            variables.update(self.variables)
        self.variables_order = list(variables)
        return variables

    # def inside_when(self):
    #     for item in self.oneofList:
    #         if isinstance(item, FormulaWhen):
    #             return True
    #     return False

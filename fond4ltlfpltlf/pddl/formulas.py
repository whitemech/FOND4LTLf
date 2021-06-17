#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of fond4ltlfpltlf.
#
# fond4ltlfpltlf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fond4ltlfpltlf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fond4ltlfpltlf.  If not, see <https://www.gnu.org/licenses/>.
#

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

    def __eq__(self, other):
        """Check the equality between two And formulas."""
        return isinstance(other, FormulaAnd) and self.andList == other.andList

    def __iter__(self):
        """Override the iterator of an And Formula."""
        return self.andList.__iter__()

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

    def __eq__(self, other):
        """Check equality between two Or formulas."""
        return isinstance(other, FormulaOr) and self.orList == other.orList


class FormulaNot:
    """A class for the Not formula."""

    def __init__(self, formula):
        """Initialize the formula."""
        self.formula = formula

    def __str__(self):
        """Represent the formula."""
        return "(not {0})".format(self.formula)

    def __eq__(self, other):
        """Check equality between two Not formulas."""
        return isinstance(other, FormulaNot) and self.formula == other.formula


class FormulaImply:
    """A class for the Imply formula."""

    def __init__(self, formula1, formula2):
        """Initialize the formula."""
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        """Represent the formula."""
        return "(imply {0} {1})".format(self.formula1, self.formula2)

    def __eq__(self, other):
        """Check equality between two Imply formulas."""
        return (
            isinstance(other, FormulaImply)
            and self.formula1 == other.formula1
            and self.formula2 == other.formula2
        )


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

    def __eq__(self, other):
        """Check equality between two Exists formulas."""
        return (
            isinstance(other, FormulaExists)
            and self.variables == other.variables
            and self.formula == other.formula
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

    def __eq__(self, other):
        """Check equality between two Forall formulas."""
        return (
            isinstance(other, FormulaForall)
            and self.variables == other.variables
            and self.formula == other.formula
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

    def __eq__(self, other):
        """Check equality between two When formulas."""
        return (
            isinstance(other, FormulaWhen)
            and self.condition == other.condition
            and self.formula == other.formula
        )


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

    def __eq__(self, other):
        """Check the equality between two OneOf formulas."""
        return (
            isinstance(other, FormulaOneOf)
            and self.oneofList == other.oneofList
            and self.flag == other.flag
        )

    def __iter__(self):
        """Override the iterator of an OneOf Formula."""
        return self.oneofList.__iter__()

    def get_set_variables(self):
        """Get variables as set."""
        variables = set()
        for formula in self.oneofList:
            if isinstance(formula, Literal):
                self.variables += formula.get_vars()
            else:
                self.variables += formula.get_variables()
                variables.update(self.variables)
        self.variables_order = list(variables)
        return variables

    # def inside_when(self):
    #     for item in self.oneofList:
    #         if isinstance(item, FormulaWhen):
    #             return True
    #     return False

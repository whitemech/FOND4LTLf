#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of FOND4LTLf.
#
# FOND4LTLf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FOND4LTLf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FOND4LTLf.  If not, see <https://www.gnu.org/licenses/>.
#
import ply.yacc as yacc

from fond4ltlf.parser.lexer import PDDLLexer
from fond4ltlf.pddl.action import Action
from fond4ltlf.pddl.domain import Domain
from fond4ltlf.pddl.formulas import (
    FormulaAnd,
    FormulaExists,
    FormulaForall,
    FormulaImply,
    FormulaNot,
    FormulaOneOf,
    FormulaOr,
    FormulaWhen,
)
from fond4ltlf.pddl.literal import Literal
from fond4ltlf.pddl.predicate import Predicate
from fond4ltlf.pddl.problem import Problem
from fond4ltlf.pddl.term import Term


class PDDLParser(object):
    def __init__(self):
        self.lexer = PDDLLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.symbols = self.lexer.reserved
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False)

    def __call__(self, s, **kwargs):
        return self.parser.parse(s, lexer=self.lexer.lexer)

    def p_pddl(self, p):
        """pddl : domain
        | problem"""
        p[0] = p[1]

    def p_domain(self, p):
        """domain : LPAR DEFINE_KEY domain_def require_def types_def constants_def predicates_def action_def_lst RPAR
        | LPAR DEFINE_KEY domain_def require_def types_def predicates_def action_def_lst RPAR
        | LPAR DEFINE_KEY domain_def require_def predicates_def action_def_lst RPAR
        | LPAR DEFINE_KEY domain_def predicates_def action_def_lst RPAR
        | LPAR DEFINE_KEY domain_def action_def_lst RPAR"""
        if len(p) == 10:
            p[0] = Domain(p[3], p[4], p[5], p[6], p[7], p[8])
        elif len(p) == 9:
            p[0] = Domain(p[3], p[4], p[5], [], p[6], p[7])
        elif len(p) == 8:
            p[0] = Domain(p[3], p[4], [], [], p[5], p[6])
        elif len(p) == 7:
            p[0] = Domain(p[3], [], [], [], p[4], p[5])
        else:
            assert len(p) == 7
            p[0] = Domain(p[3], [], [], [], [], p[4])

    def p_problem(self, p):
        """problem : LPAR DEFINE_KEY problem_def domain_pdef objects_def init_def goal_def RPAR"""
        p[0] = Problem(p[3], p[4], p[5], p[6], p[7])

    def p_domain_pdef(self, p):
        """domain_pdef : LPAR DOMAIN_PKEY NAME RPAR"""
        p[0] = p[3]

    def p_domain_def(self, p):
        """domain_def : LPAR DOMAIN_KEY NAME RPAR"""
        p[0] = p[3]

    def p_problem_def(self, p):
        """problem_def : LPAR PROBLEM_KEY NAME RPAR"""
        p[0] = p[3]

    def p_objects_def(self, p):
        """objects_def : LPAR OBJECTS_KEY typed_constants_lst RPAR"""
        p[0] = p[3]

    def p_init_def(self, p):
        """init_def : LPAR INIT_KEY LPAR AND_KEY ground_predicates_lst RPAR RPAR
        | LPAR INIT_KEY ground_predicates_lst RPAR"""
        if len(p) == 5:
            p[0] = p[3]
        elif len(p) == 8:
            p[0] = p[5]

    def p_goal_def(self, p):
        """goal_def : LPAR GOAL_KEY LPAR AND_KEY ground_predicates_lst RPAR RPAR
        | LPAR GOAL_KEY ground_predicate RPAR"""
        if len(p) == 8:
            p[0] = FormulaAnd(p[5])
        else:
            assert len(p) == 5
            p[0] = p[3]

    def p_require_def(self, p):
        """require_def : LPAR REQUIREMENTS_KEY require_key_lst RPAR"""
        p[0] = p[3]

    def p_require_key_lst(self, p):
        """require_key_lst : require_key require_key_lst
        | require_key"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_require_key(self, p):
        """require_key : STRIPS_KEY
        | EQUALITY_KEY
        | TYPING_KEY
        | ADL_KEY
        | ND_KEY"""
        p[0] = str(p[1])

    def p_types_def(self, p):
        """types_def : LPAR TYPES_KEY typed_lst_name RPAR"""
        p[0] = p[3]

    def p_constants_def(self, p):
        """constants_def : LPAR CONSTANTS_KEY typed_constants_lst RPAR
        | LPAR CONSTANTS_KEY names_lst RPAR"""
        p[0] = p[3]

    def p_typed_lst_name(self, p):
        """typed_lst_name : names_lst HYPHEN type typed_lst_name
        | names_lst HYPHEN NAME
        | names_lst"""
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = [Term.constant(value, p[3]) for value in p[1]]
        elif len(p) == 5:
            p[0] = [Term.constant(value, p[3]) for value in p[1]] + p[4]

    def p_names_lst(self, p):
        """names_lst : NAME names_lst
        | NAME"""
        if len(p) == 1:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_predicates_def(self, p):
        """predicates_def : LPAR PREDICATES_KEY predicate_def_lst RPAR"""
        p[0] = p[3]

    def p_predicate_def_lst(self, p):
        """predicate_def_lst : predicate_def predicate_def_lst
        | predicate_def"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_predicate_def(self, p):
        """predicate_def : LPAR NAME typed_variables_lst RPAR
        | LPAR NAME RPAR"""
        if len(p) == 4:
            p[0] = Predicate(p[2])
        elif len(p) == 5:
            p[0] = Predicate(p[2], p[3])

    def p_ground_predicates_lst(self, p):
        """ground_predicates_lst : ground_predicate ground_predicates_lst
        | ground_predicate"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_ground_predicate(self, p):
        """ground_predicate : LPAR NAME RPAR
        | LPAR NAME constants_lst RPAR"""
        if len(p) == 4:
            p[0] = Predicate(p[2])
        elif len(p) == 5:
            p[0] = Predicate(p[2], p[3])

    def p_constants_lst(self, p):
        """constants_lst : constant constants_lst
        | constant"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_typed_constants_lst(self, p):
        """typed_constants_lst : constants_lst HYPHEN type typed_constants_lst
        | constants_lst HYPHEN type"""
        if len(p) == 4:
            p[0] = [Term.constant(value, p[3]) for value in p[1]]
        elif len(p) == 5:
            p[0] = [Term.constant(value, p[3]) for value in p[1]] + p[4]

    def p_action_def_lst(self, p):
        """action_def_lst : action_def action_def_lst
        | action_def
        |"""
        if len(p) == 1:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_action_def(self, p):
        """action_def : LPAR ACTION_KEY NAME parameters_def precond_def effects_def RPAR"""
        p[0] = Action(p[3], p[4], p[5], p[6])

    def p_parameters_def(self, p):
        """parameters_def : PARAMETERS_KEY LPAR typed_variables_lst RPAR
        | PARAMETERS_KEY LPAR RPAR"""
        if len(p) == 4:
            p[0] = []
        elif len(p) == 5:
            p[0] = p[3]

    def p_precond_def(self, p):
        """precond_def : PRECONDITION_KEY LPAR formula RPAR"""
        p[0] = p[3]

    def p_formula(self, p):
        """formula : literal
        | AND_KEY formula_lst
        | OR_KEY formula_lst
        | NOT_KEY formula
        | IMPLY_KEY formula formula
        | EXISTS_KEY LPAR typed_variables_lst RPAR formula
        | FORALL_KEY LPAR typed_variables_lst RPAR formula
        | LPAR AND_KEY formula_lst RPAR
        | LPAR OR_KEY formula_lst RPAR
        | LPAR NOT_KEY formula RPAR
        | LPAR IMPLY_KEY formula formula RPAR
        | LPAR literal RPAR
        | LPAR EXISTS_KEY LPAR typed_variables_lst RPAR formula RPAR
        | LPAR FORALL_KEY LPAR typed_variables_lst RPAR formula RPAR"""
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            if p[1] == "and":
                p[0] = FormulaAnd(p[2])
            elif p[1] == "or":
                p[0] = FormulaOr(p[2])
            elif p[1] == "not":
                p[0] = FormulaNot(p[2])
        elif len(p) == 4:
            if p[1] == "imply":
                p[0] = FormulaImply(p[2], p[3])
            else:
                p[0] = p[2]
        elif len(p) == 5:
            if p[2] == "and":
                p[0] = FormulaAnd(p[3])
            elif p[2] == "or":
                p[0] = FormulaOr(p[3])
            elif p[2] == "not":
                p[0] = FormulaNot(p[3])
        elif len(p) == 6:
            if p[3] == "imply":
                p[0] = FormulaImply(p[3], p[4])
            elif p[1] == "exists":
                p[0] = FormulaExists(p[3], p[5])
            elif p[1] == "forall":
                p[0] = FormulaForall(p[3], p[5])
        elif len(p) == 8:
            if p[2] == "exists":
                p[0] = FormulaExists(p[4], p[6])
            elif p[2] == "forall":
                p[0] = FormulaForall(p[4], p[6])

    def p_formula_lst(self, p):
        """formula_lst : formula formula_lst
        | formula"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_effects_def(self, p):
        """effects_def : EFFECT_KEY LPAR one_eff_formula RPAR"""
        p[0] = p[3]

    # def p_eff_formula(self, p):
    #     '''eff_formula : one_eff_formula
    #                    | AND_KEY one_eff_formula_lst
    #                    | ONEOF_KEY one_eff_formula_lst'''
    #     if len(p) == 2:
    #         p[0] = p[1]
    #     elif len(p) == 3:
    #         if p[1] == 'and':
    #             p[0] = FormulaAnd(p[2])
    #         else:
    #             p[0] = FormulaOneOf(p[2])

    def p_one_eff_formula(self, p):
        """one_eff_formula : literal
        | AND_KEY
        | AND_KEY one_eff_formula_lst
        | ONEOF_KEY atomic_eff_lst
        | WHEN_KEY formula atomic_eff
        | LPAR ONEOF_KEY atomic_eff_lst RPAR
        | LPAR WHEN_KEY formula atomic_eff RPAR
        | LPAR FORALL_KEY LPAR typed_variables_lst RPAR atomic_eff RPAR
        | LPAR FORALL_KEY LPAR typed_variables_lst RPAR LPAR WHEN_KEY formula atomic_eff RPAR RPAR"""
        if len(p) == 2:
            if p[1] == "and":
                p[0] = FormulaAnd()
            else:
                p[0] = p[1]
        elif len(p) == 3:
            if p[1] == "and":
                p[0] = FormulaAnd(p[2])
            else:
                p[0] = FormulaOneOf(p[2])
        elif len(p) == 4:
            if p[1] == "when":
                p[0] = FormulaWhen(p[2], p[3])
        elif len(p) == 5:
            p[0] = FormulaOneOf(p[3])
        elif len(p) == 6:
            p[0] = FormulaWhen(p[3], p[4])
        elif len(p) == 8:
            p[0] = FormulaForall(p[4], p[6])
        elif len(p) == 12:
            nested = FormulaWhen(p[8], p[9])
            p[0] = FormulaForall(p[4], nested)

    def p_one_eff_formula_lst(self, p):
        """one_eff_formula_lst : one_eff_formula one_eff_formula_lst
        | one_eff_formula"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_atomic_eff_lst(self, p):
        """atomic_eff_lst : atomic_eff atomic_eff_lst
        | atomic_eff"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_atomic_eff(self, p):
        """atomic_eff : literal
        | AND_KEY literal_lst
        | LPAR AND_KEY RPAR
        | LPAR AND_KEY literal_lst RPAR
        | LPAR WHEN_KEY formula atomic_eff RPAR"""
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            if p[1] == "and":
                p[0] = FormulaAnd(p[2])
            # else:
            #     p[0] = FormulaOneOf(p[2])
        elif len(p) == 4:
            p[0] = FormulaAnd()
        elif len(p) == 5:
            if p[2] == "and":
                p[0] = FormulaAnd(p[3])
        elif len(p) == 6:
            p[0] = FormulaWhen(p[3], p[4])
            # else:
            #     p[0] = FormulaOneOf(p[3])

    def p_literal_lst(self, p):
        """literal_lst : literal literal_lst
        | literal"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_literal(self, p):
        """literal : LPAR NOT_KEY predicate RPAR
        | predicate"""
        if len(p) == 2:
            p[0] = Literal.positive(p[1])
        elif len(p) == 5:
            p[0] = Literal.negative(p[3])

    def p_predicate(self, p):
        """predicate : LPAR NAME variables_lst RPAR
        | LPAR EQUALS VARIABLE VARIABLE RPAR
        | LPAR NAME RPAR
        | NAME variables_lst
        | EQUALS VARIABLE VARIABLE
        | NAME"""
        if len(p) == 2:
            p[0] = Predicate(p[1])
        elif len(p) == 3:
            p[0] = Predicate(p[1], p[2])
        elif len(p) == 4:
            if p[1] == "(":
                p[0] = Predicate(p[2])
            else:
                p[0] = Predicate("=", [p[2], p[3]])
        elif len(p) == 5:
            p[0] = Predicate(p[2], p[3])
        elif len(p) == 6:
            p[0] = Predicate("=", [p[3], p[4]])

    def p_typed_variables_lst(self, p):
        """typed_variables_lst : variables_lst HYPHEN type typed_variables_lst
        | variables_lst HYPHEN type"""
        if len(p) == 4:
            p[0] = [Term.variable(name, p[3]) for name in p[1]]
        else:
            p[0] = [Term.variable(name, p[3]) for name in p[1]] + p[4]

    def p_variables_lst(self, p):
        """variables_lst : VARIABLE variables_lst
        | VARIABLE"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_type(self, p):
        """type : NAME"""
        p[0] = p[1]

    def p_constant(self, p):
        """constant : NAME"""
        p[0] = p[1]

    def p_error(self, p):
        print("Error: syntax error when parsing '{}'".format(p))


# def id_generator():
#     return ''.join(random.choices(string.digits, k=4))


if __name__ == "__main__":
    par = PDDLParser()
    with open("../../tests/data/pddl-domains/robot-coffee/domain-fond.pddl", "r") as f:
        domain = f.read()

    result = par(domain)
    print(result)

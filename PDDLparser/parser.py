import ply.yacc as yacc
from lexer import MyLexer
from domain import Domain
from action import Action
from literal import Literal
from predicate import Predicate
from term import Term
from formula import *

class MyParser(object):

    def __init__(self):
        self.lexer = MyLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.symbols = self.lexer.reserved
        self.parser = yacc.yacc(module=self)

    def __call__(self, s, **kwargs):
        return self.parser.parse(s, lexer=self.lexer.lexer)

    def p_pddl(self, p):
        '''pddl : domain'''
        p[0] = p[1]

    def p_domain(self, p):
        '''domain : LPAREN DEFINE_KEY domain_def require_def types_def predicates_def action_def_lst RPAREN'''
        p[0] = Domain(p[3], p[4], p[5], p[6], p[7])

    def p_domain_def(self, p):
        '''domain_def : LPAREN DOMAIN_KEY NAME RPAREN'''
        p[0] = p[3]

    def p_require_def(self, p):
        '''require_def : LPAREN REQUIREMENTS_KEY require_key_lst RPAREN'''
        p[0] = p[3]

    def p_require_key_lst(self, p):
        '''require_key_lst : require_key require_key_lst
                           | require_key'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_require_key(self, p):
        '''require_key : STRIPS_KEY
                       | EQUALITY_KEY
                       | TYPING_KEY
                       | ADL_KEY
                       | ND_KEY'''
        p[0] = str(p[1])

    def p_types_def(self, p):
        '''types_def : LPAREN TYPES_KEY names_lst RPAREN'''
        p[0] = p[3]

    def p_names_lst(self, p):
        '''names_lst : NAME names_lst
                     | NAME'''
        if len(p) == 1:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_predicates_def(self, p):
        '''predicates_def : LPAREN PREDICATES_KEY predicate_def_lst RPAREN'''
        p[0] = p[3]

    def p_predicate_def_lst(self, p):
        '''predicate_def_lst : predicate_def predicate_def_lst
                             | predicate_def'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_predicate_def(self, p):
        '''predicate_def : LPAREN NAME typed_variables_lst RPAREN
                         | LPAREN NAME RPAREN'''
        if len(p) == 4:
            p[0] = Predicate(p[2])
        elif len(p) == 5:
            p[0] = Predicate(p[2], p[3])

    def p_action_def_lst(self, p):
        '''action_def_lst : action_def action_def_lst
                          | action_def'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_action_def(self, p):
        '''action_def : LPAREN ACTION_KEY NAME parameters_def precond_def effects_def RPAREN'''
        p[0] = Action(p[3], p[4], p[5], p[6])

    def p_parameters_def(self, p):
        '''parameters_def : PARAMETERS_KEY LPAREN typed_variables_lst RPAREN
                          | PARAMETERS_KEY LPAREN RPAREN'''
        if len(p) == 4:
            p[0] = []
        elif len(p) == 5:
            p[0] = p[3]

    def p_precond_def(self, p):
        '''precond_def : PRECONDITION_KEY LPAREN formula RPAREN'''
        p[0] = p[3]

    def p_formula(self, p):
        '''formula : literal
                   | AND_KEY formula_lst
                   | OR_KEY formula_lst
                   | NOT_KEY formula
                   | IMPLY_KEY formula formula
                   | EXISTS_KEY LPAREN typed_variables_lst RPAREN formula
                   | FORALL_KEY LPAREN typed_variables_lst RPAREN formula
                   | LPAREN AND_KEY formula_lst RPAREN
                   | LPAREN OR_KEY formula_lst RPAREN
                   | LPAREN NOT_KEY formula RPAREN
                   | LPAREN IMPLY_KEY formula formula RPAREN
                   | LPAREN literal RPAREN
                   | LPAREN EXISTS_KEY LPAREN typed_variables_lst RPAREN formula RPAREN
                   | LPAREN FORALL_KEY LPAREN typed_variables_lst RPAREN formula RPAREN'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            if p[1] == 'and':
                p[0] = FormulaAnd(p[2])
            elif p[1] == 'or':
                p[0] = FormulaOr(p[2])
            elif p[1] == 'not':
                p[0] = FormulaNot(p[2])
        elif len(p) == 4:
            if p[1] == 'imply':
                p[0] = FormulaImply(p[2], p[3])
            else:
                p[0] = p[2]
        elif len(p) == 5:
            if p[2] == 'and':
                p[0] = FormulaAnd(p[3])
            elif p[2] == 'or':
                p[0] = FormulaOr(p[3])
            elif p[2] == 'not':
                p[0] = FormulaNot(p[3])
        elif len(p) == 6:
            if p[3] == 'imply':
                p[0] = FormulaImply(p[3], p[4])
            elif p[1] == 'exists':
                p[0] = FormulaExists(p[3], p[5])
            elif p[1] == 'forall':
                p[0] = FormulaForall(p[3], p[5])
        elif len(p) == 8:
            if p[2] == 'exists':
                p[0] = FormulaExists(p[4], p[6])
            elif p[2] == 'forall':
                p[0] = FormulaForall(p[4], p[6])

    def p_formula_lst(self, p):
        '''formula_lst : formula formula_lst
                       | formula'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_effects_def(self, p):
        '''effects_def : EFFECT_KEY LPAREN one_eff_formula RPAREN'''
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
        '''one_eff_formula : literal
                           | AND_KEY one_eff_formula_lst
                           | ONEOF_KEY atomic_eff_lst
                           | WHEN_KEY formula atomic_eff
                           | LPAREN ONEOF_KEY atomic_eff_lst RPAREN
                           | LPAREN WHEN_KEY formula atomic_eff RPAREN
                           | LPAREN FORALL_KEY LPAREN typed_variables_lst RPAREN atomic_eff RPAREN
                           | LPAREN FORALL_KEY LPAREN typed_variables_lst RPAREN LPAREN WHEN_KEY formula atomic_eff RPAREN RPAREN'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            if p[1] == 'and':
                p[0] = FormulaAnd(p[2])
            else: p[0] = FormulaOneOf(p[2])
        elif len(p) == 4:
            if p[1] == 'when':
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
        '''one_eff_formula_lst : one_eff_formula one_eff_formula_lst
                               | one_eff_formula'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_atomic_eff_lst(self, p):
        '''atomic_eff_lst : atomic_eff atomic_eff_lst
                          | atomic_eff'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_atomic_eff(self, p):
        '''atomic_eff : literal
                      | AND_KEY literal_lst
                      | LPAREN AND_KEY literal_lst RPAREN
                      | LPAREN WHEN_KEY formula atomic_eff RPAREN'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            if p[1] == 'and':
                p[0] = FormulaAnd(p[2])
            # else:
            #     p[0] = FormulaOneOf(p[2])
        elif len(p) == 5:
            if p[2] == 'and':
                p[0] = FormulaAnd(p[3])
        elif len(p) == 6:
            p[0] = FormulaWhen(p[3], p[4])
            # else:
            #     p[0] = FormulaOneOf(p[3])

    def p_literal_lst(self, p):
        '''literal_lst : literal literal_lst
                       | literal '''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_literal(self, p):
        '''literal : LPAREN NOT_KEY predicate RPAREN
                   | predicate'''
        if len(p) == 2:
            p[0] = Literal.positive(p[1])
        elif len(p) == 5:
            p[0] = Literal.negative(p[3])

    def p_predicate(self, p):
        '''predicate : LPAREN NAME variables_lst RPAREN
                     | LPAREN EQUALS VARIABLE VARIABLE RPAREN
                     | LPAREN NAME RPAREN
                     | NAME variables_lst
                     | EQUALS VARIABLE VARIABLE
                     | NAME'''
        if len(p) == 2:
            p[0] = Predicate(p[1])
        elif len(p) == 3:
            p[0] = Predicate(p[1], p[2])
        elif len(p) == 4:
            if p[1] == '(':
                p[0] = Predicate(p[2])
            else:
                p[0] = Predicate('=', [p[2], p[3]])
        elif len(p) == 5:
            p[0] = Predicate(p[2], p[3])
        elif len(p) == 6:
            p[0] = Predicate('=', [p[3], p[4]])

    def p_typed_variables_lst(self, p):
        '''typed_variables_lst : variables_lst HYPHEN type typed_variables_lst
                               | variables_lst HYPHEN type'''
        if len(p) == 4:
            p[0] = [Term.variable(name, p[3]) for name in p[1]]
        else:
            p[0] = [Term.variable(name, p[3]) for name in p[1]] + p[4]

    def p_variables_lst(self, p):
        '''variables_lst : VARIABLE variables_lst
                         | VARIABLE'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_type(self, p):
        '''type : NAME'''
        p[0] = p[1]

    def p_error(self, p):
        print("Error: syntax error when parsing '{}'".format(p))


if __name__ == '__main__':
    par = MyParser()
    with open('PDDLparser/prova.pddl', 'r') as f:
        domain = f.read()
        f.close()

    result = par(domain)
    # print(type(result.operators[1].preconditions))
    # print(result.operators[1].preconditions)
    print(result)
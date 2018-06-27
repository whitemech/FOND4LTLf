import ply.yacc as yacc
from PDDLparser.Lexer import Lexer

class Parser(object):

    def __init__(self):
        self.lexer = Lexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)
        # self.precedence = (
        #
        #     ('nonassoc', 'LPAR', 'RPAR'),
        #     ('left', 'AND', 'OR', 'IMPLIES', 'DIMPLIES', 'UNTIL', 'PASTUNTIL'),
        #     ('right', 'NEXT', 'EVENTUALLY', 'GLOBALLY', 'PASTNEXT', 'PASTEVENTUALLY', 'PASTGLOBALLY'),
        #     ('right', 'NOT')
        # )

    def __call__(self, s, **kwargs):
        return self.parser.parse(s, lexer=self.lexer.lexer)

    def p_pddl(self, p):
        '''pddl : domain
                | problem
        '''
        p[0] = p[1]

    def p_domain(self, p):
        '''domain : LPAREN DEFINE_KEY domain_def require_def types_def predicates_def action_def_lst RPAREN'''
        p[0] = Domain(p[3], p[4], p[5], p[6], p[7])

    def p_problem(self, p):
        '''problem : LPAREN DEFINE_KEY problem_def domain_def objects_def init_def goal_def RPAREN'''
        p[0] = Problem(p[3], p[4], p[5], p[6], p[7])

    def p_domain_def(self, p):
        '''domain_def : LPAREN DOMAIN_KEY NAME RPAREN'''
        p[0] = p[3]

    def p_problem_def(self, p):
        '''problem_def : LPAREN PROBLEM_KEY NAME RPAREN'''
        p[0] = p[3]

    def p_objects_def(self, p):
        '''objects_def : LPAREN OBJECTS_KEY typed_constants_lst RPAREN'''
        p[0] = p[3]

    def p_init_def(self, p):
        '''init_def : LPAREN INIT_KEY LPAREN AND_KEY ground_predicates_lst RPAREN RPAREN
                    | LPAREN INIT_KEY ground_predicates_lst RPAREN'''
        if len(p) == 5:
            p[0] = p[3]
        elif len(p) == 8:
            p[0] = p[5]

    def p_goal_def(self, p):
        '''goal_def : LPAREN GOAL_KEY LPAREN AND_KEY ground_predicates_lst RPAREN RPAREN'''
        p[0] = p[5]

    def p_require_def(self, p):
        '''require_def : LPAREN REQUIREMENTS_KEY require_key_lst RPAREN'''
        p[0] = p[3]

    def p_require_key_lst(self, p):
        '''require_key_lst : require_key require_key_lst
                           | require_key'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_require_key(self, p):
        '''require_key : STRIPS_KEY
                       | EQUALITY_KEY
                       | TYPING_KEY
                       | ADL_KEY'''
        p[0] = str(p[1])

    def p_types_def(self, p):
        '''types_def : LPAREN TYPES_KEY names_lst RPAREN'''
        p[0] = p[3]

    def p_predicates_def(self, p):
        '''predicates_def : LPAREN PREDICATES_KEY predicate_def_lst RPAREN'''
        p[0] = p[3]

    def p_predicate_def_lst(self, p):
        '''predicate_def_lst : predicate_def predicate_def_lst
                             | predicate_def'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
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
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_action_def(self, p):
        '''action_def : LPAREN ACTION_KEY NAME parameters_def action_def_body RPAREN'''
        p[0] = Action(p[3], p[4], p[5][0], p[5][1])

    def p_parameters_def(self, p):
        '''parameters_def : PARAMETERS_KEY LPAREN typed_variables_lst RPAREN
                          | PARAMETERS_KEY LPAREN RPAREN'''
        if len(p) == 4:
            p[0] = []
        elif len(p) == 5:
            p[0] = p[3]

    def p_action_def_body(self, p):
        '''action_def_body : precond_def effects_def'''
        p[0] = (p[1], p[2])

    def p_formula(self, p):
        '''formula : literal
                   | NOT_KEY formula
                   | AND_KEY formula_lst
                   | OR_KEY formula_lst
                   | IMPLY_KEY formula formula
                   | EXITST_KEY LPAREN typed_variables_lst RPAREN formula
                   | FORALL_KEY LPAREN typed_variables_lst RPAREN formula '''

        pass #TODO

    def p_precond_def(self, p):
        '''precond_def : PRECONDITION_KEY formula'''
        if len(p) == 3:
            p[0] = [p[2]]
        elif len(p) == 6:
            if p[3] != 'not':
                p[0] = [p[4]]
            else: p[0] = p[4]

    def p_one_eff_formula(self, p):
        '''one_eff_formula: atomic_effs
                          | LPAREN WHEN_KEY formula atomic_effs RPAREN
                          | LPAREN FORALL_KEY LPAREN typed_variables_lst RPAREN atomic_effs RPAREN
                          | LPAREN FORALL_KEY LPAREN typed_variables_lst RPAREN LPAREN WHEN_KEY formula atomic_effs RPAREN RPAREN'''
        pass #TODO

    def p_effects_def(self, p):
        '''effects_def : EFFECT_KEY LPAREN AND_KEY one_eff_formula_lst RPAREN
                       | EFFECT_KEY one_eff_formula'''
        if len(p) == 3:
            p[0] = [p[2]]
        elif len(p) == 6:
            p[0] = p[4]

    # def p_effects_lst(self, p):
    #     '''effects_lst : effect effects_lst
    #                    | effect'''
    #     if len(p) == 2:
    #         p[0] = [p[1]]
    #     elif len(p) == 3:
    #         p[0] = [p[1]] + p[2]

    # def p_effect(self, p):
    #     '''effect : literal
    #               | LPAREN PROBABILISTIC_KEY PROBABILITY literal RPAREN'''
    #     if len(p) == 2:
    #         p[0] = (1.0, p[1])
    #     elif len(p) == 6:
    #         p[0] = (p[3], p[4])

    def p_literals_lst(self, p):
        '''literals_lst : literal literals_lst
                        | literal'''
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

    def p_ground_predicates_lst(self, p):
        '''ground_predicates_lst : ground_predicate ground_predicates_lst
                                 | ground_predicate'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_predicate(self, p):
        '''predicate : LPAREN NAME variables_lst RPAREN
                     | LPAREN EQUALS VARIABLE VARIABLE RPAREN
                     | LPAREN NAME RPAREN'''
        if len(p) == 4:
            p[0] = Predicate(p[2])
        elif len(p) == 5:
            p[0] = Predicate(p[2], p[3])
        elif len(p) == 6:
            p[0] = Predicate('=', [p[3], p[4]])

    def p_ground_predicate(self, p):
        '''ground_predicate : LPAREN NAME constants_lst RPAREN
                            | LPAREN NAME RPAREN'''
        if len(p) == 4:
            p[0] = Predicate(p[2])
        elif len(p) == 5:
            p[0] = Predicate(p[2], p[3])

    def p_typed_constants_lst(self, p):
        '''typed_constants_lst : constants_lst HYPHEN type typed_constants_lst
                               | constants_lst HYPHEN type'''
        if len(p) == 4:
            p[0] = [Term.constant(value, p[3]) for value in p[1]]
        elif len(p) == 5:
            p[0] = [Term.constant(value, p[3]) for value in p[1]] + p[4]

    def p_typed_variables_lst(self, p):
        '''typed_variables_lst : variables_lst HYPHEN type typed_variables_lst
                               | variables_lst HYPHEN type'''
        if len(p) == 4:
            p[0] = [Term.variable(name, p[3]) for name in p[1]]
        elif len(p) == 5:
            p[0] = [Term.variable(name, p[3]) for name in p[1]] + p[4]

    def p_constants_lst(self, p):
        '''constants_lst : constant constants_lst
                         | constant'''
        if len(p) == 2:
            p[0] = [Term.constant(p[1])]
        elif len(p) == 3:
            p[0] = [Term.constant(p[1])] + p[2]

    def p_variables_lst(self, p):
        '''variables_lst : VARIABLE variables_lst
                         | VARIABLE'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_names_lst(self, p):
        '''names_lst : NAME names_lst
                     | NAME'''
        if len(p) == 1:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_type(self, p):
        '''type : NAME'''
        p[0] = p[1]

    def p_constant(self, p):
        '''constant : NAME'''
        p[0] = p[1]

    def p_error(self, p):
        print("Error: syntax error when parsing '{}'".format(p))

# if __name__ == '__main__':
#     par = MyParser()
#     while True:
#        try:
#            s = input('calc > ')
#        except EOFError:
#            break
#        if not s: continue
#        result = par(s)
#        print(result)
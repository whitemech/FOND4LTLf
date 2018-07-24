from PDDLparser.parser import MyParser
#import argparse
#from AutomaParser.aparser import parse_dot

#args_parser = argparse.ArgumentParser(description='DFAgame is a tool that takes as input a planning domain D and a goal'
                 #                                 + ' formula G and returns a new planning domain D\'')
#args_parser.add_argument('planning_domain', help='Path to planning domain D -- MANDATORY')
#args_parser.add_argument('planning_problem', help='Path to planning problelm P -- MANDATORY')
#args_parser.add_argument('goal_formula', help='Goal formula G -- MANDATORY')

#params = vars(args_parser.parse_args())
# if not params['goal_formula']:
#     print('Formula argument required!')
#     exit()
# else:
#     formula = params['goal_formula']

parser = MyParser()
with open('PDDLparser/prob.pddl', 'r') as f:
    domain = f.read()
    f.close()

parsed_domain = parser(domain)
#parsed_problem = parser(problem) --> getting initial state of pddl problem

# use LTLf2DFA tool for parsing the formula --> there will be a .dot file in the main folder

# parsed_automa = parse_dot('automa.dot')
# transition_operator = parsed_automa.create_operator_trans()

# transition_operator = 'trans\n:parameters ()\n:precondition (not turnDomain)\n:effect (and (when (and (q2) (not a)) (and (q2) (turnDomain))) (when (and (q2) (a)) (turnDomain)))\n'
# states = {'1','2','3','4'}
# alpha = ['a','b','c']
# # new_domain = parsed_domain.get_new_domain(parsed_automa.used_alpha, parsed_automa.states, transition_operator)
# new_domain = parsed_domain.get_new_domain(alpha, states, transition_operator)

print(parsed_domain)
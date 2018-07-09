import argparse

args_parser = argparse.ArgumentParser(description='DFAgame is a tool that takes as input a planning domain D and a goal'
                                                  + ' formula G and returns a new planning domain D\' ')
args_parser.add_argument('planning_domain', help='Path to planning domain D -- MANDATORY')
args_parser.add_argument('goal_formula', help='Goal formula G -- MANDATORY')

params = vars(args_parser.parse_args())
if not params['goal_formula']:
    print('Formula argument required!')
    exit()
else:
    formula = params['formula']


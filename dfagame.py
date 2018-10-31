from dfagame.PDDLparser.parser import MyParser
from ltlf2dfa.Translator import Translator
from ltlf2dfa.DotHandler import DotHandler
from dfagame.AutomaParser.symbol import Symbol
from dfagame.AutomaParser.aparser import parse_dot
from fileinput import FileInput
import argparse, os, subprocess, copy, re

args_parser = argparse.ArgumentParser(description='DFAgame is a tool that takes as input a planning domain D, a planning'
                                                  ' problem P and a goal formula G and returns a new planning domain D\'')
args_parser.add_argument('<planning_domain>', help='Path to planning domain D -- MANDATORY')
args_parser.add_argument('<planning_problem>', help='Path to planning problelm P -- MANDATORY')
args_parser.add_argument('<goal_formula>', type=str, help='Goal formula G -- MANDATORY')

params = vars(args_parser.parse_args())
pddl_parser = MyParser()

try:
    with open(params['<planning_domain>'], 'r') as f:
        domain = f.read()
        f.close()
    parsed_domain = pddl_parser(domain)
except:
    raise ValueError('[ERROR]: Could not parse domain')

try:
    with open(params['<planning_problem>'], 'r') as f:
        problem = f.read()
        f.close()
    parsed_problem = pddl_parser(problem)
except:
    raise ValueError('[ERROR]: Could not parse problem')

def compute_symb_vars(formula):
    ground_predicates = re.findall('(?<![a-z])(?!true|false)[_a-z0-9]+', str(params['<goal_formula>']))
    symb_vars_list = []
    for predicate in ground_predicates:
        temp = predicate.split('_')
        if len(temp) == 1:
            symb_vars_list.append(Symbol(temp[0]))
        else:
            symb_vars_list.append(Symbol(temp[0], temp[1:]))
    return symb_vars_list

def check_symbols(symbols):
    names = []
    for predicate in parsed_domain.predicates:
        names.append(predicate.name)
    for sym in symbols:
        if sym.name not in names:
            return False
    return True

symbols = compute_symb_vars(params['<goal_formula>'])
if not check_symbols(symbols):
    raise ValueError('[ERROR]: Formula symbols not in the domain.')

try:
    translator = Translator(params['<goal_formula>'])
    translator.formula_parser()
    translator.translate()
    translator.createMonafile(False)
    translator.invoke_mona()
    dot_handler = DotHandler()
    dot_handler.modify_dot()
    dot_handler.output_dot()
    dfa_automaton = parse_dot("automa.dot")
    operators_trans, parameters = dfa_automaton.create_operators_trans(parsed_domain.predicates, set(symbols))
    os.remove('automa.mona')
    os.remove('automa.dot')
except:
    os.remove('automa.mona')
    os.remove('automa.dot')
    raise ValueError('[ERROR]: Could not create DFA')

old_domain = copy.deepcopy(parsed_domain)

new_domain = parsed_domain.get_new_domain(parameters, dfa_automaton.states, operators_trans)
new_problem = parsed_problem.get_new_problem(list(dfa_automaton.accepting_states), symbols)

try:
    with open("./new-dom.pddl", 'w+') as dom:
        dom.write(str(new_domain))
        dom.close()
    with open("./new-prob.pddl", 'w+') as prob:
        prob.write(str(new_problem))
        prob.close()
except:
    raise IOError('[ERROR]: Something wrong occurred while writing new problem and domain.')

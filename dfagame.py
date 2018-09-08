from dfagame.PDDLparser.parser import MyParser
from ltlf2dfa.Translator import Translator
from ltlf2dfa.DotHandler import DotHandler
from dfagame.AutomaParser.aparser import parse_dot
import argparse, os, subprocess

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

try:
    translator = Translator(params['<goal_formula>'])
    translator.formula_parser()
    translator.translate()
    translator.createMonafile(False)
    translator.invoke_mona("automa.mona")
    dot_handler = DotHandler("inter-automa.dot")
    dot_handler.modify_dot()
    dot_handler.output_dot()
    dfa_automaton = parse_dot("automa.dot")
    operator_trans = dfa_automaton.create_operator_trans()
    os.remove('automa.mona')
    os.remove('automa.dot')
except:
    raise ValueError('[ERROR]: Could not create DFA')

new_domain = parsed_domain.get_new_domain(dfa_automaton.used_alpha, dfa_automaton.states, operator_trans)
new_problem = parsed_problem.get_new_problem(list(dfa_automaton.accepting_states))

try:
    with open("./new-dom.pddl", 'w+') as dom:
        dom.write(str(new_domain))
        dom.close()
    with open("./new-prob.pddl", 'w+') as prob:
        prob.write(str(new_problem))
        prob.close()
except:
    raise IOError('[ERROR]: Something wrong occurred while writing new problem and domain.')
# print('\n[PDDL DOMAIN]:\n{0}\n\n[PDDL PROBLEM]:\n{1}\n'.format(new_domain, new_problem))
try:
    cmd = "./ff -o new-dom.pddl -f new-prob.pddl"
    subprocess.call(cmd, shell=True)
except:
    raise OSError('[ERROR]: Something wrong occurred during adl2strips execution.')

try:
    with open("domain.pddl", 'r') as dom:
        lines = dom.read().splitlines()
        dom.close()



except:
    raise IOError('[ERROR]: Something wrong occurred when reading adl2strips domain')


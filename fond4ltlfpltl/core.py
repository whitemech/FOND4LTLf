from fond4ltlfpltl.PDDLparser.parser import MyParser
from ltlf2dfa.Translator import Translator
from fond4ltlfpltl.AutomaParser.symbol import Symbol
from fond4ltlfpltl.AutomaParser.aparser import parse_dot
import os, copy, re


def compute_symb_vars(formula):
    ground_predicates = re.findall('(?<![a-z])(?!true|false)[_a-z0-9]+', str(formula))
    symb_vars_list = []
    for predicate in ground_predicates:
        temp = predicate.split('_')
        if len(temp) == 1:
            symb_vars_list.append(Symbol(temp[0]))
        else:
            symb_vars_list.append(Symbol(temp[0], temp[1:]))
    return symb_vars_list


def check_symbols(symbols, parsed_domain):
    names = []
    for predicate in parsed_domain.predicates:
        names.append(predicate.name)
    for sym in symbols:
        if sym.name not in names:
            return False
    return True


def execute(planning_domain, planning_problem, goal_formula):
    """main function of the tool."""

    pddl_parser = MyParser()
    parsed_domain = pddl_parser(planning_domain)
    parsed_problem = pddl_parser(planning_problem)
    # try:
    #     with open(planning_domain, 'r') as f:
    #         domain = f.read()
    #         f.close()
    #     parsed_domain = pddl_parser(domain)
    # except:
    #     raise ValueError('[ERROR]: Could not parse domain')
    #
    # try:
    #     with open(planning_problem, 'r') as f:
    #         problem = f.read()
    #         f.close()
    #     parsed_problem = pddl_parser(problem)
    # except:
    #     raise ValueError('[ERROR]: Could not parse problem')

    symbols = compute_symb_vars(goal_formula)
    if not check_symbols(symbols, parsed_domain):
        raise ValueError('[ERROR]: Formula symbols not in the domain.')

    try:
        t = Translator(goal_formula)
        t.formula_parser()
        t.translate()
        t.createMonafile(False)  # it creates automa.mona file
        result = t.invoke_mona()
        dfa_automaton = parse_dot(result)
        operators_trans, parameters = dfa_automaton.create_operators_trans(parsed_domain.predicates, set(symbols))
        # os.remove('automa.mona')
    except:
        # os.remove('automa.mona')
        raise ValueError('[ERROR]: Could not create DFA')

    old_domain = copy.deepcopy(parsed_domain)

    new_domain = parsed_domain.get_new_domain(parameters, dfa_automaton.states, operators_trans)
    new_problem = parsed_problem.get_new_problem(list(dfa_automaton.accepting_states), symbols)

    return new_domain, new_problem

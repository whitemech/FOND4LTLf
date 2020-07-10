# -*- coding: utf-8 -*-
"""Core module of the fonod4ltlfpltlf tool."""

from fond4ltlfpltlf.parser.parser import PDDLParser
from ltlf2dfa.parser.ltlf import LTLfParser
from ltlf2dfa.parser.pltlf import PLTLfParser, ParsingError
from fond4ltlfpltlf.automa.symbol import Symbol
from fond4ltlfpltlf.automa.aparser import parse_dot
import re

FUTURE_OPS = {"X", "F", "U", "G", "WX", "R"}
PAST_OPS = {"Y", "O", "S", "H"}


def compute_symb_vars(formula):
    """Compute Symbols from the temporal formula."""
    ground_predicates = re.findall("(?!true|false)[_a-z0-9]+", str(formula))
    symb_vars_list = []
    for predicate in ground_predicates:
        temp = predicate.split("_")
        if len(temp) == 1:
            symb_vars_list.append(Symbol(temp[0]))
        else:
            symb_vars_list.append(Symbol(temp[0], temp[1:]))
    return symb_vars_list


def check_symbols(symbols, parsed_domain):
    """Check whether formula symbols are present in the PDDL domain."""
    names = []
    for predicate in parsed_domain.predicates:
        names.append(predicate.name)
    for sym in symbols:
        if sym.name not in names:
            return False
    return True


def execute(planning_domain, planning_problem, goal_formula):
    """Execute the compilation."""
    pddl_parser = PDDLParser()
    parsed_domain = pddl_parser(planning_domain)
    parsed_problem = pddl_parser(planning_problem)

    symbols = compute_symb_vars(goal_formula)
    if not check_symbols(
        symbols, parsed_domain
    ):  # TODO: it checks symbols but not objects....
        raise ValueError("[ERROR]: Formula symbols not in the domain.")

    if all(c in FUTURE_OPS for c in goal_formula if c.isupper()):
        f_parser = LTLfParser()
        try:
            formula = f_parser(goal_formula)
        except Exception:
            raise ParsingError()

    else:
        assert all(c in PAST_OPS for c in goal_formula if c.isupper())
        p_parser = PLTLfParser()
        try:
            formula = p_parser(goal_formula)
        except Exception:
            raise ParsingError()

    mona_output = formula.to_dfa(mona_dfa_out=True)
    dfa = parse_dot(mona_output)
    operators_trans, parameters = dfa.create_operators_trans(
        parsed_domain.predicates, set(symbols)
    )

    new_domain = parsed_domain.get_new_domain(parameters, dfa.states, operators_trans)
    new_problem = parsed_problem.get_new_problem(list(dfa.accepting_states), symbols)

    return new_domain, new_problem

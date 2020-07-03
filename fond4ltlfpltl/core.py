from fond4ltlfpltl.pddl.parser.parser import MyParser
from ltlf2dfa.parser.ltlf import LTLfParser
from ltlf2dfa.parser.pltlf import PLTLfParser
from fond4ltlfpltl.automa.symbol import Symbol
from fond4ltlfpltl.automa.aparser import parse_dot
import os, copy, re

FUTURE_OPS = {"X", "F", "U", "G", "WX", "R"}
PAST_OPS = {"Y", "O", "S", "H"}

def compute_symb_vars(formula):
    ground_predicates = re.findall("(?<![a-z])(?!true|false)[_a-z0-9]+", str(formula))
    symb_vars_list = []
    for predicate in ground_predicates:
        temp = predicate.split("_")
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
        raise ValueError("[ERROR]: Formula symbols not in the domain.")

    if all(c in FUTURE_OPS for c in goal_formula if c.isupper()):
        f_parser = LTLfParser()
        try:
            formula = f_parser(goal_formula)
        except Exception as e:

    else:
        assert all(c in PAST_OPS for c in goal_formula if c.isupper())
        p_parser = PLTLfParser()
        try:
            formula = p_parser(goal_formula)
        except Exception as e:
            if request.form.get("exampleCheck1"):
                return render_template("dfa.html", error=str(e).encode("utf-8"))
            return render_template("index.html", error=str(e).encode("utf-8"))

    dfa = formula.to_dfa()


    # try:
    #     t = Translator(goal_formula)
    #     t.formula_parser()
    #     t.translate()
    #     t.createMonafile(False)  # it creates automa.mona file
    #     result = t.invoke_mona()
    #     dfa_automaton = parse_dot(result)
    #     operators_trans, parameters = dfa_automaton.create_operators_trans(
    #         parsed_domain.predicates, set(symbols)
    #     )
    #     # os.remove('automa.mona')
    except:
        # os.remove('automa.mona')
        raise ValueError("[ERROR]: Could not create DFA")

    # old_domain = copy.deepcopy(parsed_domain)

    new_domain = parsed_domain.get_new_domain(
        parameters, dfa_automaton.states, operators_trans
    )
    new_problem = parsed_problem.get_new_problem(
        list(dfa_automaton.accepting_states), symbols
    )

    return new_domain, new_problem

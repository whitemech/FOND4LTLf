# -*- coding: utf-8 -*-

"""This module contains the implementations of a PDDL Predicate."""


from fond4ltlfpltlf.automa.automaton import Automaton
import re

# UNSAT_DOT = '''digraph MONA_DFA {
#  rankdir = LR;
#  center = true;
#  size = "7.5,10.5";
#  edge [fontname = Courier];
#  node [height = .5, width = .5];
#  node [shape = doublecircle];
#  node [shape = circle]; 1;
#  init [shape = plaintext, label = ""];
#  init -> 1;
#  1 -> 1 [label="true"];
# }'''


def get_value(text, regex, value_type=float):
    """Dump a value from a file based on a regex passed in."""
    # Get the text of the time
    pattern = re.compile(regex, re.MULTILINE)
    results = pattern.search(text)
    if results:
        return value_type(results.group(1))
    else:
        print("Could not find the value {}, in the text provided".format(regex))
        return value_type(0.0)


def parse_dot(mona_output):
    """Parse MONA output and initialize the DFA Automaton."""
    # initial_state = get_value(mona_output, '.*Initial state:[\s]*(\d+)\n.*', int)
    accepting_states = get_value(mona_output, r".*Accepting states:[\s]*(.*?)\n.*", str)
    accepting_states = set(
        str(x.strip()) for x in accepting_states.split() if len(x.strip()) > 0
    )
    num_states = get_value(mona_output, r".*Automaton has[\s]*(\d+)[\s]states.*", int)

    transitions = {str(k): {} for k in range(1, num_states)}
    for line in mona_output.splitlines():
        if line.startswith("State "):
            orig_state = get_value(line, r".*State[\s]*(\d+):\s.*", str)
            if orig_state == "0":
                continue
            guard = get_value(line, r".*:[\s](.*?)[\s]->.*", str)
            dest_state = get_value(line, r".*state[\s]*(\d+)[\s]*.*", str)

            transitions[orig_state][guard] = dest_state

    automaton = Automaton(
        alphabet={"0", "1", "X"},
        states=set(transitions.keys()),
        initial_state="1",
        accepting_states=accepting_states,
        transitions=transitions,
    )

    return automaton


if __name__ == "__main__":
    # path = "automa.dot"

    path = """
DFA for formula with free variables: A B
Initial state: 0
Accepting states: 2
Rejecting states: 3
Don't-care states: 0 1

Automaton has 4 states and 5 BDD-nodes
Transitions:
State 0: XX -> state 1
State 1: 0X -> state 2
State 1: 10 -> state 3
State 1: 11 -> state 2
State 2: 0X -> state 2
State 2: 10 -> state 3
State 2: 11 -> state 2
State 3: X0 -> state 3
State 3: X1 -> state 2
A counter-example of least length (1) is:
A               X 1
B               X 0

A = {0}
B = {}

A satisfying example of least length (1) is:
A               X 0
B               X X

A = {}
B = {}"""
    result = parse_dot(path)
    # print(result.create_operator_trans()+'\n')
    print(result)

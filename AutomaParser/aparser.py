import pydot
import os
from automata.fa.dfa import DFA

def import_dot(path):

    # istantiation of automaton
    # automata = DFA(
    #     states={'q0', 'q1', 'q2'},
    #     input_symbols={'0', '1'},
    #     transitions={
    #         'q0': {'0': 'q0', '1': 'q1'},
    #         'q1': {'0': 'q0', '1': 'q2'},
    #         'q2': {'0': 'q2', '1': 'q1'}
    #     },
    #     initial_state='q0',
    #     final_states={'q1'}
    # )

    dot_graph = pydot.graph_from_dot_file(path)
    graph = dot_graph[0]

    #taking integer nodes
    nodes = [] ## list of integer nodes as string (in the example: 1,2,3)
    for node in graph.get_nodes():
        if node.to_string()[:-1].isdigit(): #maybe it can be rewrited as node.get_name().isdigit():
            nodes.append(node.get_name())
        else: continue

    # sort in ascending order the list of nodes
    sorted(nodes, key=int)

    # ora possiamo assegnare all'attributo stati dell'automa la lista ordinata di nodi
    automa.states = nodes

    # getting the initial state as a string
    automa.initial_state = nodes[0]

    # let's get the accepting states
    # there is a problem recognizing accepting states
    with open(path, 'r') as file:
        lines = file.readlines()
        file.close()
    accepting_states = set() #set containing all accepting states of the automaton
    for line in lines[5:]:
        if line != '[shape=circle];\n':
            ll = line.replace(";\n", "")
            accepting_states.add(ll)
        else:
            break

    # let's get sources nodes
    sources = []
    for elem in e:
        if elem.get_source().isdigit():
            sources.append(elem.get_source())
        else: continue

    # let's get transitions
    i = 0
    transitions = dict()
    for source in sources:
        label = e[i].get_label()[1] # only support simple labels!!!!
        destination = e[i].get_destination()
        i += 1
        if source in transitions:
            transitions[source][label] = destination
        else:
            transitions[source] = dict({label: destination})

    # try to handle also complex labels
    s = e[i].get_label()
    s1 = s.replace(" ", "")
    s2 = s1.replace(",","")
    s3 = s2.replace('"','')
    s4 = s3.split('\n') # now s4 should be a list like ['01', '0X', '00']

    # compose symbols
    label = ''
    leng_elem = len(s4)
    for i in range(0,leng_elem):
        for elem in s4:
            label += elem[i]
        label+=','
    final_label = label[:-1] # as in the example we obtain '000,1X0'





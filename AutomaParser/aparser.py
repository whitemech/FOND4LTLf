import pydot
from automata.fa.dfa import DFA

def parse_dot(path):

    graph = get_graph_from_dot(path)

    #taking integer nodes
    nodes = [] ## list of integer nodes as string (in the example: 3,1,2)
    for node in graph.get_nodes():
        if node.get_name().isdigit(): #maybe it can be rewrited as node.to_string()[:-1].isdigit():
            nodes.append(node.get_name())
        else: continue

    # assign set of states
    states = set(nodes)

    # getting the initial state as a string
    initial_state = sorted(nodes, key=int)[0]

    # let's get the accepting states
    lines = get_file(path)
    accepting_states = set() #set containing all accepting states of the automaton
    for line in lines[7:]:
        if line.strip() != 'node [shape = circle];':
            temp = line.replace(";\n", "")
            accepting_states.add(temp.strip())
        else:
            break

    # let's get sources nodes
    sources = []
    for elem in graph.get_edges():
        if elem.get_source().isdigit():
            sources.append(elem.get_source())
        else: continue

    # let's get transitions
    i = 0
    transitions = dict()
    for source in sources:
        label = graph.get_edges()[i].get_label()
        final_label =  get_final_label(label)# only support simple labels!!!!
        destination = graph.get_edges()[i].get_destination()
        i += 1
        if source in transitions:
            transitions[source][final_label] = destination
        else:
            transitions[source] = dict({final_label: destination})

    print('states: '+ str(states))
    print('transitions: '+ str(transitions))
    print('init: '+ str(initial_state))
    print('final: '+ str(accepting_states))
    #istantiation of automaton
    automaton = DFA(
        states=states,
        input_symbols={'0', '1', 'X'},
        transitions=transitions,
        initial_state=initial_state,
        final_states=accepting_states
    )
    return automaton

def get_file(path):
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            file.close()
        return lines
    except IOError:
        print('[ERROR] : Not able to open the file from the path {}'.format(path))

def get_graph_from_dot(path):
    try:
        dot_graph = pydot.graph_from_dot_file(path)
        return dot_graph[0]
    except IOError:
        print('[ERROR] : Not able to import the dot file')


def get_final_label(label):

    s1 = label.replace(" ", "")
    s2 = s1.replace(",","")
    s3 = s2.replace('"','')
    s4 = s3.split('\n') # now s4 should be a list like ['01', '0X', '00']

    # compose symbols
    inter_label = ''
    leng_elem = len(s4)
    for i in range(0,leng_elem):
        for elem in s4:
            inter_label += elem[i]
            inter_label += ',' # at the end of the for we have something like '000,1X0,'

    return inter_label[:-1] # as in the example we obtain '000,1X0'

if __name__ == '__main__':
    path = "AutomaParser/automa.dot"
    result = parse_dot(path)
    print(result)
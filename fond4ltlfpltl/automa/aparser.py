from fond4ltlfpltl.automa.automa import Automa
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


#
# import pydot
#
# def get_file(path):
#     try:
#         with open(path, 'r') as file:
#             lines = file.readlines()
#             file.close()
#         return lines
#     except IOError:
#         print('[ERROR] : Not able to open the file from the path {}'.format(path))
#
# def get_graph_from_dot(path):
#     try:
#         dot_graph = pydot.graph_from_dot_file(path)
#         return dot_graph[0]
#     except IOError:
#         print('[ERROR]: Not able to import the dot file')
#
# def get_final_label(label):
#
#     s1 = label.replace(" ", "")
#     s2 = s1.replace('"','')
#
#     if s2 == '':
#         return ['X']
#     elif len(s2) < 2:
#         return [s2]
#     else:
#         s3 = s2.replace(",","")
#         s4 = s3.split('\\n') # now s4 should be a list like ['01', '0X', '00']
#
#         leng_elem = len(s4[0]) # length of elements in s4
#         temp = ''
#         inter_label = []
#         for i in range(leng_elem):
#             for elem in s4:
#                 temp += elem[i]
#             inter_label.append(temp)
#             temp = ''
#
#         return inter_label
#
# def parse_dot(path):
#
#     graph = get_graph_from_dot(path)
#
#     #taking integer nodes
#     nodes = [] ## list of integer nodes as string (in the example: 3,1,2)
#     for node in graph.get_nodes():
#         if node.get_name().isdigit(): #maybe it can be rewrited as node.to_string()[:-1].isdigit():
#             nodes.append(node.get_name())
#         else: continue
#
#     # assign set of states
#     states = set(nodes)
#
#     # getting the initial state as a string
#     initial_state = sorted(nodes, key=int)[0]
#
#     # let's get the accepting states
#     lines = get_file(path)
#     accepting_states = set() #set containing all accepting states of the automaton
#     for line in lines[7:]:
#         if line.strip() != 'node [shape = circle];':
#             temp = line.replace(";\n", "")
#             accepting_states.add(temp.strip())
#         else:
#             break
#
#     # let's get sources nodes
#     sources = []
#     for elem in graph.get_edges():
#         if elem.get_source().isdigit():
#             sources.append(elem.get_source())
#         else: continue
#
#     # let's get transitions
#     i = 0
#     transitions = dict()
#     for source in sources:
#         label = graph.get_edges()[i].get_label()
#         final_label = get_final_label(label)
#         destination = graph.get_edges()[i].get_destination()
#         #print('[LOOP #'+str(i)+'] source: '+str(source)+', destination: '+str(destination)+', label: '+str(final_label))
#         i += 1
#         for lab in final_label:
#             if source in transitions:
#                 transitions[source][lab] = destination
#             else:
#                 transitions[source] = dict({lab: destination})
#
#     #istantiation of automaton
#     automaton = Automa(
#         alphabet={'0', '1', 'X'},
#         states=states,
#         initial_state=initial_state,
#         accepting_states=accepting_states,
#         transitions=transitions
#     )
#     return automaton


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
    """Parse mona output and initialize the Automaton."""
    # initial_state = get_value(mona_output, '.*Initial state:[\s]*(\d+)\n.*', int)
    accepting_states = get_value(mona_output, r".*Accepting states:[\s]*(.*?)\n.*", str)
    accepting_states = set(
        str(x.strip()) for x in accepting_states.split() if len(x.strip()) > 0
    )
    num_states = get_value(mona_output, ".*Automaton has[\s]*(\d+)[\s]states.*", int)

    transitions = {str(k): {} for k in range(1, num_states)}
    for line in mona_output.splitlines():
        if line.startswith("State "):
            orig_state = get_value(line, r".*State[\s]*(\d+):\s.*", str)
            if orig_state == "0":
                continue
            guard = get_value(line, r".*:[\s](.*?)[\s]->.*", str)
            dest_state = get_value(line, r".*state[\s]*(\d+)[\s]*.*", str)

            transitions[orig_state][guard] = dest_state

    automaton = Automa(
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

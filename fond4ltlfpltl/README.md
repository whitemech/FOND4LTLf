# FOND 4 LTL<sub>f</sub>/PLTL<sub>f</sub>

FOND 4 LTL<sub>f</sub>/PLTL<sub>f</sub> is a tool that compiles FOND planning problems with temporally extended goals, 
specified either in LTL<sub>f</sub> or in PLTL<sub>f</sub>, into classical FOND planning problems.
In particular, the formula is first transformed into a Deterministic Finite-state Automaton (DFA), then the automaton is
encoded in PDDL actions with conditional effects. Since there aren't FOND planners able to deal with conditional 
effects, this tool also compiles out such conditional effects splitting each action in as many actions as effects. 

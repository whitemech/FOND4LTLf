# -*- coding: utf-8 -*-

"""This module contains the implementations of the automaton DFA."""


import random
import re
import string

from fond4ltlfpltlf.pddl.action import Action
from fond4ltlfpltlf.pddl.formulas import FormulaAnd, FormulaOr
from fond4ltlfpltlf.pddl.term import Term
from fond4ltlfpltlf.pddl.literal import Literal
from fond4ltlfpltlf.pddl.predicate import Predicate


class Automaton:
    """A class for the Automaton DFA.

    DFA Automaton:
    - alphabet         => set() ;
    - states           => set() ;
    - initial_state    => str() ;
    - accepting_states => set() ;
    - transitions      => dict(), where
    **key**: *source* ∈ states
    **value**: {*action*: *destination*}
    """

    def __init__(self, alphabet, states, initial_state, accepting_states, transitions):
        """Initialize the formula."""
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions
        self.trans_by_dest = self.group_conditions_by_consequence()
        self.validate()

    def valide_transition_start_states(self):
        """Validate transition start states."""
        for state in self.states:
            if state not in self.transitions:
                raise ValueError("transition start state {} is missing".format(state))

    def validate_initial_state(self):
        """Validate initial state."""
        if self.initial_state not in self.states:
            raise ValueError("initial state is not defined as state")

    def validate_accepting_states(self):
        """Validate final states."""
        if any(s not in self.states for s in self.accepting_states):
            raise ValueError("accepting states not defined as state")

    def validate_input_symbols(self):
        """Validate input symbols."""
        alphabet_pattern = self.get_alphabet_pattern()
        for state in self.states:
            for action in self.transitions[state]:
                if not re.match(alphabet_pattern, action):
                    raise ValueError("invalid transition found")

    def get_alphabet_pattern(self):
        """Get the alphabet pattern."""
        return re.compile("(^[" + "".join(self.alphabet) + "]+$)")

    def validate(self):
        """Validate the automaton."""
        self.validate_initial_state()
        self.validate_accepting_states()
        self.valide_transition_start_states()
        self.validate_input_symbols()
        return True

    def __str__(self):
        """Get the string."""
        automa = "alphabet: {}\n".format(str(self.alphabet))
        automa += "states: {}\n".format(str(self.states))
        automa += "init_state: {}\n".format(str(self.initial_state))
        automa += "accepting_states: {}\n".format(str(self.accepting_states))
        automa += "transitions: {}".format(str(self.transitions))
        return automa

    def create_operators_trans(self, domain_predicates, grounded_symbols):
        """Create operator corresponding to the automaton."""
        new_operators = []
        my_predicates = []
        for symbol in grounded_symbols:
            my_predicates.append(symbol.name)
            # if vars:
            #     my_predicates.append(name)
            # else:
            #     pass
        (parameters, obj_mapping) = self.compute_parameters(
            domain_predicates, grounded_symbols
        )
        vars_mapping = self.compute_varsMapping(grounded_symbols, obj_mapping)
        # vars_mapping, parameters = self.compute_parameters(grounded_symbols,
        #                                                    domain_predicates,
        #                                                    multiplicity_predicates)
        # print(vars_mapping)
        my_variables = self.compute_variables(parameters)
        counter = 0
        for destination, source_action in self.trans_by_dest.items():
            if source_action:
                fluents_list_precond = self.compute_preconditions(
                    source_action, vars_mapping, my_predicates, my_variables
                )
                if isinstance(fluents_list_precond, FormulaAnd):
                    new_precondition = fluents_list_precond
                else:
                    new_precondition = FormulaAnd(
                        [fluents_list_precond]
                        + [Literal.negative(Predicate("turnDomain"))]
                    )
                new_effects = self.compute_effects(destination, my_variables)
                new_operators.append(
                    Action(
                        "trans-" + str(counter),
                        parameters,
                        new_precondition,
                        new_effects,
                    )
                )
            else:
                pass
            counter += 1

        return (new_operators, parameters)

    def compute_type(self, all_predicates, name, position):
        """Compute types."""
        for predicate in all_predicates:
            if predicate.name == name:
                if predicate.args:
                    return (
                        predicate.args[position].name
                        + "".join(random.choices(string.digits, k=2)),
                        predicate.args[position].type,
                    )
                else:
                    raise ValueError(
                        "[ERROR]: Please check the instantiation on the formula"
                    )
            else:
                pass

    def compute_parameters(self, domain_predicates, grounded_symbols):
        """Compute parameters."""
        objs_set = set()
        obj_mapping = {}
        parameters = []
        for symbol in grounded_symbols:
            if symbol.objects:
                i = 0
                for obj in symbol.objects:
                    if obj not in objs_set:
                        objs_set.add(obj)
                        (name_var, type_) = self.compute_type(
                            domain_predicates, symbol.name, i
                        )
                        obj_mapping[obj] = [name_var, type_]
                        parameters.append(Term.variable(name_var, type_))
                    else:
                        pass
                    i += 1
        return parameters, obj_mapping

    def compute_varsMapping(self, grounded_symbols, obj_mapping):
        """Compute mapping between symbols and variables."""
        temp = []
        vars_mapping = {}
        for symbol in grounded_symbols:
            if symbol.objects:
                for obj in symbol.objects:
                    temp.append((obj_mapping[obj][0], obj_mapping[obj][1]))
            else:
                vars_mapping[symbol] = []
            vars_mapping[symbol] = temp
            temp = []
        return vars_mapping

    # def compute_parameters(self, symbols, all_predicates, multiplicity):
    #     params_list = []
    #     variables_mapping = {}
    #     viewed = set()
    #     vars_set = set()
    #     counter = 0
    #     for predicate in all_predicates:
    #         for my_predicate in symbols:
    #             if predicate.name == my_predicate.name and predicate.args:
    #                 if my_predicate.name not in viewed:
    #                     # vars = []
    #                     temp = []
    #                     variables_mapping[my_predicate] = []
    #                     for arg in predicate.args:
    #                         # vars.append(arg.name)
    #                         params_list.append(Term.variable(arg.name, arg.type))
    #                         temp.append((arg.name, arg.type))
    #                     variables_mapping[my_predicate] = temp
    #                     viewed.add(my_predicate.name)
    #                 else:
    #                     # qua l'ho già visto
    #                     variables_mapping[my_predicate] = []
    #                     temp = []
    #                     for arg in predicate.args:
    #                         # vars.append(arg.name)
    #                         params_list.append(Term.variable(arg.name+str(counter), arg.type))
    #                         temp.append((arg.name+str(counter), arg.type))
    #                     variables_mapping[my_predicate] = temp
    #                     counter += 1
    #             elif predicate.name == my_predicate.name:
    #                 variables_mapping[my_predicate] = []
    #             else:
    #                 pass
    #                     #raise ValueError('[ERROR]: Please check the instantiation on the formula')
    #
    #     return (variables_mapping, params_list)

    def compute_preconditions(
        self, source_action, vars_mapping, predicates_name, variables
    ):
        """Compute new preconditions."""
        if len(source_action) == 1:
            if (
                self.get_automaton_formula(
                    vars_mapping, predicates_name, source_action[0][1]
                )
                == []
            ):
                formula = Literal.positive(
                    Predicate("q" + str(source_action[0][0]), variables)
                )
            else:
                automaton_state = [
                    Literal.positive(
                        Predicate("q" + str(source_action[0][0]), variables)
                    )
                ]
                formula = FormulaAnd(
                    automaton_state
                    + self.get_automaton_formula(
                        vars_mapping, predicates_name, source_action[0][1]
                    )
                    + [Literal.negative(Predicate("turnDomain"))]
                )
        else:
            formula = FormulaOr(
                self.get_or_conditions(
                    vars_mapping, predicates_name, variables, source_action
                )
            )
        return formula

    def compute_effects(self, destination, variables):
        """Compute new effects."""
        negated_states = []
        for state in self.states:
            if state != destination:
                negated_states.append(
                    Literal.negative(Predicate("q" + str(state), variables))
                )
            else:
                pass
        automaton_destination = [
            Literal.positive(Predicate("q" + str(destination), variables))
        ]
        turnDomain = [Literal.positive(Predicate("turnDomain"))]
        formula = FormulaAnd(automaton_destination + negated_states + turnDomain)
        return formula

    def get_or_conditions(
        self, vars_mapping, predicates_name, variables, source_action_list
    ):
        """Get conditions with OR formulae."""
        items = []
        for source, action in source_action_list:
            formula = self.get_automaton_formula(vars_mapping, predicates_name, action)
            if formula == []:
                items.append(Literal.positive(Predicate("q" + str(source), variables)))
            else:
                automaton_state = [
                    Literal.positive(Predicate("q" + str(source), variables))
                ]
                items.append(
                    FormulaAnd(
                        automaton_state
                        + self.get_automaton_formula(
                            vars_mapping, predicates_name, action
                        )
                    )
                )
        return items

    def get_automaton_formula(self, vars_mapping, predicates_name, action):
        """Get the automaton formula."""
        temp = []
        i = 0
        # print(predicates_name)
        # print(vars_mapping)
        for char in action:
            if char == "1":
                # if predicates_name[i] in [x.name for x in list(vars_mapping)]:
                temp.append(
                    Literal.positive(
                        Predicate(
                            predicates_name[i],
                            [x[0] for x in vars_mapping[list(vars_mapping)[i]]],
                        )
                    )
                )
                # else:
                #     temp.append(Literal.positive(Predicate(predicates_name[i])))
            elif char == "0":
                # if predicates_name[i] in vars_mapping.keys():
                temp.append(
                    Literal.negative(
                        Predicate(
                            predicates_name[i],
                            [x[0] for x in vars_mapping[list(vars_mapping)[i]]],
                        )
                    )
                )
                # else:
                #     temp.append(Literal.negative(Predicate(predicates_name[i])))
            else:
                pass
            i += 1
        return temp

    def compute_variables(self, parameters_list):
        """Compute variables."""
        my_variables = []
        for param in parameters_list:
            my_variables.append(param.name)
        return my_variables

    # def create_operator_trans(self):
    #     '''create operator trans as a string'''
    #     operator  = 'trans\n'
    #     operator += '\t:parameters ()\n'
    #     operator += '\t:precondition (not (turnDomain))\n'
    #     operator += '\t:effect (and {0}\t)\n'.format(' '.join(self.get_whens()))
    #     return operator
    #
    # def get_whens(self):
    #     whens = []
    #     for destination, source_action in self.trans_by_dest.items():
    #         if source_action == []:
    #             pass
    #         else:
    #             whens.append(self.get_formula_when(destination, source_action))
    #     return whens
    #
    # def get_formula_when(self, destination, source_action_list):
    #     formula_when  = '(when {0} {1})\n'.format(self.get_formula_condition(source_action_list),
    #     self.get_formula_statement(destination))
    #     return formula_when
    #
    # def get_formula_condition(self, source_action_list):
    #     if len(source_action_list) == 1:
    #         if self.get_automaton_action(source_action_list[0][1]) == []:
    #             formula_condition = '(q{0})'.format(source_action_list[0][0])
    #         else:
    #             formula_condition = '(and (q{0}) {1})'.format(source_action_list[0][0],
    #             ' '.join(self.get_condition_action(source_action_list[0][1])))
    #     else:
    #         formula_condition = '(or {0})'.format(' '.join(self.get_or_conditions(source_action_list)))
    #     return formula_condition
    #
    # def get_or_conditions(self, source_action_list):
    #     items = []
    #     for source, action in source_action_list:
    #         formula_conditions = self.get_condition_action(action)
    #         if formula_conditions == []:
    #             items.append('(q{0})'.format(source))
    #         else:
    #             items.append( '(and (q{0}) {1})'.format(source, ' '.join(self.get_condition_action(action))))
    #     return items
    #
    # def get_formula_statement(self, destination):
    #     negated_states = []
    #     for state in self.states:
    #         if state != destination:
    #             negated_states.append('(not (q{0}))'.format(state))
    #         else:
    #             pass
    #     formula_statement = '(and (q{0}) {1} (turnDomain))'.format(destination, ' '.join(negated_states))
    #     return formula_statement
    #
    # def get_condition_action(self, action):
    #     temp = []
    #     length = len(action)
    #     self.used_alpha = self.en_alphabet[0:length]
    #     i = 0
    #     for char in action:
    #         if char == '1':
    #             temp.append('('+self.used_alpha[i]+')')
    #         elif char == '0':
    #             temp.append('(not ('+self.used_alpha[i]+'))')
    #         else:
    #             pass
    #         i += 1
    #         if i > self.MAX_ALPHABET:
    #             break
    #     return temp

    def create_dict_by_destination(self):
        """Group transitions by destination."""
        trans_by_dest = {}
        for state in self.states:
            trans_by_dest[state] = []
        return trans_by_dest

    def group_conditions_by_consequence(self):
        """Group conditions by consequence."""
        group_by_dest = self.create_dict_by_destination()
        for source, trans in self.transitions.items():
            i = 0
            for dest in trans.values():
                group_by_dest[dest].append((source, list(trans.keys())[i]))
                i += 1
        return group_by_dest

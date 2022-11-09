#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of fond4ltlfpltlf.
#
# fond4ltlfpltlf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fond4ltlfpltlf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fond4ltlfpltlf.  If not, see <https://www.gnu.org/licenses/>.
#
"""This module contains the implementations of the automaton DFA."""

import re

from fond4ltlfpltlf.pddl.action import Action
from fond4ltlfpltlf.pddl.formulas import FormulaAnd, FormulaOr
from fond4ltlfpltlf.pddl.literal import Literal
from fond4ltlfpltlf.pddl.predicate import Predicate
from fond4ltlfpltlf.pddl.term import Term


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
        """Create operators corresponding to the automaton."""
        new_operators = []
        my_predicates = [symbol.name for symbol in grounded_symbols]
        (parameters, obj_mapping) = self.compute_parameters(
            domain_predicates, grounded_symbols
        )
        vars_mapping = self.compute_varsMapping(grounded_symbols, obj_mapping)
        my_variables = [param.name for param in parameters]
        counter = 0
        for destination, source_action in self.trans_by_dest.items():
            if source_action:
                fluents_list_precond = self.compute_preconditions(
                    source_action, vars_mapping, my_predicates, my_variables
                )
                if isinstance(fluents_list_precond, FormulaAnd):
                    new_preconditions = [fluents_list_precond]
                else:
                    # Luigi: this should be an or
                    assert isinstance(fluents_list_precond, FormulaOr)
                    # For each disjunct I create a nre precond
                    new_preconditions = [
                        FormulaAnd(pre.andList + [Literal.negative(Predicate("turnDomain"))])
                        if isinstance(pre, FormulaAnd)
                        else FormulaAnd([pre] + [Literal.negative(Predicate("turnDomain"))])
                        for pre in fluents_list_precond.orList
                    ]
                subcounter = 0
                for newpre in new_preconditions:
                    new_effects = self.compute_effects(destination, my_variables)
                    new_operators.append(
                        Action(
                            "trans-" + str(counter) + str(subcounter),
                            parameters,
                            newpre,
                            new_effects,
                        )
                    )
                    subcounter += 1
                counter += 1
            else:
                pass

        return new_operators, parameters

    def compute_type(self, all_predicates, name, position, counter):
        """Compute types."""
        for predicate in all_predicates:
            if predicate.name == name:
                if predicate.args:
                    return (
                        predicate.args[position].name + "-{:02}".format(counter),
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
        counter = 0
        for symbol in grounded_symbols:
            if symbol.objects:
                i = 0
                for obj in symbol.objects:
                    if obj not in objs_set:
                        objs_set.add(obj)
                        (name_var, type_) = self.compute_type(
                            domain_predicates, symbol.name, i, counter
                        )
                        obj_mapping[obj] = [name_var, type_]
                        parameters.append(Term.variable(name_var, type_))
                        counter += 1
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
        for state in sorted(self.states):
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
            if not formula:
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

    def group_conditions_by_consequence(self):
        """Group conditions by consequence."""
        group_by_dest = {dest: [] for dest in self.states}
        for source, trans in self.transitions.items():
            for key, dest in zip(trans.keys(), trans.values()):
                group_by_dest[dest].append((source, key))
        return dict(sorted(group_by_dest.items()))

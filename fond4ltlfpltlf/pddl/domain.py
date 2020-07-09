# -*- coding: utf-8 -*-

"""This module contains the implementations of a PDDL Domain."""


from fond4ltlfpltlf.pddl.formulas import FormulaAnd, FormulaWhen
from fond4ltlfpltlf.pddl.action import Action
import copy


class Domain:
    """A class for the PDDL Domain."""

    def __init__(self, name, requirements, types, constants, predicates, operators):
        """Initialize the Domain."""
        self.name = name  # string
        self.requirements = requirements  # list
        self.types = types  # list
        self.constants = constants  # list
        self.predicates = predicates  # list
        self.operators = operators  # list

    def __str__(self):
        """Get the string."""
        # if ':non-deterministic' in self.requirements:
        #     self.requirements.remove(':non-deterministic')
        domain_str = "(define (domain {0})\n".format(self.name)
        domain_str += "\t(:requirements {0})\n".format(" ".join(self.requirements))
        if self.types:
            domain_str += "\t(:types {0})\n".format(" ".join(self.types))
        if self.constants:
            domain_str += "\t(:constants {0})\n".format(
                " ".join(map(str, self.constants))
            )
        domain_str += "\t(:predicates {0})\n".format(
            " ".join(map(str, self.predicates))
        )

        for op in self.operators:
            domain_str += "\t(:action {0})\n".format(str(op).replace("\n", "\n\t"))

        domain_str += ")"
        return domain_str

    def add_operators_trans(self, transition_operators):
        """Add trans actions."""
        for operator in transition_operators:
            self.operators.append(operator)

    def add_predicates(self, parameters, states):
        """Add DFA predicates."""
        self.predicates.append("(turnDomain)")
        for state in states:
            self.predicates.append(
                "(q{0} {1})".format(str(state), " ".join(map(str, parameters)))
            )

    def add_constants(self, states):
        """Add constants."""
        for state in states:
            self.constants.append("{0}".format(str(state)))

    def add_precond_effect(self):
        """Add preconditions and effects."""
        for op in self.operators:
            # if isinstance(op, str):
            #     pass
            # else:
            #     if op.isOneOf():
            #         oneof_fluent = str(op.effects)
            #         self.predicates.append(oneof_fluent)
            #     else:
            #         pass
            op.add_turn_domain()

    def get_new_domain(self, parameters, states, transition_operators):
        """Get the new domain."""
        # self.add_constants(states)
        self.compile_simple_adl()
        self.add_predicates(parameters, states)
        self.add_precond_effect()
        self.add_operators_trans(transition_operators)
        return self

    def modify_operator(self, op_copy, condition, formula):
        """Modify operator."""
        if isinstance(op_copy.preconditions, FormulaAnd):
            op_copy.preconditions.andList.append(condition)
            new_preconditions = op_copy.preconditions.andList
            new_effects = formula
        else:
            new_preconditions = FormulaAnd([op_copy.preconditions, condition])
            new_effects = formula
        new_op = Action(
            op_copy.name, op_copy.parameters, new_preconditions, new_effects
        )
        return new_op

    def compile_simple_adl(self):
        """Compile simple ADL conditional effects."""
        i = 0
        for op in self.operators:
            if isinstance(op.effects, FormulaWhen):
                # it remains only one operator, but we need to modify it
                condition_formula = op.effects.condition
                statement_formula = op.effects.formula
                new_op = self.modify_operator(
                    copy.deepcopy(op), condition_formula, statement_formula
                )
                self.operators[i] = new_op
                continue
            elif isinstance(op.effects, FormulaAnd):
                no_of_whens = op.effects.count_whens()
                if no_of_whens == 0:
                    continue
                else:
                    pos = self.operators.index(op)
                    new_op_list = self.split_operator(copy.deepcopy(op), no_of_whens)
                    self.operators[pos : pos + 1] = new_op_list  # noqa
            i += 1

    def split_operator(self, op, number):
        """Split an ADL operator into a list of operators."""
        new_op_list = []
        pair_precond_effect = []
        additionals = []
        formula = op.effects

        for item in formula.andList:
            if isinstance(item, FormulaWhen):
                formula_condition = item.condition
                formula_statement = item.formula
                pair_precond_effect.append(
                    [
                        FormulaAnd([op.preconditions, formula_condition]),
                        formula_statement,
                    ]
                )
            else:
                additionals.append(item)
        k = 1
        for j in range(len(pair_precond_effect)):
            pair_precond_effect[j][k] = FormulaAnd(
                [pair_precond_effect[j][k]] + additionals
            )

        for u in range(number):
            new_op = Action(
                op.name + "-" + str(u),
                op.parameters,
                pair_precond_effect[u][0],
                pair_precond_effect[u][1],
            )
            new_op_list.append(new_op)

        return new_op_list


##############################################################
#     def get_oneofs(self):
#         oneofs = []
#         for operator in self.operators:
#             if isinstance(operator.effects, FormulaOneOf):
#                 oneofs.append(operator.effects)
#         return oneofs
#
#     def delete_oneofs_placeholder(self):
#         temp = copy.deepcopy(self.predicates)
#         for predicate in temp:
#             if predicate._name.startswith('ONEOF'):
#                 if predicate in self.predicates:
#                     self.predicates.remove(predicate)
#             else:
#                 pass
#
#     def replace_oneofs(self, oneof_list):
#         for operator in self.operators:
#             if isinstance(operator.effects, FormulaAnd):
#                 for predicate in operator.effects.andList:
#                     if predicate.predicate.name.startswith('ONEOF'):
#                         # print(operator.effects.andList.index(predicate))
#                         oneof_item = predicate.predicate.name.split('-')
#                         id = oneof_item[1]
#                         variables_ = oneof_item[2:]
#                         new_formula = change_oneof(id, variables_, oneof_list)
#                         operator.effects.andList[operator.effects.andList.index(predicate)] = new_formula
#             else:
#                 pass
#         return self
#
# def change_oneof(id, _variables, original_oneof_list):
#     for oneof_formula in original_oneof_list:
#         if oneof_formula.id == id:
#             # substitute variables inside oneof items
#             legend = dict(zip(oneof_formula.variables_order, _variables))
#             new = substitute_variables(oneof_formula, legend)
#             # oneof_formula.flag = False
#             # print(oneof_formula)
#             return new
#
# def substitute_variables(formula, legend):
#     # print(legend)
#     subformulas_list = []
#     for subformula in formula.oneofList:
#         temp = copy.deepcopy(subformula)
#         for item in temp.andList:
#             grounded_var = ''
#             for arg in item.predicate._args:
#                 grounded_var += '-'+str(legend[arg])
#             item.predicate._name = item.predicate._name.upper()+grounded_var
#             # print(item.predicate._name)
#             item.predicate._args = []
#         subformula = copy.deepcopy(temp)
#         subformulas_list.append(subformula)
#     return FormulaOneOf('new', subformulas_list, False)

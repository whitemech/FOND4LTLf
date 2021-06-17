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

"""This module contains the implementations of a PDDL Problem."""

from fond4ltlfpltlf.pddl.formulas import FormulaAnd, FormulaOr
from fond4ltlfpltlf.pddl.predicate import Predicate
from fond4ltlfpltlf.pddl.term import Term


class Problem(object):
    """A class for the PDDL Problem."""

    def __init__(self, name, domain, objects, init, goal):
        """Initialize the formula."""
        self._name = name
        self._domain = domain
        self._objects = objects
        # self._objects = {}
        # for obj in objects:
        #     self._objects[obj.type] = self._objects.get(obj.type, [])
        #     self._objects[obj.type].append(str(obj.value))
        self._init = set(map(str, init))
        # if isinstance(goal, Iterable):
        #     self._goal = set(map(str, goal))
        # else:
        #     assert not isinstance(goal, Iterable)
        #     self._goal = {str(goal)}
        # self.new_goal = set()
        self._goal = goal

    @property
    def name(self):
        """Get the name."""
        return self._name

    @property
    def domain(self):
        """Get the domain."""
        return self._domain

    @property
    def objects(self):
        """Get the objects."""
        return self._objects

    @property
    def init(self):
        """Get the initial state."""
        return self._init

    @property
    def goal(self):
        """Get the goal state."""
        return self._goal

    def __str__(self):
        """Get the string."""
        problem_str = "(define (problem {0})\n".format(self._name)
        problem_str += "\t(:domain {0})\n".format(self._domain)
        problem_str += "\t(:objects {0})\n".format(" ".join(map(str, self._objects)))
        # problem_str += "\t(:objects"
        # for type, objects in self._objects.items():
        #     problem_str += " {0} - {1}".format(" ".join(sorted(objects)), type)
        # problem_str += ")\n"
        problem_str += "\t(:init {0})\n".format(" ".join(sorted(self._init)))

        # problem_str += "(:goal (and {0}))\n".format(" ".join(sorted(self.new_goal)))
        problem_str += "(:goal {0})\n".format(self._goal)
        problem_str += ")"
        return problem_str

    def __eq__(self, other):
        """Check equality between two PDDL Problems."""
        return (
            isinstance(other, Problem)
            and self._name == other._name
            and self._domain == other._domain
            and self._objects == other._objects
            and self._init == other._init
            and self._goal == other._goal
        )

    def make_new_init(self, obj_list):
        """Modify the initial state."""
        self._init.add("(turnDomain)")
        if obj_list:
            self._init.add("(q1 {0})".format(" ".join(obj_list)))
        else:
            self._init.add("(q1)")
        return self._init

    def make_new_goal(self, final_states, obj_list):
        """Modify the goal state."""
        self._goal = None
        # self._goal
        # self.new_goal.add("(turnDomain)")
        # self._goal.add('(turnDomain)')
        turn_domain = Predicate("turnDomain")
        if len(final_states) > 1:
            or_list = []
            for state in final_states:
                if obj_list:
                    # or_list.append("(q{0} {1})".format(str(state), " ".join(obj_list)))
                    or_list.append(
                        Predicate(
                            "q{0}".format(str(state)),
                            [Term.constant(obj) for obj in obj_list],
                        )
                    )
                else:
                    or_list.append(Predicate("q{0}".format(str(state))))
            new_formula = FormulaOr(or_list)
            # self._goal.add(str(new_formula))
            # self.new_goal.add(str(new_formula))
            self._goal = FormulaAnd([new_formula, turn_domain])
        else:
            and_list = []
            # self._goal.add('(= q {0})'.format(final_states[0]))
            if obj_list:
                and_list.append(
                    Predicate(
                        "q{0}".format(final_states[0]),
                        [Term.constant(obj) for obj in obj_list],
                    )
                )
                # self.new_goal.add(
                #     "(q{0} {1})".format(final_states[0], " ".join(obj_list))
                # )
            else:
                and_list.append(Predicate("q{0}".format(final_states[0])))
                # self.new_goal.add("(q{0})".format(final_states[0]))

            self._goal = FormulaAnd(and_list + [turn_domain])

    def get_new_problem(self, final_states, symbols_list):
        """Return the modified problem."""
        obj_list = self.extract_object_list(symbols_list)
        # self.objects_are_upper(obj_list)
        self.make_new_init(obj_list)
        self.make_new_goal(final_states, obj_list)
        return self

    def extract_object_list(self, symbols_list):
        """Return the objects list."""
        already_seen = set()
        obj_list = []
        for symbol in symbols_list:
            if symbol.objects:
                for obj in symbol.objects:
                    if obj not in already_seen:
                        already_seen.add(obj)
                        obj_list.append(obj)
                    else:
                        pass
            else:
                continue
        return obj_list

    def objects_are_upper(self, objects):
        """Check if objects are uppercase."""
        for value_list in self.objects.values():
            for val in value_list:
                if val.isupper() and val.lower() in objects:
                    objects[objects.index(val.lower())] = objects[
                        objects.index(val.lower())
                    ].upper()
                else:
                    pass

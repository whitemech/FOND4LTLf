# -*- coding: utf-8 -*-
"""Test the parsing module."""
import os
import tempfile
from collections import OrderedDict
from pathlib import Path

import pytest

from fond4ltlfpltlf.pddl.literal import Literal
from fond4ltlfpltlf.pddl.predicate import Predicate
from fond4ltlfpltlf.pddl.term import Term
from fond4ltlfpltlf.pddl.action import Action
from fond4ltlfpltlf.pddl.formulas import FormulaAnd, FormulaOr, FormulaNot, FormulaOneOf
from fond4ltlfpltlf.parser.parser import PDDLParser
from .conftest import TEST_ROOT_DIR


@pytest.mark.parametrize(
    ["domain"],
    [
        (os.path.join(TEST_ROOT_DIR, "data", "acrobatics", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "beam-walk", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "blocksworld-ipc08", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "doors", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "earth_observation", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "elevators", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "faults-ipc08", "d01.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "first-responders-ipc08", "domain.pddl"),),
        # (os.path.join(TEST_ROOT_DIR, "data", "islands", "domain.pddl"),),
        # (os.path.join(TEST_ROOT_DIR, "data", "miner", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "spiky-tireworld", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "tireworld", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "tireworld-truck", "domain.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "triangle-tireworld", "domain.pddl"),),
        # (os.path.join(TEST_ROOT_DIR, "data", "zenotravel", "domain.pddl"),),
    ],
)
def test_domain_parsing_is_deterministic(domain):
    """Test that domain parsing is deterministic."""
    parser = PDDLParser()
    domain_obj_1 = parser(open(domain).read())  # type: Domain
    temp = tempfile.mktemp()
    with open(temp, "w") as t:
        t.write(str(domain_obj_1))
    domain_obj_2 = parser(open(temp).read())
    assert domain_obj_1 == domain_obj_2


#
# @pytest.mark.parametrize(
#     ["problem"],
#     [
#         (os.path.join(TEST_ROOT_DIR, "data", "acrobatics", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "beam-walk", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "blocksworld-ipc08", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "doors", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "earth_observation", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "elevators", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "faults-ipc08", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "first-responders-ipc08", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "islands", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "miner", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "spiky-tireworld", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "tireworld", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "tireworld-truck", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "triangle-tireworld", "p01.pddl"),),
#         (os.path.join(TEST_ROOT_DIR, "data", "zenotravel", "p01.pddl"),),
#     ],
# )
# def test_problem_parsing_is_deterministic(problem):
#     """Test that problem parsing is deterministic."""
#     parser = PDDLParser()
#     problem_obj_1 = parser(open(problem).read())  # type: Problem
#     temp = tempfile.mktemp()
#     with open(temp, "w") as t:
#         t.write(str(problem_obj_1))
#     problem_obj_2 = parser(open(temp).read())
#     assert problem_obj_1 == problem_obj_2


class TestParsingDomain1:
    """Test parsing for tests/data/acrobatics/domain.pddl."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = PDDLParser()
        cls.pddl_obj = parser(
            open(str(Path(TEST_ROOT_DIR, "data", "acrobatics", "domain.pddl"))).read()
        )  # type: Domain
        cls.pddl_name = cls.pddl_obj.name
        cls.pddl_requirements = cls.pddl_obj.requirements
        cls.pddl_types = cls.pddl_obj.types
        cls.pddl_constants = cls.pddl_obj.constants
        cls.pddl_predicates = cls.pddl_obj.predicates
        cls.pddl_operators = cls.pddl_obj.operators

    def test_domain_name(self):
        """Test that the name is correct."""
        assert self.pddl_name == "acrobatics"

    def test_domain_requirements(self):
        """Test that the domain requirements are correct."""
        assert self.pddl_requirements == [":typing", ":strips", ":non-deterministic"]

    def test_domain_types(self):
        """Test that the domain types are correct."""
        assert self.pddl_types == ["location"]

    def test_domain_constants(self):
        """Test that the domain constants are correct."""
        assert self.pddl_constants == []

    def test_domain_predicates(self):
        """Test that the domain predicates are correct."""
        assert self.pddl_predicates == [
            Predicate("up"),
            Predicate("position", [Term.variable("p1", "location")]),
            Predicate(
                "next-fwd",
                [Term.variable("p1", "location"), Term.variable("p2", "location")],
            ),
            Predicate(
                "next-bwd",
                [Term.variable("p1", "location"), Term.variable("p2", "location")],
            ),
            Predicate("ladder-at", [Term.variable("p", "location")]),
            Predicate("broken-leg"),
        ]

    def test_domain_operators(self):
        """Test that the domain operators are correct."""
        op1 = Action(
            name="walk-on-beam",
            parameters=[
                Term.variable("?from", "location"),
                Term.variable("?to", "location"),
            ],
            preconditions=FormulaAnd(
                [
                    Literal.negative(Predicate("broken-leg")),
                    Literal.positive(Predicate("up")),
                    Literal.positive(Predicate("position", [Term.variable("?from")])),
                    Literal.positive(
                        Predicate(
                            "next-fwd", [Term.variable("?from"), Term.variable("?to")]
                        )
                    ),
                ]
            ),
            effects=FormulaOneOf(
                [
                    FormulaAnd(
                        [
                            Literal.positive(
                                Predicate("position", [Term.variable("?to")])
                            ),
                            Literal.negative(
                                Predicate("position", [Term.variable("?from")])
                            ),
                        ]
                    ),
                    FormulaAnd(
                        [
                            Literal.negative(Predicate("up")),
                            Literal.positive(
                                Predicate("position", [Term.variable("?to")])
                            ),
                            Literal.negative(
                                Predicate("position", [Term.variable("?from")])
                            ),
                        ]
                    ),
                ]
            ),
        )
        op2 = Action(
            name="walk-left",
            parameters=[
                Term.variable("?from", "location"),
                Term.variable("?to", "location"),
            ],
            preconditions=FormulaAnd(
                [
                    Literal.negative(Predicate("broken-leg")),
                    Literal.negative(Predicate("up")),
                    Literal.positive(Predicate("position", [Term.variable("?from")])),
                    Literal.positive(
                        Predicate(
                            "next-bwd", [Term.variable("?from"), Term.variable("?to")]
                        )
                    ),
                ]
            ),
            effects=FormulaAnd(
                [
                    Literal.positive(Predicate("position", [Term.variable("?to")])),
                    Literal.negative(Predicate("position", [Term.variable("?from")])),
                ]
            ),
        )
        op3 = Action(
            name="walk-right",
            parameters=[
                Term.variable("?from", "location"),
                Term.variable("?to", "location"),
            ],
            preconditions=FormulaAnd(
                [
                    Literal.negative(Predicate("broken-leg")),
                    Literal.negative(Predicate("up")),
                    Literal.positive(Predicate("position", [Term.variable("?from")])),
                    Literal.positive(
                        Predicate(
                            "next-fwd", [Term.variable("?from"), Term.variable("?to")]
                        )
                    ),
                ]
            ),
            effects=FormulaAnd(
                [
                    Literal.positive(Predicate("position", [Term.variable("?to")])),
                    Literal.negative(Predicate("position", [Term.variable("?from")])),
                ]
            ),
        )
        op4 = Action(
            name="climb",
            parameters=[Term.variable("?p", "location")],
            preconditions=FormulaAnd(
                [
                    Literal.negative(Predicate("broken-leg")),
                    Literal.negative(Predicate("up")),
                    Literal.positive(Predicate("position", [Term.variable("?p")])),
                    Literal.positive(Predicate("ladder-at", [Term.variable("?p")])),
                ]
            ),
            effects=FormulaAnd([Literal.positive(Predicate("up"))]),
        )
        op5 = Action(
            name="climb-down",
            parameters=[],
            preconditions=FormulaAnd(
                [
                    Literal.negative(Predicate("broken-leg")),
                    Literal.positive(Predicate("up")),
                ]
            ),
            effects=FormulaAnd([Literal.negative(Predicate("up"))]),
        )
        op6 = Action(
            name="jump-over",
            parameters=[
                Term.variable("?from", "location"),
                Term.variable("?middle", "location"),
                Term.variable("?to", "location"),
            ],
            preconditions=FormulaAnd(
                [
                    Literal.negative(Predicate("broken-leg")),
                    Literal.positive(Predicate("up")),
                    Literal.positive(Predicate("position", [Term.variable("?from")])),
                    Literal.positive(
                        Predicate(
                            "next-fwd",
                            [Term.variable("?from"), Term.variable("?middle")],
                        )
                    ),
                    Literal.positive(
                        Predicate(
                            "next-fwd", [Term.variable("?middle"), Term.variable("?to")]
                        )
                    ),
                ]
            ),
            effects=FormulaOneOf(
                [
                    FormulaAnd(
                        [
                            Literal.negative(Predicate("up")),
                            Literal.positive(Predicate("broken-leg")),
                        ]
                    ),
                    FormulaAnd(
                        [
                            Literal.negative(Predicate("up")),
                            Literal.positive(Predicate("broken-leg")),
                            Literal.positive(
                                Predicate("position", [Term.variable("?middle")])
                            ),
                            Literal.negative(
                                Predicate("position", [Term.variable("?from")])
                            ),
                        ]
                    ),
                    FormulaAnd(
                        [
                            Literal.negative(Predicate("up")),
                            Literal.positive(
                                Predicate("position", [Term.variable("?middle")])
                            ),
                            Literal.negative(
                                Predicate("position", [Term.variable("?from")])
                            ),
                        ]
                    ),
                    FormulaAnd(
                        [
                            Literal.negative(Predicate("up")),
                            Literal.positive(Predicate("broken-leg")),
                            Literal.positive(
                                Predicate("position", [Term.variable("?to")])
                            ),
                            Literal.negative(
                                Predicate("position", [Term.variable("?from")])
                            ),
                        ]
                    ),
                    FormulaAnd(
                        [
                            Literal.negative(Predicate("up")),
                            Literal.positive(
                                Predicate("position", [Term.variable("?to")])
                            ),
                            Literal.negative(
                                Predicate("position", [Term.variable("?from")])
                            ),
                        ]
                    ),
                    FormulaAnd(
                        [
                            Literal.positive(
                                Predicate("position", [Term.variable("?to")])
                            ),
                            Literal.negative(
                                Predicate("position", [Term.variable("?from")])
                            ),
                        ]
                    ),
                ]
            ),
        )
        assert self.pddl_operators == [op1, op2, op3, op4, op5, op6]


class TestParsingProblem1:
    """Test parsing for tests/data/acrobatics/p01.pddl."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = PDDLParser()
        cls.pddl_obj = parser(
            open(str(Path(TEST_ROOT_DIR, "data", "acrobatics", "p01.pddl"))).read()
        )  # type: Problem
        cls.pddl_name = cls.pddl_obj.name
        cls.pddl_domain = cls.pddl_obj.domain
        cls.pddl_objects = cls.pddl_obj.objects
        cls.pddl_init = cls.pddl_obj.init
        cls.pddl_goal = cls.pddl_obj.goal

    def test_problem_name(self):
        """Test that the name is correct."""
        assert self.pddl_name == "beam-walk-2"

    def test_problem_domain(self):
        """Test that the domain name is correct."""
        assert self.pddl_domain == "acrobatics"

    def test_problem_objects(self):
        """Test that the objects are correct."""
        assert self.pddl_objects == {"location": ["p0", "p1"]}

    def test_problem_init(self):
        """Test that the initial condition is correct."""
        assert self.pddl_init == {
            "(next-bwd p1 p0)",
            "(ladder-at p0)",
            "(next-fwd p0 p1)",
            "(position p0)",
        }

    def test_problem_goal(self):
        """Test that the goal condition is correct."""
        assert self.pddl_goal == {"(up)", "(position p1)"}

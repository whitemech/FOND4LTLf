# -*- coding: utf-8 -*-

"""Test the parsing module."""

import os
import tempfile
import pytest

from pathlib import Path
from .conftest import TEST_ROOT_DIR

from fond4ltlfpltlf.pddl.literal import Literal
from fond4ltlfpltlf.pddl.predicate import Predicate
from fond4ltlfpltlf.pddl.term import Term
from fond4ltlfpltlf.pddl.action import Action
from fond4ltlfpltlf.pddl.formulas import (
    FormulaAnd,
    FormulaOneOf,
)
from fond4ltlfpltlf.parser.parser import PDDLParser


@pytest.mark.parametrize(
    ["domain"],
    [
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "acrobatics", "domain.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "beam-walk", "domain.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "blocksworld-ipc08",
                "domain.pddl",
            ),
        ),
        (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "doors", "domain.pddl"),),
        (
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "earth_observation",
                "domain.pddl",
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "elevators", "domain.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "faults-ipc08", "d01.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "first-responders-ipc08",
                "domain.pddl",
            ),
        ),
        # (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "islands", "domain.pddl"),),
        # (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "miner", "domain.pddl"),),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "spiky-tireworld", "domain.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "tireworld", "domain.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "tireworld-truck", "domain.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "triangle-tireworld",
                "domain.pddl",
            ),
        ),
        # (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "zenotravel", "domain.pddl"),),
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


@pytest.mark.parametrize(
    ["problem"],
    [
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "acrobatics", "p01.pddl"
            ),
        ),
        (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "beam-walk", "p01.pddl"),),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "blocksworld-ipc08", "p01.pddl"
            ),
        ),
        (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "doors", "p01.pddl"),),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "earth_observation", "p01.pddl"
            ),
        ),
        (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "elevators", "p01.pddl"),),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "faults-ipc08", "p01.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "first-responders-ipc08",
                "p01.pddl",
            ),
        ),
        (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "islands", "p01.pddl"),),
        (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "miner", "p01.pddl"),),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "spiky-tireworld", "p01.pddl"
            ),
        ),
        (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "tireworld", "p01.pddl"),),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "tireworld-truck", "p01.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "triangle-tireworld", "p01.pddl"
            ),
        ),
        (
            os.path.join(
                TEST_ROOT_DIR, "data", "pddl-domains", "zenotravel", "p01.pddl"
            ),
        ),
    ],
)
def test_problem_parsing_is_deterministic(problem):
    """Test that problem parsing is deterministic."""
    parser = PDDLParser()
    problem_obj_1 = parser(open(problem).read())  # type: Problem
    temp = tempfile.mktemp()
    with open(temp, "w") as t:
        t.write(str(problem_obj_1))
    problem_obj_2 = parser(open(temp).read())
    assert problem_obj_1 == problem_obj_2


class TestParsingDomain1:
    """Test parsing for tests/data/pddl-domains/acrobatics/domain.pddl."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = PDDLParser()
        cls.pddl_obj = parser(
            open(
                str(
                    Path(
                        TEST_ROOT_DIR,
                        "data",
                        "pddl-domains",
                        "acrobatics",
                        "domain.pddl",
                    )
                )
            ).read()
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
    """Test parsing for tests/data/pddl-domains/acrobatics/p01.pddl."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = PDDLParser()
        cls.pddl_obj = parser(
            open(
                str(
                    Path(
                        TEST_ROOT_DIR, "data", "pddl-domains", "acrobatics", "p01.pddl"
                    )
                )
            ).read()
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
        assert self.pddl_objects == [
            Term.constant("p0", "location"),
            Term.constant("p1", "location"),
        ]

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
        assert self.pddl_goal == FormulaAnd(
            [Predicate("up"), Predicate("position", [Term.constant("p1")])]
        )


class TestParsingDomain2:
    """Test parsing for tests/data/pddl-domains/triangle-tireworld/domain.pddl."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = PDDLParser()
        cls.pddl_obj = parser(
            open(
                str(
                    Path(
                        TEST_ROOT_DIR,
                        "data",
                        "pddl-domains",
                        "triangle-tireworld",
                        "domain.pddl",
                    )
                )
            ).read()
        )  # type: Domain
        cls.pddl_name = cls.pddl_obj.name
        cls.pddl_requirements = cls.pddl_obj.requirements
        cls.pddl_types = cls.pddl_obj.types
        cls.pddl_constants = cls.pddl_obj.constants
        cls.pddl_predicates = cls.pddl_obj.predicates
        cls.pddl_operators = cls.pddl_obj.operators

    def test_domain_name(self):
        """Test that the name is correct."""
        assert self.pddl_name == "triangle-tire"

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
            Predicate("vehicleat", [Term.variable("loc", "location")]),
            Predicate("spare-in", [Term.variable("loc", "location")]),
            Predicate(
                "road",
                [Term.variable("from", "location"), Term.variable("to", "location")],
            ),
            Predicate("not-flattire"),
        ]

    def test_domain_operators(self):
        """Test that the domain operators are correct."""
        op1 = Action(
            name="move-car",
            parameters=[
                Term.variable("?from", "location"),
                Term.variable("?to", "location"),
            ],
            preconditions=FormulaAnd(
                [
                    Literal.positive(Predicate("vehicleat", [Term.variable("?from")])),
                    Literal.positive(
                        Predicate(
                            "road", [Term.variable("?from"), Term.variable("?to")]
                        )
                    ),
                    Literal.positive(Predicate("not-flattire")),
                ]
            ),
            effects=FormulaAnd(
                [
                    FormulaOneOf(
                        [
                            FormulaAnd(
                                [
                                    Literal.positive(
                                        Predicate("vehicleat", [Term.variable("?to")])
                                    ),
                                    Literal.negative(
                                        Predicate("vehicleat", [Term.variable("?from")])
                                    ),
                                ]
                            ),
                            FormulaAnd(
                                [
                                    Literal.positive(
                                        Predicate("vehicleat", [Term.variable("?to")])
                                    ),
                                    Literal.negative(
                                        Predicate("vehicleat", [Term.variable("?from")])
                                    ),
                                    Literal.negative(Predicate("not-flattire")),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        )
        op2 = Action(
            name="changetire",
            parameters=[Term.variable("?loc", "location"),],
            preconditions=FormulaAnd(
                [
                    Literal.positive(Predicate("spare-in", [Term.variable("?loc")])),
                    Literal.positive(Predicate("vehicleat", [Term.variable("?loc")])),
                ]
            ),
            effects=FormulaAnd(
                [
                    Literal.negative(Predicate("spare-in", [Term.variable("?loc")])),
                    Literal.positive(Predicate("not-flattire")),
                ]
            ),
        )

        assert self.pddl_operators == [
            op1,
            op2,
        ]


class TestParsingProblem2:
    """Test parsing for tests/data/pddl-domains/triangle-tireworld/p01.pddl."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = PDDLParser()
        cls.pddl_obj = parser(
            open(
                str(
                    Path(
                        TEST_ROOT_DIR,
                        "data",
                        "pddl-domains",
                        "triangle-tireworld",
                        "p01.pddl",
                    )
                )
            ).read()
        )  # type: Problem
        cls.pddl_name = cls.pddl_obj.name
        cls.pddl_domain = cls.pddl_obj.domain
        cls.pddl_objects = cls.pddl_obj.objects
        cls.pddl_init = cls.pddl_obj.init
        cls.pddl_goal = cls.pddl_obj.goal

    def test_problem_name(self):
        """Test that the name is correct."""
        assert self.pddl_name == "triangle-tire-1"

    def test_problem_domain(self):
        """Test that the domain name is correct."""
        assert self.pddl_domain == "triangle-tire"

    def test_problem_objects(self):
        """Test that the objects are correct."""
        assert self.pddl_objects == [
            Term.constant("l-1-1", "location"),
            Term.constant("l-1-2", "location"),
            Term.constant("l-1-3", "location"),
            Term.constant("l-2-1", "location"),
            Term.constant("l-2-2", "location"),
            Term.constant("l-2-3", "location"),
            Term.constant("l-3-1", "location"),
            Term.constant("l-3-2", "location"),
            Term.constant("l-3-3", "location"),
        ]

    def test_problem_init(self):
        """Test that the initial condition is correct."""
        assert self.pddl_init == {
            "(vehicleat l-1-1)",
            "(road l-1-1 l-1-2)",
            "(road l-1-2 l-1-3)",
            "(road l-1-1 l-2-1)",
            "(road l-1-2 l-2-2)",
            "(road l-2-1 l-1-2)",
            "(road l-2-2 l-1-3)",
            "(spare-in l-2-1)",
            "(spare-in l-2-2)",
            "(road l-2-1 l-3-1)",
            "(road l-3-1 l-2-2)",
            "(spare-in l-3-1)",
            "(spare-in l-3-1)",
            "(not-flattire)",
        }

    def test_problem_goal(self):
        """Test that the goal condition is correct."""
        assert self.pddl_goal == Predicate("vehicleat", [Term.constant("l-1-3")])

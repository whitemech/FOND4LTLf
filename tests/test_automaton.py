# -*- coding: utf-8 -*-

"""Test the automaton part of tool."""

from pathlib import Path

from fond4ltlfpltlf.automa.aparser import parse_dfa
from fond4ltlfpltlf.automa.symbol import Symbol
from fond4ltlfpltlf.parser.parser import PDDLParser
from fond4ltlfpltlf.pddl.action import Action
from fond4ltlfpltlf.pddl.formulas import (
    FormulaAnd,
    FormulaOneOf,
    FormulaOr,
)
from fond4ltlfpltlf.pddl.literal import Literal
from fond4ltlfpltlf.pddl.predicate import Predicate
from fond4ltlfpltlf.pddl.term import Term
from .conftest import TEST_ROOT_DIR


class TestParsingAutomaton1:
    """Test parsing for tests/data/automata/Fa.aut."""

    parser = PDDLParser()

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.aut_obj = parse_dfa(
            open(str(Path(TEST_ROOT_DIR, "data", "automata", "Fa.aut"))).read()
        )  # type: Automaton
        cls.aut_alphabet = cls.aut_obj.alphabet
        cls.aut_states = cls.aut_obj.states
        cls.aut_initial_state = cls.aut_obj.initial_state
        cls.aut_accepting_states = cls.aut_obj.accepting_states
        cls.aut_transitions = cls.aut_obj.transitions
        cls.aut_trans_by_dest = cls.aut_obj.trans_by_dest

    def test_automaton_alphabet(self):
        """Test that the alphabet is correct."""
        assert self.aut_alphabet == {"0", "1", "X"}

    def test_automaton_states(self):
        """Test that the states are correct."""
        assert self.aut_states == {"1", "2", "3"}

    def test_automaton_initial_state(self):
        """Test that the initial state is correct."""
        assert self.aut_initial_state == "1"

    def test_automaton_accepting_states(self):
        """Test that the accepting states are correct."""
        assert self.aut_accepting_states == {"3"}

    def test_automaton_transitions(self):
        """Test that the transitions are correct."""
        assert self.aut_transitions == {
            "1": {"0": "2", "1": "3"},
            "2": {"0": "2", "1": "3"},
            "3": {"X": "3"},
        }

    def test_automaton_trans_by_dest(self):
        """Test that the transitions by destination are correct."""
        assert self.aut_trans_by_dest == {
            "1": [],
            "2": [("1", "0"), ("2", "0")],
            "3": [("1", "1"), ("2", "1"), ("3", "X")],
        }

    def test_automaton_compute_parameters_1(self):
        """Test that the computation of parameters and object mapping are correct."""
        pddl_domain = self.parser(
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
        )
        grounded_symbols = [Symbol("vehicleat", ["l31"])]
        actual_params, actual_obj_map = self.aut_obj.compute_parameters(
            pddl_domain.predicates, grounded_symbols
        )
        expected_params = [Term.variable("?loc-00", "location")]
        expected_objmap = {"l31": ["?loc-00", "location"]}
        assert actual_params == expected_params and actual_obj_map == expected_objmap

    def test_automaton_compute_vars_mapping_1(self):
        """Test that the vars mapping is correct."""
        grounded_symbols = [Symbol("vehicleat", ["l31"])]
        objmap = {"l31": ["?loc-00", "location"]}
        actual_vars_map = self.aut_obj.compute_varsMapping(grounded_symbols, objmap)
        expected_vars_map = {Symbol("vehicleat", ["l31"]): [("?loc-00", "location")]}
        assert actual_vars_map == expected_vars_map

    def test_automaton_compute_parameters_2(self):
        """Test that the computation of parameters and object mapping are correct."""
        pddl_domain = self.parser(
            open(
                str(
                    Path(
                        TEST_ROOT_DIR,
                        "data",
                        "pddl-domains",
                        "blocksworld-ipc08",
                        "domain.pddl",
                    )
                )
            ).read()
        )
        grounded_symbols = [Symbol("on", ["b1", "b2"])]
        actual_params, actual_obj_map = self.aut_obj.compute_parameters(
            pddl_domain.predicates, grounded_symbols
        )
        expected_params = [
            Term.variable("?b1-00", "block"),
            Term.variable("?b2-01", "block"),
        ]
        expected_objmap = {"b1": ["?b1-00", "block"], "b2": ["?b2-01", "block"]}
        assert actual_params == expected_params and actual_obj_map == expected_objmap

    def test_automaton_compute_vars_mapping_2(self):
        """Test that the vars mapping is correct."""
        grounded_symbols = [Symbol("on", ["b1", "b2"])]
        objmap = {"b1": ["?b1-00", "block"], "b2": ["?b2-01", "block"]}
        actual_vars_map = self.aut_obj.compute_varsMapping(grounded_symbols, objmap)
        expected_vars_map = {
            Symbol("on", ["b1", "b2"]): [("?b1-00", "block"), ("?b2-01", "block")]
        }
        assert actual_vars_map == expected_vars_map

    def test_automaton_create_trans_op(self):
        """Test that the created trans operator is correct."""
        pddl_domain = self.parser(
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
        )
        grounded_symbols = [Symbol("vehicleat", ["l31"])]
        actual_trans_ops, actual_params = self.aut_obj.create_operators_trans(
            pddl_domain.predicates, grounded_symbols
        )
        expected_trans_ops = [
            Action(
                name="trans-0",
                parameters=[Term.variable("?loc-00", "location")],
                preconditions=FormulaAnd(
                    [
                        FormulaOr(
                            [
                                FormulaAnd(
                                    [
                                        Literal.positive(Predicate("q1", ["?loc-00"])),
                                        Literal.negative(
                                            Predicate("vehicleat", ["?loc-00"])
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(Predicate("q2", ["?loc-00"])),
                                        Literal.negative(
                                            Predicate("vehicleat", ["?loc-00"])
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        Literal.negative(Predicate("turnDomain")),
                    ]
                ),
                effects=FormulaAnd(
                    [
                        Literal.positive(Predicate("q2", ["?loc-00"])),
                        Literal.negative(Predicate("q1", ["?loc-00"])),
                        Literal.negative(Predicate("q3", ["?loc-00"])),
                        Literal.positive(Predicate("turnDomain")),
                    ]
                ),
            ),
            Action(
                name="trans-1",
                parameters=[Term.variable("?loc-00", "location")],
                preconditions=FormulaAnd(
                    [
                        FormulaOr(
                            [
                                FormulaAnd(
                                    [
                                        Literal.positive(Predicate("q1", ["?loc-00"])),
                                        Literal.positive(
                                            Predicate("vehicleat", ["?loc-00"])
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(Predicate("q2", ["?loc-00"])),
                                        Literal.positive(
                                            Predicate("vehicleat", ["?loc-00"])
                                        ),
                                    ]
                                ),
                                Literal.positive(Predicate("q3", ["?loc-00"])),
                            ]
                        ),
                        Literal.negative(Predicate("turnDomain")),
                    ]
                ),
                effects=FormulaAnd(
                    [
                        Literal.positive(Predicate("q3", ["?loc-00"])),
                        Literal.negative(Predicate("q1", ["?loc-00"])),
                        Literal.negative(Predicate("q2", ["?loc-00"])),
                        Literal.positive(Predicate("turnDomain")),
                    ]
                ),
            ),
        ]
        expected_params = [Term.variable("?loc-00", "location")]
        assert actual_trans_ops == expected_trans_ops
        assert actual_params == expected_params


class TestParsingAutomaton2:
    """Test parsing for tests/data/automata/Fabc.aut."""

    parser = PDDLParser()

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.aut_obj = parse_dfa(
            open(str(Path(TEST_ROOT_DIR, "data", "automata", "Fabc.aut"))).read()
        )  # type: Automaton
        cls.aut_alphabet = cls.aut_obj.alphabet
        cls.aut_states = cls.aut_obj.states
        cls.aut_initial_state = cls.aut_obj.initial_state
        cls.aut_accepting_states = cls.aut_obj.accepting_states
        cls.aut_transitions = cls.aut_obj.transitions
        cls.aut_trans_by_dest = cls.aut_obj.trans_by_dest

    def test_automaton_alphabet(self):
        """Test that the alphabet is correct."""
        assert self.aut_alphabet == {"0", "1", "X"}

    def test_automaton_states(self):
        """Test that the states are correct."""
        assert self.aut_states == {"1", "2", "3"}

    def test_automaton_initial_state(self):
        """Test that the initial state is correct."""
        assert self.aut_initial_state == "1"

    def test_automaton_accepting_states(self):
        """Test that the accepting states are correct."""
        assert self.aut_accepting_states == {"3"}

    def test_automaton_transitions(self):
        """Test that the transitions are correct."""
        assert self.aut_transitions == {
            "1": {"0XX": "2", "10X": "2", "110": "2", "111": "3"},
            "2": {"0XX": "2", "10X": "2", "110": "2", "111": "3"},
            "3": {"XXX": "3"},
        }

    def test_automaton_trans_by_dest(self):
        """Test that the transitions by destination are correct."""
        assert self.aut_trans_by_dest == {
            "1": [],
            "2": [
                ("1", "0XX"),
                ("1", "10X"),
                ("1", "110"),
                ("2", "0XX"),
                ("2", "10X"),
                ("2", "110"),
            ],
            "3": [("1", "111"), ("2", "111"), ("3", "XXX")],
        }

    def test_automaton_compute_parameters_1(self):
        """Test that the computation of parameters and object mapping are correct on triangle-tireworld."""
        pddl_domain = self.parser(
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
        )
        grounded_symbols = [
            Symbol("vehicleat", ["l31"]),
            Symbol("vehicleat", ["l12"]),
            Symbol("vehicleat", ["l22"]),
        ]
        actual_params, actual_obj_map = self.aut_obj.compute_parameters(
            pddl_domain.predicates, grounded_symbols
        )
        expected_params = [
            Term.variable("?loc-00", "location"),
            Term.variable("?loc-01", "location"),
            Term.variable("?loc-02", "location"),
        ]
        expected_objmap = {
            "l31": ["?loc-00", "location"],
            "l12": ["?loc-01", "location"],
            "l22": ["?loc-02", "location"],
        }
        assert actual_params == expected_params and actual_obj_map == expected_objmap

    def test_automaton_compute_vars_mapping_1(self):
        """Test that the vars mapping is correct."""
        grounded_symbols = [
            Symbol("vehicleat", ["l31"]),
            Symbol("vehicleat", ["l12"]),
            Symbol("vehicleat", ["l22"]),
        ]
        objmap = {
            "l31": ["?loc-00", "location"],
            "l12": ["?loc-01", "location"],
            "l22": ["?loc-02", "location"],
        }
        actual_vars_map = self.aut_obj.compute_varsMapping(grounded_symbols, objmap)
        expected_vars_map = {
            Symbol("vehicleat", ["l31"]): [("?loc-00", "location")],
            Symbol("vehicleat", ["l12"]): [("?loc-01", "location")],
            Symbol("vehicleat", ["l22"]): [("?loc-02", "location")],
        }
        assert actual_vars_map == expected_vars_map

    def test_automaton_compute_parameters_2(self):
        """Test that the computation of parameters and object mapping are correct on blocksworld."""
        pddl_domain = self.parser(
            open(
                str(
                    Path(
                        TEST_ROOT_DIR,
                        "data",
                        "pddl-domains",
                        "blocksworld-ipc08",
                        "domain.pddl",
                    )
                )
            ).read()
        )
        grounded_symbols = [
            Symbol("on", ["b1", "b2"]),
            Symbol("on", ["b2", "b5"]),
            Symbol("emptyhand"),
        ]
        actual_params, actual_obj_map = self.aut_obj.compute_parameters(
            pddl_domain.predicates, grounded_symbols
        )
        expected_params = [
            Term.variable("?b1-00", "block"),
            Term.variable("?b2-01", "block"),
            Term.variable("?b2-02", "block"),
        ]
        expected_objmap = {
            "b1": ["?b1-00", "block"],
            "b2": ["?b2-01", "block"],
            "b5": ["?b2-02", "block"],
        }
        assert actual_params == expected_params and actual_obj_map == expected_objmap

    def test_automaton_compute_vars_mapping_2(self):
        """Test that the vars mapping is correct."""
        grounded_symbols = [
            Symbol("on", ["b1", "b2"]),
            Symbol("on", ["b2", "b5"]),
            Symbol("emptyhand"),
        ]
        objmap = {
            "b1": ["?b1-00", "block"],
            "b2": ["?b2-01", "block"],
            "b5": ["?b2-02", "block"],
        }
        actual_vars_map = self.aut_obj.compute_varsMapping(grounded_symbols, objmap)
        expected_vars_map = {
            Symbol("on", ["b1", "b2"]): [("?b1-00", "block"), ("?b2-01", "block")],
            Symbol("on", ["b2", "b5"]): [("?b2-01", "block"), ("?b2-02", "block")],
            Symbol("emptyhand"): [],
        }
        assert actual_vars_map == expected_vars_map

    def test_automaton_create_trans_op_1(self):
        """Test that the created trans operator is correct."""
        pddl_domain = self.parser(
            open(
                str(
                    Path(
                        TEST_ROOT_DIR,
                        "data",
                        "pddl-domains",
                        "blocksworld-ipc08",
                        "domain.pddl",
                    )
                )
            ).read()
        )
        grounded_symbols = [
            Symbol("on", ["b1", "b2"]),
            Symbol("on", ["b2", "b5"]),
            Symbol("emptyhand"),
        ]
        actual_trans_ops, actual_params = self.aut_obj.create_operators_trans(
            pddl_domain.predicates, grounded_symbols
        )
        expected_trans_ops = [
            Action(
                name="trans-0",
                parameters=[
                    Term.variable("?b1-00", "block"),
                    Term.variable("?b2-01", "block"),
                    Term.variable("?b2-02", "block"),
                ],
                preconditions=FormulaAnd(
                    [
                        FormulaOr(
                            [
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate(
                                                "q1", ["?b1-00", "?b2-01", "?b2-02"],
                                            )
                                        ),
                                        Literal.negative(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate(
                                                "q1", ["?b1-00", "?b2-01", "?b2-02"],
                                            )
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.negative(
                                            Predicate("on", ["?b2-01", "?b2-02"],)
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate(
                                                "q1", ["?b1-00", "?b2-01", "?b2-02"],
                                            )
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b2-01", "?b2-02"],)
                                        ),
                                        Literal.negative(Predicate("emptyhand")),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate(
                                                "q2", ["?b1-00", "?b2-01", "?b2-02"],
                                            )
                                        ),
                                        Literal.negative(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate(
                                                "q2", ["?b1-00", "?b2-01", "?b2-02"],
                                            )
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.negative(
                                            Predicate("on", ["?b2-01", "?b2-02"],)
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate(
                                                "q2", ["?b1-00", "?b2-01", "?b2-02"],
                                            )
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b2-01", "?b2-02"],)
                                        ),
                                        Literal.negative(Predicate("emptyhand")),
                                    ]
                                ),
                            ]
                        ),
                        Literal.negative(Predicate("turnDomain")),
                    ]
                ),
                effects=FormulaAnd(
                    [
                        Literal.positive(
                            Predicate("q2", ["?b1-00", "?b2-01", "?b2-02"],)
                        ),
                        Literal.negative(
                            Predicate("q1", ["?b1-00", "?b2-01", "?b2-02"],)
                        ),
                        Literal.negative(
                            Predicate("q3", ["?b1-00", "?b2-01", "?b2-02"],)
                        ),
                        Literal.positive(Predicate("turnDomain")),
                    ]
                ),
            ),
            Action(
                name="trans-1",
                parameters=[
                    Term.variable("?b1-00", "block"),
                    Term.variable("?b2-01", "block"),
                    Term.variable("?b2-02", "block"),
                ],
                preconditions=FormulaAnd(
                    [
                        FormulaOr(
                            [
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate(
                                                "q1", ["?b1-00", "?b2-01", "?b2-02"],
                                            )
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b2-01", "?b2-02"],)
                                        ),
                                        Literal.positive(Predicate("emptyhand")),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate(
                                                "q2", ["?b1-00", "?b2-01", "?b2-02"],
                                            )
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(
                                            Predicate("on", ["?b2-01", "?b2-02"],)
                                        ),
                                        Literal.positive(Predicate("emptyhand")),
                                    ]
                                ),
                                Literal.positive(
                                    Predicate("q3", ["?b1-00", "?b2-01", "?b2-02"],)
                                ),
                            ]
                        ),
                        Literal.negative(Predicate("turnDomain")),
                    ]
                ),
                effects=FormulaAnd(
                    [
                        Literal.positive(
                            Predicate("q3", ["?b1-00", "?b2-01", "?b2-02"],)
                        ),
                        Literal.negative(
                            Predicate("q1", ["?b1-00", "?b2-01", "?b2-02"],)
                        ),
                        Literal.negative(
                            Predicate("q2", ["?b1-00", "?b2-01", "?b2-02"],)
                        ),
                        Literal.positive(Predicate("turnDomain")),
                    ]
                ),
            ),
        ]
        expected_params = [
            Term.variable("?b1-00", "block"),
            Term.variable("?b2-01", "block"),
            Term.variable("?b2-02", "block"),
        ]
        assert actual_trans_ops == expected_trans_ops
        assert actual_params == expected_params

    def test_automaton_create_trans_op_2(self):
        """Test that the created trans operator is correct."""
        pddl_domain = self.parser(
            open(
                str(
                    Path(
                        TEST_ROOT_DIR,
                        "data",
                        "pddl-domains",
                        "blocksworld-ipc08",
                        "domain.pddl",
                    )
                )
            ).read()
        )
        grounded_symbols = [
            Symbol("emptyhand"),
            Symbol("on", ["b", "e"]),
            Symbol("ontable", ["e"]),
        ]
        actual_trans_ops, actual_params = self.aut_obj.create_operators_trans(
            pddl_domain.predicates, grounded_symbols
        )
        expected_trans_ops = [
            Action(
                name="trans-0",
                parameters=[
                    Term.variable("?b1-00", "block"),
                    Term.variable("?b2-01", "block"),
                ],
                preconditions=FormulaAnd(
                    [
                        FormulaOr(
                            [
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate("q1", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.negative(Predicate("emptyhand")),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate("q1", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(Predicate("emptyhand")),
                                        Literal.negative(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate("q1", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(Predicate("emptyhand")),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.negative(
                                            Predicate("ontable", ["?b2-01"],)
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate("q2", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.negative(Predicate("emptyhand")),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate("q2", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(Predicate("emptyhand")),
                                        Literal.negative(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate("q2", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(Predicate("emptyhand")),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.negative(
                                            Predicate("ontable", ["?b2-01"],)
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        Literal.negative(Predicate("turnDomain")),
                    ]
                ),
                effects=FormulaAnd(
                    [
                        Literal.positive(Predicate("q2", ["?b1-00", "?b2-01"],)),
                        Literal.negative(Predicate("q1", ["?b1-00", "?b2-01"],)),
                        Literal.negative(Predicate("q3", ["?b1-00", "?b2-01"],)),
                        Literal.positive(Predicate("turnDomain")),
                    ]
                ),
            ),
            Action(
                name="trans-1",
                parameters=[
                    Term.variable("?b1-00", "block"),
                    Term.variable("?b2-01", "block"),
                ],
                preconditions=FormulaAnd(
                    [
                        FormulaOr(
                            [
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate("q1", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(Predicate("emptyhand")),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(
                                            Predicate("ontable", ["?b2-01"],)
                                        ),
                                    ]
                                ),
                                FormulaAnd(
                                    [
                                        Literal.positive(
                                            Predicate("q2", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(Predicate("emptyhand")),
                                        Literal.positive(
                                            Predicate("on", ["?b1-00", "?b2-01"],)
                                        ),
                                        Literal.positive(
                                            Predicate("ontable", ["?b2-01"],)
                                        ),
                                    ]
                                ),
                                Literal.positive(
                                    Predicate("q3", ["?b1-00", "?b2-01"],)
                                ),
                            ]
                        ),
                        Literal.negative(Predicate("turnDomain")),
                    ]
                ),
                effects=FormulaAnd(
                    [
                        Literal.positive(Predicate("q3", ["?b1-00", "?b2-01"],)),
                        Literal.negative(Predicate("q1", ["?b1-00", "?b2-01"],)),
                        Literal.negative(Predicate("q2", ["?b1-00", "?b2-01"],)),
                        Literal.positive(Predicate("turnDomain")),
                    ]
                ),
            ),
        ]
        expected_params = [
            Term.variable("?b1-00", "block"),
            Term.variable("?b2-01", "block"),
        ]
        assert actual_trans_ops == expected_trans_ops
        assert actual_params == expected_params


class TestParsingAutomaton3:
    """Test parsing for tests/data/automata/GaimpliesXb.aut."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.aut_obj = parse_dfa(
            open(str(Path(TEST_ROOT_DIR, "data", "automata", "GaimpliesXb.aut"))).read()
        )  # type: Automaton
        cls.aut_alphabet = cls.aut_obj.alphabet
        cls.aut_states = cls.aut_obj.states
        cls.aut_initial_state = cls.aut_obj.initial_state
        cls.aut_accepting_states = cls.aut_obj.accepting_states
        cls.aut_transitions = cls.aut_obj.transitions
        cls.aut_trans_by_dest = cls.aut_obj.trans_by_dest

    def test_automaton_alphabet(self):
        """Test that the alphabet is correct."""
        assert self.aut_alphabet == {"0", "1", "X"}

    def test_automaton_states(self):
        """Test that the states are correct."""
        assert self.aut_states == {"1", "2", "3", "4"}

    def test_automaton_initial_state(self):
        """Test that the initial state is correct."""
        assert self.aut_initial_state == "1"

    def test_automaton_accepting_states(self):
        """Test that the accepting states are correct."""
        assert self.aut_accepting_states == {"2"}

    def test_automaton_transitions(self):
        """Test that the transitions are correct."""
        assert self.aut_transitions == {
            "1": {"0X": "2", "1X": "3"},
            "2": {"0X": "2", "1X": "3"},
            "3": {"00": "4", "01": "2", "10": "4", "11": "3"},
            "4": {"XX": "4"},
        }

    def test_automaton_trans_by_dest(self):
        """Test that the transitions by destination are correct."""
        assert self.aut_trans_by_dest == {
            "1": [],
            "2": [("1", "0X"), ("2", "0X"), ("3", "01")],
            "3": [("1", "1X"), ("2", "1X"), ("3", "11")],
            "4": [("3", "00"), ("3", "10"), ("4", "XX")],
        }

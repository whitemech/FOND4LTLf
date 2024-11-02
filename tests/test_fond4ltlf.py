#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of FOND4LTLf.
#
# FOND4LTLf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FOND4LTLf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FOND4LTLf.  If not, see <https://www.gnu.org/licenses/>.
#

"""Test the fond4ltlf tool."""

import os

import pytest

import fond4ltlf.core
from fond4ltlf.automa.symbol import Symbol

from .conftest import TEST_ROOT_DIR


def test_compute_formula_symbols():
    """Test symbols check."""
    formula = "vehicleat_l31 & O(vehicleat_l12)"
    syms = fond4ltlf.core.compute_symb_vars(formula)
    true_syms = [Symbol("vehicleat", ["l31"]), Symbol("vehicleat", ["l12"])]
    assert true_syms == syms

    formula = "F(emptyhand & on_b_e & ontable_e)"
    syms = fond4ltlf.core.compute_symb_vars(formula)
    true_syms = [
        Symbol("emptyhand"),
        Symbol("on", ["b", "e"]),
        Symbol("ontable", ["e"]),
    ]
    assert true_syms == syms


@pytest.mark.parametrize(
    ["domain", "problem", "formula"],
    [
        (
            os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "acrobatics", "domain.pddl"),
            os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "acrobatics", "p01.pddl"),
            "F(up & position_p1)",
        ),
        (
            os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "beam-walk", "domain.pddl"),
            os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "beam-walk", "p01.pddl"),
            "F(up & position_p3)",
        ),
        (
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "blocksworld-ipc08",
                "domain.pddl",
            ),
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "blocksworld-ipc08",
                "p01.pddl",
            ),
            "F(emptyhand & on_b1_b2 & on_b2_b5)",
        ),
        (
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "blocksworld-ipc08",
                "domain.pddl",
            ),
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "blocksworld-ipc08",
                "p00.pddl",
            ),
            "F(emptyhand & on_b_e & ontable_e)",
        ),
        # (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "islands", "domain.pddl"),),
        # (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "miner", "domain.pddl"),),
        (
            os.path.join(
                TEST_ROOT_DIR,
                "data",
                "pddl-domains",
                "triangle-tireworld",
                "domain.pddl",
            ),
            os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "triangle-tireworld", "p01.pddl"),
            "vehicleat_l31 & O(vehicleat_l12)",
        ),
        # (os.path.join(TEST_ROOT_DIR, "data", "pddl-domains", "zenotravel", "domain.pddl"),),
    ],
)
def test_execute(domain, problem, formula):
    """Test to check that the output is deterministic."""
    temp_d = domain
    temp_p = problem

    in_domain_1 = open(domain).read()  # type: Domain
    in_problem_1 = open(problem).read()  # type: Problem
    in_domain_2 = open(temp_d).read()  # type: Domain
    in_problem_2 = open(temp_p).read()  # type: Problem

    out_domain_1, out_problem_1 = fond4ltlf.core.execute(in_domain_1, in_problem_1, formula)

    # temp_d = tempfile.mktemp()
    # temp_p = tempfile.mktemp()
    # with open(temp_d, "w") as t_1, open(temp_p, "w") as t_2:
    #     t_1.write(str(in_domain_1))
    #     t_2.write(str(in_problem_1))
    # in_domain_2 = parser(open(temp_d).read())  # type: Domain
    # in_problem_2 = parser(open(temp_p).read())  # type: Problem

    out_domain_2, out_problem_2 = fond4ltlf.core.execute(in_domain_2, in_problem_2, formula)

    assert out_domain_1 == out_domain_2
    assert out_problem_1 == out_problem_2

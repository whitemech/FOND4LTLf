# -*- coding: utf-8 -*-

"""Test the fonod4ltlfpltlf tool."""

import fond4ltlfpltlf.core
from fond4ltlfpltlf.automa.symbol import Symbol


def test_check_symbols():
    """Test symbols check."""
    formula = "vehicleat_l31 & O(vehicleat_l12)"
    syms = fond4ltlfpltlf.core.compute_symb_vars(formula)
    true_syms = [Symbol("vehicleat", ["l31"]), Symbol("vehicleat", ["l12"])]
    assert true_syms == syms


# def test_execute():
#     # formula_1 = "F(atperson_p0_c3 & atperson_p1_c4)" # zenotravel
#     formula_1 = "vehicleat_l31 & O(vehicleat_l12)"
#     in_domain = open("../tests/data/triangle-tireworld/domain.pddl").read()
#     in_problem = open("../tests/data/triangle-tireworld/p01.pddl").read()
#
#     domain_prime, problem_prime = fond4ltlfpltlf.core.execute(in_domain, in_problem, formula_1)

# print(
#     "======== Domain File ========\n{}\n\n======== Problem File ========\n{}".format(
#         domain_prime, problem_prime
#     )
# )

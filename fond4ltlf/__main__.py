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
"""This is the command line tool for the FOND4LTLf tool."""

import click  # type: ignore

from fond4ltlf.core import execute


@click.command()
@click.option(
    "-d",
    "--in-domain",
    required=True,
    help="Path to PDDL domain file.",
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "-p",
    "--in-problem",
    required=True,
    help="Path to PDDL problem file.",
    type=click.Path(exists=True, readable=True),
)
@click.option("--goal", "-g", help="LTLf or PLTLf goal formula.", type=str)
@click.option(
    "--out-domain",
    "-outd",
    default="./new-domain.pddl",
    help="Path to PDDL file to store the new domain.",
    type=click.Path(dir_okay=False),
)
@click.option(
    "--out-problem",
    "-outp",
    default="./new-problem.pddl",
    help="Path to PDDL file to store the new problem.",
    type=click.Path(dir_okay=False),
)
def main(in_domain, in_problem, goal, out_domain, out_problem):
    """From FOND Planning for LTLf/PLTLf Goals to Classical FOND Planning."""
    try:
        with open(in_domain, "r") as d:
            pddl_domain = d.read()
        with open(in_problem, "r") as p:
            pddl_problem = p.read()
    except Exception:
        raise IOError("[ERROR]: Something wrong occurred while parsing the domain and problem.")

    domain_prime, problem_prime = execute(pddl_domain, pddl_problem, goal)

    try:
        with open(out_domain, "w+") as dom:
            dom.write(str(domain_prime))
        with open(out_problem, "w+") as prob:
            prob.write(str(problem_prime))
    except Exception:
        raise IOError("[ERROR]: Something wrong occurred while writing new problem and domain.")


if __name__ == "__main__":
    main()  # pragma: no cover

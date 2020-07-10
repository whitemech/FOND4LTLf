#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the command line tool for the FOND4LTLfPLTLf tool."""
import click

from fond4ltlfpltlf.core import execute


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
        raise IOError(
            "[ERROR]: Something wrong occurred while parsing the domain and problem."
        )

    domain_prime, problem_prime = execute(pddl_domain, pddl_problem, goal)

    # print(
    #     "======== Domain File ========\n{}\n\n======== Problem File ========\n{}".format(
    #         domain_prime, problem_prime
    #     )
    # )

    try:
        with open(out_domain, "w+") as dom:
            dom.write(str(domain_prime))
        with open(out_problem, "w+") as prob:
            prob.write(str(problem_prime))
    except Exception:
        raise IOError(
            "[ERROR]: Something wrong occurred while writing new problem and domain."
        )


if __name__ == "__main__":
    main()  # pragma: no cover

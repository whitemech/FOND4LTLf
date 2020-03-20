#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the command line tool for translating HOA to DOT format."""
import click

from fond4ltlfpltl.core import execute


@click.command()
@click.argument('domain', type=str)
@click.argument('problem', type=str)
@click.argument('temporal_goal', type=str)
def main(domain, problem, temporal_goal):
    """main function for cli."""
    pddl_domain = open(domain).read()
    pddl_problem = open(problem).read()
    domain_prime, problem_prime = execute(pddl_domain, pddl_problem, temporal_goal)

    print("======== Domain File ========\n{}\n\n======== Problem File ========\n{}".format(domain_prime, problem_prime))

    # try:
    #     with open("dom-prime.pddl", 'w+') as dom:
    #         dom.write(str(domain_prime))
    #     with open("prob-prime.pddl", 'w+') as prob:
    #         prob.write(str(problem_prime))
    # except:
    #     raise IOError('[ERROR]: Something wrong occurred while writing new problem and domain.')


if __name__ == '__main__':
    main()  # pragma: no cover

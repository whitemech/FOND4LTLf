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

    return domain_prime, problem_prime


# def main(infile, output):
#     """From HOA to DOT format."""
#     input_string = open(infile).read()
#     parser = HOAParser()
#     hoa = parser(input_string)  # type: HOA
#     print(hoa.dumps(), file=open(output, "w") if output is not None else None)


if __name__ == '__main__':
    main()  # pragma: no cover

# domain_prime, problem_prime = execute(domain, problem, goal)

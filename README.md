<h1 align="center">
  FOND 4 LTL<sub>f</sub>
</h1>

<p align="center">
  <a href="">
    <img alt="test" src="https://github.com/whitemech/FOND4LTLf/workflows/test/badge.svg">
  </a>
  <a href="">
    <img alt="lint" src="https://github.com/whitemech/FOND4LTLf/workflows/lint/badge.svg">
  </a>
  <a href="">
    <img alt="docs" src="https://github.com/whitemech/FOND4LTLf/workflows/docs/badge.svg">
  </a>
</p>
<p align="center">
  <a href="https://codecov.io/gh/whitemech/FOND4LTLf">
    <img src="https://codecov.io/gh/whitemech/FOND4LTLf/branch/master/graph/badge.svg?token=KKWRAH29O7"/>
  </a>
  <a href="https://www.mkdocs.org/">
    <img alt="" src="https://img.shields.io/badge/docs-mkdocs-9cf">
  </a>
  <a href="https://github.com/whitemech/FOND4LTLf/blob/master/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/badge/license-LGPLv3%2B-blue">
  </a>
</p>
<p align="center">
<a href="https://doi.org/10.5281/zenodo.4876281"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4876281.svg" alt="DOI"></a>
</p>

FOND 4 LTL<sub>f</sub> is a tool that compiles Fully Observable Non-Deterministic (FOND) planning
problems with temporally extended goals, specified either in LTL<sub>f</sub> or in PLTL<sub>f</sub>, into classical FOND
planning problems.

## Prerequisites

This tool is based on the following libraries:

- [ltlf2dfa 1.0.1](https://pypi.org/project/ltlf2dfa/)
- [ply](https://pypi.org/project/ply/)
- [click](https://pypi.org/project/click/)

They are automatically added while installing FOND4LTL<sub>f</sub>.

## Install

- Intall from source (`master` branch):

```
pip install git+https://github.com/whitemech/FOND4LTLf.git
```

- or, clone the repository and install:

```
git clone https://github.com/whitemech/FOND4LTLf.git
cd FOND4LTLf
pip install .
```

## Usage

The output of the CLI is the following:

```bash
user:~$ fond4ltlf --help
Usage: fond4ltlf [OPTIONS]

  From FOND Planning for LTLf/PLTLf Goals to Classical FOND Planning.

Options:
  -d, --in-domain PATH       Path to PDDL domain file.  [required]
  -p, --in-problem PATH      Path to PDDL problem file.  [required]
  -g, --goal TEXT            LTLf or PLTLf goal formula.
  -outd, --out-domain FILE   Path to PDDL file to store the new domain.
  -outp, --out-problem FILE  Path to PDDL file to store the new problem.
  -n, --no-disj-preconds     No disjunctive preconditions.
  --help                     Show this message and exit.
```

For instance, you can call `FOND4LTLf` as follows:

```bash
fond4ltlf -d <path/to/domain.pddl> -p <path/to/problem.pddl> -g "formula"
```

## Features

* Syntax and parsing support FOND Planning in PDDL
* Compilation of Deterministic Finite-state Automaton into PDDL

## Development

Contributions are welcome! Here's how to set up the development environment:
- set up your preferred virtualenv environment
- clone the repo: `git clone https://github.com/IBM/nl2ltl.git && cd nl2ltl`
- install dependencies: `pip install -e .`
- install dev dependencies: `pip install -e ".[dev]"`
- install pre-commit: `pre-commit install`

## Tests

To run tests: `tox`

To run only the code tests: `tox -e py3.10`

To run only the code style checks: `tox -e ruff-check`

## License

FOND4LTL<sub>f</sub> is released under the GNU Lesser General Public License v3.0 or later (LGPLv3+).

Copyright 2019-2024 WhiteMech

## Author

[Francesco Fuggitti](https://francescofuggitti.github.io/)


